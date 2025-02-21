from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import models
import forms
from note import note_bp

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

# Connect to database
models.init_db(app)

# Set up LoginManager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# load_user function
@login_manager.user_loader
def load_user(user_id):
    return models.db.session.get(models.User, user_id)  # Use session.get() from db imported from models.py

# Register Note Blueprint
app.register_blueprint(note_bp)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home')
@login_required
def home():
    return render_template("home.html", user=current_user.username)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        user = models.User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('note.view_notes'))  # Edit to go directly to the note.
        else:
            flash('Invalid username or password!', 'danger')

    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = forms.RegisterForm()
    if form.validate_on_submit():
        existing_user = models.User.query.filter_by(username=form.username.data).first()
        if existing_user:
            flash('Username already exists!', 'danger')
            return redirect(url_for('register'))
        
        hashed_password = generate_password_hash(form.password.data)
        new_user = models.User(username=form.username.data, password=hashed_password)
        models.db.session.add(new_user)
        models.db.session.commit()

        flash('Account created successfully!', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)