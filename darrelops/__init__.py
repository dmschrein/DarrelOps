"""
Top-level package for DarrelOps.
"""
# darrelops/__init__.py

from .extensions import app, db
import os
import logging

__app_name__ = "darrelops"
__version__ = "0.1.0"

(
    SUCCESS,
    DIR_ERROR,
    FILE_ERROR,
    REG_ERROR,
    ART_READ_ERROR, 
    ART_WRITE_ERROR,
    JSON_ERROR,
) = range(7)

ERRORS = {
    DIR_ERROR: "config directory error",
    FILE_ERROR: "config file error",
    REG_ERROR: "program registration error",
    ART_READ_ERROR: "artifactory read error",
    ART_WRITE_ERROR: "artifactory write error",
}

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
