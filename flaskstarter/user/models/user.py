import pendulum
import sqlalchemy as sa

from flask_login import UserMixin

from flaskstarter.extensions import db


class User(UserMixin, db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(256), unique=True)
    first_name = db.Column(db.String(256))
    last_name = db.Column(db.String(256))
    avatar_url = db.Column(db.String, unique=True)
    email = db.Column(db.String(100), unique=True)

    created_on = db.Column(db.TIMESTAMP, server_default=sa.func.now())
    last_login_on = db.Column(db.TIMESTAMP)

    def __init__(self, username, first_name, last_name, email, avatar_url):
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.avatar_url = avatar_url
        self.email = email
        self.active = 1
        self.created_on = pendulum.now()
        self.updated_on = pendulum.now()

    @property
    def is_active(self):
        return self.active

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def __repr__(self):
        return self.username


class OAuth(db.Model):
    __tablename__ = 'user_oauth'

    id = db.Column(db.Integer, primary_key=True)

    provider = db.Column(db.String(50))
    provider_user_id = db.Column(db.String(256), unique=True)

    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    user = db.relationship(User)

    created_on = db.Column(db.TIMESTAMP, server_default=sa.func.now())
