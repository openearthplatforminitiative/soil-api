import asyncio
import logging
import os
import time

from fastapi import APIRouter

from soil_api.utils.response_generator import generate_soil_layer

logging.basicConfig(level=logging.INFO)

from soil_api.config import settings
from soil_api.dependencies.queryparams import (
    DepthQueryDep,
    LocationQueryDep,
    PropertyQueryDep,
    ValueQueryDep,
)
from soil_api.models.soil import (
    GeometryType,
    PointGeometry,
    SoilLayerList,
    SoilPropertyJSON,
    SoilType,
    SoilTypeJSON,
    SoilTypes,
)
from soil_api.utils.point_extraction import extract_point_from_raster

router = APIRouter(tags=["soil"])


@router.get(
    "/type",
    summary="Get soil type",
    description="Returns the soil type for the given location",
)
async def get_soil_type(
    location_query: LocationQueryDep,
) -> SoilTypeJSON:
    soil_map = "wrb"
    soil_map_fname = settings.soil_maps[soil_map]
    soil_map_path = os.path.join(settings.soil_maps_url, soil_map, soil_map_fname)
    lat, lon = location_query
    value = await extract_point_from_raster(
        raster_path=soil_map_path, latitude=lat, longitude=lon
    )

    soil_type_ = SoilTypes.__members__.get(f"t{value}", SoilTypes.No_information)
    # soil_type_ = settings.soil_types_mapping.get(value, SoilTypes.No_information)
    soil_type = SoilType(
        soil_type=soil_type_,
    )

    response = SoilTypeJSON(
        properties=soil_type,
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
                soil_map_fname = f"{property}_{depth}_{value_type}.vrt"
                soil_map_path = os.path.join(
                    settings.soil_maps_url, property, soil_map_fname
                )
                soil_map_fnames.append(soil_map_path)
                all_properties.append(property)
                all_depths.append(depth)
                all_value_types.append(value_type)

    lat, lon = location
    values = await parallel_extraction(soil_map_fnames, lat, lon, transform_CRS=True)

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


async def parallel_extraction(raster_paths, latitude, longitude, transform_CRS=False):
    start_time = time.time()  # Record start time
    tasks = [
        extract_point_from_raster(raster_path, latitude, longitude, transform_CRS)
        for raster_path in raster_paths
    ]
    results = await asyncio.gather(*tasks)
    end_time = time.time()  # Record end time
    elapsed_time = end_time - start_time
    logging.info(f"Parallel execution time: {elapsed_time} seconds")
    return results


async def sequential_extraction(raster_paths, latitude, longitude, transform_CRS=False):
    start_time = time.time()  # Record start time
    results = []
    for raster_path in raster_paths:
        value = await extract_point_from_raster(
            raster_path, latitude, longitude, transform_CRS
        )
        results.append(value)
    end_time = time.time()  # Record end time
    elapsed_time = end_time - start_time
    logging.info(f"Sequential execution time: {elapsed_time} seconds")
    return results
