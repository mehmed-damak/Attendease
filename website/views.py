from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for, session
from flask_login import login_user, login_required, logout_user, current_user
from . models import *
from . models import User, Course, UserCourse
from . import db
import json
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

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
        if not course or not member:
            flash('coursecode or user does not exist', category='error')
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

@views.route('/student-home', methods=['GET', 'POST'])
@login_required
def studentHome():
    courses=current_user.courses
    relations = []
    for course in courses:
        relation = UserCourse.query.filter_by(course_id=course.id, user_id=current_user.id) 
        relations.append(relation)
    return render_template("studenthome.html", user=current_user, courses=courses, relations=relations)


@views.route('/teacher-home', methods = ['GET', 'POST'])
@login_required
def teacherHome():
    state = session.get('state')
    courses=current_user.courses
    students=[]
    relations=UserCourse.query.all()
    return render_template("teacherhome.html", user=current_user, courses=courses, relations=relations)
    
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
            new_course=Course(coursecode=coursecode, coursename=coursename, status=False)
            db.session.add(new_course)
            db.session.commit()
            flash('Course created', category='success')
    
    return render_template("createCourse.html", user=current_user)

@views.route('/toggle/<int:currentcourse>', methods=['GET', 'POST'])
def toggle(currentcourse):
    courses=Course.query.all()
    for course in courses:
        if currentcourse == course.id:
            course.status = not course.status
            db.session.commit()
        else:
            course.status=False
            db.session.commit()
    current_course=Course.query.filter_by(id=currentcourse)
    while current_course.status == True:
        reader=SimpleMFRC22()
        id, text = reader.read
        activeuser=User.query.filter_by(firstName=text)
        currentrelation=User.query.filter_by(course_id=current_course.id, user_id=activeuser.id)
        currentrelation.attendance = currentrelalation.attendance + 1
    return redirect(url_for('views.teacherHome'))#this is your next task

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