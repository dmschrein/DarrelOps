"""Initialize and configure extensions"""
# darrelops/utils/extensions.py

from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from apscheduler.schedulers.background import BackgroundScheduler


db = SQLAlchemy()
api = Api()
scheduler = BackgroundScheduler()

def init_extensions(app):
    db.init_app(app)
    api.init_app(app)
    scheduler.start()
    