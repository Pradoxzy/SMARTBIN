from firebase_config import get_database

database = get_database()

test_data = {
    "bin_id": "TEST-BIN-001",
    "fill_level": 65,
    "battery": 87,
    "status": "MEDIUM",
    "location": "Zone A"
}

database.child("bins").child("TEST-BIN-001").set(test_data)

print("SUCCESS!")
print("Test SmartBin data was sent to Firebase.")
