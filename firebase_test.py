from firebase_config import get_database


# ============================================================
# TEST FIREBASE REALTIME DATABASE CONNECTION
# ============================================================

database = get_database()

# Read BIN-001 from Firebase Realtime Database
reference = database.reference("bins/BIN-001")

data = reference.get()


# ============================================================
# DISPLAY RESULT
# ============================================================

if data:
    print("===================================")
    print("Firebase connection successful!")
    print("===================================")

    print("\nBIN-001 data:")
    print(data)

else:
    print("===================================")
    print("Firebase connected, but BIN-001 was not found.")
    print("===================================")