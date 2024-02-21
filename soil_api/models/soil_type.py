from __future__ import annotations

from enum import Enum
from typing import List

from pydantic import BaseModel, Field, field_serializer

from soil_api.models.shared import BoundingBoxGeometry, FeatureType, PointGeometry


class SoilTypes(Enum):
    Acrisols = 0
    Albeluvisols = 1
    Alisols = 2
    Andosols = 3
    Arenosols = 4
    Calcisols = 5
    Cambisols = 6
    Chernozems = 7
    Cryosols = 8
    Durisols = 9
    Ferralsols = 10
    Fluvisols = 11
    Gleysols = 12
    Gypsisols = 13
    Histosols = 14
    Kastanozems = 15
    Leptosols = 16
    Lixisols = 17
    Luvisols = 18
    Nitisols = 19
    Phaeozems = 20
    Planosols = 21
    Plinthosols = 22
    Podzols = 23
    Regosols = 24
    Solonchaks = 25
    Solonetz = 26
    Stagnosols = 27
    Umbrisols = 28
    Vertisols = 29
    No_information = 255  # SoilGrids WRB code for no data


class SoilTypeProbability(BaseModel):
    soil_type: SoilTypes = Field(..., description="The soil type", example="Acrisols")
    probability: int = Field(
        ...,
        description="The probability of the soil type as an integer between 0 and 100",
        example=70,
    )

    @field_serializer("soil_type")
    def serialize_group(self, soil_type: SoilTypes, _info):
        return soil_type.name


class SoilTypeInfo(BaseModel):
    most_probable_soil_type: SoilTypes = Field(
        ...,
        description="The most probable soil type at the queried location",
        example="Acrisols",
    )
    probabilities: List[SoilTypeProbability] | None = Field(
        None, description="The soil type probabilities"
    )

    @field_serializer("most_probable_soil_type")
    def serialize_group(self, most_probable_soil_type: SoilTypes, _info):
        return most_probable_soil_type.name


class SoilTypeSummary(BaseModel):
    soil_type: SoilTypes = Field(..., description="The soil type", example="Acrisols")
    count: int = Field(
        ...,
        description="The number of occurrences of the soil type within the queried bounding box",
        example=70,
    )

    @field_serializer("soil_type")
    def serialize_group(self, soil_type: SoilTypes, _info):
        return soil_type.name


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
