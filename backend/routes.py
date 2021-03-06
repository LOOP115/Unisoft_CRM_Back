import json
from datetime import datetime
from flask import jsonify, json, request, abort
from flask import render_template, url_for, flash, redirect
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message
from backend.forms import RequestResetForm, ResetPasswordForm

from backend import app, db, bcrypt, mail
from backend.models import User, Contact, Activity, Incident
from flask_cors import CORS


cors = CORS(app, supports_credentials=True, withCredentials=True)
Base = "https://unisoft-crm.herokuapp.com/"
# Base = "http://localhost:3000/"

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
    if valid_result == "Valid":
        hashed_password = bcrypt.generate_password_hash(request_data['password']).decode('utf-8')
        user = User(username=request_data['username'], firstname=request_data['firstname'],
                    lastname=request_data['lastname'], email=request_data['email'],
                    birth=get_date(request_data['birth']), password=hashed_password)
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
    if request_data['firstname'] != current_user.firstname or request_data['lastname'] != current_user.lastname:
        count -= 1
    if get_date(request_data['birth']) != current_user.birth:
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
        if valid_result == "Valid":
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
    msg.body = f'''To reset your password, visit the following link:
{url_for('reset_token', token=token, _external=True)}
If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)


@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(Base)
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(Base + "login")
    return render_template('reset_request.html', title='Reset Password', form=form)


@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(Base + "login")
    return render_template('reset_token.html', title='Reset Password', form=form)


@app.route("/deleteAccount", methods=['POST'])
@login_required
def delete_account():
    userid = current_user.id
    try:
        contact_list = Contact.query.filter_by(user_id=userid).all()
        for cont in contact_list:
            db.session.delete(cont)

        activity_list = Activity.query.filter_by(user_id=userid).all()
        for act in activity_list:
            db.session.delete(act)

        logout_user()
        user = User.query.get_or_404(userid)
        db.session.delete(user)
        db.session.commit()
    except:
        return {"error": "Can't delete account"}, 300
    return "Account deleted", 200


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


@app.route('/contact/filter/<string:company>', methods=['GET'])
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


def incident_serializer(incident):
    creator = User.query.get(incident.launcher)
    return {
        "actid": incident.id,
        "title": incident.title,
        "desc": incident.desc,
        "time": incident.time,
        "location": incident.location,
        "status": incident.status,
        "accept": incident.accept,
        "creatorid": incident.launcher,
        "creatorFirstName": creator.firstname,
        "creatorLastName": creator.lastname
    }


def send_email(contact, title, content):
    msg = Message(title, sender='noreply@unisoft.com', recipients=[contact.email])
    msg.body = content
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


@app.route('/activity/<int:activity_id>/participants', methods=['get'])
@login_required
def activity_participants(activity_id):
    activity = Activity.query.get_or_404(activity_id)
    if activity.creator != current_user:
        abort(403)
    result = [*map(contact_serializer, activity.events)]

    for contact in result:
        user = User.query.filter_by(email=contact['email']).first()
        if (user):
            incident = Incident.query.filter_by(user_id=user.id, title=activity.title, location=activity.location,
                                                time=activity.time).first()
            if (incident):
                contact['accept'] = incident.accept
            else:
                contact['accept'] = "Invitation not sent"
        else:
            contact['accept'] = "Not a user"

    return jsonify(result), 200


@app.route('/activity/<int:activity_id>/invite/send', methods=['POST'])
@login_required
def send_invite(activity_id):
    activity = Activity.query.get_or_404(activity_id)
    if activity.creator != current_user:
        abort(403)
    try:
        request_data = json.loads(request.data)
    except:
        return {"error": "Json load error"}, 500

    title = request_data['title']
    content = request_data['content']
    for contact in activity.events:
        send_email(contact, title, content)
        user = User.query.filter_by(email=contact.email).first()
        if (user):
            incident = Incident(title=activity.title, desc=activity.desc,
                                time=activity.time, location=activity.location,
                                status=activity.status, accept=False, launcher=current_user.id)
            user.incident.append(incident)

    db.session.commit()
    return "sent", 200


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
    try:
        request_data = json.loads(request.data)
    except:
        return {"error": "Json load error"}, 500

    title = request_data['title']
    content = request_data['content']
    for contact in activity.events:
        send_email(contact, title, content)
    return "sent", 200


@app.route('/incident/<int:incident_id>', methods=['GET'])
@login_required
def get_incident(incident_id):
    incident = Incident.query.get_or_404(incident_id)
    return incident_serializer(incident), 200


@app.route('/incident/all', methods=['GET'])
@login_required
def list_incident():
    userid = current_user.id
    try:
        incident_list = Incident.query.filter_by(user_id=userid).all()
    except:
        return {"error": "Can't filter"}, 300
    return jsonify([*map(incident_serializer, incident_list)]), 200


@app.route('/incident/<int:incident_id>/delete', methods=['POST'])
@login_required
def delete_incident(incident_id):
    incident = Incident.query.get_or_404(incident_id)
    if incident.attend != current_user:
        abort(403)
    db.session.delete(incident)
    db.session.commit()
    return "deleted", 200


@app.route('/incident/<int:incident_id>/accept', methods=['POST'])
@login_required
def accept_incident(incident_id):
    incident = Incident.query.get_or_404(incident_id)
    if incident.attend != current_user:
        abort(403)
    incident.accept = True
    db.session.commit()
    return "accept", 200


@app.route('/incident/<int:incident_id>/reject', methods=['POST'])
@login_required
def reject_incident(incident_id):
    incident = Incident.query.get_or_404(incident_id)
    if incident.attend != current_user:
        abort(403)
    incident.accept = False
    db.session.commit()
    return "reject", 200
