import pathlib

from fastapi import FastAPI
from fastapi.openapi.docs import get_redoc_html
from fastapi.staticfiles import StaticFiles

from soil_api.config import settings
from soil_api.openapi import openapi
from soil_api.routes import soil_routes, system_resources


def get_application() -> FastAPI:
    this_dir = pathlib.Path(__file__).parent

    api = FastAPI(
        root_path=settings.api_root_path,
        redoc_url=None,
    )
    api.include_router(soil_routes.router)
    api.include_router(system_resources.router)

    api.openapi_schema = openapi.custom_openapi(api, this_dir / "example_code")

    return api


app = get_application()


@app.get("/redoc", include_in_schema=False)
def redoc():
    return get_redoc_html(
        openapi_url=f"{settings.api_root_path}/openapi.json",
        title="Soil API",
        redoc_favicon_url="https://www.openepi.io/favicon.ico",
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "soil_api.__main__:app",
        host=settings.server_bind_host,
        port=settings.server_bind_port,
    )
