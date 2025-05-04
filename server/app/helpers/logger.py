import logging
from logging.handlers import RotatingFileHandler
import os

LOG_DIR = "../logs"
LOG_FILE = "app.log"

# Create logs directory if it doesn't exist
os.makedirs(LOG_DIR, exist_ok=True)

# Log format
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

logging.basicConfig(
    level=logging.INFO,
    format=LOG_FORMAT,
    datefmt=DATE_FORMAT,
    handlers=[
        RotatingFileHandler(
            filename=os.path.join(LOG_DIR, LOG_FILE),
            backupCount=10,
            maxBytes=5 * 1024 * 1024,  # 5MB
            encoding="utf-8"
        ),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("LibraryAppLogger")
