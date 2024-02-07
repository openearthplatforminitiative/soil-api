from __future__ import annotations

from enum import Enum
from typing import List

from pydantic import BaseModel, Field

from soil_api.models.shared import BoundingBoxGeometry, FeatureType, PointGeometry


class SoilTypes(Enum):
    t0 = "Acrisols"
    t1 = "Albeluvisols"
    t2 = "Alisols"
    t3 = "Andosols"
    t4 = "Arenosols"
    t5 = "Calcisols"
    t6 = "Cambisols"
    t7 = "Chernozems"
    t8 = "Cryosols"
    t9 = "Durisols"
    t10 = "Ferralsols"
    t11 = "Fluvisols"
    t12 = "Gleysols"
    t13 = "Gypsisols"
    t14 = "Histosols"
    t15 = "Kastanozems"
    t16 = "Leptosols"
    t17 = "Lixisols"
    t18 = "Luvisols"
    t19 = "Nitisols"
    t20 = "Phaeozems"
    t21 = "Planosols"
    t22 = "Plinthosols"
    t23 = "Podzols"
    t24 = "Regosols"
    t25 = "Solonchaks"
    t26 = "Solonetz"
    t27 = "Stagnosols"
    t28 = "Umbrisols"
    t29 = "Vertisols"
    No_information = "No information available"


class SoilTypeProbability(BaseModel):
    soil_type: SoilTypes = Field(..., description="The soil type", example="Acrisols")
    probability: int = Field(
        ...,
        description="The probability of the soil type as an integer between 0 and 100",
        example=70,
    )


class SoilTypeInfo(BaseModel):
    most_probable_soil_type: SoilTypes = Field(
        ...,
        description="The most probable soil type at the queried location",
        example="Acrisols",
    )
    probabilities: List[SoilTypeProbability] | None = Field(
        None, description="The soil type probabilities"
    )


class SoilTypeSummary(BaseModel):
    soil_type: SoilTypes = Field(..., description="The soil type", example="Acrisols")
    count: int = Field(
        ...,
        description="The number of occurrences of the soil type within the queried bounding box",
        example=70,
    )


class SoilTypeJSON(BaseModel):
    type: FeatureType = Field(
        description="The feature type of the geojson-object",
    )
    geometry: PointGeometry = Field(
        ...,
        description="The geometry of the queried location",
    )
    properties: SoilTypeInfo = Field(
        ...,
        description="The soil type information at the queried location",
    )


class SoilTypeSummaryInfo(BaseModel):
    summaries: List[SoilTypeSummary] = Field(
        ..., description="The soil type summaries within the queried bounding box"
    )


class SoilTypeSummaryJSON(BaseModel):
    type: FeatureType = Field(
        description="The feature type of this geojson-object",
    )
    geometry: BoundingBoxGeometry = Field(
        ...,
        description="The geometry of the queried location",
    )
    properties: SoilTypeSummaryInfo = Field(
        ...,
        description="The soil type summary information",
    )
