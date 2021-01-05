"""Configuration of database."""
import pyrebase
import os
from decouple import config
API_KEY = config("DB_KEY")
GLOBAL_PATH = os.path.dirname(__file__)


def configure():
    """Config database.

    Returns:
        object: database object
    """
    config = {
        "apiKey": API_KEY,
        "authDomain": "alfalfa-28add.firebaseapp.com",
        "databaseURL": "https://alfalfa-28add-default-rtdb.firebaseio.com/",
        "storageBucket": "alfalfa-28add.appspot.com"
    }
    # Initializing pyrebase
    firebase = pyrebase.initialize_app(config)

    # Initializing Database
    db = firebase.database()
    return db
