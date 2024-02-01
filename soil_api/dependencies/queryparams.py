from datetime import date
from typing import Annotated

from fastapi import Depends, HTTPException, Query

from soil_api.utils.validation_helpers import (
    validate_coordinates,
    validate_depth,
    validate_property,
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


def depth_and_property_query_dependency(
    depth: Annotated[
        str,
        Query(
            title="depth range",
            description="Depth range in cm. One of: 0-5, 5-15, 15-30, 30-60, 60-100, or 100-200. For property 'ocs' only 0-30 is available.",
            example="0-5",
        ),
    ],
    property: Annotated[
        str,
        Query(
            title="property",
            description="Soil property. One of: bdod, cec, cfvo, clay, nitrogen, ocd, ocs, phh2o, sand, silt, soc.",
            example="bdod",
        ),
    ],
) -> tuple[str, str]:
    validate_property(property)
    validate_depth(depth, property)
    return depth, property


DepthAndPropertyQuery = tuple[str, str]

DepthAndPropertyQueryDep = Annotated[
    DepthAndPropertyQuery, Depends(depth_and_property_query_dependency)
]
