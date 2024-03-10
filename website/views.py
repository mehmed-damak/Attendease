from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from . models import *
from . models import User, Course
from . import db
import json
views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    courses = Course.query.all()
    if request.method == 'POST':
        
        coursecode=request.form.get('coursecode')
        email=request.form.get('email')
        addremove=request.form.get('addremove')
    
        
        member = User.query.filter_by(email=email).first()
        course = Course.query.filter_by(coursecode=coursecode).first()
        if not course and not member:
            flash('user not in course', category='error')
            return redirect(url_for('views.home'))
        relation = UserCourse.query.filter_by(user_id=member.id, course_id=course.id).first()
        
        if not member:
            flash("user does not exist", category='error')
        elif not course:
            flash("course does not exist", category='error')
        elif addremove != 'remove' and addremove != 'add':
            flash("'remove' or 'add'", category='error')
        elif addremove == 'add':
            if relation:
                flash("member of class", category='error')
                return redirect(url_for('views.home'))
            member.courses.append(course)
            db.session.commit()
        elif addremove == 'remove':
            if not relation:
                flash("Not member of class", category='error')
                return redirect(url_for('views.home'))
            member.courses.remove(course)
            db.session.commit()
            
            
    return render_template("home.html", user=current_user, courses=courses)

 
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

'''
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
'''


'''
    if request.method == 'POST':
        note = request.form.get('note')
        if len(note) < 1:
            flash("Note is too short", category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added', category='success')
            
    
'''