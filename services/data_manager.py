import pandas as pd
import streamlit as st
from skyfield.api import load
from datetime import datetime
import os


# -----------------------------
# CSV
# -----------------------------

@st.cache_data
def load_dataframe(df):
    filtered_df = df[(df["Status"] == "Operational") &
    (~df["Mission Type"].str.contains("Space Science", case=False, na=False)) &
    (df["NORAD ID"].astype(str).str.strip().str.upper() != "N/A")]
    return filtered_df

@st.cache_data
def load_all_dataframe():
    return pd.read_csv("data/All_Satellites.csv")

@st.cache_data
def load_dataframe_for_live_map(df):
    filtered_df = df[[
    "Satellite Name",
    "NORAD ID",
    "Operating Country",
    "Operating Organization",
    "Mission Type"
    ]]
    return filtered_df

# -----------------------------
# TLE Dictionary
# -----------------------------

@st.cache_resource
def load_tle_dictionary():

    satellites = load.tle_file("data/objects_orbiting_data.tle")

    return {
        sat.model.satnum: sat
        for sat in satellites
    }


# -----------------------------
# Timescale
# -----------------------------

@st.cache_resource
def load_timescale():
    return load.timescale()


# -----------------------------
# Refresh Cache
# -----------------------------

def refresh():

    load_tle_dictionary.clear()

    load_dataframe.clear()

    load_dataframe_for_live_map.clear()


# for collision

import numpy as np

MU = 398600.4418
EARTH_RADIUS = 6378.137


def extract_parameters(satellite):

    # NORAD
    norad = satellite.model.satnum

    # Inclination
    inclination = np.degrees(
        satellite.model.inclo
    )

    # Mean Motion
    n = satellite.model.no_kozai / 60

    # Semi-major Axis
    semi_major = (MU / (n*n)) ** (1/3)

    # Altitude
    altitude = semi_major - EARTH_RADIUS

    # Orbit Regime
    if altitude < 2000:
        regime = "LEO"

    elif altitude < 35786:
        regime = "MEO"

    elif abs(altitude-35786) < 500:
        regime = "GEO"

    else:
        regime = "HEO"

    return {

        "norad": norad,

        "inclination": inclination,

        "altitude": altitude,

        "orbit": regime

    }

