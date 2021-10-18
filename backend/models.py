from backend import db, login_manager, app
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    firstname = db.Column(db.String(20), nullable=False)
    lastname = db.Column(db.String(20), nullable=False)
    birth = db.Column(db.DateTime, nullable=True)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    contact = db.relationship('Contact', backref='owner', lazy=True)
    activity = db.relationship('Activity', backref='creator', lazy=True)
    incident = db.relationship('Incident', backref='attend', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.firstname} {self.lastname}', '{self.email}')"

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'userid': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['userid']
        except:
            return None
        return User.query.get(user_id)


events = db.Table('events',
                  db.Column('activity_id', db.Integer, db.ForeignKey('activity.id'), primary_key=True),
                  db.Column('contact_id', db.Integer, db.ForeignKey('contact.id'), primary_key=True)
                  )


class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(20), nullable=False)
    lastname = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    company = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Contact('{self.firstname} {self.lastname}', '{self.phone}', '{self.email}', '{self.company}')"


class Activity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    desc = db.Column(db.String(200), nullable=False)
    time = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(10), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    events = db.relationship('Contact', secondary=events,
                             lazy='subquery', backref=db.backref('activities', lazy=True))

    def __repr__(self):
        return f"Activity('{self.title}', '{self.desc}', '{self.time}', '{self.location}', '{self.status}')"


class Incident(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    desc = db.Column(db.String(200), nullable=False)
    time = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(10), nullable=False)
    accept = db.Column(db.Boolean, nullable=False)
    launcher = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Activity('{self.title}', '{self.time}', '{self.location}', '{self.status}', '{self.accept}') "
