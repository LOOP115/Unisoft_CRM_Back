# This module is to test APIs created

import requests

BASE = "http://127.0.0.1:5000/"

#response = requests.get(BASE + "test/Jack")

response = requests.post(BASE + "register", json={"username":"test1", "email": "test1@test.com", "password":123456})

#response = requests.post(BASE + "test/jack")

print(response)