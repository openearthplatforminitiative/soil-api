import asyncio
import logging
import os
import time

logging.basicConfig(level=logging.INFO)

from fastapi import APIRouter

from soil_api import constants
from soil_api.dependencies.queryparams import (
    BboxQueryDep,
    DepthQueryDep,
    LocationQueryDep,
    PropertyQueryDep,
    SoilTypeTopKDep,
    ValueQueryDep,
)
from soil_api.models.shared import (
    BoundingBoxGeometry,
    FeatureType,
    GeometryType,
    PointGeometry,
)
from soil_api.models.soil_property import SoilLayerList, SoilPropertyJSON
from soil_api.models.soil_type import (
    SoilTypeInfo,
    SoilTypeJSON,
    SoilTypeProbability,
    SoilTypes,
    SoilTypeSummary,
    SoilTypeSummaryInfo,
    SoilTypeSummaryJSON,
)
from soil_api.utils.bbox_extraction import extract_bbox_from_raster
from soil_api.utils.point_extraction import (
    extract_point_from_raster,
    transfrom_coordinates_to_homolosine_crs,
)
from soil_api.utils.response_generator import generate_soil_layer

router = APIRouter(tags=["soil"])


@router.get(
    "/type",
    summary="Get soil type",
    description="Returns the most probable soil type for the given location",
    response_model_exclude_none=True,
)
async def get_soil_type(
    location_query: LocationQueryDep, top_k: SoilTypeTopKDep
) -> SoilTypeJSON:
    # Define the path to the WRB soil map and extract the most probable
    # soil type at the given location
    wrb_soil_map = "wrb"
    wrb_soil_map_fname = constants.SOIL_MAPS[wrb_soil_map]
    wrb_soil_map_path = os.path.join(
        constants.SOIL_MAPS_URL, wrb_soil_map, wrb_soil_map_fname
    )
    lat, lon = location_query
    value = await extract_point_from_raster(
        raster_path=wrb_soil_map_path, latitude=lat, longitude=lon
    )
    # Extract the name of the most probable soil type
    # from the SoilTypes enum using the value extracted from the raster
    most_probable_soil_type = SoilTypes(value)

    # Define the paths to the additional soil maps and extract the probabilities
    # for the most probable soil type and the top k-1 most probable soil types
    # If the most probable soil type is No_information, this step is skipped
    # If top_k is 1, only the raster for the most probable soil type is queried
    # If top_k is > 1, the rasters for all soil types are queried because
    # all probabilities are needed to find the top_k most probable soil types
    additional_soil_types = []
    additional_soil_maps = []
    if most_probable_soil_type != SoilTypes.No_information:  # .value:
        if top_k == 1:
            additional_soil_types = [most_probable_soil_type]
            additional_soil_maps = [
                os.path.join(
                    constants.SOIL_MAPS_URL,
                    wrb_soil_map,
                    f"{most_probable_soil_type.name}.vrt",
                )
            ]
        elif top_k > 1:
            # get a list of all soil types from the enum except No_information
            additional_soil_types = [
                soil_type
                for soil_type in SoilTypes
                if soil_type != SoilTypes.No_information
            ]
            additional_soil_maps = [
                os.path.join(
                    constants.SOIL_MAPS_URL, wrb_soil_map, f"{soil_type.name}.vrt"
                )
                for soil_type in additional_soil_types
            ]

    # Run parallel extraction for the additional soil mapsq
    soil_type_probabilities = await run_parallel(
        extract_point_from_raster,
        [(raster_path, lat, lon) for raster_path in additional_soil_maps],
    )

    # Merge the additional soil types and their probabilities
    merged_soil_type_probabilities = list(
        zip(additional_soil_types, soil_type_probabilities)
    )

    # Remove all elements where the probability is 0
    merged_soil_type_probabilities = [
        (soil_type, type_probability)
        for soil_type, type_probability in merged_soil_type_probabilities
        if type_probability != 0
    ]

    # Sort the merged soil types by probability and keep the top k
    merged_soil_type_probabilities = sorted(
        merged_soil_type_probabilities, key=lambda x: x[1], reverse=True
    )[:top_k]

    # Create a list of SoilTypeProbability objects
    probabilities = []
    for soil_type, type_probability in merged_soil_type_probabilities:
        soil_probability = SoilTypeProbability(
            soil_type=soil_type,
            probability=type_probability,
        )
        probabilities.append(soil_probability)

    # If no probabilities are found, set the probabilities to None
    # so that the response model will not include the probabilities field
    if not probabilities:
        probabilities = None

    soil_type_info = SoilTypeInfo(
        most_probable_soil_type=most_probable_soil_type,
        probabilities=probabilities,
    )

    response = SoilTypeJSON(
        type=FeatureType.Feature,
        properties=soil_type_info,
        geometry=PointGeometry(coordinates=[lon, lat], type=GeometryType.Point),
    )
    return response


@router.get(
    "/property",
    summary="Get soil property",
    description=(
        "Returns the values of the soil properties for the given "
        "location and depths. "
        "Note: The ocs property is only available for the 0-30cm "
        "depth and vice versa. If the depth and property are "
        "incompatible, the response will not include the property."
    ),
    response_model_exclude_unset=True,
)
async def get_soil_property(
    location: LocationQueryDep,
    depths: DepthQueryDep,
    properties: PropertyQueryDep,
    value_types: ValueQueryDep,
) -> SoilPropertyJSON:
    # Define paths to the soil maps and store property names, depths
    # and value types in lists for easier creation of the response model
    soil_map_fnames = []
    all_properties = []
    all_depths = []
    all_value_types = []
    for property in properties:
        for depth in depths:
            for value_type in value_types:
                all_properties.append(property)
                all_depths.append(depth)
                all_value_types.append(value_type)
                # ocs is only available for 0-30cm (and vice versa)
                # for uncompatible cases, set the soil map path to None
                # so that the raster extraction step is skipped
                if (property == "ocs" and depth != "0-30cm") or (
                    depth == "0-30cm" and property != "ocs"
                ):
                    soil_map_fnames.append(None)
                else:
                    soil_map_fname = f"{property}_{depth}_{value_type}.vrt"
                    soil_map_path = os.path.join(
                        constants.SOIL_MAPS_URL, property, soil_map_fname
                    )
                    soil_map_fnames.append(soil_map_path)

    # Convert the coordinates to the homolosine CRS
    # because the soil maps are in this CRS
    input_lat, input_lon = location
    lat, lon = transfrom_coordinates_to_homolosine_crs(
        latitude=input_lat, longitude=input_lon
    )

    # Run parallel extraction for the soil maps
    values = await run_parallel(
        extract_point_from_raster,
        [(raster_path, lat, lon) for raster_path in soil_map_fnames],
    )

    # Create a dictionary to store the extracted values
    soil_map_info = {}
    for property, depth, value_type, value in zip(
        all_properties, all_depths, all_value_types, values
    ):
        # If the value is a no data value, skip it
        if value != constants.NO_DATA_VAL:
            # If the property is not in the dictionary, add it
            if property not in soil_map_info:
                soil_map_info[property] = {}
            # If the depth is not in the dictionary, add it
            if depth not in soil_map_info[property]:
                soil_map_info[property][depth] = {}
            # If the value is a soilgrids no data value, set it to None
            # A soilgrids no data value often represents a body of water
            if value in constants.NO_DATA_VALS_SOILGRIDS:
                value = None
            soil_map_info[property][depth][value_type] = value

    # Create a list of SoilLayer objects and fill them using
    # the soil_map_info dictionary. Skip the properties that
    # are not in the dictionary (i.e., the ones with all no data values)
    all_soil_layers = []
    for property in properties:
        if property in soil_map_info:
            all_soil_layers.append(
                generate_soil_layer(property, soil_map_info[property])
            )

    soil_layer_list = SoilLayerList(
        layers=all_soil_layers,
    )
    response = SoilPropertyJSON(
        type=FeatureType.Feature,
        properties=soil_layer_list,
        geometry=PointGeometry(
            coordinates=[input_lon, input_lat], type=GeometryType.Point
        ),
    )
    return response


@router.get(
    "/type/summary",
    summary="Get soil type summary",
    description=(
        "Returns the a summary of the soil types present in the "
        "given bounding box, represented by a mapping of each soil "
        "type to the number of occurrences in the bounding box"
    ),
    response_model_exclude_none=True,
)
async def get_soil_type_summary(bbox: BboxQueryDep) -> SoilTypeSummaryJSON:
    # Define the path to the WRB soil map
    wrb_soil_map = "wrb"
    wrb_soil_map_fname = constants.SOIL_MAPS[wrb_soil_map]
    wrb_soil_map_path = os.path.join(
        constants.SOIL_MAPS_URL, wrb_soil_map, wrb_soil_map_fname
    )

    # Extract the soil types and their counts from the WRB soil map
    types_counts = extract_bbox_from_raster(wrb_soil_map_path, bbox)

    # create a Polygon from the bounding box
    polygon = [
        [
            [bbox[0], bbox[1]],
            [bbox[2], bbox[1]],
            [bbox[2], bbox[3]],
            [bbox[0], bbox[3]],
            [bbox[0], bbox[1]],
        ]
    ]

    # Create a list of SoilTypeSummary objects
    summaries = [
        SoilTypeSummary(
            soil_type=SoilTypes(key),
            count=count,
        )
        for key, count in sorted(types_counts.items(), key=lambda x: x[1], reverse=True)
    ]

    soil_type_summaries = SoilTypeSummaryInfo(summaries=summaries)
    response = SoilTypeSummaryJSON(
        type=FeatureType.Feature,
        properties=soil_type_summaries,
        geometry=BoundingBoxGeometry(coordinates=polygon, type=GeometryType.Polygon),
    )

    return response


async def run_parallel(target_function: callable, args_list: list) -> list:
    start_time = time.time()
    logging.info(f"Running parallel extraction for {len(args_list)} rasters")
    tasks = [target_function(*args) for args in args_list]
    results = await asyncio.gather(*tasks)
    end_time = time.time()
    elapsed_time = end_time - start_time
    logging.info(f"Parallel execution time: {elapsed_time} seconds")
    return results


# Just to see the difference between sequential and parallel execution
async def run_sequential(target_function: callable, args_list: list) -> list:
    start_time = time.time()
    logging.info(f"Running sequential extraction for {len(args_list)} rasters")
    results = []
    for args in args_list:
        value = await target_function(*args)
        results.append(value)
    end_time = time.time()
    elapsed_time = end_time - start_time
    logging.info(f"Sequential execution time: {elapsed_time} seconds")
    return results
