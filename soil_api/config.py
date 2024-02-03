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

    soil_maps_url: str = "https://files.isric.org/soilgrids/latest/data"
    soil_maps: dict = {"wrb": "MostProbable.vrt"}
    homolosine_crs_wkt: str = (
        'PROJCS["Homolosine", GEOGCS["WGS 84", DATUM["WGS_1984", '
        'SPHEROID["WGS 84",6378137,298.257223563, AUTHORITY["EPSG","7030"]], '
        'AUTHORITY["EPSG","6326"]], PRIMEM["Greenwich",0, AUTHORITY["EPSG","8901"]], '
        'UNIT["degree",0.0174532925199433, AUTHORITY["EPSG","9122"]], '
        'AUTHORITY["EPSG","4326"]], PROJECTION["Interrupted_Goode_Homolosine"], UNIT["Meter",1]]'
    )
    isric_roi: dict = {
        "min_lat": -90,
        "max_lat": 90,
        "min_lon": -180.0,
        "max_lon": 180,
    }
    depths: dict = {
        "0-5cm": {"top_depth": 0, "bottom_depth": 5, "unit_depth": "cm"},
        "0-30cm": {"top_depth": 0, "bottom_depth": 30, "unit_depth": "cm"},
        "5-15cm": {"top_depth": 5, "bottom_depth": 15, "unit_depth": "cm"},
        "15-30cm": {"top_depth": 15, "bottom_depth": 30, "unit_depth": "cm"},
        "30-60cm": {"top_depth": 30, "bottom_depth": 60, "unit_depth": "cm"},
        "60-100cm": {"top_depth": 60, "bottom_depth": 100, "unit_depth": "cm"},
        "100-200cm": {"top_depth": 100, "bottom_depth": 200, "unit_depth": "cm"},
    }
    no_data_vals: list = [-32768, 65535, -99999]


settings = Settings()
