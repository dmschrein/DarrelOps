"""Extensions for Darrel Ops"""
# darrelops/extensions.py

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
import atexit
import os

# Initialize app
app = Flask(__name__)


# DB Setup
basedir = os.path.abspath(os.path.dirname(__file__))
database_path = os.path.join(basedir, 'artifactory', 'database.db')

# Ensure the directory exists
if not os.path.exists(os.path.join(basedir, 'artifactory')):
    os.makedirs(os.path.join(basedir, 'artifactory'))

# Update the SQLAlchemy configuration to use the absolute path
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{database_path}'

db = SQLAlchemy(app)
api = Api(app)

# Creat API endpoints
from darrelops.models import CProgramModel
from darrelops.api import RegisterProgram, ListArtifacts, DownloadArtifact
@app.route('/')
def home():
    return '<h1>Welcome to Darrel Ops for C Programs!</h1>'       

@app.route('/status')
def status():
    programs = CProgramModel.query.all()
    return render_template('status.html', programs=programs)

api.add_resource(RegisterProgram, '/api/register') 
api.add_resource(DownloadArtifact, '/api/artifact/download/<int:program_id>/<string:version>')
api.add_resource(ListArtifacts, '/api/artifacts', '/api/artifacts/<int:program_id>')


# Initiaze the scheduler
scheduler = BackgroundScheduler()
scheduler.start()

def register_scheduler_jobs():
    from .services import check_for_new_commits
    scheduler.add_job(
        func=check_for_new_commits,
        trigger=IntervalTrigger(seconds=120),
        id='check_for_new_commits',
        name='Check for new commits every 120 seconds',
        replace_existing=True
    )
    
# call register_scheduler
register_scheduler_jobs()

# Shutdown the scheduler when the exiting the app
atexit.register(lambda: scheduler.shutdown())