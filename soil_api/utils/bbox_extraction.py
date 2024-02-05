import numpy as np
import rasterio
from rasterio.windows import from_bounds


def extract_bbox_from_raster(raster_path: str, bbox: list[float]) -> dict:
    """Extracts the counts of unique elements within the
    specified bounding box from the raster.

    Args:
    - raster_path (str): Path to the raster file.
    - bbox (list[float]): The bounding box to extract from with
        the format [minx, miny, maxx, maxy].

    Returns:
    dict: A dictionary with the unique elements as keys and
        their counts as values.
    """
    with rasterio.open(raster_path) as src:
        # Get the window corresponding to the bounding box
        window = from_bounds(*bbox, transform=src.transform)
        # Read the data within the specified window
        data = src.read(window=window)
        # Use numpy.unique to get unique elements and their counts
        unique_elements, element_counts = np.unique(data, return_counts=True)
        element_counts_dict = dict(zip(unique_elements, element_counts))
        return element_counts_dict
