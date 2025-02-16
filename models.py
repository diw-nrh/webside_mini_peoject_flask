from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

# กำหนดฐานข้อมูล SQLite3
db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

def init_db(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()
        db.session.commit()