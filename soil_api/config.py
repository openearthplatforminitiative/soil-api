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
    soil_types_mapping: dict = {
        0: "Acrisols",
        1: "Albeluvisols",
        2: "Alisols",
        3: "Andosols",
        4: "Arenosols",
        5: "Calcisols",
        6: "Cambisols",
        7: "Chernozems",
        8: "Cryosols",
        9: "Durisols",
        10: "Ferralsols",
        11: "Fluvisols",
        12: "Gleysols",
        13: "Gypsisols",
        14: "Histosols",
        15: "Kastanozems",
        16: "Leptosols",
        17: "Lixisols",
        18: "Luvisols",
        19: "Nitisols",
        20: "Phaeozems",
        21: "Planosols",
        22: "Plinthosols",
        23: "Podzols",
        24: "Regosols",
        25: "Solonchaks",
        26: "Solonetz",
        27: "Stagnosols",
        28: "Umbrisols",
        29: "Vertisols",
    }
    isric_roi: dict = {
        "min_lat": -90,
        "max_lat": 90,
        "min_lon": -180.0,
        "max_lon": 180,
    }
    depths: list = ["0-5", "5-15", "15-30", "30-60", "60-100", "100-200"]
    no_data_val: int = -32768
    soil_property_to_unit_mapping: dict = {
        "bdod": "cg/cm³",
        "cec": "mmol(c)/kg",
        "cfvo": "cm³/dm³",
        "clay": "g/kg",
        "nitrogen": "cg/kg",
        "ocd": "hg/m³",
        "ocs": "t/ha",
        "phh2o": "pH*10",
        "sand": "g/kg",
        "silt": "g/kg",
        "soc": "dg/kg",
    }


settings = Settings()
