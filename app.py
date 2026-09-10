import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="SmartBin AI",
    page_icon="🗑️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# DATA
# ============================================================

bins = pd.DataFrame([
    {
        "Bin ID": "BIN-001",
        "Location": "Area 1",
        "Fill Level": 35,
        "Status": "Normal",
        "Latitude": 13.0827,
        "Longitude": 80.2707
    },
    {
        "Bin ID": "BIN-002",
        "Location": "Area 2",
        "Fill Level": 78,
        "Status": "Warning",
        "Latitude": 13.0838,
        "Longitude": 80.2720
    },
    {
        "Bin ID": "BIN-003",
        "Location": "Area 3",
        "Fill Level": 94,
        "Status": "Critical",
        "Latitude": 13.0819,
        "Longitude": 80.2740
    },
    {
        "Bin ID": "BIN-004",
        "Location": "Area 4",
        "Fill Level": 52,
        "Status": "Normal",
        "Latitude": 13.0848,
        "Longitude": 80.2690
    },
    {
        "Bin ID": "BIN-005",
        "Location": "Area 5",
        "Fill Level": 88,
        "Status": "Warning",
        "Latitude": 13.0805,
        "Longitude": 80.2680
    }
])

# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    /* ------------------------------
       GLOBAL
    ------------------------------ */

    .stApp {
        background:
            radial-gradient(
                circle at 80% 5%,
                rgba(255, 0, 60, 0.055),
                transparent 25%
            ),
            radial-gradient(
                circle at 15% 35%,
                rgba(255, 190, 0, 0.035),
                transparent 25%
            ),
            #050607;
        color: #f4f4f5;
    }

    .main {
        background: #050607;
    }

    [data-testid="stAppViewContainer"] {
        background: #050607;
    }

    [data-testid="stHeader"] {
        background: rgba(0,0,0,0.78);
    }


    /* ------------------------------
       SIDEBAR
    ------------------------------ */

    section[data-testid="stSidebar"] {
        background:
            linear-gradient(
                180deg,
                #090b0c 0%,
                #070809 55%,
                #050607 100%
            );

        border-right: 1px solid rgba(255,255,255,0.08);
    }

    section[data-testid="stSidebar"] > div {
        padding-top: 25px;
    }

    .brand {
        padding: 8px 4px 28px 4px;
    }

    .brand-title {
        font-size: 26px;
        font-weight: 800;
        letter-spacing: -0.8px;
        color: #ffffff;
    }

    .brand-subtitle {
        margin-top: 5px;
        color: #777d83;
        font-size: 13px;
    }


    /* ------------------------------
       SIDEBAR BUTTONS
    ------------------------------ */

    section[data-testid="stSidebar"] .stButton > button {
        width: 100%;
        border: 1px solid transparent;
        border-radius: 12px;
        background: transparent;
        color: #9ba1a8;
        text-align: left;
        padding: 12px 15px;
        margin: 3px 0;
        transition: all 0.2s ease;
    }

    section[data-testid="stSidebar"] .stButton > button:hover {
        background: rgba(255,255,255,0.055);
        border-color: rgba(255,255,255,0.08);
        color: #ffffff;
        transform: translateX(3px);
    }


    /* ------------------------------
       MAIN TITLES
    ------------------------------ */

    .hero-title {
        font-size: 48px;
        font-weight: 850;
        letter-spacing: -2px;
        margin-bottom: 4px;
        color: #ffffff;
    }

    .hero-subtitle {
        font-size: 16px;
        color: #858b91;
        margin-bottom: 35px;
    }

    .section-title {
        font-size: 28px;
        font-weight: 800;
        letter-spacing: -0.8px;
        color: #ffffff;
        margin-top: 18px;
        margin-bottom: 4px;
    }

    .section-subtitle {
        color: #777d83;
        font-size: 14px;
        margin-bottom: 18px;
    }


    /* ------------------------------
       CARDS
    ------------------------------ */

    div[data-testid="stVerticalBlockBorderWrapper"] {
        background:
            linear-gradient(
                145deg,
                rgba(28,30,31,0.92),
                rgba(10,11,12,0.96)
            );

        border: 1px solid rgba(255,255,255,0.075);
        border-radius: 18px;
        box-shadow:
            0 12px 35px rgba(0,0,0,0.30),
            inset 0 1px 0 rgba(255,255,255,0.035);

        transition:
            transform 0.22s ease,
            border-color 0.22s ease,
            box-shadow 0.22s ease;
    }

    div[data-testid="stVerticalBlockBorderWrapper"]:hover {
        transform: translateY(-3px);
        border-color: rgba(255,255,255,0.15);
        box-shadow:
            0 18px 45px rgba(0,0,0,0.42),
            inset 0 1px 0 rgba(255,255,255,0.05);
    }


    /* ------------------------------
       METRICS
    ------------------------------ */

    [data-testid="stMetric"] {
        background:
            linear-gradient(
                145deg,
                #151718,
                #0b0c0d
            );

        border: 1px solid rgba(255,255,255,0.07);
        border-radius: 17px;
        padding: 20px 22px;
        box-shadow:
            0 10px 30px rgba(0,0,0,0.25);
    }

    [data-testid="stMetricLabel"] {
        color: #777d83 !important;
        font-size: 12px !important;
        font-weight: 700 !important;
        text-transform: uppercase;
        letter-spacing: 1.1px;
    }

    [data-testid="stMetricValue"] {
        color: #ffffff !important;
        font-weight: 800 !important;
    }


    /* ------------------------------
       BUTTONS
    ------------------------------ */

    .stButton > button {
        background: #111415;
        color: #e8e9ea;
        border: 1px solid rgba(255,255,255,0.10);
        border-radius: 11px;
        transition: all 0.2s ease;
    }

    .stButton > button:hover {
        background: #191c1d;
        border-color: rgba(255,255,255,0.24);
        color: white;
        transform: translateY(-2px);
    }


    /* ------------------------------
       DATAFRAME
    ------------------------------ */

    [data-testid="stDataFrame"] {
        border-radius: 15px;
        overflow: hidden;
    }


    /* ------------------------------
       DIVIDER
    ------------------------------ */

    hr {
        border-color: rgba(255,255,255,0.07);
        margin: 35px 0;
    }


    /* ------------------------------
       ALERT CARDS
    ------------------------------ */

    .alert-normal {
        border-left: 4px solid #20e070;
        background:
            linear-gradient(
                90deg,
                rgba(32,224,112,0.10),
                rgba(32,224,112,0.025)
            );
        padding: 17px 20px;
        border-radius: 12px;
        margin-bottom: 12px;
    }

    .alert-warning {
        border-left: 4px solid #ffd21f;
        background:
            linear-gradient(
                90deg,
                rgba(255,210,31,0.12),
                rgba(255,210,31,0.025)
            );
        padding: 17px 20px;
        border-radius: 12px;
        margin-bottom: 12px;
    }

    .alert-critical {
        border-left: 4px solid #ff304f;
        background:
            linear-gradient(
                90deg,
                rgba(255,48,79,0.15),
                rgba(255,48,79,0.025)
            );
        padding: 17px 20px;
        border-radius: 12px;
        margin-bottom: 12px;
    }

    .alert-title {
        font-weight: 750;
        color: #ffffff;
        font-size: 15px;
    }

    .alert-description {
        color: #92979d;
        font-size: 13px;
        margin-top: 4px;
    }


    /* ------------------------------
       STATUS DOTS
    ------------------------------ */

    .green-dot {
        color: #20e070;
        font-size: 20px;
    }

    .yellow-dot {
        color: #ffd21f;
        font-size: 20px;
    }

    .red-dot {
        color: #ff304f;
        font-size: 20px;
    }


    /* ------------------------------
       SMALL LABELS
    ------------------------------ */

    .eyebrow {
        color: #737a80;
        font-size: 11px;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 1.5px;
    }

    .big-number {
        color: #ffffff;
        font-size: 38px;
        font-weight: 850;
        line-height: 1.1;
    }

    .muted {
        color: #72787e;
        font-size: 13px;
    }


    /* ------------------------------
       LIVE PILL
    ------------------------------ */

    .live-pill {
        display: inline-block;
        padding: 7px 12px;
        border-radius: 999px;
        border: 1px solid rgba(32,224,112,0.25);
        background: rgba(32,224,112,0.07);
        color: #20e070;
        font-size: 12px;
        font-weight: 700;
    }


    /* ------------------------------
       SCROLLBAR
    ------------------------------ */

    ::-webkit-scrollbar {
        width: 7px;
    }

    ::-webkit-scrollbar-track {
        background: #050607;
    }

    ::-webkit-scrollbar-thumb {
        background: #272a2c;
        border-radius: 10px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: #3b3f42;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# SESSION STATE
# ============================================================

if "page" not in st.session_state:
    st.session_state.page = "Bin Monitoring"

if "selected_bin" not in st.session_state:
    st.session_state.selected_bin = "BIN-003"


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        """
        <div class="brand">
            <div class="brand-title">🗑️ SmartBin AI</div>
            <div class="brand-subtitle">Intelligent waste management</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    if st.button("◉  Bin Monitoring", use_container_width=True):
        st.session_state.page = "Bin Monitoring"

    if st.button("⌖  Live Map", use_container_width=True):
        st.session_state.page = "Live Map"

    if st.button("✦  AI Priority", use_container_width=True):
        st.session_state.page = "AI Priority"

    if st.button("⚠  Alerts", use_container_width=True):
        st.session_state.page = "Alerts"

    st.divider()

    st.markdown("**SYSTEM STATUS**")

    st.markdown(
        '<span class="green-dot">●</span> Sensors connected',
        unsafe_allow_html=True
    )

    st.markdown(
        '<span class="green-dot">●</span> Data pipeline active',
        unsafe_allow_html=True
    )

    st.markdown(
        '<span class="green-dot">●</span> AI engine ready',
        unsafe_allow_html=True
    )

    st.divider()

    st.caption("SmartBin AI • Real-time monitoring")


# ============================================================
# TOP HEADER
# ============================================================

st.markdown(
    '<div class="hero-title">SmartBin AI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="hero-subtitle">'
    'Intelligent monitoring, AI-powered collection priority, '
    'and optimized waste collection.'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<span class="live-pill">● LIVE SYSTEM &nbsp; | &nbsp; DATA MONITORING ACTIVE</span>',
    unsafe_allow_html=True
)

st.write("")


# ============================================================
# OVERVIEW
# ============================================================

total_bins = len(bins)
high_fill = len(bins[bins["Fill Level"] >= 80])
warnings = len(bins[bins["Status"] == "Warning"])
critical = len(bins[bins["Status"] == "Critical"])

st.markdown(
    '<div class="section-title">Overview</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-subtitle">'
    'Current status of all monitored smart bins'
    '</div>',
    unsafe_allow_html=True
)

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric("Total Bins", total_bins)

with c2:
    st.metric("High Fill", high_fill)

with c3:
    st.metric("Warnings", warnings)

with c4:
    st.metric("Critical", critical)


# ============================================================
# BIN MONITORING
# ============================================================

if st.session_state.page == "Bin Monitoring":

    st.divider()

    st.markdown(
        '<div class="section-title">Bin Monitoring</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-subtitle">'
        'Real-time fill levels across monitored locations'
        '</div>',
        unsafe_allow_html=True
    )

    # Sort highest priority first
    display_bins = bins.sort_values(
        by="Fill Level",
        ascending=False
    )

    table = display_bins[
        ["Bin ID", "Location", "Fill Level", "Status"]
    ].copy()

    table["Fill Level"] = table["Fill Level"].astype(str) + "%"

    st.dataframe(
        table,
        use_container_width=True,
        hide_index=True
    )

    st.write("")

    # Individual bin cards
    for _, row in display_bins.iterrows():

        with st.container(border=True):

            left, middle, right = st.columns([2.2, 3, 1.5])

            with left:
                st.markdown(
                    f"### {row['Bin ID']}"
                )

                st.caption(row["Location"])

            with middle:

                st.progress(
                    min(row["Fill Level"] / 100, 1.0)
                )

                st.caption(
                    f"Fill level: {row['Fill Level']}%"
                )

            with right:

                if row["Status"] == "Critical":
                    st.error("🔴 CRITICAL")

                elif row["Status"] == "Warning":
                    st.warning("🟡 WARNING")

                else:
                    st.success("🟢 NORMAL")

                if st.button(
                    "View details",
                    key=f"details_{row['Bin ID']}"
                ):
                    st.session_state.selected_bin = row["Bin ID"]


    # Selected bin details
    st.divider()

    selected = bins[
        bins["Bin ID"] == st.session_state.selected_bin
    ].iloc[0]

    st.markdown(
        '<div class="section-title">Selected Bin</div>',
        unsafe_allow_html=True
    )

    detail1, detail2 = st.columns([1, 1.5])

    with detail1:

        with st.container(border=True):

            st.markdown(
                '<div class="eyebrow">SELECTED BIN</div>',
                unsafe_allow_html=True
            )

            st.markdown(
                f'<div class="big-number">{selected["Bin ID"]}</div>',
                unsafe_allow_html=True
            )

            st.write("")

            st.write(f"**Location:** {selected['Location']}")

            st.write(
                f"**Current fill:** {selected['Fill Level']}%"
            )

            if selected["Status"] == "Critical":
                st.error("Immediate collection required.")

            elif selected["Status"] == "Warning":
                st.warning("Collection should be planned soon.")

            else:
                st.success("Bin operating normally.")

    with detail2:

        st.markdown("### Fill Level Trend")

        trend_values = [
            max(selected["Fill Level"] - 66, 10),
            max(selected["Fill Level"] - 54, 20),
            max(selected["Fill Level"] - 42, 30),
            max(selected["Fill Level"] - 28, 40),
            max(selected["Fill Level"] - 15, 50),
            selected["Fill Level"]
        ]

        trend = pd.DataFrame(
            {
                "Fill Level": trend_values
            },
            index=[
                "08:00",
                "10:00",
                "12:00",
                "14:00",
                "16:00",
                "Now"
            ]
        )

        st.line_chart(
            trend,
            height=300
        )


# ============================================================
# LIVE MAP
# ============================================================

elif st.session_state.page == "Live Map":

    st.divider()

    st.markdown(
        '<div class="section-title">Live Map</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-subtitle">'
        'Click a marker to inspect a monitored bin'
        '</div>',
        unsafe_allow_html=True
    )

    center_lat = bins["Latitude"].mean()
    center_lon = bins["Longitude"].mean()

    smart_map = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=16,
        tiles="CartoDB dark_matter"
    )

    for _, row in bins.iterrows():

        if row["Status"] == "Critical":
            marker_color = "red"

        elif row["Status"] == "Warning":
            marker_color = "orange"

        else:
            marker_color = "green"

        popup_text = (
            f"<b>{row['Bin ID']}</b><br>"
            f"{row['Location']}<br>"
            f"Fill: {row['Fill Level']}%<br>"
            f"Status: {row['Status']}"
        )

        folium.Marker(
            location=[
                row["Latitude"],
                row["Longitude"]
            ],
            popup=popup_text,
            tooltip=f"{row['Bin ID']} • {row['Location']}",
            icon=folium.Icon(
                color=marker_color,
                icon="trash",
                prefix="fa"
            )
        ).add_to(smart_map)

    st_folium(
        smart_map,
        width=None,
        height=580,
        returned_objects=[]
    )


# ============================================================
# AI PRIORITY
# ============================================================

elif st.session_state.page == "AI Priority":

    st.divider()

    st.markdown(
        '<div class="section-title">AI Collection Priority</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-subtitle">'
        'Collection order generated from current fill levels'
        '</div>',
        unsafe_allow_html=True
    )

    priority = bins.sort_values(
        by="Fill Level",
        ascending=False
    ).reset_index(drop=True)

    priority["Priority"] = range(1, len(priority) + 1)

    for _, row in priority.iterrows():

        if row["Fill Level"] >= 90:
            level = "CRITICAL"
            icon = "🔴"
            explanation = "Immediate collection recommended."

        elif row["Fill Level"] >= 80:
            level = "HIGH"
            icon = "🟡"
            explanation = "Collection should be scheduled soon."

        elif row["Fill Level"] >= 60:
            level = "MEDIUM"
            icon = "🟡"
            explanation = "Continue monitoring."

        else:
            level = "LOW"
            icon = "🟢"
            explanation = "No immediate action required."

        with st.container(border=True):

            a, b, c = st.columns([0.7, 2.2, 2.5])

            with a:
                st.markdown(
                    f"### #{row['Priority']}"
                )

            with b:
                st.markdown(
                    f"**{row['Bin ID']} — {row['Location']}**"
                )

                st.progress(
                    min(row["Fill Level"] / 100, 1.0)
                )

                st.caption(
                    f"{row['Fill Level']}% full"
                )

            with c:

                st.markdown(
                    f"### {icon} {level}"
                )

                st.caption(explanation)


# ============================================================
# ALERTS
# ============================================================

elif st.session_state.page == "Alerts":

    st.divider()

    st.markdown(
        '<div class="section-title">Alerts</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-subtitle">'
        'Important collection and capacity notifications'
        '</div>',
        unsafe_allow_html=True
    )

    critical_bins = bins[
        bins["Status"] == "Critical"
    ]

    warning_bins = bins[
        bins["Status"] == "Warning"
    ]

    normal_bins = bins[
        bins["Status"] == "Normal"
    ]

    # Critical alerts
    for _, row in critical_bins.iterrows():

        st.markdown(
            f"""
            <div class="alert-critical">
                <div class="alert-title">
                    🔴 {row["Bin ID"]} at {row["Location"]} is {row["Fill Level"]}% full
                </div>
                <div class="alert-description">
                    Immediate collection recommended.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # Warning alerts
    for _, row in warning_bins.iterrows():

        st.markdown(
            f"""
            <div class="alert-warning">
                <div class="alert-title">
                    🟡 {row["Bin ID"]} at {row["Location"]} is {row["Fill Level"]}% full
                </div>
                <div class="alert-description">
                    Collection needed soon.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # Normal status
    for _, row in normal_bins.iterrows():

        st.markdown(
            f"""
            <div class="alert-normal">
                <div class="alert-title">
                    🟢 {row["Bin ID"]} at {row["Location"]} is operating normally
                </div>
                <div class="alert-description">
                    Current fill level: {row["Fill Level"]}%.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


# ============================================================
# FOOTER
# ============================================================

st.divider()

left, right = st.columns([3, 1])

with left:
    st.caption(
        "SmartBin AI • Intelligent waste management system"
    )

with right:
    st.caption(
        "● System online"
    )