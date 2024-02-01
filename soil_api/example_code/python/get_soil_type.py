from httpx import Client

with Client() as client:
    # Get the soil type at the queried location
    response = client.get(
        url="$endpoint_url",
        params={"lat": 60.1, "lon": 9.58},
    )

    # Get the soil type
    json = response.json()
    soil_type = json["properties"]["soil_type"]

    print(f"Soil type: {soil_type}")
