from . import db 
from flask_login import UserMixin
from sqlalchemy.sql import func

user_course=db.Table('user_course',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('course_id', db.Integer, db.ForeignKey('course.id'))
    )

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    firstName = db.Column(db.String(150))
    notes = db.relationship('Note')
    role = db.Column(db.String(50))
#    courses = db.relationship('Course', secondary=user_course, backref='members')
    
class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    coursecode = db.Column(db.String(100))
    coursename = db.Column(db.String(100))
    
    