import logging.config
import os

import dotenv
from flask import Flask

dotenv.load_dotenv()

DEBUG = True

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__, static_folder='static/wp-content', static_url_path='/wp-content')

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "root": {
        "level": "DEBUG",
        "handlers": ["console", "file"],
    },
    "formatters": {
        "simple": {"format": "%(asctime)s: %(message)s"},
        "detailed": {"format": "%(asctime)s %(levelname)-6s: %(module)s: %(message)s"},
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
        "file": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": 'app.log',
            "formatter": "detailed",
        },
    },
    "loggers": {},
}
logging.config.dictConfig(LOGGING)
logging.getLogger('sqlalchemy').setLevel(logging.WARNING)

# Directory to store uploaded files
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# import firebase_admin
# from firebase_admin import credentials, firestore
#
# # Initialize Firebase Admin SDK
# cred = credentials.Certificate("path/to/serviceAccountKey.json")
# firebase_admin.initialize_app(cred)
#
# # Initialize Firestore client
# db = firestore.client()

if DEBUG:
    PORT = 5000
    HOST = "0.0.0.0"
    SCHEMA = "http"

    WAIT_TIME_VALIDATION = 3
else:
    PORT = 5000
    HOST = "0.0.0.0"
    SCHEMA = "http"

    WAIT_TIME_VALIDATION = 30

SERVER_BASE_URL = f'{SCHEMA}://{HOST}:{PORT}'

# Convert the file at flask-frontend or worker-backend
CONVERSION_AT_FRONTEND = True
