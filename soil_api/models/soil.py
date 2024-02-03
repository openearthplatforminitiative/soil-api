from __future__ import annotations

from enum import Enum
from typing import List

from pydantic import BaseModel, Field


class FeatureType(Enum):
    Feature = "Feature"


class GeometryType(Enum):
    Point = "Point"


# class SoilTypes(Enum):
#     Acrisols = "Acrisols"
#     Albeluvisols = "Albeluvisols"
#     Alisols = "Alisols"
#     Andosols = "Andosols"
#     Arenosols = "Arenosols"
#     Calcisols = "Calcisols"
#     Cambisols = "Cambisols"
#     Chernozems = "Chernozems"
#     Cryosols = "Cryosols"
#     Durisols = "Durisols"
#     Ferralsols = "Ferralsols"
#     Fluvisols = "Fluvisols"
#     Gleysols = "Gleysols"
#     Gypsisols = "Gypsisols"
#     Histosols = "Histosols"
#     Kastanozems = "Kastanozems"
#     Leptosols = "Leptosols"
#     Lixisols = "Lixisols"
#     Luvisols = "Luvisols"
#     Nitisols = "Nitisols"
#     Phaeozems = "Phaeozems"
#     Planosols = "Planosols"
#     Plinthosols = "Plinthosols"
#     Podzols = "Podzols"
#     Regosols = "Regosols"
#     Solonchaks = "Solonchaks"
#     Solonetz = "Solonetz"
#     Stagnosols = "Stagnosols"
#     Umbrisols = "Umbrisols"
#     Vertisols = "Vertisols"
#     No_information = "No information available."


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
    No_information = "No information available."


class SoilTypeProbability(BaseModel):
    soil_type: SoilTypes = Field(
        ..., description="The queried soil type", example="Acrisols"
    )
    probability: int = Field(
        ...,
        description="The probability of the queried soil type as an integer between 0 and 100",
        example=70,
    )


class SoilTypeInfo(BaseModel):
    soil_type: SoilTypes = Field(
        ..., description="The queried soil type", example="Acrisols"
    )
    probabilities: List[SoilTypeProbability] | None = Field(
        None, description="The queried soil type probabilities"
    )


class SoilPropertiesNames(Enum):
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


class SoilPropertiesCodes(Enum):
    bdod = "bdod"  # cg/cm³
    cec = "cec"  # mmol(c)/kg
    cfvo = "cfvo"  # cm³/dm³
    clay = "clay"  # g/kg
    nitrogen = "nitrogen"  # cg/kg
    ocd = "ocd"  # hg/m³
    ocs = "ocs"  # t/ha
    phh2o = "phh2o"  # pH*10
    sand = "sand"  # g/kg
    silt = "silt"  # g/kg
    soc = "soc"  # dg/kg


class SoilPropertyUnits(Enum):
    bdod = "cg/cm³"
    cec = "mmol(c)/kg"
    cfvo = "cm³/dm³"
    clay = "g/kg"
    nitrogen = "cg/kg"
    ocd = "hg/m³"
    ocs = "t/ha"
    phh2o = "pH*10"
    sand = "g/kg"
    silt = "g/kg"
    soc = "dg/kg"


class SoilProperty(BaseModel):
    value: int | str = Field(
        ..., description="The value of the queried soil property", example=50
    )
    unit: str = Field(
        ..., description="The unit of the queried soil property", example="g/kg"
    )
    property: SoilPropertiesNames = Field(
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


class SoilLayerList(BaseModel):
    layers: List[SoilLayer] = Field(..., description="The queried soil layers")


class SoilLayer(BaseModel):
    code: SoilPropertiesCodes = Field(
        ..., description="The soil property code", example="bdod"
    )
    name: SoilPropertiesNames = Field(
        ..., description="The name of the soil property", example="Bulk density"
    )
    unit: SoilPropertyUnits = Field(
        ..., description="The unit of the queried soil property", example="g/kg"
    )
    depths: List[SoilDepth] = Field(..., description="The queried soil depths")


class SoilPropertyValues(BaseModel):
    mean: float | None = Field(
        None, description="The mean value of the queried soil property", example=50
    )
    Q0_05: float | None = Field(
        None, description="The 5th percentile of the queried soil property", example=40
    )
    Q0_5: float | None = Field(
        None, description="The 50th percentile of the queried soil property", example=50
    )
    Q0_95: float | None = Field(
        None, description="The 95th percentile of the queried soil property", example=60
    )
    uncertainty: float | None = Field(
        None, description="The uncertainty of the queried soil property", example=5
    )


class SoilDepthLabels(Enum):
    depth_0_5 = "0-5cm"
    depth_5_15 = "5-15cm"
    depth_15_30 = "15-30cm"
    depth_30_60 = "30-60cm"
    depth_60_100 = "60-100cm"
    depth_100_200 = "100-200cm"
    depth_0_30 = "0-30cm"


class SoilDepth(BaseModel):
    range: DepthRange = Field(..., description="The queried soil depth range")
    label: SoilDepthLabels = Field(..., description="The queried soil depth label")
    values: SoilPropertyValues = Field(
        ..., description="The queried soil property values"
    )


class DepthRange(BaseModel):
    top_depth: int = Field(
        ..., description="The top depth of the queried soil property", example=0
    )
    bottom_depth: int = Field(
        ..., description="The bottom depth of the queried soil property", example=5
    )
    unit_depth: str = Field(
        ..., description="The unit of the queried soil property", example="cm"
    )


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
    properties: SoilLayerList = Field(
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
    properties: SoilTypeInfo = Field(
        ...,
        description="The queried soil type information",
    )
