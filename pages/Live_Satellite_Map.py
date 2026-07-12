import streamlit as st
from services import asset_utils, satellite_locator, map_renderer
from services import data_manager as dm
from streamlit_autorefresh import st_autorefresh


# -------------------------------------------------------------------------------------------------------
# Page Configuration
# -------------------------------------------------------------------------------------------------------

st.set_page_config(
    page_title="OrbitWatch",
    page_icon="🛰",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st_autorefresh(interval=10000, limit=None, key="live_map_refresh")

# --------------------------------------------------------------------------------------------------------
# Session State
# --------------------------------------------------------------------------------------------------------

if "selected_norad" not in st.session_state:
    st.session_state.selected_norad = None

if "locations" not in st.session_state:
    st.session_state.locations = []

# ---------------------------------------------------------------------------------------------------------
# Background
# ---------------------------------------------------------------------------------------------------------

asset_utils.set_background("assets/earth_background.jpg")

# ----------------------------------------------------------------------------------------------------------
# Title
# ----------------------------------------------------------------------------------------------------------

st.markdown(
    """
    <h1 style='text-align:center; color:white;'>
        🗺️ Live Satellite Map
    </h1>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <h5 style='text-align:center; color:#BFC9D9;'>
        Select a satellite below to view its location and details.
    </h5>
    """,
    unsafe_allow_html=True,
)

# ------------------------------------------------------------------------------------------------------------
# Load Data
# ------------------------------------------------------------------------------------------------------------
all_df = dm.load_all_dataframe()
df = dm.load_dataframe(all_df)


# Get live locations of all satellites
locations = satellite_locator.locate_all_satellites(df)


# Save in session state
st.session_state.locations = locations

# -------------------------------------------------------------------------------------------------------------
# World Map
# --------------------------------------------------------------------------------------------------------------
map_renderer.live_map(df)




# =============================================================================================================
# LEFT PANEL
# ==============================================================================================================
left, right = st.columns(2)
with left:

    st.subheader("🛰 Indian Satellites")

    search = st.text_input(
        "Search Satellite",
        placeholder="Search by satellite name..."
    )

    if search:
        df = df[
            df["Satellite Name"]
            .str.contains(search, case=False, na=False)
        ]

    # Header
    h1, h2, h3, h4, h5 = st.columns([9,9,9,9,9])

    h1.markdown("**Satellite**")
    h2.markdown("**Operating Country**")
    h3.markdown("**Operating Organization**")
    h4.markdown("**Mission**")
    h5.markdown("**Action**")

    st.divider()

    with st.container(height=450):

        for _, row in df.iterrows():

            c1, c2, c3, c4, c5 = st.columns([9,9,9,9,9])

            c1.write(row["Satellite Name"])
            c2.write(row["Operating Country"])
            c3.write(row["Operating Organization"])
            c4.write(row["Mission Type"])

            if c5.button(
                "🔍 Explore",
                key=f"explore_{row['NORAD ID']}"
            ):

                st.session_state.selected_norad = row["NORAD ID"]

                st.rerun()

# ==================================================
# RIGHT PANEL
# ==================================================

with right:

    with st.container(border=True):

        st.subheader("🛰 Satellite Details")

        if st.session_state.selected_norad is None:

            st.info(
                "Select a satellite from the left to display its information."
            )

        else:

            satellite = df[
                df["NORAD ID"] == st.session_state.selected_norad
            ].iloc[0]

            st.markdown(f"### {satellite['Satellite Name']}")
            st.write(f"**NORAD ID:** {satellite['NORAD ID']}")
            st.write(f"**Operating Country:** {satellite['Operating Country']}")
            st.write(f"**Operating Organization:** {satellite['Operating Organization']}")
            st.write(f"**Mission Type:** {satellite['Mission Type']}")
            st.write(f"**Orbit Type:** {satellite['Orbit Type']}")
            st.write(f"**Launch Date:** {satellite['Launch Date']}")
            st.write(f"**Remarks:** {satellite['Remarks']}")

            st.divider()

            selected_location = next(
                (
                    sat for sat in st.session_state.locations
                    if sat["NORAD ID"] == st.session_state.selected_norad
                ),
                None
                )

            if selected_location is not None:

                st.write(f"**Latitude:** {selected_location['latitude']:.4f}°")

                st.write(f"**Longitude:** {selected_location['longitude']:.4f}°")

                st.write(f"**Altitude:** {selected_location['altitude']:.2f} km")

                st.divider()

                st.write("Want to predict it orbit for next few hours ?")
                
                if st.button("Predict orbit"):
                    st.switch_page("pages/Orbit_Predictor.py")

            else:

                st.warning("Unable to determine the satellite location.")
st.subheader("Important note")
st.info("""
    The page refreshes every few seconds once for more precise information.

    Some satellites are unable to track although they are active.

    The satellites which are not moving are **Geo Stationary Satellites**.
""")