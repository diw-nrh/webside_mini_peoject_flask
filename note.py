from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models import db, Note, Comment
from forms import NoteForm, CommentForm
import os
from werkzeug.utils import secure_filename

note_bp = Blueprint('note', __name__)
