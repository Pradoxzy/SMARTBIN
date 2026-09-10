import time


def create_lora_packet(bin_data):
    """
    Creates a simulated LoRaWAN uplink packet.
    """

    packet = {
        "protocol": "SIMULATED_LORAWAN",
        "device_id": bin_data["bin_id"],
        "timestamp": bin_data["timestamp"],

        "payload": {
            "fill_level": bin_data["fill_level"],
            "battery": bin_data["battery"],
            "status": bin_data["status"],
            "latitude": bin_data["latitude"],
            "longitude": bin_data["longitude"]
        }
    }

    return packet


def transmit_packet(packet):
    """
    Simulates transmission from the virtual ESP32
    to the virtual municipal gateway.
    """

    print("\n📡 SIMULATED LORAWAN")
    print("---------------------------")

    print("Sending packet...")
    
    time.sleep(1)

    print("Packet transmitted successfully!")

    return packet