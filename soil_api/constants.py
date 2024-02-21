SOIL_MAPS_URL: str = "https://files.isric.org/soilgrids/latest/data"
SOIL_MAPS: dict = {"wrb": "MostProbable.vrt"}
HOMOLOSINE_CRS_WKT: str = (
    'PROJCS["Homolosine", GEOGCS["WGS 84", DATUM["WGS_1984", '
    'SPHEROID["WGS 84",6378137,298.257223563, AUTHORITY["EPSG","7030"]], '
    'AUTHORITY["EPSG","6326"]], PRIMEM["Greenwich",0, AUTHORITY["EPSG","8901"]], '
    'UNIT["degree",0.0174532925199433, AUTHORITY["EPSG","9122"]], '
    'AUTHORITY["EPSG","4326"]], PROJECTION["Interrupted_Goode_Homolosine"], UNIT["Meter",1]]'
)
ISRIC_ROI: dict = {
    "min_lat": -90,
    "max_lat": 90,
    "min_lon": -180.0,
    "max_lon": 180,
}
NO_DATA_VALS_SOILGRIDS: list = [-32768, 65535]
NO_DATA_VAL: int = -99999
