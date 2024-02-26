from httpx import Client

with Client() as client:
    # Get a summary of the soil types in the queried bounding box, represented
    # by a mapping of each soil type to the number of occurrences in the bounding box
    response = client.get(
        url="$endpoint_url",
        params={"min_lon": 9.5, "max_lon": 9.6, "min_lat": 60.1, "max_lat": 60.12},
    )

    json = response.json()

    # Get the summary of the soil types in the bounding box
    summary_list = json["properties"]["summaries"]

    # Get the soil type and the number of occurrences
    soil_type_1 = summary_list[0]["soil_type"]
    count_1 = summary_list[0]["count"]
    soil_type_2 = summary_list[1]["soil_type"]
    count_2 = summary_list[1]["count"]

    print(f"Soil type: {soil_type_1}, Count: {count_1}")
    print(f"Soil type: {soil_type_2}, Count: {count_2}")
