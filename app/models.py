from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class Patient(db.Model):
    id = db.Column(db.String(50), primary_key=True)
    blood_type = db.Column(db.String(10), nullable=False)
    last_transfusion = db.Column(db.Date, nullable=False)
    urgency = db.Column(db.Float, nullable=False)

class Donor(db.Model):
    id = db.Column(db.String(50), primary_key=True)
    blood_type = db.Column(db.String(10), nullable=False)
    last_donation = db.Column(db.Date, nullable=False)
    frequency = db.Column(db.Integer, nullable=False)
    response_time_hours = db.Column(db.Integer, nullable=False)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
