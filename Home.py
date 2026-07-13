from datetime import datetime, timezone
import streamlit as st
from services import asset_utils
from services import data_manager as dm
from services import TLE_utils

# -----------------------------------------
# Start background TLE auto-updater
# (runs once per app process, refreshes every 4 hours)
# -----------------------------------------
TLE_utils.start_tle_scheduler()

# -----------------------------------------
# Page Configuration
# -----------------------------------------
st.set_page_config(
    page_title="OrbitWatch",
    page_icon="🛰",
    layout="wide",
    initial_sidebar_state="collapsed"
)
st.markdown("""
<style>
/* Hide the sidebar completely */
[data-testid="stSidebar"] {
    display: none;
}

/* Hide the sidebar toggle button (arrow/hamburger) */
[data-testid="stSidebarCollapsedControl"] {
    display: none;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------------------
# Background
# -----------------------------------------
asset_utils.set_background("assets/earth_background.jpg")

# -----------------------------------------
# initialize Dataset
# -----------------------------------------

all_df = dm.load_all_dataframe()
df = dm.load_dataframe(all_df)




# -----------------------------------------
# Calculations
# -----------------------------------------
#total_countries = all_df["Operating Country"].nunique()
total_satellites = len(all_df)

mission_types = all_df["Mission Type"].nunique()

recent_launch  = all_df.iloc[-1, 1]

recent_launch_date = all_df.iloc[-1,2]

status = all_df.iloc[-1,4]

# ------------------------------------------------------------------------------------------------------------
# Hero Section
# -------------------------------------------------------------------------------------------------------------
st.markdown(
    """
    <h1 style='text-align:center; color:white;'>
        🛰 OrbitWatch
    </h1>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <h4 style='text-align:center; color:#BFC9D9;'>
        Indian Satellite Space Situational Awareness Platform
    </h4>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div style="
        text-align:center;
        max-width:950px;
        margin:auto;
        font-size:18px;
        color:#E5E7EB;
        line-height:1.8;
    ">
        OrbitWatch is a <b>Space Situational Awareness (SSA)</b> platform
        that monitors Indian satellites using real-time orbital data.
        It provides live satellite tracking, mission insights, orbit analytics,
        and fleet information through an interactive dashboard, helping users
        better understand India's active space infrastructure.
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("<br>", unsafe_allow_html=True)
st.divider()

# --------------------------------------------------------------------------------------------------------------
# KPI Cards
# --------------------------------------------------------------------------------------------------------------
left, c1, c2, c3, right = st.columns([2, 2, 2, 2, 1])

with c1:
    st.metric(
        "Total Satellites",
        f"{total_satellites:,}"
    )

with c2:
    st.metric(
        "Mission Types",
        f"{mission_types:,}"
    )

with c3:
    st.metric(
        "Recent Launch",
        f"{recent_launch}"
    )
    st.metric(
        "Date of Launch",
        f"{recent_launch_date}"
    )
    st.metric(
        "Status",
        f"{status}"
    )

st.markdown("<br>", unsafe_allow_html=True)

# -------------------------------------------------------------------------------------------------------------
# Fleet Overview
# -------------------------------------------------------------------------------------------------------------
st.subheader("Fleet Overview")

st.info(
    f"""
OrbitWatch is currently tracking **{total_satellites} Indian satellites including active and inactive and**
covering **{mission_types} mission categories**.

The platform provides live monitoring, orbit analytics, mission insights,
and future orbit prediction to improve awareness of India's space assets.
"""
)

st.subheader("NOTE")

tle_status = TLE_utils.get_last_update_status()

if tle_status is None:
    st.warning(
        "🟡 TLE update status is not available yet — the auto-updater "
        "hasn't completed its first run. This usually resolves within a "
        "few seconds of the app starting."
    )
else:
    last_updated = datetime.fromisoformat(tle_status["timestamp"])
    minutes_ago = int((datetime.now(timezone.utc) - last_updated).total_seconds() // 60)

    if minutes_ago < 60:
        ago_text = f"{minutes_ago} minute{'s' if minutes_ago != 1 else ''} ago"
    else:
        hours_ago = minutes_ago // 60
        ago_text = f"{hours_ago} hour{'s' if hours_ago != 1 else ''} ago"

    if tle_status["success"]:
        st.success(
            f"""
🟢 **TLE data is up to date** — last refreshed **{ago_text}** ({last_updated.strftime('%Y-%m-%d %H:%M:%S')} UTC).

The data auto-refreshes every {TLE_utils.UPDATE_INTERVAL_HOURS} hours. These satellite details are approximated using orbital calculations and should be used for educational purposes only.
"""
        )
    else:
        st.error(
            f"""
🔴 **The last TLE update attempt failed** 

OrbitWatch is still showing the most recently downloaded TLE data .
"""
        )

st.divider()

#-------------------------------------------------------------------------------------------------------------
#Features
#-------------------------------------------------------------------------------------------------------------

st.markdown(
    """
    <h2 style="text-align:center;">
        Features
    </h2>
    """,
    unsafe_allow_html=True
)

with st.container(border=True):

    st.markdown("""
        <h4 style="text-align:center;">🗺️ Live Satellite Map</h4>
        <p style="text-align:center;">
            Monitor the live positions of Indian satellites on an interactive world map.
        </p>
    """, unsafe_allow_html=True)

    _, c, _ = st.columns([1,2,1])

    with c:
        if st.button(
            "Explore",
            width="stretch",
            key="Live Satellite Map"
        ):
            st.switch_page("pages/Live_Satellite_Map.py")


with st.container(border=True):

    st.markdown("""
        <h4 style="text-align:center;">🔮 Orbit Predictor</h4>
        <p style="text-align:center;">
            Get future predictions of the Indian satellite
        </p>
    """, unsafe_allow_html=True)

    _, c, _ = st.columns([1,2,1])

    with c:
        if st.button(
            "Explore",
            width="stretch",
            key="Orbit Predictor"
        ):
            st.switch_page("pages/Orbit_Predictor.py")


with st.container(border=True):

    st.markdown("""
        <h4 style="text-align:center;">📊 Analytics</h4>
        <p style="text-align:center;">
            Visualize trends, missions, and orbital distributions.
        </p>
    """, unsafe_allow_html=True)

    _, c, _ = st.columns([1,2,1])

    with c:
        if st.button(
            "Explore",
            width="stretch",
            key="Analytics"
        ):
            st.switch_page("pages/Analytics.py")

st.divider()


#---------------------------------------------------------------------------------------------------------
#footer
#---------------------------------------------------------------------------------------------------------

st.markdown(
    """
    <div style="
        text-align:center;
        color:#B0BEC5;
        font-size:15px;
        padding-top:20px;
        padding-bottom:10px;
    ">

    <h4 style="color:white;">🛰 OrbitWatch</h4>

    <p>
    Empowering Space Situational Awareness through real-time satellite tracking
    and orbital analytics.
    </p>
    <h4 style="color:white;">Acknowledgements</h4>

    <p>
    Orbital (TLE) data provided by <b>CelesTrak</b>.<br>
    Satellite propagation powered by <b>Skyfield</b>.<br>
    Satellite metadata compiled from publicly available ISRO and related sources.
    </p>
    <p>
    © 2026 <b>OrbitWatch India</b> | Built by <b>Shaukat Muchukota</b>
    </p>

    <p>
    <a href="https://github.com/Shaukat2896/OrbitWatch-India---Indian-Satellite-Space-Situational-Awareness-Platform" target="_blank">GitHub</a>
    &nbsp;&nbsp;|&nbsp;&nbsp;
    <a href="https://linkedin.com/in/shaukat-muchukota-024048322" target="_blank">LinkedIn</a>
    &nbsp;&nbsp;|&nbsp;&nbsp;
    <a href="mailto:shaukat2896@gmail.com">Email</a>
    </p>

    <p style="font-size:13px;">
    Version 1.0
    </p>

    </div>
    """,
    unsafe_allow_html=True,
)

