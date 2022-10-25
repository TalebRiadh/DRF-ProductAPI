import requests

endpoint = "http://localhost:8000/api/products/"

data = {
    "title": "Nestle water",
    "price": 2.99
}

get_response = requests.post(endpoint, json=data)


print(get_response.json())