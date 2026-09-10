import firebase_admin
from firebase_admin import credentials, db

# ============================================================
# FIREBASE CONFIGURATION
# ============================================================

# Name of your private Firebase service-account JSON file.
# IMPORTANT: This file must NOT be uploaded to GitHub.
SERVICE_ACCOUNT_KEY = "smartbin.json"

# Firebase Realtime Database URL
DATABASE_URL = "https://smartbins-c5b57-default-rtdb.asia-southeast1.firebasedatabase.app/"


# ============================================================
# INITIALIZE FIREBASE
# ============================================================

if not firebase_admin._apps:
    cred = credentials.Certificate(SERVICE_ACCOUNT_KEY)

    firebase_admin.initialize_app(
        cred,
        {
            "databaseURL": DATABASE_URL
        }
    )


# ============================================================
# DATABASE ACCESS
# ============================================================

def get_database():
    """Return the Firebase Realtime Database module."""
    return db