import requests
import json

url = 'https://jsonplaceholder.typicode.com/posts'
data = {
    'title': 'foo',
    'body': 'bar',
    'userId': 1
}
headers = {
    'Content-type': 'application/json; charset=UTF-8'
}

response = requests.post(url, data=json.dumps(data), headers=headers)
json_response = response.json()
print(json_response)

tarkesh2512
6kdCtGM5QP8dwWtK