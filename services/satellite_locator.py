from datetime import datetime, timedelta

from skyfield.api import wgs84
from services import data_manager as dm
import streamlit as st


def locate_satellite(norad_id):
    """
    Returns the current latitude and longitude of a satellite.

    Returns:
        {
            "latitude": float,
            "longitude": float,
            "altitude": float
        }
    """

    tle_dict = dm.load_tle_dictionary()
    ts = dm.load_timescale()

    satellite = tle_dict.get(norad_id)

    if satellite is None:
        return None

    t = ts.now()

    geocentric = satellite.at(t)

    subpoint = wgs84.subpoint(geocentric)

    return {
        "latitude": subpoint.latitude.degrees,
        "longitude": subpoint.longitude.degrees,
        "altitude": subpoint.elevation.km
    }

#locate all the satellites

def locate_all_satellites(df):

    locations = []

    for norad_id in df["NORAD ID"]:

        location = locate_satellite(norad_id)

        if location is None:
            continue

        location["NORAD ID"] = norad_id

        locations.append(location)

    return locations


# ---------------------------------------------------------------------------
# Locate a satellite at an arbitrary skyfield Time (used for predictions)
# ---------------------------------------------------------------------------
def locate_satellite_at(norad_id, t):
    """
    Returns the latitude/longitude/altitude of a satellite at a given
    skyfield Time object `t`.
    """

    tle_dict = dm.load_tle_dictionary()

    satellite = tle_dict.get(norad_id)

    if satellite is None:
        return None

    geocentric = satellite.at(t)

    subpoint = wgs84.subpoint(geocentric)

    return {
        "latitude": subpoint.latitude.degrees,
        "longitude": subpoint.longitude.degrees,
        "altitude": subpoint.elevation.km
    }


# ---------------------------------------------------------------------------
# Predict a satellite's future position + build a ground track between now
# and that future time (used by the Orbit Predictor page)
# ---------------------------------------------------------------------------
def predict_satellite_position(norad_id, hours_ahead):
    """
    Predicts where a satellite will be `hours_ahead` hours from now.

    Returns:
        {
            "current": {"latitude", "longitude", "altitude"},
            "future":  {"latitude", "longitude", "altitude"},
            "track": [(lat, lon), (lat, lon), ...]   # ground track samples
        }
        or None if the satellite has no TLE data available.
    """

    ts = dm.load_timescale()

    t_now = ts.now()

    future_dt = datetime.utcnow() + timedelta(hours=hours_ahead)

    t_future = ts.utc(
        future_dt.year,
        future_dt.month,
        future_dt.day,
        future_dt.hour,
        future_dt.minute,
        future_dt.second
    )

    current = locate_satellite_at(norad_id, t_now)
    future = locate_satellite_at(norad_id, t_future)

    if current is None or future is None:
        return None

    # Number of ground-track sample points: denser for longer durations,
    # capped so the map stays fast to draw.
    num_points = int(min(300, max(20, abs(hours_ahead) * 15)))

    tt_start = t_now.tt
    tt_end = t_future.tt

    track = []

    for i in range(num_points + 1):
        fraction = i / num_points
        t_sample = ts.tt_jd(tt_start + fraction * (tt_end - tt_start))

        position = locate_satellite_at(norad_id, t_sample)

        if position is not None:
            track.append((position["latitude"], position["longitude"]))

    return {
        "current": current,
        "future": future,
        "track": track,
        "current_time": t_now.utc_datetime(),
        "future_time": t_future.utc_datetime()
    }
