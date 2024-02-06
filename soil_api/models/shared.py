from __future__ import annotations

from enum import Enum
from typing import List

from pydantic import BaseModel, Field


class FeatureType(Enum):
    Feature = "Feature"


class GeometryType(Enum):
    Point = "Point"
    Polygon = "Polygon"


class PointGeometry(BaseModel):
    coordinates: List[float] = Field(
        description="[longitude, latitude] decimal coordinates",
        example=[60.5, 11.59],
        min_items=2,
        max_items=2,
    )
    type: GeometryType


class BoundingBoxGeometry(BaseModel):
    coordinates: List[List[List[float]]] = Field(
        description="[[[min_lon, min_lat], [max_lon, min_lat], [max_lon, max_lat], [min_lon, max_lat], [min_lon, min_lat]]]",
        example=[
            [[60.5, 11.59], [60.6, 11.59], [60.6, 11.6], [60.5, 11.6], [60.5, 11.59]]
        ],
    )
    type: GeometryType
