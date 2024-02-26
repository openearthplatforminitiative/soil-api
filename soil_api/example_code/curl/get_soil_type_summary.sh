# Get a summary of the soil types in the queried bounding box, represented
# by a mapping of each soil type to the number of occurrences in the bounding box
curl -i -X GET $endpoint_url?min_lon=9.5&max_lon=9.6&min_lat=60.1&max_lat=60.12