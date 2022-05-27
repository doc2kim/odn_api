import requests

response = requests.get("http://api.odn-it.com")
print(response.json())