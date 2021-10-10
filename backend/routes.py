import os
import secrets
import json
from PIL import Image
from datetime import datetime
from flask import Flask, jsonify, json
from flask import render_template as rt
from flask import url_for, flash, redirect, request, abort
from flask_login import login_user, current_user, logout_user, login_required
from flask_restful import Resource, reqparse
from flask_mail import Message

from backend import app, db, bcrypt, mail
from backend.models import User, Contact, Activity
from backend.forms import RegistrationForm, LoginForm, UpdateAccountForm
from flask_cors import CORS

# cors settings
cors = CORS(app, resources={r"*": {"origins": "*"}}, supports_credentials=True)

@app.route('/')
@app.route('/home')
def home():
    return "This is backend home, see more pls follow README"


def get_date(date):
    return datetime.strptime(date, '%Y-%m-%d').date()


def get_datetime(date_time):
    return datetime.strptime(date_time, '%Y-%m-%d %H:%M:%S')


# Authentication
########################################################################
def user_serializer(user):
    return {
        "userid": user.id,
        "username": user.username,
        "firstname": user.firstname,
        "lastname": user.lastname,
        "email": user.email,
        "birth": user.birth
    }


def valid_account(username, email):
    has_username = User.query.filter_by(username=username).first()
    has_email = User.query.filter_by(email=email).first()
    if has_username and has_email:
        return "Username and email have been taken"
    if has_username:
        return "Username has been taken"
    if has_email:
        return "Email has been taken"
    return "Valid"


@app.route("/register", methods=['POST'])
def register():
    try:
        request_data = json.loads(request.data)
    except:
        return {"error": "Json load error"}, 500
    valid_result = valid_account(request_data['username'], request_data['email'])
    if (valid_result == "Valid"):
        hashed_password = bcrypt.generate_password_hash(request_data['password']).decode('utf-8')
        user = User(username=request_data['username'], firstname=request_data['firstname'], lastname=request_data['lastname'], 
                    email=request_data['email'], birth=get_date(request_data['birth']), password=hashed_password)
        db.session.add(user)
        db.session.commit()
        return user_serializer(user), 200
    return {"error": valid_result}, 300


@app.route("/login", methods=['POST'])
def login():
    try:
        request_data = json.loads(request.data)
    except:
        return {"error": "Json load error"}, 500
    
    user = User.query.filter_by(email=request_data['email']).first()
    if user and bcrypt.check_password_hash(user.password, request_data['password']):
        login_user(user, remember=request_data)
        return user_serializer(current_user), 200
    return {"error": "Invalid email or password"}, 300


@app.route("/logout", methods=['GET'])
@login_required
def logout():
    logout_user()
    return "exit"


def valid_account_update(username, email, request_data):
    has_username = False
    has_email = False
    count = 2
    if request_data['username'] != current_user.username:
        has_username = User.query.filter_by(username=username).first()
        count -= 1
    if request_data['email'] != current_user.email:
        has_email = User.query.filter_by(email=email).first()
        count -= 1
    if has_username and has_email:
        return "Username and email have been taken"
    if has_username:
        return "Username has been taken"
    if has_email:
        return "Email has been taken"
    if count == 2:
        return "No change"
    return "Valid"


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    if request.method == 'GET':
        return user_serializer(current_user), 200
        
    if request.method == 'POST':
        try:
            request_data = json.loads(request.data)
        except:
            return {"error": "Json load error"}, 500

        valid_result = valid_account_update(request_data['username'], request_data['email'], request_data)
        if (valid_result == "Valid"):
            current_user.username = request_data['username']
            current_user.firstname = request_data['firstname']
            current_user.lastname = request_data['lastname']
            current_user.birth = get_date(request_data['birth'])
            current_user.email = request_data['email']
            db.session.commit()
        return user_serializer(current_user), 200
        return {"error": valid_result}, 300


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='noreply@unisoft.com',
                  recipients=[user.email])
    msg.body = f'''To reset your password, please visit the following link:
https://unisoft-backend.herokuapp.com/reset_password/{token}

If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)


@app.route("/reset_password", methods=['POST'])
def reset_request():
    try:
        request_data = json.loads(request.data)
    except:
        return {"error": "Json load error"}, 500

    user = User.query.filter_by(email=request_data['email']).first()
    if user:
        try:
            send_reset_email(user)
        except:
            return {"error": "resend"}, 300
        return {"userid": user.id}, 200
    return {"error": "Invalid email"}, 300


@app.route("/reset_password/<token>", methods=['POST'])
def reset_token(token):
    user = User.verify_reset_token(token)
    if user is None:
        return {"error": "Invalid or expired token"}, 300
    
    try:
        request_data = json.loads(request.data)
    except:
        return {"error": "Json load error"}, 500

    user.password = request_data['password']
    db.session.commit()
    return {"userid": user.id}, 200


# Contacts
########################################################################
def contact_serializer(contact):
    return {
        "contactid": contact.id,
        "firstname": contact.firstname,
        "lastname": contact.lastname,
        "email": contact.email,
        "phone": contact.phone,
        "company": contact.company,
        "ownerid": contact.owner.id,
        "owner": contact.owner.username
    }


@app.route('/contact/new', methods=['POST'])
@login_required
def new_contact():
    try:
        request_data = json.loads(request.data)
    except:
        return {"error": "Json load error"}, 500

    try:
        contact = Contact(firstname=request_data['firstname'], lastname=request_data['lastname'], 
                          email=request_data['email'], phone=request_data['phone'], 
                          company=request_data['company'], owner=current_user)
    except:
        return {"error": "Can't create contact"}, 300

    db.session.add(contact)
    db.session.commit()
    return contact_serializer(contact), 200


@app.route('/contact/<int:contact_id>', methods=['GET'])
@login_required
def get_contact(contact_id):
    contact = Contact.query.get_or_404(contact_id)
    return contact_serializer(contact), 200

@app.route('/contact/<int:contact_id>/delete', methods=['POST'])
@login_required
def delete_contact(contact_id):
    contact = Contact.query.get_or_404(contact_id)
    if contact.owner != current_user:
        abort(403)
    db.session.delete(contact)
    db.session.commit()
    return "deleted", 200


@app.route('/contact/<int:contact_id>/update', methods=['GET', 'POST'])
@login_required
def update_contact(contact_id):
    contact = Contact.query.get_or_404(contact_id)
    if contact.owner != current_user:
        abort(403)
    if request.method == 'GET':
        return contact_serializer(contact), 200

    try:
        request_data = json.loads(request.data)
    except:
        return {"error": "Json load error"}, 500

    contact.firstname = request_data['firstname']
    contact.lastname = request_data['lastname']
    contact.email = request_data['email']
    contact.phone = request_data['phone']
    contact.company = request_data['company']
    db.session.commit()
    return contact_serializer(contact), 200


@app.route('/contact/all', methods=['GET'])
@login_required
def list_contact():
    userid = current_user.id
    try:
        contact_list = Contact.query.filter_by(user_id=userid).all()
    except:
        return {"error": "Can't filter"}, 300
    return jsonify([*map(contact_serializer, contact_list)]), 200


@app.route('/contact/<string:company>', methods=['GET'])
@login_required
def company_contact(company):
    userid = current_user.id
    try:
        contact_list = Contact.query.filter_by(user_id=userid, company=company).all()
    except:
        return {"error": "Can't filter"}, 300
    return jsonify([*map(contact_serializer, contact_list)]), 200


# Activities
########################################################################
def activity_serializer(activity):
    return {
        "actid": activity.id,
        "title": activity.title,
        "desc": activity.desc,
        "time": activity.time,
        "location": activity.location,
        "status": activity.status,
        "creator": activity.creator.username,
        "creatorid": activity.creator.id,
        "invite": [*map(contact_serializer, activity.events)]
    }


def send_invite_email(contact):
    msg = Message('New Activity Invitation',
                  sender='noreply@unisoft.com',
                  recipients=[contact.email])
    msg.body = f'''I am glad to invite you to our new event.'''
    mail.send(msg)


def send_update_email(contact):
    msg = Message('Activity Updates',
                  sender='noreply@unisoft.com',
                  recipients=[contact.email])
    msg.body = f'''The activity has following updates.'''
    mail.send(msg)


@app.route('/activity/new', methods=['POST'])
@login_required
def new_activity():
    try:
        request_data = json.loads(request.data)
    except:
        return {"error": "Json load error"}, 500

    try:
        activity = Activity(title=request_data['title'], desc=request_data['desc'], 
                            time=get_datetime(request_data['time']), location=request_data['location'], 
                            status=request_data['status'], creator=current_user)
    except:
        return {"error": "Can't create activity"}, 300

    db.session.add(activity)
    db.session.commit()
    return activity_serializer(activity), 200


@app.route('/activity/<int:activity_id>', methods=['GET'])
@login_required
def get_activity(activity_id):
    activity = Activity.query.get_or_404(activity_id)
    return activity_serializer(activity), 200


@app.route('/activity/<int:activity_id>/delete', methods=['POST'])
@login_required
def delete_activity(activity_id):
    activity = Activity.query.get_or_404(activity_id)
    if activity.creator != current_user:
        abort(403)
    db.session.delete(activity)
    db.session.commit()
    return "deleted", 200


@app.route('/activity/all', methods=['GET'])
@login_required
def list_activity():
    userid = current_user.id
    try:
        activity_list = Activity.query.filter_by(user_id=userid).all()
    except:
        return {"error": "Can't filter"}, 300
    return jsonify([*map(activity_serializer, activity_list)]), 200


@app.route('/activity/<int:activity_id>/invite', methods=['POST'])
@login_required
def activity_invite(activity_id):
    activity = Activity.query.get_or_404(activity_id)
    if activity.creator != current_user:
        abort(403)
    try:
        request_data = json.loads(request.data)
    except:
        return {"error": "Json load error"}, 500
    
    for contact in request_data:
        new_attend = Contact.query.get_or_404(contact['contact_id'])
        activity.events.append(new_attend)
    db.session.commit()
    return activity_serializer(activity), 200


@app.route('/activity/<int:activity_id>/invite/<int:contact_id>/delete', methods=['POST'])
@login_required
def activity_invite_delete(activity_id, contact_id):
    activity = Activity.query.get_or_404(activity_id)
    if activity.creator != current_user:
        abort(403)
    
    contact = Contact.query.get_or_404(contact_id)
    if contact.owner != current_user:
        abort(403)
    
    activity.events.remove(contact)
    db.session.commit()
    return "deleted", 200


@app.route('/activity/<int:activity_id>/invite/send', methods=['POST'])
@login_required
def send_invite(activity_id):
    activity = Activity.query.get_or_404(activity_id)
    if activity.creator != current_user:
        abort(403)
    for contact in activity.events:
        send_invite_email(contact)
    return "sent", 300


@app.route('/activity/<int:activity_id>/update', methods=['GET', 'POST'])
@login_required
def update_activity(activity_id):
    activity = Activity.query.get_or_404(activity_id)
    if activity.creator != current_user:
        abort(403)
    if request.method == 'GET':
        return activity_serializer(activity), 200

    try:
        request_data = json.loads(request.data)
    except:
        return {"error": "Json load error"}, 500

    activity.title = request_data['title']
    activity.desc = request_data['desc']
    activity.time = get_datetime(request_data['time'])
    activity.location = request_data['location']
    activity.status = request_data['status']
    db.session.commit()
    return activity_serializer(activity), 200


@app.route('/activity/<int:activity_id>/update/send', methods=['POST'])
@login_required
def send_update(activity_id):
    activity = Activity.query.get_or_404(activity_id)
    if activity.creator != current_user:
        abort(403)
    for contact in activity.events:
        send_update_email(contact)
    return "sent", 300

