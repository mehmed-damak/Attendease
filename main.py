from website import create_app, models
from website import db
from website.models import *
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
from apscheduler.schedulers.background import BackgroundScheduler

app = create_app()

if __name__ == '__main__':
    
    app.run(host='0.0.0.0', port=5000, debug=True)
    #This runs the app
