from httpx import Client

with Client() as client:
    # Get the most probable soil type at the queried location
    response = client.get(
        url="$endpoint_url",
        params={"lat": 60.1, "lon": 9.58},
    )

    json = response.json()

    # Get the most probable soil type
    most_probable_soil_type = json["properties"]["most_probable_soil_type"]

    print(f"Most probable soil type: {most_probable_soil_type}")

    # Get the most probable soil type at the queried location
    # and the probability of the top 3 most probable soil types
    response = client.get(
        url="$endpoint_url",
        params={"lat": 60.1, "lon": 9.58, "top_k": 3},
    )

    json = response.json()

    # Get the soil type and probability for the second most probable soil type
    soil_type = json["properties"]["probabilities"][1]["soil_type"]
    probability = json["properties"]["probabilities"][1]["probability"]

    print(f"Soil type: {soil_type}, Probability: {probability}")
