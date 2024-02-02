from typing import Annotated, List

from fastapi import Depends, Query

from soil_api.config import settings
from soil_api.models.soil import SoilPropertiesCodes, SoilPropertyValues
from soil_api.utils.validation_helpers import (
    validate_coordinates,
    validate_depth,
    validate_depths,
    validate_properties,
    validate_property,
    validate_values,
)

# Define a union type for the dependency
LocationQuery = tuple[float, float]


def location_query_dependency(
    lon: Annotated[float, Query(title="lon", description="Longitude", example=9.58)],
    lat: Annotated[float, Query(title="lat", description="Latitude", example=60.10)],
) -> LocationQuery:
    validate_coordinates(latitude=lat, longitude=lon)
    return lat, lon


LocationQueryDep = Annotated[LocationQuery, Depends(location_query_dependency)]


# def depth_and_property_query_dependency(
#     properties: List[str] = Query(
#         list(SoilPropertiesCodes.__members__),
#         title="properties to include",
#         description="List of soil properties to include in the query.",
#     ),
#     depths: List[str] = Query(
#         list(settings.depths.keys()),
#         title="depths to include",
#         description="List of depths to include in the query.",
#     ),
#     values: List[str] = Query(
#         list(SoilPropertyValues.__annotations__),
#         title="values to include",
#         description="List of values to include in the query.",
#     ),
# ) -> tuple[str, str]:
#     validate_properties(properties)
#     validate_depths(depths)
#     validate_values(values)
#     return depths, properties, values


def depth_dependency(
    depths: List[str] = Query(
        list(settings.depths.keys()),
        title="depths to include",
        description="List of depths to include in the query.",
    ),
) -> List[str]:
    validate_depths(depths)
    return depths


DepthQueryDep = Annotated[List[str], Depends(depth_dependency)]


def property_dependency(
    properties: List[str] = Query(
        list(SoilPropertiesCodes.__members__),
        title="properties to include",
        description="List of soil properties to include in the query.",
    ),
) -> List[str]:
    validate_properties(properties)
    return properties


PropertyQueryDep = Annotated[List[str], Depends(property_dependency)]


def value_dependency(
    values: List[str] = Query(
        list(SoilPropertyValues.__annotations__),
        title="values to include",
        description="List of values to include in the query.",
    ),
) -> List[str]:
    validate_values(values)
    return values


ValueQueryDep = Annotated[List[str], Depends(value_dependency)]


# DepthAndPropertyQuery = tuple[List[str], List[str], List[str]]
# DepthAndPropertyQueryDep = Annotated[
#     DepthAndPropertyQuery, Depends(depth_and_property_query_dependency)
# ]
