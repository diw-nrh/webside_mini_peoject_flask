from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models import db, Note, Comment
from forms import NoteForm, CommentForm
import os
from werkzeug.utils import secure_filename

note_bp = Blueprint('note', __name__)

# กำหนดโฟลเดอร์สำหรับอัปโหลดรูปภาพ
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS