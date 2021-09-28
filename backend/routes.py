import os
import secrets
from PIL import Image
from flask import Flask, jsonify, json
from flask import render_template as rt
from flask import url_for, flash, redirect, request, abort
from flask_login import login_user, current_user, logout_user, login_required
from flask_restful import Resource, reqparse

from backend import app, db, bcrypt
from backend.models import User
from backend.forms import RegistrationForm, LoginForm, UpdateAccountForm


@app.route('/')
@app.route('/home')
def home():
    return "HomePage"


def valid_account(username, email):
    has_username = User.query.filter_by(username=username).first()
    has_email = User.query.filter_by(email=email).first()
    if has_username and has_email:
        return "User and email have been taken"
    if has_username:
        return "The username has been taken"
    if has_email:
        return "The email has been taken"
    return "Valid"


@app.route("/register", methods=['POST'])
def register():
    request_data = json.loads(request.data)
    valid_result = valid_account(request_data['username'], request_data['email'])
    if (valid_result == "Valid"):
        user = User(username=request_data['username'], email=request_data['email'], password=request_data['password'])
        db.session.add(user)
        db.session.commit()
        return {
            "userid": user.id,
            "username": user.username,
            "email": user.email
        }, 200
    return {"register error": valid_result}, 300


@app.route("/login", methods=['POST'])
def login():
    request_data = json.loads(request.data)
    user = User.query.filter_by(email=request_data['email']).first()
    if user and (request_data['password'] == user.password):
        login_user(user, remember=request_data)
        return {
            "userid": current_user.id,
            "username": current_user.username,
            "email": current_user.email
        }
    return {"error": "Invalid email or password"}, 300


@app.route("/logout", methods=['GET'])
@login_required
def logout():
    logout_user()
    return "Exit"


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
        return "User and email have been taken"
    if has_username:
        return "The username has been taken"
    if has_email:
        return "The email has been taken"
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
        request_data = json.loads(request.data)
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
        return valid_result
