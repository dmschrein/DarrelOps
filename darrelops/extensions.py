from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
import atexit

#TODO: add logic for fetching new commits made to the repo

# Initialize app
db_cprogram = SQLAlchemy()
db_artfact = SQLAlchemy()

app = Flask(__name__)

app.config['SQLALCHEMY_BINDS'] = {
    'cprogram_db': 'sqlite:///cprogram.db',
    'artfact_db': 'sqlite:///artfact.db'
}

db_cprogram.init_app(app)
db_artfact.init_app(app)

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