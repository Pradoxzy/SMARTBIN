import random
import time
from datetime import datetime

from lora_simulator import transmit_packet


# ============================================================
# 8 VIRTUAL SMART BINS
# ============================================================

BINS = [
    {
        "bin_id": "BIN-001",
        "latitude": 13.0418,
        "longitude": 80.2341
    },
    {
        "bin_id": "BIN-002",
        "latitude": 13.0067,
        "longitude": 80.2572
    },
    {
        "bin_id": "BIN-003",
        "latitude": 12.9815,
        "longitude": 80.2180
    },
    {
        "bin_id": "BIN-004",
        "latitude": 13.0067,
        "longitude": 80.2206
    },
    {
        "bin_id": "BIN-005",
        "latitude": 12.9830,
        "longitude": 80.2594
    },
    {
        "bin_id": "BIN-006",
        "latitude": 13.0185,
        "longitude": 80.2425
    },
    {
        "bin_id": "BIN-007",
        "latitude": 13.0280,
        "longitude": 80.2480
    },
    {
        "bin_id": "BIN-008",
        "latitude": 12.9950,
        "longitude": 80.2350
    }
]


# ============================================================
# STATUS CALCULATION
# ============================================================

def get_status(fill_level):

    if fill_level >= 90:
        return "CRITICAL"

    elif fill_level >= 70:
        return "HIGH"

    elif fill_level >= 40:
        return "MODERATE"

    else:
        return "LOW"


# ============================================================
# CREATE SENSOR PACKET
# ============================================================

def create_bin_packet(bin_info):

    fill_level = random.randint(20, 100)

    battery = random.randint(70, 100)

    status = get_status(fill_level)

    return {
        "device_id": bin_info["bin_id"],

        "timestamp": datetime.now().isoformat(),

        "payload": {
            "fill_level": fill_level,
            "battery": battery,
            "status": status,
            "latitude": bin_info["latitude"],
            "longitude": bin_info["longitude"]
        }
    }


# ============================================================
# MAIN SIMULATOR
# ============================================================

def main():

    print("\n========================================")
    print("       🗑️ SMARTBIN AI SIMULATOR")
    print("========================================")

    print("\nSimulating 8 SmartBins...\n")

    while True:

        for bin_info in BINS:

            packet = create_bin_packet(bin_info)

            payload = packet["payload"]

            print("\n----------------------------------------")

            print(f"🗑️ BIN: {bin_info['bin_id']}")

            print(
                f"📊 Fill Level: "
                f"{payload['fill_level']}%"
            )

            print(
                f"🔋 Battery: "
                f"{payload['battery']}%"
            )

            print(
                f"🚨 Status: "
                f"{payload['status']}"
            )

            print(
                f"📍 Location: "
                f"{payload['latitude']}, "
                f"{payload['longitude']}"
            )

            transmit_packet(packet)

            time.sleep(2)


# ============================================================
# START
# ============================================================

if __name__ == "__main__":
    main()