import os
from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Query

from soil_api.config import settings
from soil_api.dependencies.queryparams import DepthAndPropertyQueryDep, LocationQueryDep
from soil_api.models.soil import (
    GeometryType,
    PointGeometry,
    SoilProperties,
    SoilProperty,
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
    value = extract_point_from_raster(
        raster_path=soil_map_path, latitude=lat, longitude=lon
    )

    soil_type_ = settings.soil_types_mapping.get(value, SoilTypes.No_information)
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
)
async def get_soil_property(
    location_query: LocationQueryDep, depth_and_property: DepthAndPropertyQueryDep
) -> SoilPropertyJSON:
    depth, property = depth_and_property
    soil_map = property
    soil_map_fname = f"{soil_map}_{depth}cm_mean.vrt"
    soil_map_path = os.path.join(settings.soil_maps_url, soil_map, soil_map_fname)
    lat, lon = location_query
    value = extract_point_from_raster(
        raster_path=soil_map_path, latitude=lat, longitude=lon, transform_CRS=True
    )
    if value == settings.no_data_val:
        value = "No information available."

    soil_property = SoilProperty(
        value=value,
        unit=settings.soil_property_to_unit_mapping[property],
        property=SoilProperties.__members__[property],
    )

    response = SoilPropertyJSON(
        properties=soil_property,
        geometry=PointGeometry(coordinates=[lon, lat], type=GeometryType.Point),
    )
    return response
