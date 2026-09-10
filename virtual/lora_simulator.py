from gateway import receive_packet


def transmit_packet(packet):

    print("\n📡 SIMULATED LoRaWAN")
    print("----------------------------")

    print(
        f"Transmitting packet from "
        f"{packet['device_id']}..."
    )

    print("Packet transmitted successfully!")

    receive_packet(packet)