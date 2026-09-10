import os
import requests
import folium
import pandas as pd
import streamlit as st
import firebase_admin

from dotenv import load_dotenv
from firebase_admin import credentials, db
from streamlit_folium import st_folium
from streamlit_autorefresh import st_autorefresh


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="SmartBin AI",
    page_icon="♻️",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# FIREBASE
# ============================================================

ROOT = os.path.dirname(
    os.path.abspath(__file__)
)

load_dotenv(
    os.path.join(ROOT, ".env")
)

FIREBASE_DATABASE_URL = os.getenv(
    "FIREBASE_DATABASE_URL"
)

SERVICE_ACCOUNT = os.path.join(
    ROOT,
    "serviceAccountKey.json"
)


def initialize_firebase():

    if not FIREBASE_DATABASE_URL:

        st.error(
            "FIREBASE_DATABASE_URL is missing from .env"
        )

        st.stop()

    if not os.path.exists(SERVICE_ACCOUNT):

        st.error(
            "serviceAccountKey.json not found."
        )

        st.stop()

    if not firebase_admin._apps:

        cred = credentials.Certificate(
            SERVICE_ACCOUNT
        )

        firebase_admin.initialize_app(
            cred,
            {
                "databaseURL":
                    FIREBASE_DATABASE_URL
            }
        )


initialize_firebase()


# ============================================================
# ONLY 5 SMART BINS
# ============================================================

BIN_IDS = [
    "BIN-001",
    "BIN-002",
    "BIN-003",
    "BIN-004",
    "BIN-005",
]


# ============================================================
# CHENNAI LOCATIONS
# ============================================================

BIN_INFO = {

    "BIN-001": {
        "location": "Marina Promenade",
        "zone": "Central",
        "latitude": 13.0499,
        "longitude": 80.2824,
    },

    "BIN-002": {
        "location": "Anna Salai Junction",
        "zone": "Central",
        "latitude": 13.0569,
        "longitude": 80.2425,
    },

    "BIN-003": {
        "location": "Triplicane Market",
        "zone": "East",
        "latitude": 13.0588,
        "longitude": 80.2750,
    },

    "BIN-004": {
        "location": "Nungambakkam High Road",
        "zone": "North",
        "latitude": 13.0569,
        "longitude": 80.2421,
    },

    "BIN-005": {
        "location": "Royapettah Clock Tower",
        "zone": "West",
        "latitude": 13.0524,
        "longitude": 80.2676,
    },
}


# ============================================================
# COLLECTION DEPOT
# ============================================================

DEPOT_LAT = 13.0788
DEPOT_LON = 80.2613


# ============================================================
# OSRM
# ============================================================

OSRM_URL = (
    "https://router.project-osrm.org"
)


# ============================================================
# STYLE
# ============================================================

st.markdown(
    """
    <style>

    .stApp {
        background:
            radial-gradient(
                circle at 85% 0%,
                rgba(34,197,94,.12),
                transparent 25%
            ),
            #070b14;
    }

    [data-testid="stHeader"] {
        background: rgba(7,11,20,.85);
    }

    section[data-testid="stSidebar"] {
        background: #0b1220;
    }

    .brand {
        font-size: 1.45rem;
        font-weight: 800;
        color: #f8fafc;
    }

    .brand-subtitle {
        color: #94a3b8;
        font-size: .82rem;
        margin-bottom: 1rem;
    }

    .title {
        font-size: 3rem;
        font-weight: 800;
        color: #f8fafc;
        letter-spacing: -.05em;
    }

    .subtitle {
        color: #94a3b8;
        margin-bottom: 1.5rem;
    }

    [data-testid="stMetric"] {
        background: rgba(17,24,39,.8);
        border: 1px solid rgba(148,163,184,.16);
        border-radius: 15px;
        padding: 1rem;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# FIREBASE → LIVE BIN DATA
# ============================================================

def get_live_bins():

    try:

        firebase_bins = db.reference(
            "/bins"
        ).get()

    except Exception as error:

        st.error(
            "Firebase connection failed."
        )

        st.exception(error)

        return pd.DataFrame()

    if not firebase_bins:

        return pd.DataFrame()

    rows = []

    for bin_id in BIN_IDS:

        if bin_id not in firebase_bins:
            continue

        firebase_data = firebase_bins[
            bin_id
        ]

        if not isinstance(
            firebase_data,
            dict
        ):
            continue

        try:

            fill = float(
                firebase_data.get(
                    "fill_level",
                    0
                )
            )

        except:

            fill = 0

        try:

            battery = float(
                firebase_data.get(
                    "battery",
                    100
                )
            )

        except:

            battery = 100

        location = BIN_INFO[
            bin_id
        ]

        rows.append(
            {
                "Bin ID":
                    bin_id,

                "Location":
                    location[
                        "location"
                    ],

                "Zone":
                    location[
                        "zone"
                    ],

                "Fill Level":
                    fill,

                "Battery":
                    battery,

                "Latitude":
                    location[
                        "latitude"
                    ],

                "Longitude":
                    location[
                        "longitude"
                    ],

                "Timestamp":
                    firebase_data.get(
                        "timestamp",
                        ""
                    ),
            }
        )

    if not rows:

        return pd.DataFrame()

    return pd.DataFrame(rows)


# ============================================================
# STATUS
# ============================================================

def calculate_status(
    fill
):

    if fill >= 90:

        return "Critical"

    elif fill >= 75:

        return "Warning"

    else:

        return "Normal"


# ============================================================
# AI SCORE
# ============================================================

def calculate_ai_score(
    fill,
    battery
):

    if fill >= 90:

        fill_score = 70

    elif fill >= 70:

        fill_score = 50

    elif fill >= 40:

        fill_score = 30

    else:

        fill_score = 10

    if battery < 20:

        battery_score = 20

    elif battery < 40:

        battery_score = 10

    else:

        battery_score = 5

    score = min(
        fill_score
        + battery_score,
        100
    )

    if score >= 80:

        priority = "URGENT"

    elif score >= 60:

        priority = "HIGH"

    elif score >= 40:

        priority = "SCHEDULED"

    else:

        priority = "MONITOR"

    return score, priority


# ============================================================
# PROCESS LIVE DATA
# ============================================================

def process_bins(
    bins
):

    if bins.empty:

        return bins

    result = bins.copy()

    result["Status"] = (
        result["Fill Level"]
        .apply(
            calculate_status
        )
    )

    ai_results = result.apply(
        lambda row:
            calculate_ai_score(
                row["Fill Level"],
                row["Battery"]
            ),
        axis=1
    )

    result["AI Score"] = [
        result_value[0]
        for result_value in ai_results
    ]

    result["Priority"] = [
        result_value[1]
        for result_value in ai_results
    ]

    return result


# ============================================================
# 🔥 DYNAMIC ROUTE OPTIMIZATION
# ============================================================

def optimize_route(
    bins
):

    if bins.empty:

        return None

    # --------------------------------------------------------
    # ONLY COLLECT BINS THAT CURRENTLY NEED ATTENTION
    # --------------------------------------------------------

    collection_bins = bins[
        bins["Fill Level"] >= 70
    ].copy()

    # If no bin is >=70%, select the
    # two highest AI-priority bins.
    if collection_bins.empty:

        collection_bins = (
            bins
            .sort_values(
                "AI Score",
                ascending=False
            )
            .head(2)
            .copy()
        )

    if collection_bins.empty:

        return None

    # --------------------------------------------------------
    # BUILD OSRM COORDINATE LIST
    #
    # OSRM uses:
    # longitude,latitude
    #
    # NOT:
    # latitude,longitude
    # --------------------------------------------------------

    coordinates = [
        f"{DEPOT_LON},{DEPOT_LAT}"
    ]

    for _, row in collection_bins.iterrows():

        coordinates.append(
            f"{row['Longitude']},{row['Latitude']}"
        )

    coordinate_string = ";".join(
        coordinates
    )

    # --------------------------------------------------------
    # OSRM TRIP SERVICE
    #
    # This actually optimizes waypoint order.
    # --------------------------------------------------------

    url = (
        f"{OSRM_URL}"
        f"/trip/v1/driving/"
        f"{coordinate_string}"
    )

    params = {
        "roundtrip": "true",
        "source": "first",
        "overview": "full",
        "geometries": "geojson",
        "steps": "true",
    }

    try:

        response = requests.get(
            url,
            params=params,
            timeout=15
        )

        response.raise_for_status()

        data = response.json()

    except Exception as error:

        st.warning(
            "OSRM route service unavailable. "
            "Using AI priority order."
        )

        fallback = (
            collection_bins
            .sort_values(
                [
                    "AI Score",
                    "Fill Level"
                ],
                ascending=False
            )
            .reset_index(drop=True)
        )

        return {
            "bins":
                fallback,

            "distance_km":
                None,

            "duration_minutes":
                None,

            "geometry":
                None,

            "optimized":
                False,
        }

    if data.get(
        "code"
    ) != "Ok":

        return None

    # --------------------------------------------------------
    # GET OPTIMIZED WAYPOINT ORDER
    # --------------------------------------------------------

    waypoints = data.get(
        "waypoints",
        []
    )

    optimized_bins = []

    for waypoint in waypoints:

        waypoint_index = waypoint.get(
            "waypoint_index"
        )

        # Index 0 = depot.
        if (
            waypoint_index is None
            or waypoint_index == 0
        ):
            continue

        bin_position = (
            waypoint_index - 1
        )

        if (
            0
            <= bin_position
            < len(collection_bins)
        ):

            optimized_bins.append(
                collection_bins.iloc[
                    bin_position
                ]
            )

    if optimized_bins:

        optimized_df = pd.DataFrame(
            optimized_bins
        ).reset_index(
            drop=True
        )

    else:

        optimized_df = (
            collection_bins
            .sort_values(
                "AI Score",
                ascending=False
            )
            .reset_index(
                drop=True
            )
        )

    # --------------------------------------------------------
    # ROUTE INFORMATION
    # --------------------------------------------------------

    distance_km = (
        data.get(
            "trips",
            [{}]
        )[0]
        .get(
            "distance",
            0
        )
        / 1000
    )

    duration_minutes = (
        data.get(
            "trips",
            [{}]
        )[0]
        .get(
            "duration",
            0
        )
        / 60
    )

    geometry = (
        data.get(
            "trips",
            [{}]
        )[0]
        .get(
            "geometry"
        )
    )

    return {
        "bins":
            optimized_df,

        "distance_km":
            distance_km,

        "duration_minutes":
            duration_minutes,

        "geometry":
            geometry,

        "optimized":
            True,
    }


# ============================================================
# CREATE LIVE MAP
# ============================================================

def create_live_map(
    bins
):

    if bins.empty:

        return None

    center = [
        bins["Latitude"].mean(),
        bins["Longitude"].mean()
    ]

    map_object = folium.Map(
        location=center,
        zoom_start=13,
        tiles="OpenStreetMap"
    )

    # Depot
    folium.Marker(
        location=[
            DEPOT_LAT,
            DEPOT_LON
        ],
        tooltip="Collection Depot",
        popup="Collection Depot",
        icon=folium.Icon(
            color="blue",
            icon="home"
        )
    ).add_to(
        map_object
    )

    colors = {
        "Critical": "red",
        "Warning": "orange",
        "Normal": "green"
    }

    for _, row in bins.iterrows():

        popup = (
            f"<b>{row['Bin ID']}</b><br>"
            f"{row['Location']}<br>"
            f"Fill: {row['Fill Level']:.0f}%<br>"
            f"Battery: {row['Battery']:.0f}%<br>"
            f"AI Score: {row['AI Score']}/100<br>"
            f"Status: {row['Status']}"
        )

        folium.CircleMarker(
            location=[
                row["Latitude"],
                row["Longitude"]
            ],

            radius=11
            if row["Status"]
            == "Critical"
            else 8,

            color=colors[
                row["Status"]
            ],

            fill=True,

            fill_color=colors[
                row["Status"]
            ],

            fill_opacity=.9,

            tooltip=(
                f"{row['Bin ID']} · "
                f"{row['Fill Level']:.0f}%"
            ),

            popup=folium.Popup(
                popup,
                max_width=250
            )
        ).add_to(
            map_object
        )

    return map_object


# ============================================================
# CREATE OPTIMIZED ROUTE MAP
# ============================================================

def create_route_map(
    route_data
):

    route_bins = route_data[
        "bins"
    ]

    if route_bins.empty:

        return None

    map_object = folium.Map(
        location=[
            route_bins[
                "Latitude"
            ].mean(),

            route_bins[
                "Longitude"
            ].mean()
        ],

        zoom_start=13,

        tiles="OpenStreetMap"
    )

    # --------------------------------------------------------
    # DEPOT
    # --------------------------------------------------------

    folium.Marker(
        location=[
            DEPOT_LAT,
            DEPOT_LON
        ],

        tooltip="Collection Depot",

        popup="START / END DEPOT",

        icon=folium.Icon(
            color="blue",
            icon="home"
        )
    ).add_to(
        map_object
    )

    # --------------------------------------------------------
    # REAL OSRM ROAD ROUTE
    # --------------------------------------------------------

    geometry = route_data[
        "geometry"
    ]

    if geometry:

        route_coordinates = []

        for lon, lat in geometry[
            "coordinates"
        ]:

            route_coordinates.append(
                [lat, lon]
            )

        folium.PolyLine(
            route_coordinates,
            color="#22c55e",
            weight=6,
            opacity=.9
        ).add_to(
            map_object
        )

    # --------------------------------------------------------
    # NUMBERED STOPS
    # --------------------------------------------------------

    for number, (_, row) in enumerate(
        route_bins.iterrows(),
        start=1
    ):

        popup = (
            f"<b>STOP #{number}</b><br>"
            f"{row['Bin ID']}<br>"
            f"{row['Location']}<br><br>"
            f"Fill: "
            f"{row['Fill Level']:.0f}%<br>"
            f"AI Score: "
            f"{row['AI Score']}/100<br>"
            f"Priority: "
            f"{row['Priority']}"
        )

        folium.Marker(
            location=[
                row["Latitude"],
                row["Longitude"]
            ],

            tooltip=(
                f"Stop #{number} · "
                f"{row['Bin ID']}"
            ),

            popup=folium.Popup(
                popup,
                max_width=250
            ),

            icon=folium.DivIcon(
                html=f"""
                <div style="
                    background:#22c55e;
                    color:#07111f;
                    width:32px;
                    height:32px;
                    border-radius:50%;
                    display:flex;
                    align-items:center;
                    justify-content:center;
                    font-weight:900;
                    border:3px solid #07111f;
                    font-size:14px;
                ">
                    {number}
                </div>
                """
            )
        ).add_to(
            map_object
        )

    return map_object


# ============================================================
# COMMAND CENTRE
# ============================================================

def show_command_centre(
    bins
):

    st.markdown(
        '<div class="title">'
        'Command centre'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        'Real-time capacity risk, sensor health, '
        'AI priority and collection demand.'
        '</div>',
        unsafe_allow_html=True
    )

    if bins.empty:

        st.warning(
            "Waiting for Firebase data..."
        )

        return

    total = len(bins)

    critical = int(
        (
            bins["Status"]
            == "Critical"
        ).sum()
    )

    high_priority = int(
        (
            bins["AI Score"]
            >= 65
        ).sum()
    )

    average_fill = (
        bins["Fill Level"]
        .mean()
    )

    cards = st.columns(4)

    cards[0].metric(
        "Visible bins",
        total
    )

    cards[1].metric(
        "Critical risk",
        critical
    )

    cards[2].metric(
        "High-priority stops",
        high_priority
    )

    cards[3].metric(
        "Average fill",
        f"{average_fill:.0f}%"
    )

    st.markdown(
        "### Collection queue"
    )

    table = (
        bins
        .sort_values(
            "AI Score",
            ascending=False
        )
        [
            [
                "Bin ID",
                "Location",
                "Zone",
                "Fill Level",
                "Status",
                "AI Score",
                "Battery"
            ]
        ]
        .copy()
    )

    table = table.rename(
        columns={
            "Fill Level":
                "Fill (%)",

            "AI Score":
                "AI Score"
        }
    )

    st.dataframe(
        table,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# LIVE MAP
# ============================================================

def show_live_map(
    bins
):

    st.markdown(
        '<div class="title">'
        'Live map'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        'Live GPS locations from the SmartBin system.'
        '</div>',
        unsafe_allow_html=True
    )

    if bins.empty:

        st.warning(
            "Waiting for Firebase..."
        )

        return

    map_object = create_live_map(
        bins
    )

    st_folium(
        map_object,
        height=580,
        use_container_width=True,
        returned_objects=[],
        key="live_map"
    )


# ============================================================
# AI COLLECTION PLAN
# ============================================================

def show_ai_plan(
    bins
):

    st.markdown(
        '<div class="title">'
        'AI collection plan'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        'Live collection priority based on current bin conditions.'
        '</div>',
        unsafe_allow_html=True
    )

    if bins.empty:

        st.warning(
            "Waiting for Firebase..."
        )

        return

    plan = (
        bins
        .sort_values(
            [
                "AI Score",
                "Fill Level"
            ],
            ascending=False
        )
    )

    for number, (_, row) in enumerate(
        plan.iterrows(),
        start=1
    ):

        with st.container(
            border=True
        ):

            left, middle, right = st.columns(
                [3, 1, 1]
            )

            left.markdown(
                f"**#{number} · "
                f"{row['Bin ID']} · "
                f"{row['Location']}**"
            )

            left.progress(
                int(
                    row["Fill Level"]
                ),
                text=(
                    f"{row['Fill Level']:.0f}% full"
                )
            )

            middle.metric(
                "AI Score",
                int(
                    row["AI Score"]
                )
            )

            right.metric(
                "Priority",
                row["Priority"]
            )


# ============================================================
# 🚛 ROUTE OPTIMIZER PAGE
# ============================================================

def show_route_optimizer(
    bins
):

    st.markdown(
        '<div class="title">'
        'Route optimizer'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        'Dynamic road route calculated from the current Firebase bin conditions.'
        '</div>',
        unsafe_allow_html=True
    )

    if bins.empty:

        st.warning(
            "Waiting for Firebase..."
        )

        return

    # --------------------------------------------------------
    # 🔥 THIS IS THE IMPORTANT PART
    #
    # Every dashboard refresh:
    #
    # Firebase → latest fill values
    #             ↓
    #         AI scores
    #             ↓
    #       collection bins
    #             ↓
    #         OSRM /trip
    #             ↓
    #       NEW route
    #
    # --------------------------------------------------------

    route_data = optimize_route(
        bins
    )

    if not route_data:

        st.success(
            "No route required."
        )

        return

    route_bins = route_data[
        "bins"
    ]

    distance = route_data[
        "distance_km"
    ]

    duration = route_data[
        "duration_minutes"
    ]

    # --------------------------------------------------------
    # ROUTE METRICS
    # --------------------------------------------------------

    cards = st.columns(4)

    cards[0].metric(
        "Collection stops",
        len(route_bins)
    )

    if distance is not None:

        cards[1].metric(
            "Road distance",
            f"{distance:.2f} km"
        )

    else:

        cards[1].metric(
            "Road distance",
            "Calculating..."
        )

    if duration is not None:

        cards[2].metric(
            "Estimated drive",
            f"{duration:.0f} min"
        )

    else:

        cards[2].metric(
            "Estimated drive",
            "Calculating..."
        )

    cards[3].metric(
        "Route status",
        "OPTIMIZED"
        if route_data["optimized"]
        else "AI ORDER"
    )

    # --------------------------------------------------------
    # MAP + ORDER
    # --------------------------------------------------------

    map_column, order_column = st.columns(
        [1.7, 1]
    )

    with map_column:

        route_map = create_route_map(
            route_data
        )

        if route_map:

            st_folium(
                route_map,
                height=560,
                use_container_width=True,
                returned_objects=[],
                key="optimized_route_map"
            )

    with order_column:

        st.markdown(
            "### Live collection order"
        )

        for number, (_, row) in enumerate(
            route_bins.iterrows(),
            start=1
        ):

            with st.container(
                border=True
            ):

                st.markdown(
                    f"### #{number}"
                )

                st.markdown(
                    f"**{row['Bin ID']}**"
                )

                st.caption(
                    row["Location"]
                )

                st.write(
                    f"Fill: "
                    f"{row['Fill Level']:.0f}%"
                )

                st.write(
                    f"AI Score: "
                    f"{row['AI Score']}/100"
                )

                st.write(
                    f"Priority: "
                    f"{row['Priority']}"
                )

        st.success(
            "Route recalculated from live Firebase data."
        )


# ============================================================
# ALERTS
# ============================================================

def show_alerts(
    bins
):

    st.markdown(
        '<div class="title">'
        'Alerts'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        'Live alerts from current SmartBin conditions.'
        '</div>',
        unsafe_allow_html=True
    )

    if bins.empty:

        st.warning(
            "Waiting for Firebase..."
        )

        return

    alerts = bins[
        (
            bins["Status"]
            != "Normal"
        )
        |
        (
            bins["Battery"]
            < 40
        )
    ].sort_values(
        "AI Score",
        ascending=False
    )

    if alerts.empty:

        st.success(
            "No active alerts."
        )

        return

    for _, row in alerts.iterrows():

        if row["Status"] == "Critical":

            st.error(
                f"{row['Bin ID']} — "
                f"{row['Location']} is "
                f"{row['Fill Level']:.0f}% full."
            )

        elif row["Status"] == "Warning":

            st.warning(
                f"{row['Bin ID']} — "
                f"{row['Location']} is "
                f"{row['Fill Level']:.0f}% full."
            )

        if row["Battery"] < 40:

            st.info(
                f"{row['Bin ID']} battery: "
                f"{row['Battery']:.0f}%"
            )


# ============================================================
# MAIN
# ============================================================

def main():

    # --------------------------------------------------------
    # AUTO REFRESH EVERY 5 SECONDS
    # --------------------------------------------------------

    st_autorefresh(
        interval=5000,
        key="smartbin_live_refresh"
    )

    # --------------------------------------------------------
    # GET LIVE FIREBASE DATA
    # --------------------------------------------------------

    bins = get_live_bins()

    bins = process_bins(
        bins
    )

    # --------------------------------------------------------
    # SIDEBAR
    # --------------------------------------------------------

    with st.sidebar:

        st.markdown(
            '<div class="brand">'
            '♻️ SmartBin AI'
            '</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="brand-subtitle">'
            'Waste operations command centre'
            '</div>',
            unsafe_allow_html=True
        )

        page = st.radio(
            "Navigation",
            [
                "Command centre",
                "Live map",
                "AI collection plan",
                "Route optimizer",
                "Alerts"
            ],
            label_visibility="collapsed"
        )

        st.divider()

        if not bins.empty:

            st.success(
                f"🟢 {len(bins)} / 5 bins connected"
            )

        else:

            st.error(
                "🔴 Waiting for bins"
            )

        st.caption(
            "Firebase → Live data"
        )

        st.caption(
            "Refresh: 5 seconds"
        )

    # --------------------------------------------------------
    # PAGE
    # --------------------------------------------------------

    if page == "Command centre":

        show_command_centre(
            bins
        )

    elif page == "Live map":

        show_live_map(
            bins
        )

    elif page == "AI collection plan":

        show_ai_plan(
            bins
        )

    elif page == "Route optimizer":

        show_route_optimizer(
            bins
        )

    elif page == "Alerts":

        show_alerts(
            bins
        )


# ============================================================
# START
# ============================================================

if __name__ == "__main__":

    main()