import asyncio
from functools import partial

import numpy as np
import rasterio
from rasterio.crs import CRS
from rasterio.warp import transform_geom

from soil_api.config import settings


async def extract_point_from_raster(
    raster_path, latitude, longitude, transform_CRS=False
) -> int:
    """Extracts value from raster at given point.

    Args:
    - raster_path (str): Path to raster file.
    - latitude (float): Latitude in decimal degrees.
    - longitude (float): Longitude in decimal degrees.
    - transform_CRS (bool, optional): Whether to transform the coordinates to the
                                      Homolosine CRS. Defaults to False.

    Returns:
    int: Value at given point.
    """
    if transform_CRS:
        feature = {"type": "Point", "coordinates": [longitude, latitude]}

        crs = CRS.from_string(settings.homolosine_crs_wkt)

        # Project the feature to the desired CRS
        feature_proj = transform_geom(CRS.from_epsg(4326), crs, feature)

        longitude = feature_proj["coordinates"][0]
        latitude = feature_proj["coordinates"][1]

    loop = asyncio.get_running_loop()
    try:
        src = await loop.run_in_executor(None, rasterio.open, raster_path)
        value_generator = await loop.run_in_executor(
            None, partial(src.sample, [[longitude, latitude]])
        )
        value = next(value_generator)[0]
        src.close()
    except rasterio.errors.RasterioIOError:
        return -32768
    return value

    # perform a try-except block to catch any exceptions
    # that might occur when opening the raster file
    # try:
    #     async with rasterio.open(raster_path) as src:
    #         return src.sample([[longitude, latitude]])[0][0]
    # except Exception as e:
    #     # if an exception occurs, return 0
    #     return -1

    # async with rasterio.open(raster_path) as src:
    #     return src.sample([[longitude, latitude]])[0][0]
