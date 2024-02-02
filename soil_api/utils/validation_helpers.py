from fastapi import HTTPException

from soil_api.config import settings
from soil_api.models.soil import SoilPropertiesCodes, SoilPropertyValues

ISRIC_ROI = settings.isric_roi


def validate_property(property: str) -> None:
    """Validate the property parameter.

    Parameters:
    - property (str): The soil property to validate.

    Returns:
    None
    """
    if property not in SoilPropertiesCodes.__members__:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid property: {property}. Must be one of: {', '.join(SoilPropertiesCodes.__members__)}",
        )


def validate_properties(properties: list[str]) -> None:
    """Validate the properties parameter.

    Parameters:
    - properties (list[str]): The soil properties to validate.

    Returns:
    None
    """
    # Check if all properties are valid using set intersection
    invalid_properties = set(properties) - set(SoilPropertiesCodes.__members__)
    if invalid_properties:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid properties: {', '.join(invalid_properties)}. Must be one of: {', '.join(SoilPropertiesCodes.__members__)}",
        )


def validate_coordinates(latitude: float, longitude: float) -> None:
    """
    Check if the given point is within the region of interest (ROI).
    If not, raise an HTTPException with status code 404.

    Parameters:
    - latitude (float): The latitude of the point.
    - longitude (float): The longitude of the point.

    Returns:
    None
    """
    point_within_roi = (
        ISRIC_ROI["min_lat"] <= latitude <= ISRIC_ROI["max_lat"]
        and ISRIC_ROI["min_lon"] <= longitude <= ISRIC_ROI["max_lon"]
    )

    if not point_within_roi:
        raise HTTPException(
            status_code=404,
            detail="Queried coordinates are outside the region of interest",
        )


def validate_depth(depth: str, property: str) -> None:
    """Validate the depth parameter.

    Parameters:
    - depth (str): The depth to validate.
    - property (str): The soil property to validate.

    Returns:
    None
    """
    if property == "ocs" and depth != "0-30":
        raise HTTPException(
            status_code=400,
            detail=f"Invalid depth: '{depth}' for property 'ocs'. Must be '0-30'.",
        )
    elif property != "ocs" and depth not in list(settings.depths.keys):
        raise HTTPException(
            status_code=400,
            detail=f"Invalid depth: '{depth}' for property '{property}'. Must be one of: {', '.join(list(settings.depths.keys()))}",
        )


def validate_depths(depths: list[str]) -> None:
    """Validate the depths parameter.

    Parameters:
    - depths (list[str]): The depths to validate.

    Returns:
    None
    """
    invalid_depths = set(depths) - set(settings.depths.keys())
    if invalid_depths:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid depths: {', '.join(invalid_depths)}. Must be one of: {', '.join(list(settings.depths.keys()))}",
        )


def validate_values(values: list[str]) -> None:
    """Validate the values parameter.

    Parameters:
    - values (list[str]): The values to validate.

    Returns:
    None
    """
    invalid_values = set(values) - set(SoilPropertyValues.__annotations__)
    if invalid_values:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid values: {', '.join(invalid_values)}. Must be one of: {', '.join(SoilPropertyValues.__annotations__)}",
        )
