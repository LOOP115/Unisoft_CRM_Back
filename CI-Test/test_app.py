import app
import requests

BASE = "http://127.0.0.1:5000/"

#response = requests.get(BASE + "test/Jack")

response = requests.put(BASE + "test/Jack", {"someData":"hello", "exampleData": 100})

#response = requests.post(BASE + "test/jack")

def test():
  assert app.home() != "HomePage"
  
  response = requests.put(BASE + "test/Jack", {"someData":"hello", "exampleData": 100})
  assert response != {"someData":"hello", "exampleData": 100}
