import logging
import os
from pathlib import Path
from string import Template

from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.routing import APIRoute

from soil_api.config import settings

supported_languages = {"cURL": "sh", "JavaScript": "js", "Python": "py"}


def custom_openapi(app: FastAPI, example_code_dir: Path):
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="Soil API",
        version=settings.version,
        description=settings.api_description,
        routes=app.routes,
        servers=[{"url": settings.api_url}],
    )

    routes_that_need_doc = [
        route for route in app.routes if isinstance(route, APIRoute)
    ]
    for route in routes_that_need_doc:
        code_samples = []
        for lang in supported_languages:
            file_with_code_sample = (
                example_code_dir
                / lang.lower()
                / f"{route.name}.{supported_languages[lang]}"
            )
            if os.path.isfile(file_with_code_sample):
                with open(file_with_code_sample) as f:
                    code_template = Template(f.read())
                    code_samples.append(
                        {
                            "lang": lang,
                            "source": code_template.safe_substitute(
                                endpoint_url=f"{settings.api_url}{route.path}",
                            ),
                        }
                    )
            else:
                logging.warning(
                    "No code sample found for route %s and language %s",
                    route.path,
                    lang,
                )

        if code_samples:
            openapi_schema["paths"][route.path]["get"]["x-codeSamples"] = code_samples

    return openapi_schema
