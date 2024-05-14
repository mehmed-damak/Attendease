from website import create_app, models
from website import db
from website.models import *
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
from apscheduler.schedulers.background import BackgroundScheduler

app = create_app()

scheduler=BackgroundScheduler()
def backgroundtask():
    reader = SimpleMFRC522()
    id, text = reader.read()
    print(id)
    print(text)
    courses=Course.query.all()
    students=User.query.all()
    activecourse=Course.query.filter_by(status=True)
    currentstudent=User.query.filter_by(firstName=text)
    currentrelation=User.query.filter_by(course_id=activecourse.id, user_id=currentstudent.id)
    currentrelation.attendance = currentrelation.attendance + 1       
    
scheduler.add_job(func=backgroundtask, trigger='interval', seconds=2)

if __name__ == '__main__':
    scheduler.start()
    app.run(host='0.0.0.0', port=5000, debug=True)
    #This runs the app
