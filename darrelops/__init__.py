"""
Top-level package for DarrelOps.
"""
# darrelops/__init__.py

from .extensions import app, db
import os
import logging

__app_name__ = "darrelops"
__version__ = "0.1.0"


def create_database():
    if not os.path.exists('artifactory'):
        os.makedirs('artifactory')
    
    basedir = os.path.abspath(os.path.dirname(__file__))
    # Check if the database file exists in the 'artifactory' directory
    database_path = os.path.join(basedir, 'artifactory', 'database.db')
    if not os.path.exists(database_path):
        with app.app_context():
            db.create_all()
        print("Database created successfully.")
    else:
        print("Database already exists")


logging.basicConfig(
    level=logging.INFO,  # Set the logging level
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Log message format
    handlers=[
        logging.StreamHandler(),  # Output to console
        logging.FileHandler("app.log"),  # Output to a log file
    ]
)

logger = logging.getLogger(__name__)  # Create a logger for the current module
