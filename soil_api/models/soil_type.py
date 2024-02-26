from enum import Enum
from typing import List

from pydantic import BaseModel, Field, field_serializer

from soil_api.models.shared import BoundingBoxGeometry, FeatureType, PointGeometry


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
    No_information = "No information"


soil_type_dict = {
    0: SoilTypes.Acrisols,
    1: SoilTypes.Albeluvisols,
    2: SoilTypes.Alisols,
    3: SoilTypes.Andosols,
    4: SoilTypes.Arenosols,
    5: SoilTypes.Calcisols,
    6: SoilTypes.Cambisols,
    7: SoilTypes.Chernozems,
    8: SoilTypes.Cryosols,
    9: SoilTypes.Durisols,
    10: SoilTypes.Ferralsols,
    11: SoilTypes.Fluvisols,
    12: SoilTypes.Gleysols,
    13: SoilTypes.Gypsisols,
    14: SoilTypes.Histosols,
    15: SoilTypes.Kastanozems,
    16: SoilTypes.Leptosols,
    17: SoilTypes.Lixisols,
    18: SoilTypes.Luvisols,
    19: SoilTypes.Nitisols,
    20: SoilTypes.Phaeozems,
    21: SoilTypes.Planosols,
    22: SoilTypes.Plinthosols,
    23: SoilTypes.Podzols,
    24: SoilTypes.Regosols,
    25: SoilTypes.Solonchaks,
    26: SoilTypes.Solonetz,
    27: SoilTypes.Stagnosols,
    28: SoilTypes.Umbrisols,
    29: SoilTypes.Vertisols,
    255: SoilTypes.No_information,  # SoilGrids WRB code for no data
}


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
