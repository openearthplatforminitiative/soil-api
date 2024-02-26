from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    version: str = "0.0.1"
    server_bind_port: int = 8080
    server_bind_host: str = "0.0.0.0"

    api_root_path: str = ""

    api_description: str = (
        "This is a RESTful service that provides soil "
        "information based on data sourced from "
        '<a href="https://www.isric.org/explore/soilgrids">SoilGrids</a>. '
        "<br/>The data are freely available for use under the "
        '<a href="https://creativecommons.org/licenses/by/4.0/">CC BY 4.0 license</a>.'
    )

    api_domain: str = "localhost"

    @property
    def api_url(self):
        if self.api_domain == "localhost":
            return f"http://{self.api_domain}:{self.server_bind_port}"
        else:
            return f"https://{self.api_domain}{self.api_root_path}"


settings = Settings()
