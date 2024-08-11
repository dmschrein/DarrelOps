from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
import atexit

#TODO: add logic for fetching new commits made to the repo

# Initialize app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
api = Api(app)

# Initiaze the scheduler
scheduler = BackgroundScheduler()
scheduler.start()

def register_scheduler_jobs():
    from .services import check_for_new_commits
    scheduler.add_job(
        func=check_for_new_commits,
        trigger=IntervalTrigger(seconds=300),
        id='check_for_new_commits',
        name='Check for new commits every 5 minutes',
        replace_existing=True
    )
    
# call register_scheduler
register_scheduler_jobs()

# Shutdown the scheduler when the exiting the app
atexit.register(lambda: scheduler.shutdown())