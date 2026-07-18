import streamlit as st

from services import asset_utils, map_renderer, satellite_locator
from services import data_manager as dm
from streamlit_autorefresh import st_autorefresh

# -----------------------------------------------------------------------
# Page Configuration
# -----------------------------------------------------------------------
st.set_page_config(
    page_title="OrbitWatch",
    page_icon="🛰",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st_autorefresh(interval=10000, limit=None, key="live_map_refresh")

# -----------------------------------------------------------------------
# Session State
# -----------------------------------------------------------------------
if "prediction_result" not in st.session_state:
    st.session_state.prediction_result = None

if "prediction_satellite" not in st.session_state:
    st.session_state.prediction_satellite = None

# -----------------------------------------------------------------------
# Background
# -----------------------------------------------------------------------
asset_utils.set_background("assets/earth_background.jpg")

# -----------------------------------------------------------------------
# Title
# -----------------------------------------------------------------------
st.markdown(
    """
    <h1 style='text-align:center; color:white;'>Orbit Predictor</h1>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <h5 style='text-align:center; color:#BFC9D9;'>
        Select a satellite and a time ahead to predict its future position.
    </h5>
    """,
    unsafe_allow_html=True,
)

st.markdown("<br>", unsafe_allow_html=True)

# -----------------------------------------------------------------------
# Load Data
# -----------------------------------------------------------------------
all_df = dm.load_all_dataframe()
df = dm.load_dataframe(all_df)
df = df[df["NORAD ID"].notna()].reset_index(drop=True)

# -----------------------------------------------------------------------
# Controls + Map layout
# -----------------------------------------------------------------------
controls_col, map_col = st.columns([1, 2])

with controls_col:

    with st.container(border=True):

        st.subheader("🛰 Prediction Settings")

        if len(df) == 0:
            st.warning("No trackable satellites are available right now.")
            satellite_name = None
        else:
            satellite_name = st.selectbox(
                "Select Satellite",
                options=df["Satellite Name"].tolist()
            )

        hours_ahead = st.number_input(
            "Predict position after (hours)",
            min_value=0.1,
            max_value=168.0,
            value=1.0,
            step=0.5,
            help="How many hours into the future to predict the satellite's position (up to 7 days)."
        )

        predict_clicked = st.button(
            "Predict Position",
            width="stretch",
            disabled=(satellite_name is None)
        )

        if predict_clicked and satellite_name is not None:

            selected_row = df[df["Satellite Name"] == satellite_name].iloc[0]
            norad_id = selected_row["NORAD ID"]

            with st.spinner("Propagating orbit..."):
                result = satellite_locator.predict_satellite_position(norad_id, hours_ahead)

            if result is None:
                st.session_state.prediction_result = None
                st.error("Unable to predict this satellite's position. TLE data may be unavailable.")
            else:
                st.session_state.prediction_result = result
                st.session_state.prediction_satellite = {
                    "name": satellite_name,
                    "norad_id": norad_id,
                    "hours_ahead": hours_ahead
                }

        st.divider()

        result = st.session_state.prediction_result
        info = st.session_state.prediction_satellite

        if result is not None and info is not None:

            st.markdown(f"**Satellite:** {info['name']}")
            st.markdown(f"**NORAD ID:** {int(info['norad_id'])}")

            st.markdown("##### 🟢 Current Position")
            st.write(f"Latitude: {result['current']['latitude']:.4f}°")
            st.write(f"Longitude: {result['current']['longitude']:.4f}°")
            st.write(f"Altitude: {result['current']['altitude']:.2f} km")
            st.caption(f"As of {result['current_time'].strftime('%Y-%m-%d %H:%M:%S')} UTC")

            st.markdown(f"##### 🔴 Predicted Position (+{info['hours_ahead']}h)")
            st.write(f"Latitude: {result['future']['latitude']:.4f}°")
            st.write(f"Longitude: {result['future']['longitude']:.4f}°")
            st.write(f"Altitude: {result['future']['altitude']:.2f} km")
            st.caption(f"As of {result['future_time'].strftime('%Y-%m-%d %H:%M:%S')} UTC")

        else:
            st.info("Select a satellite and a time, then click **Predict Position**.")

with map_col:

    result = st.session_state.prediction_result

    if result is not None:
        image = map_renderer.draw_prediction_map(
            "assets/World_Map.jpg",
            current=result["current"],
            future=result["future"],
            track=result["track"]
        )
    else:
        # Empty world map before any prediction has been made
        image = map_renderer.draw_prediction_map("assets/World_Map.jpg")

    st.image(image, width="stretch")

    legend_l, legend_c, legend_r = st.columns(3)
    legend_l.markdown("🟢 **Current Position**")
    legend_c.markdown("🔷 **Ground Track**")
    legend_r.markdown("🔴 **Predicted Position**")

st.divider()

st.subheader("Important note")
st.info(
    """
    Predictions are computed using SGP4/Skyfield orbital propagation based
    on the latest available TLE data. Accuracy decreases the further into
    the future the prediction extends, and results should be used for
    educational purposes only, not for operational or mission-critical
    decisions.

    Some satellites are unable to track, because their information may not be available publicly.

    Some satellites are not moving, because they are Geo Stationary Satellites.

    """
)
