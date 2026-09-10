from firebase_config import get_database


def calculate_priority(bin_data):

    fill_level = float(
        bin_data.get("fill_level", 0)
    )

    battery = float(
        bin_data.get("battery", 100)
    )

    score = 0

    # Fill level is the main factor
    if fill_level >= 90:
        score += 70
    elif fill_level >= 70:
        score += 50
    elif fill_level >= 40:
        score += 30
    else:
        score += 10

    # Battery contribution
    if battery < 20:
        score += 20
    elif battery < 40:
        score += 10
    else:
        score += 5

    # Convert score to priority
    if score >= 80:
        priority = "CRITICAL"
    elif score >= 60:
        priority = "HIGH"
    elif score >= 40:
        priority = "MEDIUM"
    else:
        priority = "LOW"

    return priority, score


def analyze_bins():

    database = get_database()

    bins = database.child("bins").get()

    if not bins:

        print("No SmartBin data found.")

        return {}


    results = {}

    for bin_id, bin_data in bins.items():

        if not isinstance(bin_data, dict):
            continue

        priority, score = calculate_priority(
            bin_data
        )

        bin_data["priority"] = priority
        bin_data["priority_score"] = score

        # Store AI result back in Firebase
        database \
            .child("bins") \
            .child(bin_id) \
            .update({
                "priority": priority,
                "priority_score": score
            })

        results[bin_id] = bin_data

    return results


if __name__ == "__main__":

    results = analyze_bins()

    print("\n====================================")
    print("        SMARTBIN AI ANALYSIS")
    print("====================================")

    for bin_id, data in results.items():

        print(f"\n{bin_id}")
        print(
            f"Fill Level: "
            f"{data.get('fill_level', 0)}%"
        )
        print(
            f"Priority: "
            f"{data.get('priority', 'LOW')}"
        )
        print(
            f"Score: "
            f"{data.get('priority_score', 0)}"
        )