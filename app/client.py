import requests

# response = requests.post("http://127.0.0.1:5000/ads",
#                          json={"title": "Iphone X",
#                                "description": "Prodam nedorogo",
#                                "owner": "Andrey"})
# print(response.status_code)
# print(response.text)
#
# id = response.json()["id"]
# response = requests.get(
#     f"http://127.0.0.1:5000/ads/{id}",
# )
# print(response.status_code)
# print(response.text)

# response = requests.patch("http://127.0.0.1:5000/ads/1",
#                           json={"title": "Iphone 13",
#                                 "description": "Prodam ochen dorogo"}, )
# print(response.status_code)
# print(response.text)
#
# response = requests.get(
#     "http://127.0.0.1:5000/ads/1",
# )
# print(response.status_code)
# print(response.text)

response = requests.delete(
    "http://127.0.0.1:5000/ads/1",
)
print(response.status_code)
print(response.text)


response = requests.get(
    "http://127.0.0.1:5000/ads/1",
)
print(response.status_code)
print(response.text)
