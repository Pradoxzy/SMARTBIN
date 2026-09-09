import os
from pathlib import Path

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from dotenv import load_dotenv


# Folder containing this file
BASE_DIR = Path(__file__).resolve().parent

# Load the .env file from virtual_bin
load_dotenv(BASE_DIR / ".env")


# Read Firebase settings
SERVICE_ACCOUNT_NAME = os.getenv("FIREBASE_SERVICE_ACCOUNT")
DATABASE_URL = os.getenv("FIREBASE_DATABASE_URL")


# Check that the .env values exist
if not SERVICE_ACCOUNT_NAME:
    raise ValueError(
        "FIREBASE_SERVICE_ACCOUNT is missing from .env"
    )

if not DATABASE_URL:
    raise ValueError(
        "FIREBASE_DATABASE_URL is missing from .env"
    )


# Create the full path to the service-account JSON file
SERVICE_ACCOUNT_PATH = BASE_DIR / SERVICE_ACCOUNT_NAME


# Connect to Firebase only once
if not firebase_admin._apps:

    cred = credentials.Certificate(
        str(SERVICE_ACCOUNT_PATH)
    )

    firebase_admin.initialize_app(
        cred,
        {
            "databaseURL": DATABASE_URL
        }
    )


def get_database():
    return db