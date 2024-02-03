import asyncio
import logging
import os
import time

from fastapi import APIRouter

from soil_api.utils.bbox_extraction import extract_bbox_from_raster
from soil_api.utils.response_generator import generate_soil_layer

logging.basicConfig(level=logging.INFO)

from soil_api.config import settings
from soil_api.dependencies.queryparams import (
    BboxQueryDep,
    DepthQueryDep,
    LocationQueryDep,
    PropertyQueryDep,
    SoilTypeCountDep,
    ValueQueryDep,
)
from soil_api.models.soil import (
    BoundingBoxGeometry,
    GeometryType,
    PointGeometry,
    SoilLayerList,
    SoilPropertyJSON,
    SoilTypeInfo,
    SoilTypeJSON,
    SoilTypeProbability,
    SoilTypes,
    SoilTypeSummaries,
    SoilTypeSummary,
    SoilTypeSummaryJSON,
)
from soil_api.utils.point_extraction import extract_point_from_raster

router = APIRouter(tags=["soil"])


@router.get(
    "/type",
    summary="Get soil type",
    description="Returns the soil type for the given location",
    response_model_exclude_none=True,
)
async def get_soil_type(
    location_query: LocationQueryDep, count: SoilTypeCountDep
) -> SoilTypeJSON:
    wrb_soil_map = "wrb"

    wrb_soil_map_fname = settings.soil_maps[wrb_soil_map]
    wrb_soil_map_path = os.path.join(
        settings.soil_maps_url, wrb_soil_map, wrb_soil_map_fname
    )
    lat, lon = location_query
    value = await extract_point_from_raster(
        raster_path=wrb_soil_map_path, latitude=lat, longitude=lon
    )

    # get the value of the enum member with the name t{value} and use
    # the default value SoilTypes.No_information if the value is not found
    # soil_type = SoilTypes.get(f"t{value}", SoilTypes.No_information)
    most_probable_soil_type = SoilTypes.__members__.get(
        f"t{value}", SoilTypes.No_information
    ).value

    additional_soil_types = []
    additional_soil_maps = []
    if most_probable_soil_type == SoilTypes.No_information.value:
        pass
    elif count == 1:
        additional_soil_types = [most_probable_soil_type]
        additional_soil_maps = [
            os.path.join(
                settings.soil_maps_url, wrb_soil_map, f"{most_probable_soil_type}.vrt"
            )
        ]
        logging.info(f"Additional soil types: {additional_soil_types}")
        logging.info(f"Additional soil maps: {additional_soil_maps}")
    elif count > 1:
        # get a list of all soil type names from the enum except No_information
        additional_soil_types = [
            soil_type.value
            for soil_type in SoilTypes
            if soil_type != SoilTypes.No_information
        ]
        # additional_soil_types = list(SoilTypes.__members__.values())
        logging.info(f"Additional soil types: {additional_soil_types}")
        # additional_soil_types.remove(SoilTypes.No_information)
        additional_soil_maps = [
            os.path.join(settings.soil_maps_url, wrb_soil_map, f"{soil_type}.vrt")
            for soil_type in additional_soil_types
        ]

    soil_type_probabilities = await run_parallel(
        extract_point_from_raster,
        [(raster_path, lat, lon) for raster_path in additional_soil_maps],
    )

    merged_soil_type_probabilities = list(
        zip(additional_soil_types, soil_type_probabilities)
    )
    logging.info(f"Merged soil type probabilities: {merged_soil_type_probabilities}")
    # remove all elements where the probability is 0
    merged_soil_type_probabilities = [
        (soil_type, type_probability)
        for soil_type, type_probability in merged_soil_type_probabilities
        if type_probability not in [0, -99999]
    ]
    logging.info(f"Merged soil type probabilities: {merged_soil_type_probabilities}")
    merged_soil_type_probabilities = sorted(
        merged_soil_type_probabilities, key=lambda x: x[1], reverse=True
    )[:count]
    logging.info(f"Merged soil type probabilities: {merged_soil_type_probabilities}")
    probabilities = []
    for soil_type, type_probability in merged_soil_type_probabilities:
        soil_probability = SoilTypeProbability(
            soil_type=soil_type,
            probability=type_probability,
        )
        probabilities.append(soil_probability)
    if not probabilities:
        probabilities = None

    # soil_type_ = settings.soil_types_mapping.get(value, SoilTypes.No_information)
    soil_type_info = SoilTypeInfo(
        soil_type=most_probable_soil_type,
        probabilities=probabilities,
    )

    response = SoilTypeJSON(
        properties=soil_type_info,
        geometry=PointGeometry(coordinates=[lon, lat], type=GeometryType.Point),
    )
    return response


@router.get(
    "/property",
    summary="Get soil property",
    description="Returns the soil property for the given location",
    response_model_exclude_none=True,
)
async def get_soil_property(
    location: LocationQueryDep,
    depths: DepthQueryDep,
    properties: PropertyQueryDep,
    value_types: ValueQueryDep,
) -> SoilPropertyJSON:
    soil_map_fnames = []
    all_properties = []
    all_depths = []
    all_value_types = []
    for property in properties:
        for depth in depths:
            for value_type in value_types:
                # if (property == "ocs" and depth != "0-30cm") or (
                #     depth == "0-30cm" and property != "ocs"
                # ):
                #     continue
                # replace underscores with dots in value_type
                all_properties.append(property)
                all_depths.append(depth)
                all_value_types.append(value_type)
                if "_" in value_type:
                    value_type = value_type.replace("_", ".")
                soil_map_fname = f"{property}_{depth}_{value_type}.vrt"
                soil_map_path = os.path.join(
                    settings.soil_maps_url, property, soil_map_fname
                )
                soil_map_fnames.append(soil_map_path)

    lat, lon = location
    transform_CRS = True

    values = await run_parallel(
        extract_point_from_raster,
        [(raster_path, lat, lon, transform_CRS) for raster_path in soil_map_fnames],
    )

    soil_map_info = {}
    for property, depth, value_type, value in zip(
        all_properties, all_depths, all_value_types, values
    ):
        if property not in soil_map_info:
            soil_map_info[property] = {}
        if depth not in soil_map_info[property]:
            soil_map_info[property][depth] = {}
        if value not in settings.no_data_vals:
            soil_map_info[property][depth][value_type] = value

    all_soil_layers = []
    for property in properties:
        all_soil_layers.append(generate_soil_layer(property, soil_map_info[property]))

    soil_layer_list = SoilLayerList(
        layers=all_soil_layers,
    )

    response = SoilPropertyJSON(
        properties=soil_layer_list,
        geometry=PointGeometry(coordinates=[lon, lat], type=GeometryType.Point),
    )
    return response


async def run_parallel(target_function, args_list):
    start_time = time.time()  # Record start time
    logging.info(f"Running parallel extraction for {len(args_list)} rasters")
    tasks = [target_function(*args) for args in args_list]
    results = await asyncio.gather(*tasks)
    end_time = time.time()  # Record end time
    elapsed_time = end_time - start_time
    logging.info(f"Parallel execution time: {elapsed_time} seconds")
    return results


async def run_sequential(target_function, args_list):
    start_time = time.time()  # Record start time
    logging.info(f"Running sequential extraction for {len(args_list)} rasters")
    results = []
    for args in args_list:
        value = await target_function(*args)
        results.append(value)
    end_time = time.time()  # Record end time
    elapsed_time = end_time - start_time
    logging.info(f"Sequential execution time: {elapsed_time} seconds")
    return results


@router.get(
    "/type/summary",
    summary="Get soil type summary for a given bounding box",
    description="Returns the a summary of the soil types present in the given boux",
    response_model_exclude_none=True,
)
async def get_soil_type_summary(bbox: BboxQueryDep) -> SoilTypeSummaryJSON:
    wrb_soil_map = "wrb"
    wrb_soil_map_fname = settings.soil_maps[wrb_soil_map]
    wrb_soil_map_path = os.path.join(
        settings.soil_maps_url, wrb_soil_map, wrb_soil_map_fname
    )
    types_counts = extract_bbox_from_raster(wrb_soil_map_path, bbox)

    # map every key to the corresponding soil type
    # soil_type_counts = {}
    # for key, value in types_counts.items():
    #     soil_type = SoilTypes.__members__.get(f"t{key}", SoilTypes.No_information)
    #     soil_type_counts[soil_type.value] = value

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

    soil_type_summaries = SoilTypeSummaries(
        summaries=[
            SoilTypeSummary(
                soil_type=SoilTypes.__members__.get(
                    f"t{key}", SoilTypes.No_information
                ),
                count=count,
            )
            for key, count in sorted(
                types_counts.items(), key=lambda x: x[1], reverse=True
            )
        ]
    )

    response = SoilTypeSummaryJSON(
        properties=soil_type_summaries,
        geometry=BoundingBoxGeometry(coordinates=polygon, type=GeometryType.Polygon),
    )

    return response
