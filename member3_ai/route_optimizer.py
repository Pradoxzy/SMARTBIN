from firebase_config import get_database


def optimize_route(bins):
    """
    Create a simple collection route.
    Highest-priority bins are visited first.
    """

    priority_order = {
        "HIGH": 1,
        "MEDIUM": 2,
        "LOW": 3
    }

    sorted_bins = sorted(
        bins.items(),
        key=lambda item: (
            priority_order.get(
                item[1].get("priority", "LOW"),
                3
            ),
            -float(item[1].get("fill_level", 0))
        )
    )

    return sorted_bins


def run_route_optimizer():
    """Read AI-prioritized bins from Firebase and create a route."""

    database = get_database()

    bins = database.child("bins").get()

    if not bins:
        print("No SmartBin data found.")
        return

    route = optimize_route(bins)

    print("\n===== SMARTBIN COLLECTION ROUTE =====\n")

    for position, (bin_id, bin_data) in enumerate(route, start=1):

        print(f"{position}. {bin_id}")
        print(f"   Location: {bin_data.get('location', 'Unknown')}")
        print(f"   Fill Level: {bin_data.get('fill_level', 0)}%")
        print(f"   Priority: {bin_data.get('priority', 'LOW')}")
        print(f"   Score: {bin_data.get('priority_score', 0)}")
        print()


if __name__ == "__main__":
    run_route_optimizer()
    