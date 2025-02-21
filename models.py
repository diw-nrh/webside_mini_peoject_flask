from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    image_filename = db.Column(db.String(200))  # Store the image file name
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Build relationships with users
    user = db.relationship('User', backref=db.backref('notes', lazy=True))  # Relationship with User


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    note_id = db.Column(db.Integer, db.ForeignKey('note.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())


# models.py
def init_db(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()
        db.session.commit()

