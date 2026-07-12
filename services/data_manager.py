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

    satellites = load.tle_file("data/active_satellites_TLE_data.tle")

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


