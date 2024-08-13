from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
import atexit
import os

#TODO: add logic for fetching new commits made to the repo

# Initialize app
app = Flask(__name__)

# DB Setup
# Get the absolute path to the 'artifactory' directory
basedir = os.path.abspath(os.path.dirname(__file__))
database_path = os.path.join(basedir, 'artifactory', 'database.db')

# Ensure the directory exists
if not os.path.exists(os.path.join(basedir, 'artifactory')):
    os.makedirs(os.path.join(basedir, 'artifactory'))

# Update the SQLAlchemy configuration to use the absolute path
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{database_path}'

db = SQLAlchemy(app)
api = Api(app)

# Initiaze the scheduler
scheduler = BackgroundScheduler()
scheduler.start()

def register_scheduler_jobs():
    from .services import check_for_new_commits
    scheduler.add_job(
        func=check_for_new_commits,
        trigger=IntervalTrigger(seconds=60),
        id='check_for_new_commits',
        name='Check for new commits every 60 seconds',
        replace_existing=True
    )
    
# call register_scheduler
register_scheduler_jobs()

# Shutdown the scheduler when the exiting the app
atexit.register(lambda: scheduler.shutdown())