import requests

from firebase_config import get_database


# Virtual municipal depot
DEPOT = {
    "latitude": 12.8215,
    "longitude": 80.0435
}


# Free OSRM routing service
OSRM_URL = "https://router.project-osrm.org/route/v1/driving"


def optimize_route(bins):
    """
    Create a collection route using OSRM.

    Bins are first ordered by AI priority.
    OSRM then calculates the actual road route
    through those locations.
    """

    priority_order = {
        "CRITICAL": 1,
        "HIGH": 2,
        "MEDIUM": 3,
        "LOW": 4
    }

    valid_bins = []

    for bin_id, data in bins.items():

        latitude = data.get("latitude")
        longitude = data.get("longitude")

        if latitude is None or longitude is None:
            continue

        valid_bins.append(
            (
                bin_id,
                data
            )
        )

    if not valid_bins:
        return None

    # First prioritize bins using our AI score.
    valid_bins.sort(
        key=lambda item: (
            priority_order.get(
                item[1].get("priority", "LOW"),
                4
            ),
            -float(
                item[1].get("priority_score", 0)
            ),
            -float(
                item[1].get("fill_level", 0)
            )
        )
    )

    # Depot first
    coordinates = [
        f"{DEPOT['longitude']},{DEPOT['latitude']}"
    ]

    # Add bins
    for bin_id, data in valid_bins:
        coordinates.append(
            f"{float(data['longitude'])},{float(data['latitude'])}"
        )

    # Return to depot
    coordinates.append(
        f"{DEPOT['longitude']},{DEPOT['latitude']}"
    )

    coordinate_string = ";".join(coordinates)

    params = {
        "overview": "full",
        "geometries": "geojson",
        "steps": "false"
    }

    try:

        response = requests.get(
            f"{OSRM_URL}/{coordinate_string}",
            params=params,
            timeout=20
        )

        response.raise_for_status()

        result = response.json()

    except requests.RequestException as error:

        print("OSRM routing failed:")
        print(error)

        return None

    if result.get("code") != "Ok":

        print("OSRM returned an error:")
        print(result)

        return None

    route = result["routes"][0]

    distance_km = route["distance"] / 1000

    duration_minutes = route["duration"] / 60

    route_points = []

    geometry = route.get("geometry", {})

    for longitude, latitude in geometry.get(
        "coordinates",
        []
    ):

        route_points.append(
            (
                latitude,
                longitude
            )
        )

    return {
        "bins": valid_bins,
        "distance_km": distance_km,
        "duration_minutes": duration_minutes,
        "route_points": route_points
    }


def run_route_optimizer():

    database = get_database()

    bins = database.child("bins").get()

    if not bins:

        print("No SmartBin data found.")

        return

    route = optimize_route(bins)

    if not route:

        print("Could not create route.")

        return

    print("\n====================================")
    print("      🚚 SMARTBIN OPTIMIZED ROUTE")
    print("====================================")

    print(
        f"\nTotal Distance: "
        f"{route['distance_km']:.2f} km"
    )

    print(
        f"Estimated Time: "
        f"{route['duration_minutes']:.1f} minutes"
    )

    print("\nCollection Order:\n")

    for position, (bin_id, data) in enumerate(
        route["bins"],
        start=1
    ):

        print(
            f"{position}. {bin_id}"
        )

        print(
            f"   Fill Level: "
            f"{data.get('fill_level', 0)}%"
        )

        print(
            f"   Priority: "
            f"{data.get('priority', 'LOW')}"
        )

        print(
            f"   Score: "
            f"{data.get('priority_score', 0)}"
        )

        print(
            f"   Location: "
            f"{data.get('latitude')}, "
            f"{data.get('longitude')}"
        )

        print()

    print("====================================")


if __name__ == "__main__":
    run_route_optimizer()