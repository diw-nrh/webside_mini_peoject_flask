from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models import db, Note, Comment
from forms import NoteForm, CommentForm
import os
from werkzeug.utils import secure_filename

note_bp = Blueprint('note', __name__)

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@note_bp.route('/add_note', methods=['GET', 'POST'])
@login_required
def add_note():
    form = NoteForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        image = form.image.data

        image_filename = None
        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            image_path = os.path.join(UPLOAD_FOLDER, filename)
            image.save(image_path)
            image_filename = filename

        new_note = Note(title=title, content=content, image_filename=image_filename, user_id=current_user.id)
        db.session.add(new_note)
        db.session.commit()

        flash('บันทึกโน้ตเรียบร้อยแล้ว!', 'success')
        return redirect(url_for('note.view_notes'))

    return render_template('add_note.html', form=form)

@note_bp.route('/notes')
@login_required
def view_notes():
    notes = Note.query.filter_by(user_id=current_user.id).all()
    return render_template('home.html', notes=notes, user=current_user.username)

@note_bp.route('/note/<int:note_id>', methods=['GET', 'POST'])
@login_required
def view_note(note_id):
    note = Note.query.get_or_404(note_id)
    if note.user_id != current_user.id:
        flash('คุณไม่มีสิทธิ์เข้าถึงโน้ตนี้!', 'danger')
        return redirect(url_for('note.view_notes'))

    form = CommentForm()

    if form.validate_on_submit():
        new_comment = Comment(note_id=note.id, content=form.content.data)
        db.session.add(new_comment)
        db.session.commit()
        flash('ความคิดเห็นถูกเพิ่มแล้ว!', 'success')
        return redirect(url_for('note.view_note', note_id=note.id))

    return render_template('note_detail.html', note=note, form=form)
