from typing import Annotated, List

from fastapi import Depends, Query

from soil_api.models.soil_property import (
    SoilDepthLabels,
    SoilPropertiesCodes,
    SoilPropertyValueTypes,
)
from soil_api.utils.validation_helpers import validate_bbox


def location_query_dependency(
    lon: Annotated[
        float,
        Query(title="lon", description="Longitude", example=9.58, ge=-180, le=180),
    ],
    lat: Annotated[
        float, Query(title="lat", description="Latitude", example=60.10, ge=-90, le=90)
    ],
) -> tuple[float, float]:
    return lat, lon


LocationQueryDep = Annotated[tuple[float, float], Depends(location_query_dependency)]


def soil_type_top_k_dependency(
    top_k: Annotated[
        int,
        Query(
            title="top_k",
            description="Number of most probable soil types that will be returned, sorted by probability in descending order",
            ge=0,
            le=30,
            example=0,
        ),
    ] = 0,
) -> int:
    return top_k


SoilTypeTopKDep = Annotated[int, Depends(soil_type_top_k_dependency)]


def depth_dependency(
    depths: Annotated[
        List[SoilDepthLabels],
        Query(
            title="depths to include",
            description="List of depths to include in the query.",
            min_length=1,
        ),
    ]
) -> List[SoilDepthLabels]:
    return depths


DepthQueryDep = Annotated[List[SoilDepthLabels], Depends(depth_dependency)]


def property_dependency(
    properties: Annotated[
        List[SoilPropertiesCodes],
        Query(
            title="properties to include",
            description="List of soil properties to include in the query.",
            min_length=1,
        ),
    ]
) -> List[SoilPropertiesCodes]:
    return properties


PropertyQueryDep = Annotated[List[SoilPropertiesCodes], Depends(property_dependency)]


def value_dependency(
    values: Annotated[
        List[SoilPropertyValueTypes],
        Query(
            title="values to include",
            description="List of values to include in the query.",
            min_length=1,
        ),
    ]
) -> List[SoilPropertyValueTypes]:
    return values


ValueQueryDep = Annotated[List[SoilPropertyValueTypes], Depends(value_dependency)]


def bbox_query_dependency(
    min_lon: Annotated[
        float,
        Query(
            title="min_lon",
            description="Minimum longitude",
            example=9.58,
            ge=-180,
            le=180,
        ),
    ],
    max_lon: Annotated[
        float,
        Query(
            title="max_lon",
            description="Maximum longitude",
            example=9.60,
            ge=-180,
            le=180,
        ),
    ],
    min_lat: Annotated[
        float,
        Query(
            title="min_lat",
            description="Minimum latitude",
            example=60.10,
            ge=-90,
            le=90,
        ),
    ],
    max_lat: Annotated[
        float,
        Query(
            title="max_lat",
            description="Maximum latitude",
            example=60.12,
            ge=-90,
            le=90,
        ),
    ],
) -> List[float]:
    bbox = [min_lon, min_lat, max_lon, max_lat]
    validate_bbox(bbox)
    return bbox


BboxQueryDep = Annotated[List[float], Depends(bbox_query_dependency)]
