"""
Top-level package for DarrelOps.
"""
# darrelops/__init__.py

from flask import Flask
import os
from .utils.logging_setup import setup_logging
from .utils.extensions import scheduler, init_extensions, db
from .utils.config import DbConfig
from atexit import register as atexit_register
from apscheduler.triggers.interval import IntervalTrigger
from .utils.constants import *
from .utils.logging_setup import setup_logging
from .api import initialize_routes


__app_name__ = "darrelops"
__version__ = "0.1.0"

def create_app():
    """Application factory function for Darrel Ops Project"""

    app = Flask(__app_name__)
    
    # Config setup db
    app.config.from_object(DbConfig)

    # initialize extensions
    init_extensions(app)

    # setup logging
    setup_logging()
    
    initialize_routes(app)
    
    with app.app_context():
        db.create_all()

    # Shutdown the scheduler when exiting the app
    atexit_register(lambda: scheduler.shutdown())
    
    return app