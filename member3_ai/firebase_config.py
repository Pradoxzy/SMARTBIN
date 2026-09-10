import os
from pathlib import Path

import firebase_admin
from firebase_admin import credentials, db
from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parent.parent

load_dotenv(PROJECT_ROOT / ".env")

firebase_database_url = os.getenv("FIREBASE_DATABASE_URL")

if not firebase_database_url:
    raise ValueError("FIREBASE_DATABASE_URL is missing from .env")


if not firebase_admin._apps:

    service_account_path = PROJECT_ROOT / "serviceAccountKey.json"

    if not service_account_path.exists():
        raise FileNotFoundError(
            "serviceAccountKey.json was not found."
        )

    credential = credentials.Certificate(
        str(service_account_path)
    )

    firebase_admin.initialize_app(
        credential,
        {
            "databaseURL": firebase_database_url
        }
    )


def get_database():
    return db.reference("/")