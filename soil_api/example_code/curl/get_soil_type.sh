# Get the most probable soil type at the queried location
curl -i -X GET $endpoint_url?lat=60.1&lon=9.58

# Get the most probable soil type at the queried location
# and the probability of the top 3 most probable soil types
curl -i -X GET $endpoint_url?lat=60.1&lon=9.58&top_k=3
