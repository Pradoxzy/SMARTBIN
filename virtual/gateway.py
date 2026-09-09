from firebase_config import get_database


def receive_packet(packet):
    """
    Simulates the municipal gateway receiving
    a LoRaWAN packet and forwarding it to Firebase.
    """

    print("\n🏢 VIRTUAL MUNICIPAL GATEWAY")
    print("----------------------------")

    print(
        f"📡 Packet received from: "
        f"{packet['device_id']}"
    )

    print("📦 Decoding packet...")

    payload = packet["payload"]

    # Convert the received LoRaWAN payload
    # into structured SmartBin data.
    data = {
        "bin_id": packet["device_id"],
        "timestamp": packet["timestamp"],
        "fill_level": payload["fill_level"],
        "battery": payload["battery"],
        "status": payload["status"],
        "latitude": payload["latitude"],
        "longitude": payload["longitude"],
        "communication": "SIMULATED_LORAWAN",
        "gateway": "VIRTUAL_MUNICIPAL_GATEWAY"
    }

    print("\nReceived data:")
    print(f"Fill Level : {data['fill_level']}%")
    print(f"Battery    : {data['battery']}%")
    print(f"Status     : {data['status']}")

    print(
        f"Location   : "
        f"{data['latitude']}, {data['longitude']}"
    )

    print("\n☁️ Sending data to Firebase...")

    try:
        # Get the Firebase database reference.
        database = get_database()

        # get_database() already returns a Firebase
        # Reference, so use .child() instead of
        # calling .reference() again.
        reference = (
            database
            .child("bins")
            .child(data["bin_id"])
        )

        # Store the latest SmartBin data.
        reference.set(data)

        print("✅ Firebase updated successfully!")

    except Exception as error:
        print("❌ Firebase update failed.")
        print("Error:", error)
        