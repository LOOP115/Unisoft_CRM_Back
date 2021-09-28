import requests

BASE = "http://127.0.0.1:5000/"

def test_home():
  response = requests.get(BASE + "home")
  assert response.status_code != 404 and response.status_code!=500

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
def test_valid_login():
  response = requests.post(BASE + "register", json={"username":"test", "email": "test@test.com", "password":123456})
  if(response.status_code == 500 or response.status_code == 404):
    assert response.status_code!=404 and response.status_code!=500
  
  requests.post(BASE + "login", json={"username":"test", "email": "test@test.com", "password":123456})

  