from flask import Flask, session
from flask.sessions import SecureCookieSessionInterface
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_cors import CORS

app = Flask(__name__)
# cors settings
cors = CORS(app, resources={r"*": {"origins": "*"}}, supports_credentials=True, withCredentials=True)

app.config['SECRET_KEY'] = 'ITPROJECT'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
api = Api(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
session_cookie = SecureCookieSessionInterface().get_signing_serializer(app)


@app.after_request
def cookies(response):
    same_cookie = session_cookie.dumps(dict(session))
    response.headers.add("Set-Cookie", f"session={same_cookie}; Secure; HttpOnly; SameSite=None; Path=/;")
    return response


# Mail Config
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = "unisoft6969@gmail.com"
app.config['MAIL_PASSWORD'] = "innrgezfveffibgt"
mail = Mail(app)

from backend import routes
from backend import apis
