import asyncio
from functools import partial

import rasterio
from fastapi import HTTPException
from rasterio.crs import CRS
from rasterio.warp import transform_geom

from soil_api.config import settings


def transfrom_coordinates_to_homolosine_crs(
    latitude: float, longitude: float
) -> tuple[float, float]:
    """Transforms coordinates to the Homolosine CRS.

    Args:
    - latitude (float): Latitude in decimal degrees.
    - longitude (float): Longitude in decimal degrees.

    Returns:
    tuple: Transformed coordinates.
    """
    feature = {"type": "Point", "coordinates": [longitude, latitude]}
    crs = CRS.from_string(settings.homolosine_crs_wkt)
    feature_proj = transform_geom(CRS.from_epsg(4326), crs, feature)
    latitude = feature_proj["coordinates"][1]
    longitude = feature_proj["coordinates"][0]
    return latitude, longitude


async def extract_point_from_raster(
    raster_path: str, latitude: float, longitude: float
) -> int:
    """Extracts value from raster at given point.
    If raster_path is None, returns settings.no_data_val.
    If the raster file cannot be read, returns an HTTPException.

    Args:
    - raster_path (str): Path to raster file.
    - latitude (float): Latitude in decimal degrees.
    - longitude (float): Longitude in decimal degrees.

    Returns:
    int: Value at given point.
    """
    if raster_path is None:
        return settings.no_data_val
    loop = asyncio.get_running_loop()
    try:
        src = await loop.run_in_executor(None, rasterio.open, raster_path)
        value_generator = await loop.run_in_executor(
            None, partial(src.sample, [[longitude, latitude]])
        )
        value = next(value_generator)[0]
        src.close()
    except rasterio.errors.RasterioIOError as e:
        # return HTTP exception
        raise HTTPException(
            status_code=404,
            detail=f"Error reading raster file: {raster_path}. Due to: {str(e)}",
        )
    return value
