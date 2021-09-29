import requests
import time

BASE = "http://127.0.0.1:5000/"

def test_put():
  response = requests.put(BASE + "test/Jack", json={"someData":"hello", "exampleData": 100})
  assert response.status_code!=404 and response.status_code!=500

def test_register():
  response = requests.post(BASE + "register", json={"username":"test", "email": "test@test.com", "password":123456})
  assert response.status_code!=404 and response.status_code!=500

def test_login():
  r = {"email": "test@test.com", "password":"123456"}
  response = requests.post(BASE + "login", json= r)
  assert response.status_code!=404 and response.status_code!=500

# test whether registered account can log in or not
def test_validLogin():
  response = requests.post(BASE + "register", json={"username":"test", "email": "test@test.com", "password":"123456"})
  if(response.status_code >= 500 or response.status_code == 404):
    assert response.status_code!=404 and response.status_code!=500
  
  response = requests.post(BASE + "login", json={"email": "test@test.com", "password":"123456"})
  if(response.status_code >= 500 or response.status_code == 404):
    assert response.status_code!=404 and response.status_code!=500
  assert response.status_code==200

# test whether wrong password can log in
def test_InvalidLogin():
  response = requests.post(BASE + "register", json={"username":"test", "email": "test@test.com", "password":"123456"})
  response = requests.post(BASE + "login", json={"username":"test", "email": "test@test.com", "password":"654321asd"})
  assert response.status_code!=200

# test Log out and login cookies
def test_logout():
  r = requests.post(BASE + "login", json={"username":"test", "email": "test@test.com", "password":"123456"})
  cookies = r.cookies
  r = requests.get(BASE + "logout", cookies=cookies)
  assert r.status_code == 200

# test account and login cookies
def test_account():
  r = requests.post(BASE + "login", json={"username":"test", "email": "test@test.com", "password":"123456"})
  cookies = r.cookies
  r = requests.get(BASE + "account", cookies=cookies)
  requests.get(BASE + "logout", cookies=cookies)
  assert r.status_code == 200

# test update account 
def test_updateAccount():
  r = requests.post(BASE + "login", json={"username":"test", "email": "test@test.com", "password":"123456"})
  cookies = r.cookies
  r = requests.post(BASE + "account", cookies=cookies, json={"username":"test", "email": "test@test.com"})
  requests.get(BASE + "logout", cookies=cookies)
  assert r.status_code < 400