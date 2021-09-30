import os
import secrets
import json
from PIL import Image
from flask import Flask, jsonify, json
from flask import render_template as rt
from flask import url_for, flash, redirect, request, abort
from flask_login import login_user, current_user, logout_user, login_required
from flask_restful import Resource, reqparse
from flask_mail import Message

from backend import app, db, bcrypt, mail
from backend.models import User, Contact
from backend.forms import RegistrationForm, LoginForm, UpdateAccountForm
from flask_cors import CORS

# cors settings
cors = CORS(app, resources={r"*": {"origins": "*"}}, supports_credentials=True)

@app.route('/')
@app.route('/home')
def home():
    return "home"

# Authentication
########################################################################
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
        user = User(username=request_data['username'], email=request_data['email'], password=hashed_password)
        db.session.add(user)
        db.session.commit()
        return {
            "userid": user.id,
            "username": user.username,
            "email": user.email
        }, 200
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
        return {
            "userid": current_user.id,
            "username": current_user.username,
            "email": current_user.email
        }, 200
    return {"error": "Invalid email or password"}, 300


@app.route("/logout", methods=['GET'])
@login_required
def logout():
    logout_user()
    return "exit"


# def save_picture_profile(form_picture):
#     random_hex = secrets.token_hex(8)
#     _, f_ext = os.path.splitext(form_picture.filename)
#     picture_fn = random_hex + f_ext
#     picture_path = os.path.join(app.root_path, 'static/profile_img', picture_fn)

#     output_size = (125, 125)
#     i = Image.open(form_picture)
#     i.thumbnail(output_size)
#     i.save(picture_path)
#     return picture_fn


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
        return {
            "userid": current_user.id,
            "username": current_user.username,
            "email": current_user.email
        }

    if request.method == 'POST':
        try:
            request_data = json.loads(request.data)
        except:
            return {"error": "Json load error"}, 500

        valid_result = valid_account_update(request_data['username'], request_data['email'], request_data)
        if (valid_result == "Valid"):
            current_user.username = request_data['username']
            current_user.email = request_data['email']
            db.session.commit()
            return {
                "userid": current_user.id,
                "username": current_user.username,
                "email": current_user.email
            }
        return {"error": valid_result}, 300


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='noreply@unisoft.com',
                  recipients=[user.email])
    msg.body = f'''To reset your password, please visit the following link:
http://127.0.0.1:5000//reset_password/{token}

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
        "ownerid": current_user.id,
        "owner": current_user.username
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


