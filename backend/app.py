import os
import sys

import click
from flask import Flask
from flask import redirect, url_for, abort, render_template, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField
from wtforms.validators import DataRequired

app = Flask(__name__)

# Members API route
@app.route("/members")
def members():
    return {"members": ["Member1", "member2", "member3"]}

if __name__ == "__main__":
    app.run(debug=True)