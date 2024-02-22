from fastapi import HTTPException

from soil_api import constants

ISRIC_ROI = constants.ISRIC_ROI


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
