from __future__ import annotations

from enum import Enum
from typing import List

from pydantic import BaseModel, Field


class FeatureType(Enum):
    Feature = "Feature"


class GeometryType(Enum):
    Point = "Point"


class SoilTypes(Enum):
    Acrisols = "Acrisols"
    Albeluvisols = "Albeluvisols"
    Alisols = "Alisols"
    Andosols = "Andosols"
    Arenosols = "Arenosols"
    Calcisols = "Calcisols"
    Cambisols = "Cambisols"
    Chernozems = "Chernozems"
    Cryosols = "Cryosols"
    Durisols = "Durisols"
    Ferralsols = "Ferralsols"
    Fluvisols = "Fluvisols"
    Gleysols = "Gleysols"
    Gypsisols = "Gypsisols"
    Histosols = "Histosols"
    Kastanozems = "Kastanozems"
    Leptosols = "Leptosols"
    Lixisols = "Lixisols"
    Luvisols = "Luvisols"
    Nitisols = "Nitisols"
    Phaeozems = "Phaeozems"
    Planosols = "Planosols"
    Plinthosols = "Plinthosols"
    Podzols = "Podzols"
    Regosols = "Regosols"
    Solonchaks = "Solonchaks"
    Solonetz = "Solonetz"
    Stagnosols = "Stagnosols"
    Umbrisols = "Umbrisols"
    Vertisols = "Vertisols"
    No_information = "No information available."


class SoilType(BaseModel):
    soil_type: SoilTypes = Field(
        ..., description="The queried soil type", example="Acrisols"
    )


class SoilProperties(Enum):
    bdod = "Bulk density"  # cg/cm³
    cec = "Cation exchange capacity (CEC pH 7)"  # mmol(c)/kg
    cfvo = "Coarse fragments"  # cm³/dm³
    clay = "Clay"  # g/kg
    nitrogen = "Nitrogen"  # cg/kg
    ocd = "Organic carbon density"  # hg/m³
    ocs = "Organic carbon stocks"  # t/ha
    phh2o = "pH water"  # pH*10
    sand = "Sand"  # g/kg
    silt = "Silt"  # g/kg
    soc = "Soil organic carbon"  # dg/kg


class SoilProperty(BaseModel):
    value: int | str = Field(
        ..., description="The value of the queried soil property", example=50
    )
    unit: str = Field(
        ..., description="The unit of the queried soil property", example="g/kg"
    )
    property: SoilProperties = Field(
        ..., description="The queried soil property", example="Soil organic carbon"
    )


class PointGeometry(BaseModel):
    coordinates: List[float] = Field(
        description="[longitude, latitude] decimal coordinates",
        example=[60.5, 11.59],
        min_items=2,
        max_items=2,
    )
    type: GeometryType


class SoilPropertyJSON(BaseModel):
    type: FeatureType = Field(
        description="The feature type of this geojson-object",
        default=FeatureType.Feature,
        example="Feature",
    )
    geometry: PointGeometry = Field(
        ...,
        description="The geometry of the queried location",
    )
    properties: SoilProperty = Field(
        ...,
        description="The queried soil property information",
    )


class SoilTypeJSON(BaseModel):
    type: FeatureType = Field(
        description="The feature type of this geojson-object",
        default=FeatureType.Feature,
        example="Feature",
    )
    geometry: PointGeometry = Field(
        ...,
        description="The geometry of the queried location",
    )
    properties: SoilType = Field(
        ...,
        description="The queried soil type information",
    )
