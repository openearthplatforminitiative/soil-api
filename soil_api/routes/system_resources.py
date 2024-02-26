import os

import rasterio
from fastapi import APIRouter, Response
from healthcheck import HealthCheck

from soil_api import constants
from soil_api.config import settings

router = APIRouter()


def soilgrids_healthcheck():
    soil_map = "wrb"
    soil_map_fname = constants.SOIL_MAPS[soil_map]
    soil_map_path = os.path.join(constants.SOIL_MAPS_URL, soil_map, soil_map_fname)
    try:
        with rasterio.open(soil_map_path) as src:
            return True, "SoilGrids service is available"
    except Exception as e:
        return False, f"SoilGrids service not available: {str(e)}"


health = HealthCheck(success_ttl=120)
health.add_check(soilgrids_healthcheck)
health.add_section("version", settings.version)


@router.get(
    "/ready",
    summary="Check if this service is ready to receive requests",
    description="Returns a message describing the status of this service",
    tags=["health"],
)
async def ready() -> Response:
    message, status_code, headers = health.run()
    return Response(content=message, headers=headers, status_code=status_code)


@router.get(
    "/health",
    summary="Check if this service is alive",
    description="Returns a simple message to indicate that this service is alive",
    tags=["health"],
)
async def liveness() -> dict[str, str]:
    return {"message": "Ok"}
