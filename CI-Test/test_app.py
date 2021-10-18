import requests


BASE = "http://127.0.0.1:5000/"


def test_put():
    response = requests.put(BASE + "test/Jack", json={"someData": "hello", "exampleData": 100})
    assert response.status_code != 404 and response.status_code != 500


# Authentication
########################################################################
# test registration
def test_register():
    response = requests.post(BASE + "register", json={"username": "test", "firstname": "py", "lastname": "test",
                                                      "email": "test@test.com", "birth": "1999-01-01",
                                                      "password": "123456"})
    assert response.status_code != 404 and response.status_code != 500
    response = requests.post(BASE + "register", json={"username": "abcd", "firstname": "ab", "lastname": "cd",
                                                      "email": "abcd@test.com", "birth": "1999-01-01",
                                                      "password": "123456"})
    assert response.status_code != 404 and response.status_code != 500


# test login
def test_login():
    r = {"email": "test@test.com", "password": "123456"}
    response = requests.post(BASE + "login", json=r)
    assert response.status_code != 404 and response.status_code != 500


# test whether registered account can log in or not
def test_validLogin():
    response = requests.post(BASE + "register", json={"username": "test", "firstname": "py", "lastname": "test",
                                                      "email": "test@test.com", "birth": "1999-01-01",
                                                      "password": "123456"})
    if (response.status_code >= 500 or response.status_code == 404):
        assert response.status_code != 404 and response.status_code != 500

    response = requests.post(BASE + "login", json={"email": "test@test.com", "password": "123456"})
    if (response.status_code >= 500 or response.status_code == 404):
        assert response.status_code != 404 and response.status_code != 500
    assert response.status_code == 200


# test whether wrong password can log in
def test_InvalidLogin():
    response = requests.post(BASE + "register", json={"username": "test", "firstname": "py", "lastname": "test",
                                                      "email": "test@test.com", "birth": "1999-01-01",
                                                      "password": "123456"})
    response = requests.post(BASE + "login",
                             json={"username": "test", "email": "test@test.com", "password": "654321asd"})
    assert response.status_code != 200


# test Log out and login cookies
def test_logout():
    r = requests.post(BASE + "login", json={"username": "test", "email": "test@test.com", "password": "123456"})
    cookies = r.cookies
    r = requests.get(BASE + "logout", cookies=cookies)
    assert r.status_code == 200


# test account and login cookies
def test_account():
    r = requests.post(BASE + "login", json={"username": "test", "email": "test@test.com", "password": "123456"})
    cookies = r.cookies
    r = requests.get(BASE + "account", cookies=cookies)
    requests.get(BASE + "logout", cookies=cookies)
    assert r.status_code == 200


# test update account
def test_updateAccount():
    r = requests.post(BASE + "login", json={"username": "test", "email": "test@test.com", "password": "123456"})
    cookies = r.cookies
    r = requests.post(BASE + "account", cookies=cookies,
                      json={"username": "testupdate", "firstname": "py", "lastname": "test",
                            "email": "test@test.com", "birth": "1999-01-01", "password": "123456"})
    requests.get(BASE + "logout", cookies=cookies)
    assert r.status_code < 400


# # test reset password with valid email
# def test_resetPassword():
#     r = requests.post(BASE + "register", json={"username": "test8888", "firstname": "loa", "lastname": "ding",
#                                                "email": "szej18@gmail.com", "birth": "1999-01-01",
#                                                "password": "123456"})
#     r = requests.post(BASE + "reset_password", json={"email": "szej18@gmail.com"})
#     assert r.status_code == 200


# # test reset password with invalid email
# def test_resetPasswordInvalid():
#     r = requests.post(BASE + "reset_password", json={"email": "xxxxx"})
#     assert r.status_code == 200


# Contacts
########################################################################
# test add new contacts
def test_addContact():
    r = requests.post(BASE + "login", json={"username": "test", "email": "test@test.com", "password": "123456"})
    cookies = r.cookies
    # add contact 1
    r = requests.post(BASE + "contact/new", cookies=cookies, json={
        "firstname": "contact",
        "lastname": "1",
        "email": "abcd@test.com",
        "phone": "12345678",
        "company": "unimelb"
    })
    assert r.status_code == 200
    # add contact 2
    r = requests.post(BASE + "contact/new", cookies=cookies, json={
        "firstname": "contact",
        "lastname": "2",
        "email": "contact2@uni.com",
        "phone": "12345678",
        "company": "unisoft"
    })
    assert r.status_code == 200
    # add contact 3
    r = requests.post(BASE + "contact/new", cookies=cookies, json={
        "firstname": "contact",
        "lastname": "3",
        "email": "contact3@uni.com",
        "phone": "12345678",
        "company": "unisoft"
    })
    assert r.status_code == 200
    # add contact 4
    r = requests.post(BASE + "contact/new", cookies=cookies, json={
        "firstname": "contact",
        "lastname": "4",
        "email": "contact4@uni.com",
        "phone": "12345678",
        "company": "unimelb"
    })
    assert r.status_code == 200


# test get contacts
def test_getContact():
    r = requests.post(BASE + "login", json={"username": "test", "email": "test@test.com", "password": "123456"})
    cookies = r.cookies
    # get valid contact
    r = requests.get(BASE + "contact/1", cookies=cookies)
    assert r.status_code == 200
    r = requests.get(BASE + "contact/2", cookies=cookies)
    assert r.status_code == 200
    # invalid get
    r = requests.get(BASE + "contact/10", cookies=cookies)
    assert r.status_code == 404


# test get all contacts
def test_getAllContacts():
    r = requests.post(BASE + "login", json={"username": "test", "email": "test@test.com", "password": "123456"})
    cookies = r.cookies
    r = requests.get(BASE + "contact/all", cookies=cookies)
    assert r.status_code == 200


# test delete contact
def test_deleteContact():
    r = requests.post(BASE + "login", json={"username": "test", "email": "test@test.com", "password": "123456"})
    cookies = r.cookies
    # delete valid contact
    r = requests.post(BASE + "contact/4/delete", cookies=cookies)
    assert r.status_code == 200


# test update contact
def test_updateContact():
    r = requests.post(BASE + "login", json={"username": "test", "email": "test@test.com", "password": "123456"})
    cookies = r.cookies
    r = requests.get(BASE + "contact/2/update", cookies=cookies)
    assert r.status_code == 200
    r = requests.post(BASE + "contact/2/update", cookies=cookies, json={
        "firstname": "contact",
        "lastname": "11",
        "email": "contact11@uni.com",
        "phone": "12345678",
        "company": "unisoft"
    })
    assert r.status_code == 200


# test filtering contacts by company
def test_filterContactCompany():
    r = requests.post(BASE + "login", json={"username": "test", "email": "test@test.com", "password": "123456"})
    cookies = r.cookies
    r = requests.get(BASE + "contact/unisoft", cookies=cookies)
    assert r.status_code == 200


# Activities
########################################################################
# test add new activities
def test_addActivity():
    r = requests.post(BASE + "login", json={"username": "test", "email": "test@test.com", "password": "123456"})
    cookies = r.cookies
    r = requests.post(BASE + "activity/new", cookies=cookies, json={
        "title": "Activity1",
        "desc": "Fantastic",
        "time": "2022-1-1 11:11:11",
        "location": "Mars",
        "status": "upcoming"
    })
    assert r.status_code == 200
    r = requests.post(BASE + "activity/new", cookies=cookies, json={
        "title": "Activity2",
        "desc": "Amazing",
        "time": "2022-2-2 22:22:22",
        "location": "Mecury",
        "status": "upcoming"
    })
    assert r.status_code == 200
    r = requests.post(BASE + "activity/new", cookies=cookies, json={
        "title": "Activity3",
        "desc": "Awesome",
        "time": "2022-10-10 10:10:10",
        "location": "Earth",
        "status": "upcoming"
    })
    assert r.status_code == 200


# test delete activity
def test_deleteActivity():
    r = requests.post(BASE + "login", json={"username": "test", "email": "test@test.com", "password": "123456"})
    cookies = r.cookies
    # delete valid activity
    r = requests.post(BASE + "activity/3/delete", cookies=cookies)
    assert r.status_code == 200


# test get activites
def test_getActivity():
    r = requests.post(BASE + "login", json={"username": "test", "email": "test@test.com", "password": "123456"})
    cookies = r.cookies
    r = requests.get(BASE + "activity/1", cookies=cookies)
    assert r.status_code == 200
    r = requests.get(BASE + "activity/all", cookies=cookies)
    assert r.status_code == 200


# test inviting contacts to activity
def test_inviteContact():
    r = requests.post(BASE + "login", json={"username": "test", "email": "test@test.com", "password": "123456"})
    cookies = r.cookies
    r = requests.post(BASE + "activity/1/invite", cookies=cookies, json=[
        {"contact_id": 1},
        {"contact_id": 2},
        {"contact_id": 3}
    ])
    assert r.status_code == 200


# test delete participant from activity
def test_deleteParticipant():
    r = requests.post(BASE + "login", json={"username": "test", "email": "test@test.com", "password": "123456"})
    cookies = r.cookies
    r = requests.post(BASE + "activity/1/invite/3/delete", cookies=cookies)
    assert r.status_code == 200


# test update activity content
def test_updateActivity():
    r = requests.post(BASE + "login", json={"username": "test", "email": "test@test.com", "password": "123456"})
    cookies = r.cookies
    r = requests.get(BASE + "activity/2/update", cookies=cookies)
    assert r.status_code == 200
    r = requests.post(BASE + "activity/2/update", cookies=cookies, json={
        "title": "Activity22",
        "desc": "Unprecedented",
        "time": "2022-11-11 11:11:11",
        "location": "Sun",
        "status": "upcoming"
    })
    assert r.status_code == 200


# test sending invition mails
def test_sendInvitation():
    r = requests.post(BASE + "login", json={"username": "test", "email": "test@test.com", "password": "123456"})
    cookies = r.cookies
    r = requests.post(BASE + "activity/1/invite/send", cookies=cookies, json={
        "title": "New",
        "content": "new"
    })
    assert r.status_code == 200


# test sending updates mails
def test_sendUpdate():
    r = requests.post(BASE + "login", json={"username": "test", "email": "test@test.com", "password": "123456"})
    cookies = r.cookies
    r = requests.post(BASE + "activity/1/update/send", cookies=cookies, json={
        "title": "Update",
        "content": "update"
    })
    assert r.status_code == 200


# test get invitation
def test_getIncident():
    r = requests.post(BASE + "login", json={"username": "abcd", "email": "abcd@test.com", "password": "123456"})
    cookies = r.cookies
    r = requests.get(BASE + "incident/1", cookies=cookies)
    assert r.status_code == 200


# test get all invitations
def test_getAllIncident():
    r = requests.post(BASE + "login", json={"username": "abcd", "email": "abcd@test.com", "password": "123456"})
    cookies = r.cookies
    r = requests.get(BASE + "incident/all", cookies=cookies)
    assert r.status_code == 200


# test accept/reject invitation
def test_replyIncident():
    r = requests.post(BASE + "login", json={"username": "abcd", "email": "abcd@test.com", "password": "123456"})
    cookies = r.cookies
    r = requests.post(BASE + "incident/1/accept", cookies=cookies)
    assert r.status_code == 200
    r = requests.post(BASE + "incident/1/reject", cookies=cookies)
    assert r.status_code == 200


# test get all particpants
def test_getAllParticipants():
    r = requests.post(BASE + "login", json={"username": "test", "email": "test@test.com", "password": "123456"})
    cookies = r.cookies
    r = requests.get(BASE + "activity/1/participants", cookies=cookies)
    assert r.status_code == 200


# test delete invitation
def test_deleteIncident():
    r = requests.post(BASE + "login", json={"username": "abcd", "email": "abcd@test.com", "password": "123456"})
    cookies = r.cookies
    r = requests.post(BASE + "incident/1/delete", cookies=cookies)
    assert r.status_code == 200


# Finally delete the test account
########################################################################
def test_deleteAccount():
    r = requests.post(BASE + "login", json={"username": "test", "email": "test@test.com", "password": "123456"})
    cookies = r.cookies
    r = requests.post(BASE + "deleteAccount", cookies=cookies)
    assert r.status_code == 200
