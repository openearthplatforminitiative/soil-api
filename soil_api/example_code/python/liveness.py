from httpx import Client

with Client() as client:
    response = client.get(url="$endpoint_url")
    print(response.json()["message"])
