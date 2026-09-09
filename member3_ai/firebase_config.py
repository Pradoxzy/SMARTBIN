import os
from pathlib import Path

import firebase_admin
from firebase_admin import credentials, db
from dotenv import load_dotenv


# Find the main SMARTBIN project folder
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Load .env from the SMARTBIN folder
load_dotenv(PROJECT_ROOT / ".env")

# Get Firebase database URL
firebase_database_url = os.getenv("FIREBASE_DATABASE_URL")


# Initialize Firebase only once
if not firebase_admin._apps:

    # Find the private Firebase service-account key
    service_account_path = PROJECT_ROOT / "serviceAccountKey.json"

    # Create Firebase credentials
    credential = credentials.Certificate(str(service_account_path))

    # Connect to Firebase Realtime Database
    firebase_admin.initialize_app(
        credential,
        {
            "databaseURL": firebase_database_url
        }
    )


def get_database():
    """Return the Firebase Realtime Database reference."""
    return db.reference("/")
    