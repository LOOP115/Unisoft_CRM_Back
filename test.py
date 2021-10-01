# This module is to test APIs created

import requests

BASE = "http://127.0.0.1:5000/"

#response = requests.get(BASE + "test/Jack")
#response = requests.post(BASE + "login", json={"username":"test", "email": "test@test.com", "password":"123456"})
#c=response.cookies
#response = requests.get("http://127.0.0.1:5000/logout", cookies=c )
#response = requests.post(BASE + "test/jack")
for i in range(10) :
    response = requests.post(BASE + "reset_password", json={"email": "szej18@gmail.com"})
    if(response.status_code>=400):
        print("Wrong")