# This module is to test APIs created

import requests

BASE = "https://unisoft-app.herokuapp.com/"

#response = requests.get(BASE + "test/Jack")

response = requests.post(BASE + "register", json={"username":"test2", "email": "test2@test.com", "password":123456})

#response = requests.post(BASE + "test/jack")

print(response)