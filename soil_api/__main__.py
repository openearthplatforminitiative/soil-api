import pathlib

from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.openapi.docs import get_redoc_html
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from prometheus_fastapi_instrumentator import Instrumentator
from pydantic_core import PydanticUndefinedType

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

    # The OpenEPI logo needs to be served as a static file since it is referenced in the OpenAPI schema
    app.mount("/static", StaticFiles(directory="assets/"), name="static")


    api.openapi_schema = openapi.custom_openapi(api, this_dir / "example_code")
    Instrumentator().instrument(api).expose(api)
    return api


app = get_application()


# Workaround for empty/missing list params
# Won't be necessary when this issue is resolved:
# https://github.com/tiangolo/fastapi/issues/9920
@app.exception_handler(RequestValidationError)
async def request_validation_exception_handler(
    _req: Request, exc: RequestValidationError
) -> JSONResponse:
    """Handle request validation errors."""
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "detail": jsonable_encoder(
                exc.errors(),
                custom_encoder={
                    PydanticUndefinedType: lambda _: None,
                },
            )
        },
    )


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
