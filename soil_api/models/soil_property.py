from __future__ import annotations

from enum import Enum
from typing import List

from pydantic import BaseModel, Field

from soil_api.models.shared import FeatureType, PointGeometry


class SoilPropertiesNames(Enum):
    bdod = "Bulk density"
    cec = "Cation exchange capacity (CEC pH 7)"
    cfvo = "Coarse fragments"
    clay = "Clay"
    nitrogen = "Nitrogen"
    ocd = "Organic carbon density"
    ocs = "Organic carbon stocks"
    phh2o = "pH water"
    sand = "Sand"
    silt = "Silt"
    soc = "Soil organic carbon"


class SoilPropertiesCodes(Enum):
    bdod = "bdod"
    cec = "cec"
    cfvo = "cfvo"
    clay = "clay"
    nitrogen = "nitrogen"
    ocd = "ocd"
    ocs = "ocs"
    phh2o = "phh2o"
    sand = "sand"
    silt = "silt"
    soc = "soc"


class SoilPropertiesMappedUnits(Enum):
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


class SoilPropertiesTargetUnits(Enum):
    bdod = "kg/dm³"
    cec = "cmol(c)/kg"
    cfvo = "cm³/100cm³"
    clay = "%"
    nitrogen = "g/kg"
    ocd = "hg/m³"
    ocs = "kg/m²"
    phh2o = "pH"
    sand = "%"
    silt = "%"
    soc = "g/kg"


class SoilPropertiesConversionFactors(Enum):
    bdod = 100
    cec = 10
    cfvo = 10
    clay = 10
    nitrogen = 100
    ocd = 10
    ocs = 10
    phh2o = 10
    sand = 10
    silt = 10
    soc = 10


class SoilLayerList(BaseModel):
    layers: List[SoilLayer] = Field(..., description="The queried soil property layers")


class SoilPropertyUnit(BaseModel):
    d_factor: SoilPropertiesConversionFactors = Field(
        ..., description="The conversion factor", example=10
    )
    mapped_units: SoilPropertiesMappedUnits = Field(
        ..., description="The mapped unit of the soil property", example="cm³/dm³"
    )
    target_units: SoilPropertiesTargetUnits = Field(
        ..., description="The target unit of the soil property", example="m³/ha"
    )
    uncertainty_unit: str = Field(
        ..., description="The unit of the uncertainty", example=""
    )


class SoilLayer(BaseModel):
    code: SoilPropertiesCodes = Field(
        ..., description="The soil property code", example="bdod"
    )
    name: SoilPropertiesNames = Field(
        ..., description="The name of the soil property", example="Bulk density"
    )
    unit_measure: SoilPropertyUnit = Field(
        ..., description="The unit of the soil property"
    )
    depths: List[SoilDepth] = Field(
        ..., description="The queried soil depths with values"
    )


class SoilPropertyValues(BaseModel):
    mean: float | None = Field(
        None, description="The mean value of the soil property", example=50
    )
    Q0_05: float | None = Field(
        None,
        description="The 5th percentile of the soil property",
        example=40,
        alias="Q0.05",
    )
    Q0_5: float | None = Field(
        None,
        description="The 50th percentile of the soil property",
        example=50,
        alias="Q0.5",
    )
    Q0_95: float | None = Field(
        None,
        description="The 95th percentile of the soil property",
        example=60,
        alias="Q0.95",
    )
    uncertainty: float | None = Field(
        None, description="The uncertainty of the soil property", example=5
    )


class SoilDepthLabels(Enum):
    depth_0_5 = "0-5cm"
    depth_0_30 = "0-30cm"
    depth_5_15 = "5-15cm"
    depth_15_30 = "15-30cm"
    depth_30_60 = "30-60cm"
    depth_60_100 = "60-100cm"
    depth_100_200 = "100-200cm"


# Create a reverse lookup dictionary
REVERSE_DEPTH_LOOKUP = {
    v.value: k for k, v in list(SoilDepthLabels.__members__.items())
}


# Function to get the enum member using the reverse lookup
def get_soil_depth_from_label(depth_string: str) -> SoilDepthLabels:
    try:
        return REVERSE_DEPTH_LOOKUP[depth_string]
    except KeyError:
        raise ValueError(f"No soil depth label found for '{depth_string}'")


class SoilDepthTop(Enum):
    depth_0_5 = 0
    depth_0_30 = 0
    depth_5_15 = 5
    depth_15_30 = 15
    depth_30_60 = 30
    depth_60_100 = 60
    depth_100_200 = 100


class SoilDepthBottom(Enum):
    depth_0_5 = 5
    depth_0_30 = 30
    depth_5_15 = 15
    depth_15_30 = 30
    depth_30_60 = 60
    depth_60_100 = 100
    depth_100_200 = 200


class SoilDepthUnits(Enum):
    depth_0_5 = "cm"
    depth_0_30 = "cm"
    depth_5_15 = "cm"
    depth_15_30 = "cm"
    depth_30_60 = "cm"
    depth_60_100 = "cm"
    depth_100_200 = "cm"


class SoilDepth(BaseModel):
    range: DepthRange = Field(..., description="The soil depth range")
    label: SoilDepthLabels = Field(..., description="The soil depth label")
    values: SoilPropertyValues = Field(
        ..., description="The queried soil property values"
    )


class DepthRange(BaseModel):
    top_depth: SoilDepthTop = Field(..., description="The top depth", example=0)
    bottom_depth: SoilDepthBottom = Field(
        ..., description="The bottom depth", example=5
    )
    unit_depth: SoilDepthUnits = Field(
        ..., description="The unit of the depth range", example="cm"
    )


class SoilPropertyJSON(BaseModel):
    type: FeatureType = Field(
        description="The feature type of the geojson-object",
    )
    geometry: PointGeometry = Field(
        ...,
        description="The geometry of the queried location",
    )
    properties: SoilLayerList = Field(
        ...,
        description="The queried soil property information",
    )
