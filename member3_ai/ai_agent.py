from firebase_config import get_database


def calculate_priority(bin_data):
    """
    Analyze SmartBin sensor data and calculate collection priority.
    """

    fill_level = float(bin_data.get("fill_level", 0))
    battery = float(bin_data.get("battery", 100))

    # Calculate priority based mainly on fill level
    if fill_level >= 80:
        priority = "HIGH"
        score = 90
    elif fill_level >= 50:
        priority = "MEDIUM"
        score = 60
    else:
        priority = "LOW"
        score = 30

    # Add a small urgency factor if battery is very low
    if battery < 20:
        score += 5

    return {
        "priority": priority,
        "priority_score": score
    }


def run_ai_agent():
    """Read bins from Firebase and analyze them."""

    database = get_database()

    bins = database.child("bins").get()

    if not bins:
        print("No SmartBin data found in Firebase.")
        return

    print("\n===== SMARTBIN AI AGENT =====\n")

    for bin_id, bin_data in bins.items():

        result = calculate_priority(bin_data)

        # Save AI result back to Firebase
        database.child("bins").child(bin_id).update(result)

        print(f"Bin: {bin_id}")
        print(f"Fill Level: {bin_data.get('fill_level', 0)}%")
        print(f"Battery: {bin_data.get('battery', 0)}%")
        print(f"Priority: {result['priority']}")
        print(f"Priority Score: {result['priority_score']}")
        print("-----------------------------")


if __name__ == "__main__":
    run_ai_agent()
    