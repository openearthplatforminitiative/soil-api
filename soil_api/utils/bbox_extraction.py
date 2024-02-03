import numpy as np
import rasterio
from rasterio.windows import from_bounds

# Bounding box coordinates (minx, miny, maxx, maxy)
# Needs to be in the same CRS as the raster
# So EPSG:4326 for the wrb map and Homolosine for the ocs map
# bbox = (-122.3, 37.8, -122.2, 37.9)
# bbox = (-8533366.3, 5034390.3, -8532366.6, 5035129.8)


# bbox = (-13093449.3551741037517786,4207876.7519857408478856, -13082006.8144019693136215,4219008.7010650578886271)


def extract_bbox_from_raster(raster_path, bbox):
    with rasterio.open(raster_path) as src:
        # Get the window corresponding to the bounding box
        window = from_bounds(*bbox, transform=src.transform)

        # Read the data within the specified window
        data = src.read(window=window)

        # Use numpy.unique to get unique elements and their counts
        unique_elements, element_counts = np.unique(data, return_counts=True)

        # Create a dictionary from the results
        element_counts_dict = dict(zip(unique_elements, element_counts))

        return element_counts_dict
