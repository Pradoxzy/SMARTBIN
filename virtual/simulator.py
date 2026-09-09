import random
import time
from datetime import datetime

from lora_simulator import create_lora_packet, transmit_packet

from gateway import receive_packet

BIN_ID = "BIN-001"

LATITUDE = 12.8236
LONGITUDE = 80.0454

fill_level = 35
battery = 95


def simulate_ultrasonic_sensor():
    """
    Simulates an ultrasonic sensor measuring
    how full the waste bin is.
    """

    global fill_level

    # Simulate waste increasing or occasionally decreasing
    change = random.choice([0, 1, 2, 3, 4, -1])

    fill_level += change

    # Keep the value between 0% and 100%
    fill_level = max(0, min(100, fill_level))

    return fill_level


def simulate_battery():
    """
    Simulates gradual battery usage.
    """

    global battery

    battery -= random.choice([0, 0, 1])

    battery = max(10, battery)

    return battery


def calculate_status(fill_level):
    """
    Determines the bin status from its fill level.
    """

    if fill_level >= 90:
        return "CRITICAL"

    elif fill_level >= 75:
        return "WARNING"

    elif fill_level >= 50:
        return "MODERATE"

    else:
        return "NORMAL"


def generate_bin_data():

    fill = simulate_ultrasonic_sensor()
    battery_level = simulate_battery()

    status = calculate_status(fill)

    data = {
        "bin_id": BIN_ID,
        "timestamp": datetime.now().isoformat(),

        "fill_level": fill,
        "battery": battery_level,
        "status": status,

        "latitude": LATITUDE,
        "longitude": LONGITUDE
    }

    return data


def main():

    print("===================================")
    print("     SMARTBIN VIRTUAL SIMULATOR")
    print("===================================")

    while True:

        bin_data = generate_bin_data()

        print("\n🗑️ VIRTUAL SMARTBIN")
        print("---------------------------")

        print(f"Bin ID       : {bin_data['bin_id']}")
        print(f"Fill Level   : {bin_data['fill_level']}%")
        print(f"Battery      : {bin_data['battery']}%")
        print(f"Status       : {bin_data['status']}")
        print(f"Location     : {bin_data['latitude']}, {bin_data['longitude']}")
        print(f"Timestamp    : {bin_data['timestamp']}")

        packet = create_lora_packet(bin_data)
        transmit_packet(packet)
        receive_packet(packet)

        print("\nWaiting for next reading...")

        time.sleep(5)


if __name__ == "__main__":
    main()