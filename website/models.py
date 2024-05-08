from . import db 
from flask_login import UserMixin
from sqlalchemy.sql import func


class UserCourse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
    absences = db.Column(db.Integer)
    

    
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    firstName = db.Column(db.String(150))
    #notes = db.relationship('Note')
    role = db.Column(db.String(50))
    rfid = db.Column(db.String(30), unique=True)
    courses = db.relationship('Course', secondary='user_course', back_populates='users')
    attendance = db.Column(db.Integer)
    
class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    coursecode = db.Column(db.String(100))
    coursename = db.Column(db.String(100))
    users = db.relationship('User', secondary='user_course', back_populates='courses')
 
#this is an association viariable
#user_course=db.Table('user_course',
#    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
#    db.Column('course_id', db.Integer, db.ForeignKey('course.id'))
#    )   

#class Note(db.Model):
#    id = db.Column(db.Integer, primary_key=True)
#    data = db.Column(db.String(10000))
#    date = db.Column(db.DateTime(timezone=True), default=func.now())
#    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))