
"""Sets up the logging"""
# darrelops/utils/logging_setup.py
import logging


# logging 
def setup_logging():
    
    logging.basicConfig(
        level=logging.INFO,  # Set the logging level
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Log message format
        handlers=[
            logging.StreamHandler(),  # Output to console
            logging.FileHandler("app.log"),  # Output to a log file
        ]
    )

logger = logging.getLogger(__name__)  # Create a logger for the current module
