import requests

url = 'http://127.0.0.1:8000/api/'

request = requests.get(url + 'random')
print(request.json())

request = requests.get(url + 'register')
print(request.json())

request = requests.get(url + 'unregister')
print(request.json())

request = requests.get(url + 'available-nodes-by-zone')
print(request.json())

