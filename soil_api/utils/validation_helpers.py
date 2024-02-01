from fastapi import HTTPException

from soil_api.config import settings
from soil_api.models.soil import SoilProperties

ISRIC_ROI = settings.isric_roi


def validate_property(property: str) -> None:
    """Validate the property parameter.

    Parameters:
    - property (str): The soil property to validate.

    Returns:
    None
    """
    if property not in SoilProperties.__members__:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid property: {property}. Must be one of: {', '.join(SoilProperties.__members__)}",
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
    elif property != "ocs" and depth not in settings.depths:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid depth: '{depth}' for property '{property}'. Must be one of: {', '.join(settings.depths)}",
        )
