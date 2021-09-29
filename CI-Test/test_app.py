import requests

BASE = "http://127.0.0.1:5000/"

def test_put():
  response = requests.put(BASE + "test/Jack", json={"someData":"hello", "exampleData": 100})
  assert response.status_code!=404 and response.status_code!=500

def test_register():
  response = requests.post(BASE + "register", json={"username":"test", "email": "test@test.com", "password":123456})
  assert response.status_code!=404 and response.status_code!=500

def test_home():
  response = requests.get(BASE + "home")
  assert response.status_code != 404

def test_put():
  response = requests.put(BASE + "test/Jack", {"someData":"hello", "exampleData": 100})
  assert response.status_code!=404

def test_register():
  r = {"username":"d32e1dsa", "email": "adaes12n@uni.com", "password":12345}
  response = requests.post(BASE + "register", json= r)
  assert response.status_code!=404

def test_login():
  r = {"email": "adaes12n@uni.com", "password":12345}
  response = requests.post(BASE + "register", json= r)
  assert response.status_code!=404
