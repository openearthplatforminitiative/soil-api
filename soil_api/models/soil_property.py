from enum import Enum
from typing import List

from pydantic import BaseModel, Field

from soil_api.models.shared import FeatureType, PointGeometry


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


class SoilMappedUnits(Enum):
    cg_cm3 = "cg/cm³"
    mmol_c_kg = "mmol(c)/kg"
    cm3_dm3 = "cm³/dm³"
    g_kg = "g/kg"
    cg_kg = "cg/kg"
    hg_m3 = "hg/m³"
    t_ha = "t/ha"
    pH_10 = "pH*10"
    dg_kg = "dg/kg"


class SoilTargetUnits(Enum):
    kg_dm3 = "kg/dm³"
    cmol_c_kg = "cmol(c)/kg"
    cm3_100cm3 = "cm³/100cm³"
    percent = "%"
    g_kg = "g/kg"
    hg_m3 = "hg/m³"
    kg_m2 = "kg/m²"
    pH = "pH"


class SoilConversionFactors(Enum):
    ten = 10
    hundred = 100


soil_property_dict = {
    SoilPropertiesCodes.bdod: {
        "name": "Bulk density",
        "mapped_units": SoilMappedUnits.cg_cm3,
        "target_units": SoilTargetUnits.kg_dm3,
        "conversion_factor": SoilConversionFactors.hundred,
    },
    SoilPropertiesCodes.cec: {
        "name": "Cation exchange capacity (CEC pH 7)",
        "mapped_units": SoilMappedUnits.mmol_c_kg,
        "target_units": SoilTargetUnits.cmol_c_kg,
        "conversion_factor": SoilConversionFactors.ten,
    },
    SoilPropertiesCodes.cfvo: {
        "name": "Coarse fragments",
        "mapped_units": SoilMappedUnits.cm3_dm3,
        "target_units": SoilTargetUnits.cm3_100cm3,
        "conversion_factor": SoilConversionFactors.ten,
    },
    SoilPropertiesCodes.clay: {
        "name": "Clay",
        "mapped_units": SoilMappedUnits.g_kg,
        "target_units": SoilTargetUnits.percent,
        "conversion_factor": SoilConversionFactors.ten,
    },
    SoilPropertiesCodes.nitrogen: {
        "name": "Nitrogen",
        "mapped_units": SoilMappedUnits.cg_kg,
        "target_units": SoilTargetUnits.g_kg,
        "conversion_factor": SoilConversionFactors.hundred,
    },
    SoilPropertiesCodes.ocd: {
        "name": "Organic carbon density",
        "mapped_units": SoilMappedUnits.hg_m3,
        "target_units": SoilTargetUnits.hg_m3,
        "conversion_factor": SoilConversionFactors.ten,
    },
    SoilPropertiesCodes.ocs: {
        "name": "Organic carbon stocks",
        "mapped_units": SoilMappedUnits.t_ha,
        "target_units": SoilTargetUnits.kg_m2,
        "conversion_factor": SoilConversionFactors.ten,
    },
    SoilPropertiesCodes.phh2o: {
        "name": "pH water",
        "mapped_units": SoilMappedUnits.pH_10,
        "target_units": SoilTargetUnits.pH,
        "conversion_factor": SoilConversionFactors.ten,
    },
    SoilPropertiesCodes.sand: {
        "name": "Sand",
        "mapped_units": SoilMappedUnits.g_kg,
        "target_units": SoilTargetUnits.percent,
        "conversion_factor": SoilConversionFactors.ten,
    },
    SoilPropertiesCodes.silt: {
        "name": "Silt",
        "mapped_units": SoilMappedUnits.g_kg,
        "target_units": SoilTargetUnits.percent,
        "conversion_factor": SoilConversionFactors.ten,
    },
    SoilPropertiesCodes.soc: {
        "name": "Soil organic carbon",
        "mapped_units": SoilMappedUnits.dg_kg,
        "target_units": SoilTargetUnits.g_kg,
        "conversion_factor": SoilConversionFactors.ten,
    },
}


class SoilPropertyUnit(BaseModel):
    conversion_factor: SoilConversionFactors = Field(
        ..., description="The conversion factor", example=10
    )
    mapped_units: SoilMappedUnits = Field(
        ..., description="The mapped unit of the soil property", example="cm³/dm³"
    )
    target_units: SoilTargetUnits = Field(
        ..., description="The target unit of the soil property", example="m³/ha"
    )
    uncertainty_unit: str = Field(
        ..., description="The unit of the uncertainty", example=""
    )


class SoilDepthLabels(Enum):
    depth_0_5 = "0-5cm"
    depth_0_30 = "0-30cm"
    depth_5_15 = "5-15cm"
    depth_15_30 = "15-30cm"
    depth_30_60 = "30-60cm"
    depth_60_100 = "60-100cm"
    depth_100_200 = "100-200cm"


class SoilDepths(Enum):
    d_0 = 0
    d_5 = 5
    d_15 = 15
    d_30 = 30
    d_60 = 60
    d_100 = 100
    d_200 = 200


class SoilDepthUnits(Enum):
    cm = "cm"


soil_depth_dict = {
    SoilDepthLabels.depth_0_5: {
        "top_depth": SoilDepths.d_0,
        "bottom_depth": SoilDepths.d_5,
        "unit_depth": SoilDepthUnits.cm,
    },
    SoilDepthLabels.depth_0_30: {
        "top_depth": SoilDepths.d_0,
        "bottom_depth": SoilDepths.d_30,
        "unit_depth": SoilDepthUnits.cm,
    },
    SoilDepthLabels.depth_5_15: {
        "top_depth": SoilDepths.d_5,
        "bottom_depth": SoilDepths.d_15,
        "unit_depth": SoilDepthUnits.cm,
    },
    SoilDepthLabels.depth_15_30: {
        "top_depth": SoilDepths.d_15,
        "bottom_depth": SoilDepths.d_30,
        "unit_depth": SoilDepthUnits.cm,
    },
    SoilDepthLabels.depth_30_60: {
        "top_depth": SoilDepths.d_30,
        "bottom_depth": SoilDepths.d_60,
        "unit_depth": SoilDepthUnits.cm,
    },
    SoilDepthLabels.depth_60_100: {
        "top_depth": SoilDepths.d_60,
        "bottom_depth": SoilDepths.d_100,
        "unit_depth": SoilDepthUnits.cm,
    },
    SoilDepthLabels.depth_100_200: {
        "top_depth": SoilDepths.d_100,
        "bottom_depth": SoilDepths.d_200,
        "unit_depth": SoilDepthUnits.cm,
    },
}

top_depth, bottom_depth, depth_unit = soil_depth_dict[SoilDepthLabels.depth_0_5]


class DepthRange(BaseModel):
    top_depth: SoilDepths = Field(..., description="The top depth", example=0)
    bottom_depth: SoilDepths = Field(..., description="The bottom depth", example=5)
    unit_depth: SoilDepthUnits = Field(
        ..., description="The unit of the depth range", example="cm"
    )


class SoilPropertyValueTypes(Enum):
    mean = "mean"
    Q0_05 = "Q0.05"
    Q0_5 = "Q0.5"
    Q0_95 = "Q0.95"
    uncertainty = "uncertainty"


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


class SoilDepth(BaseModel):
    range: DepthRange = Field(..., description="The soil depth range")
    label: SoilDepthLabels = Field(..., description="The soil depth label")
    values: SoilPropertyValues = Field(
        ..., description="The queried soil property values"
    )


class SoilLayer(BaseModel):
    code: SoilPropertiesCodes = Field(
        ..., description="The soil property code", example="bdod"
    )
    name: str = Field(
        ..., description="The name of the soil property", example="Bulk density"
    )
    unit_measure: SoilPropertyUnit = Field(
        ..., description="The unit of the soil property"
    )
    depths: List[SoilDepth] = Field(
        ..., description="The queried soil depths with values"
    )


class SoilLayerList(BaseModel):
    layers: List[SoilLayer] = Field(..., description="The queried soil property layers")


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
