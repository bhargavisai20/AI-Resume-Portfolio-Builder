from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)

    # Basic Auth
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(200))

    # Profile Fields
    phone = db.Column(db.String(20))
    linkedin = db.Column(db.String(200))
    github = db.Column(db.String(200))
    location = db.Column(db.String(100))
    bio = db.Column(db.Text)
    profile_photo = db.Column(db.String(200))  # stores filename

    resumes = db.relationship('Resume', backref='user', lazy=True)


class Resume(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    skills = db.Column(db.Text)
    education = db.Column(db.Text)
    experience = db.Column(db.Text)
    projects = db.Column(db.Text)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)