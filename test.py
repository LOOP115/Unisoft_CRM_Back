# This module is to test APIs created

import requests

BASE = "http://127.0.0.1:5000/"

#response = requests.get(BASE + "test/Jack")

response = requests.put(BASE + "test/Jack", {"someData":"hello", "exampleData": 100})

#response = requests.post(BASE + "test/jack")

print(response.json())