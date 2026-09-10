from firebase_config import get_database


def receive_packet(packet):
    """
    Simulates the municipal gateway receiving
    a LoRaWAN packet and forwarding it to Firebase.
    """

    print("\n🏢 VIRTUAL MUNICIPAL GATEWAY")
    print("---------------------------")

    print(
        f"📡 Packet received from: "
        f"{packet['device_id']}"
    )

    print("📦 Decoding packet...")

    payload = packet["payload"]

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
        f"{data['latitude']}, "
        f"{data['longitude']}"
    )

    print("\n☁️ Sending data to Firebase...")

    try:

        database = get_database()

        reference = database.reference(
            f"bins/{data['bin_id']}"
        )

        reference.set(data)

        print("✅ Firebase updated successfully!")

    except Exception as error:

        print("❌ Firebase update failed.")
        print("Error:", error)