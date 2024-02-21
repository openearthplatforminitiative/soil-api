from fastapi import HTTPException
from soil_api import constants

from soil_api.models.soil_property import (
    SoilDepthLabels,
    SoilPropertiesCodes,
    SoilPropertyValueTypes,
)

ISRIC_ROI = constants.ISRIC_ROI


def validate_properties(properties: list[str]) -> None:
    """Validate the properties parameter. If any of the properties are
    invalid, raise an HTTPException with status code 400.

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
            detail=(
                f"Invalid properties: {', '.join(invalid_properties)}. "
                f"Must be one of: {', '.join(SoilPropertiesCodes.__members__)}"
            ),
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


def validate_depths(depths: list[str]) -> None:
    """Validate the depths parameter. If any of the depths are invalid,
    raise an HTTPException with status code 400.

    Parameters:
    - depths (list[str]): The depths to validate.

    Returns:
    None
    """
    all_depth_labels = [depth.value for depth in SoilDepthLabels]
    invalid_depths = set(depths) - set(all_depth_labels)
    if invalid_depths:
        raise HTTPException(
            status_code=400,
            detail=(
                f"Invalid depths: {', '.join(invalid_depths)}. Must"
                f" be one of: {', '.join(all_depth_labels)}"
            ),
        )


def validate_values(values: list[str]) -> None:
    """Validate the values parameter. If any of the values are invalid,
    raise an HTTPException with status code 400.

    Parameters:
    - values (list[str]): The values to validate.

    Returns:
    None
    """
    all_value_types = [v.value for v in SoilPropertyValueTypes]
    invalid_values = set(values) - set(all_value_types)
    if invalid_values:
        raise HTTPException(
            status_code=400,
            detail=(
                f"Invalid values: {', '.join(invalid_values)}. Must "
                f"be one of: {', '.join(all_value_types)}"
            ),
        )


def validate_bbox(bbox: list[float]) -> None:
    """Validate the bbox parameter. If the bbox is invalid, raise an
    HTTPException with status code 400. If the bbox is outside the region
    of interest, raise an HTTPException with status code 404.

    Parameters:
    - bbox (list[float]): The bounding box to validate.

    Returns:
    None
    """
    if bbox[0] > bbox[2] or bbox[1] > bbox[3]:
        raise HTTPException(
            status_code=400,
            detail=(
                f"Invalid bbox: {bbox}. The first two values must be the lower "
                "left corner and the last two values must be the upper right corner."
            ),
        )
