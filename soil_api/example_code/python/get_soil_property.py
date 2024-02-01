from httpx import Client

with Client() as client:
    # Get the value of the soil property at the queried location and depth
    response = client.get(
        url="$endpoint_url",
        params={"lat": 60.1, "lon": 9.58, "depth": "0-5", "property": "bdod"},
    )

    json = response.json()

    # Get the soil property value, unit and name
    value = json["properties"]["value"]
    unit = json["properties"]["unit"]
    property = json["properties"]["property"]

    print(f"{property} value: {value} {unit}")
