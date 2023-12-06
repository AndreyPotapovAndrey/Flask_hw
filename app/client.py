import requests

# response = requests.post("http://127.0.0.1:5000/users",
#                          json={"name": "user_1", "password": "jmbpdotrkmsdrij09oij4903tujnuinvr-09"}
#                          # headers={"token": "some_token"},
#                          # params={"name": "John", "age": 20}
#                          # Можно использовать метод params, а не явно передавать значения в query string
#                          )
# print(response.status_code)
# print(response.text)

# response = requests.get(
#     "http://127.0.0.1:5000/users/1",
# )
# print(response.status_code)
# print(response.text)

# response = requests.patch("http://127.0.0.1:5000/users/1", json={"password": "1234"},)
# print(response.status_code)
# print(response.text)

# response = requests.patch("http://127.0.0.1:5000/users/1", json={"name": "new_user_name"},)
# print(response.status_code)
# print(response.text)
#
# response = requests.get(
#     "http://127.0.0.1:5000/users/1",
# )
# print(response.status_code)
# print(response.text)

response = requests.delete(
    "http://127.0.0.1:5000/users/1",
)
print(response.status_code)
print(response.text)


response = requests.get(
    "http://127.0.0.1:5000/users/1",
)
print(response.status_code)
print(response.text)
