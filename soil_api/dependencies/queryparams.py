from typing import Annotated, List

from fastapi import Depends, Query

from soil_api.config import settings
from soil_api.models.soil import SoilPropertiesCodes
from soil_api.utils.validation_helpers import (
    validate_bbox,
    validate_coordinates,
    validate_depths,
    validate_properties,
    validate_values,
)

LocationQuery = tuple[float, float]


def location_query_dependency(
    lon: Annotated[float, Query(title="lon", description="Longitude", example=9.58)],
    lat: Annotated[float, Query(title="lat", description="Latitude", example=60.10)],
) -> LocationQuery:
    validate_coordinates(latitude=lat, longitude=lon)
    return lat, lon


LocationQueryDep = Annotated[LocationQuery, Depends(location_query_dependency)]


def soil_type_count_dependency(
    top_k: Annotated[
        int,
        Query(
            title="top_k",
            description="Number of most probable soil types to return",
            ge=0,
            le=30,
        ),
    ] = 0,
) -> int:
    return top_k


SoilTypeCountDep = Annotated[int, Depends(soil_type_count_dependency)]


def depth_dependency(
    depths: Annotated[
        List[str],
        Query(
            title="depths to include",
            description="List of depths to include in the query.",
        ),
    ] = list(settings.depths.keys()),
) -> List[str]:
    validate_depths(depths)
    return depths


DepthQueryDep = Annotated[List[str], Depends(depth_dependency)]


def property_dependency(
    properties: Annotated[
        List[str],
        Query(
            title="properties to include",
            description="List of soil properties to include in the query.",
        ),
    ] = list(SoilPropertiesCodes.__members__),
) -> List[str]:
    validate_properties(properties)
    return properties


PropertyQueryDep = Annotated[List[str], Depends(property_dependency)]


def value_dependency(
    values: Annotated[
        List[str],
        Query(
            title="values to include",
            description="List of values to include in the query.",
        ),
    ] = settings.soil_property_value_types  # list(SoilPropertyValues.__annotations__),
) -> List[str]:
    validate_values(values)
    return values


ValueQueryDep = Annotated[List[str], Depends(value_dependency)]


def bbox_query_dependency(
    bbox: Annotated[
        List[float],
        Query(
            title="bbox",
            description="Bounding box coordinates (min lon, min lat, max lon, max lat)",
            example=[9.58, 60.10, 9.60, 60.12],
        ),
    ],
) -> List[float]:
    validate_bbox(bbox)
    return bbox


BboxQueryDep = Annotated[List[float], Depends(bbox_query_dependency)]
