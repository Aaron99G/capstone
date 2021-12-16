from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func, functions


class Food(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(150))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    calories = db.Column(db.Integer)
    protein = db.Column(db.Integer)
    carbs = db.Column(db.Integer)
    fats = db.Column(db.Integer)
    total_cals = db.Column(db.Integer)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    foods = db.relationship('Food')
    kals = db.Column(db.Integer)
    
    
class Day(db.Model):
    day_id = db.Column(db.Integer, primary_key=True)