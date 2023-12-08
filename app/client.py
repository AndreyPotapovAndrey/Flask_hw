import requests

# response = requests.post("http://127.0.0.1:5000/ads",
#                          json={"id": "1",
#                                "title": "Iphone X",
#                                "description": "Prodam nedorogo",
#                                "owner": "Andrey"})
# print(response.status_code)
# print(response.text)
#
# response = requests.get(
#     "http://127.0.0.1:5000/ads/1",
# )
# print(response.status_code)
# print(response.text)

# response = requests.patch("http://127.0.0.1:5000/users/1", json={"title": "Iphone 12", "discription": "Prodam dorogo"},)
# print(response.status_code)
# print(response.text)
#
# response = requests.get(
#     "http://127.0.0.1:5000/ads/1",
# )
# print(response.status_code)
# print(response.text)
#
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


