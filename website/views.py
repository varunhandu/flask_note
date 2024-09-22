from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from . import db
from .models import Note
import json

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note_content = request.form.get('note')
        if len(note_content) < 1:
            flash('empty note', category='error')
        else:
            note_obj = Note(data=note_content, user_id=current_user.id)
            db.session.add(note_obj)
            db.session.commit()
            flash('note posted', category='success')

    return render_template("home.html", user=current_user)

@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    note_id = note['noteId']
    selected_note = Note.query.get(note_id)

    if selected_note:
        if selected_note.user_id == current_user.id:
            db.session.delete(selected_note)
            db.session.commit()
    return jsonify({})
