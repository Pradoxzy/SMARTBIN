from firebase_config import get_database


def receive_packet(packet):

    print("\n====================================")
    print("   VIRTUAL MUNICIPAL GATEWAY")
    print("====================================")

    device_id = packet["device_id"]
    payload = packet["payload"]

    print(f"Packet received from: {device_id}")
    print("Decoding packet...")

    data = {
        "bin_id": device_id,
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

    try:

        database = get_database()

        reference = (
            database
            .child("bins")
            .child(device_id)
        )

        reference.set(data)

        print(
            f"Firebase updated successfully "
            f"for {device_id}!"
        )

    except Exception as error:

        print("Firebase update failed.")
        print("Error:", error)