import requests
import time

BASE = "http://127.0.0.1:5000/"

def test_put():
  response = requests.put(BASE + "test/Jack", json={"someData":"hello", "exampleData": 100})
  assert response.status_code!=404 and response.status_code!=500


# Authentication
########################################################################
def test_register():
  response = requests.post(BASE + "register", json={"username":"test", "firstname":"py", "lastname":"test", 
                                                    "email": "test@test.com", "birth": "1999-01-01", "password":"123456"})
  assert response.status_code!=404 and response.status_code!=500

def test_login():
  r = {"email": "test@test.com", "password":"123456"}
  response = requests.post(BASE + "login", json= r)
  assert response.status_code!=404 and response.status_code!=500

# test whether registered account can log in or not
def test_validLogin():
  response = requests.post(BASE + "register", json={"username":"test", "firstname":"py", "lastname":"test", 
                                                    "email": "test@test.com", "birth": "1999-01-01", "password":"123456"})
  if(response.status_code >= 500 or response.status_code == 404):
    assert response.status_code!=404 and response.status_code!=500
  
  response = requests.post(BASE + "login", json={"email": "test@test.com", "password":"123456"})
  if(response.status_code >= 500 or response.status_code == 404):
    assert response.status_code!=404 and response.status_code!=500
  assert response.status_code==200

# test whether wrong password can log in
def test_InvalidLogin():
  response = requests.post(BASE + "register", json={"username":"test", "firstname":"py", "lastname":"test", 
                                                    "email": "test@test.com", "birth": "1999-01-01", "password":"123456"})
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
  r = requests.post(BASE + "account", cookies=cookies, json={"username":"testupdate", "firstname":"py", "lastname":"test", 
                                                              "email": "test@test.com", "birth": "1999-01-01", "password":"123456"})
  requests.get(BASE + "logout", cookies=cookies)
  assert r.status_code < 400

# test reset password with valid email
def test_resetPassword():
  r = requests.post(BASE + "register", json={"username":"test8888", "firstname":"loa", "lastname":"ding", 
                                             "email": "szej18@gmail.com", "birth": "1999-01-01", "password":"123456"})
  r = requests.post(BASE + "reset_password", json={"email": "szej18@gmail.com"})
  assert r.status_code == 200

# test reset password with invalid email
def test_resetPasswordInvalid():
  r = requests.post(BASE + "reset_password", json={"email": "xxxxx"})
  assert r.status_code == 300


# Contacts
########################################################################
# test add new contacts
def test_addContact():
  r = requests.post(BASE + "login", json={"username":"test", "email": "test@test.com", "password":"123456"})
  cookies = r.cookies
  # add contact 1
  r = requests.post(BASE + "contact/new",cookies=cookies, json={
    "firstname": "contact",
    "lastname": "1",
    "email": "contact1@uni.com",
    "phone": "12345678",
    "company": "unimelb"
    })
  assert r.status_code == 200
  # add contact 2
  r = requests.post(BASE + "contact/new",cookies=cookies, json={
    "firstname": "contact",
    "lastname": "2",
    "email": "contact2@uni.com",
    "phone": "12345678",
    "company": "unisoft"
    })
  assert r.status_code == 200

# test get contacts
def test_getContact():
  r = requests.post(BASE + "login", json={"username":"test", "email": "test@test.com", "password":"123456"})
  cookies = r.cookies 
  # get valid contact
  r = requests.get(BASE + "contact/1",cookies=cookies)
  assert r.status_code == 200
  r = requests.get(BASE + "contact/2",cookies=cookies)
  assert r.status_code == 200
  # invalid get
  r = requests.get(BASE + "contact/3",cookies=cookies)
  assert r.status_code == 404

# test get all contacts
def test_getAllContacts():
  r = requests.post(BASE + "login", json={"username":"test", "email": "test@test.com", "password":"123456"})
  cookies = r.cookies 
  r = requests.get(BASE + "contact/all",cookies=cookies)
  assert r.status_code == 200

# test delete contact
def test_deleteContact():
  r = requests.post(BASE + "login", json={"username":"test", "email": "test@test.com", "password":"123456"})
  cookies = r.cookies
  # delete valid contact
  r = requests.post(BASE + "contact/2/delete",cookies=cookies)
  assert r.status_code == 200

# test update contact
def test_updateContact():
  r = requests.post(BASE + "login", json={"username":"test", "email": "test@test.com", "password":"123456"})
  cookies = r.cookies
  r = requests.get(BASE + "contact/1/update",cookies=cookies)
  assert r.status_code == 200
  r = requests.post(BASE + "contact/1/update",cookies=cookies, json={
    "firstname": "contact",
    "lastname": "11",
    "email": "contact11@uni.com",
    "phone": "12345678",
    "company": "unisoft"
    })
  assert r.status_code == 200

# test filtering contacts by company
def test_filterContactCompany():
  r = requests.post(BASE + "login", json={"username":"test", "email": "test@test.com", "password":"123456"})
  cookies = r.cookies
  r = requests.get(BASE + "contact/unisoft",cookies=cookies)
  assert r.status_code == 200


# Activities
########################################################################
def test_addActivity():
  r = requests.post(BASE + "login", json={"username":"test", "email": "test@test.com", "password":"123456"})
  cookies = r.cookies
  r = requests.post(BASE + "activity/new",cookies=cookies, json={
    "title": "Activity1",
    "desc": "Fantastic",
    "time": "2022-1-1 11:11:11",
    "location": "Mars",
    "status": "upcoming"
  })
  assert r.status_code == 200
  r = requests.post(BASE + "activity/new",cookies=cookies, json={
    "title": "Activity2",
    "desc": "Amazing",
    "time": "2022-2-2 22:22:22",
    "location": "Mecury",
    "status": "upcoming"
  })
  assert r.status_code == 200
  r = requests.post(BASE + "activity/new",cookies=cookies, json={
    "title": "Activity3",
    "desc": "Awesome",
    "time": "2022-10-10 10:10:10",
    "location": "Earth",
    "status": "upcoming"
  })
  assert r.status_code == 200

def test_deleteActivity():
  r = requests.post(BASE + "login", json={"username":"test", "email": "test@test.com", "password":"123456"})
  cookies = r.cookies
  # delete valid activity
  r = requests.post(BASE + "activity/3/delete",cookies=cookies)
  assert r.status_code == 200

def test_getActivity():
  r = requests.post(BASE + "login", json={"username":"test", "email": "test@test.com", "password":"123456"})
  cookies = r.cookies
  r = requests.get(BASE + "activity/1",cookies=cookies)
  assert r.status_code == 200
  r = requests.get(BASE + "activity/all",cookies=cookies)
  assert r.status_code == 200

def test_inviteContact():
  r = requests.post(BASE + "login", json={"username":"test", "email": "test@test.com", "password":"123456"})
  cookies = r.cookies
  r = requests.post(BASE + "activity/1/invite",cookies=cookies, json=[
    {"contact_id": 1},
    {"contact_id": 2},
    {"contact_id": 3}
  ])
  assert r.status_code == 200


