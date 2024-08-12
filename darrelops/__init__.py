"""
Top-level package for DarrelOps.
"""
# darrelops/__init__.py

from .extensions import app, db_cprogram, db_artfact, api
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

# for filesystem
ARTIFACTORY_BASE_DIR = os.getenv('ARTIFACTORY_BASE_DIR', default=os.path.join(os.getcwd(), 'artifactory'))


def create_cprogram_tables():
    with app.app_context():
        db_cprogram.create_all()
        
def create_artifact_tables():
    with app.app_context():
        db_artfact.create_all()
    
logging.basicConfig(
    level=logging.INFO,  # Set the logging level
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Log message format
    handlers=[
        logging.StreamHandler(),  # Output to console
        logging.FileHandler("app.log"),  # Output to a log file
    ]
)

logger = logging.getLogger(__name__)  # Create a logger for the current module
