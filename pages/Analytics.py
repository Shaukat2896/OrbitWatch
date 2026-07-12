import streamlit as st
import pandas as pd
import plotly.express as px

from services import asset_utils, satellite_locator
from services import data_manager as dm

# -----------------------------------------------------------------------
# Page Configuration
# -----------------------------------------------------------------------
st.set_page_config(
    page_title="OrbitWatch",
    page_icon="🛰",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# -----------------------------------------------------------------------
# Background
# -----------------------------------------------------------------------
asset_utils.set_background("assets/earth_background.jpg")

# -----------------------------------------------------------------------
# Plotly dark / transparent theme so charts blend with the app
# -----------------------------------------------------------------------
CHART_LAYOUT = dict(
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#E5E7EB"),
    margin=dict(l=10, r=10, t=50, b=10),
)

COLOR_SEQUENCE = px.colors.sequential.Teal + px.colors.sequential.Blues


def style_fig(fig):
    fig.update_layout(**CHART_LAYOUT)
    return fig


# -----------------------------------------------------------------------
# Title
# -----------------------------------------------------------------------
st.markdown(
    """
    <h1 style='text-align:center; color:white;'>📊 Analytics</h1>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <h5 style='text-align:center; color:#BFC9D9;'>
        Insights and trends across India's satellite fleet
    </h5>
    """,
    unsafe_allow_html=True,
)

st.markdown("<br>", unsafe_allow_html=True)

# -----------------------------------------------------------------------
# Load & clean data
# -----------------------------------------------------------------------
all_df = dm.load_all_dataframe()

df = all_df.copy()

df["Status"] = df["Status"].str.strip().str.title()

df["Launch Year"] = pd.to_datetime(
    df["Launch Date"], format="%d-%m-%Y", errors="coerce"
).dt.year

# Primary mission category (strip parenthetical sub-types, e.g.
# "Earth Observation (Radar Imaging)" -> "Earth Observation")
df["Mission Category"] = (
    df["Mission Type"]
    .str.split(" (", n=1, expand=False, regex=False)
    .str[0]
)

# Operational, trackable subset (same rules used across the app)
operational_df = dm.load_dataframe(all_df)
trackable_df = operational_df[operational_df["NORAD ID"].notna()]

# -----------------------------------------------------------------------
# KPI Cards
# -----------------------------------------------------------------------
total_satellites = len(df)
active_count = int((df["Status"] == "Operational").sum())
inactive_count = total_satellites - active_count
mission_types = df["Mission Category"].nunique()
orbit_types = df["Orbit Type"].nunique()

k1, k2, k3, k4, k5 = st.columns(5)

k1.metric("Total Satellites", f"{total_satellites:,}")
k2.metric("Active", f"{active_count:,}")
k3.metric("Inactive", f"{inactive_count:,}")
k4.metric("Mission Categories", f"{mission_types:,}")
k5.metric("Orbit Types", f"{orbit_types:,}")

st.divider()

# -----------------------------------------------------------------------
# Row 1: Status split + Orbit Type split
# -----------------------------------------------------------------------
c1, c2 = st.columns(2)

with c1:
    st.subheader("Operational Status")

    status_counts = df["Status"].value_counts().reset_index()
    status_counts.columns = ["Status", "Count"]

    fig_status = px.pie(
        status_counts,
        names="Status",
        values="Count",
        hole=0.5,
        color_discrete_sequence=["#2ED573", "#FF6B6B"]
    )
    fig_status.update_traces(textinfo="percent+label")
    st.plotly_chart(style_fig(fig_status), width="stretch")

with c2:
    st.subheader("Orbit Type Distribution")

    orbit_counts = df["Orbit Type"].value_counts().reset_index()
    orbit_counts.columns = ["Orbit Type", "Count"]

    fig_orbit = px.pie(
        orbit_counts,
        names="Orbit Type",
        values="Count",
        hole=0.5,
        color_discrete_sequence=COLOR_SEQUENCE
    )
    fig_orbit.update_traces(textinfo="percent")
    st.plotly_chart(style_fig(fig_orbit), width="stretch")

st.divider()

# -----------------------------------------------------------------------
# Row 2: Mission type distribution
# -----------------------------------------------------------------------
st.subheader("Mission Type Distribution")

mission_counts = (
    df["Mission Category"]
    .value_counts()
    .reset_index()
)
mission_counts.columns = ["Mission Category", "Count"]

fig_mission = px.bar(
    mission_counts,
    x="Count",
    y="Mission Category",
    orientation="h",
    color="Count",
    color_continuous_scale="Teal",
    text="Count"
)
fig_mission.update_layout(yaxis=dict(categoryorder="total ascending"))
fig_mission.update_traces(textposition="outside")
st.plotly_chart(style_fig(fig_mission), width="stretch")

st.divider()

# -----------------------------------------------------------------------
# Row 3: Launch timeline
# -----------------------------------------------------------------------
st.subheader("Satellites Launched Per Year")

launches_per_year = (
    df.dropna(subset=["Launch Year"])
    .groupby("Launch Year")
    .size()
    .reset_index(name="Count")
)
launches_per_year["Launch Year"] = launches_per_year["Launch Year"].astype(int)

fig_timeline = px.bar(
    launches_per_year,
    x="Launch Year",
    y="Count",
    color="Count",
    color_continuous_scale="Blues"
)
fig_timeline.update_layout(bargap=0.15)
st.plotly_chart(style_fig(fig_timeline), width="stretch")

st.divider()

# -----------------------------------------------------------------------
# Row 4: Mission type vs status (stacked)
# -----------------------------------------------------------------------
st.subheader("Mission Category vs Operational Status")

mission_status = (
    df.groupby(["Mission Category", "Status"])
    .size()
    .reset_index(name="Count")
)

fig_mission_status = px.bar(
    mission_status,
    x="Count",
    y="Mission Category",
    color="Status",
    orientation="h",
    barmode="stack",
    color_discrete_map={"Operational": "#2ED573", "Not Operational": "#FF6B6B"}
)
fig_mission_status.update_layout(
    yaxis=dict(categoryorder="total ascending")
)
st.plotly_chart(style_fig(fig_mission_status), width="stretch")

st.divider()

# -----------------------------------------------------------------------
# Row 5: Operating organization
# -----------------------------------------------------------------------
st.subheader("Top Operating Organizations")

org_counts = df["Operating Organization"].value_counts().head(8).reset_index()
org_counts.columns = ["Operating Organization", "Count"]

fig_org = px.bar(
    org_counts,
    x="Count",
    y="Operating Organization",
    orientation="h",
    color="Count",
    color_continuous_scale="Purples",
    text="Count"
)
fig_org.update_layout(yaxis=dict(categoryorder="total ascending"))
fig_org.update_traces(textposition="outside")
st.plotly_chart(style_fig(fig_org), width="stretch")

st.divider()

# -----------------------------------------------------------------------
# Row 6: Live orbital altitude insights (operational + trackable only)
# -----------------------------------------------------------------------
st.subheader("Live Orbital Altitude Insights")

st.caption(
    "Computed in real time from current TLE data for operational, "
    "trackable satellites only."
)

if len(trackable_df) == 0:
    st.warning("No trackable operational satellites available to compute altitude insights.")
else:
    with st.spinner("Calculating live altitudes..."):
        locations = satellite_locator.locate_all_satellites(trackable_df)

    if len(locations) == 0:
        st.warning("Unable to determine live positions for any satellite right now.")
    else:
        alt_df = pd.DataFrame(locations)

        a1, a2, a3 = st.columns(3)
        a1.metric("Average Altitude", f"{alt_df['altitude'].mean():,.0f} km")
        a2.metric("Lowest Altitude", f"{alt_df['altitude'].min():,.0f} km")
        a3.metric("Highest Altitude", f"{alt_df['altitude'].max():,.0f} km")

        fig_alt = px.histogram(
            alt_df,
            x="altitude",
            nbins=25,
            labels={"altitude": "Altitude (km)"},
            color_discrete_sequence=["#38BDF8"]
        )
        fig_alt.update_layout(bargap=0.1)
        st.plotly_chart(style_fig(fig_alt), width="stretch")

st.divider()

# -----------------------------------------------------------------------
# Note
# -----------------------------------------------------------------------
st.info(
    """
These analytics are computed from the OrbitWatch satellite dataset and,
where noted, from live TLE-derived orbital positions. Figures are
approximate and intended for educational purposes only.
"""
)
