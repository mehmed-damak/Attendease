from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_user, login_required, logout_user, current_user
from . models import *
from . import db
import json
views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')
        if len(note) < 1:
            flash("Note is too short", category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added', category='success')
            
    return render_template("home.html", user=current_user)

@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
    
    return jsonify({})

@views.route('/create-course', methods=['GET', 'POST'])
def createCourse():
    if request.method=='POST':
        coursecode = request.form.get('coursecode')
        coursename = request.form.get('coursename')
        course = Course.query.filter_by(coursecode=coursecode).first()
        if course:
            flash('Course exists', category='error')
        elif len(coursecode)!=5:
            flash('wrong course code format, must be 5 alphanumeric characters', category='error')
        elif len(coursename)<6:
            flash('course name too short', category='error')
        else:
            new_course=Course(coursecode=coursecode, coursename=coursename)
            db.session.add(new_course)
            db.session.commit()
            flash('Course created', category='success')
    
    return render_template("createCourse.html", user=current_user)
