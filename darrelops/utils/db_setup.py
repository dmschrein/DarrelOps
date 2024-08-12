"""Set up the database"""
# darrelops/utils/db_setup.py

from .extensions import db, app

def create_db():
    with app.app_context():
        db.create_all()