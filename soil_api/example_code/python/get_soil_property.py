from httpx import Client

with Client() as client:
    # Get the mean value of the soil property at the queried location and depth
    response = client.get(
        url="$endpoint_url",
        params={
            "lat": 60.1,
            "lon": 9.58,
            "depths": "0-5cm",
            "properties": "bdod",
            "values": "mean",
        },
    )

    json = response.json()

    # Get the soil information for the bdod property
    bdod = json["properties"]["layers"][0]

    # Get the soil property unit and name
    bdod_name = bdod["name"]
    bdod_unit = bdod["unit"]

    # Get the soil property mean value at depth 0-5cm
    bdod_depth = bdod["depths"][0]["label"]
    bdod_value = bdod["depths"][0]["values"]["mean"]

    print(
        f"Soil property: {bdod_name}, Depth: {bdod_depth}, Value: {bdod_value} {bdod_unit}"
    )

    # Get the mean and the 0.05 quantile of the soil properties at the queried location and depths
    response_multi = client.get(
        url="$endpoint_url",
        params={
            "lat": 60.1,
            "lon": 9.58,
            "depths": ["0-5cm", "100-200cm"],
            "properties": ["bdod", "phh2o"],
            "values": ["mean", "Q0.05"],
        },
    )

    json_multi = response_multi.json()

    # Get the soil information for the phh2o property
    phh2o = json_multi["properties"]["layers"][1]

    # Get the soil property unit and name
    phh2o_name = phh2o["name"]
    phh2o_unit = phh2o["unit"]

    # Get the soil property 0.05 quantile value at depth 100-200cm
    phh2o_depth = phh2o["depths"][1]["label"]
    phh2o_value = phh2o["depths"][1]["values"]["Q0.05"]

    print(
        f"Soil property: {phh2o_name}, Depth: {phh2o_depth}, Value: {phh2o_value} {phh2o_unit}"
    )
