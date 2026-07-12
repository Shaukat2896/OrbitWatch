import os
import time
import json
import threading
from datetime import datetime, timezone

import requests
import streamlit as st
from dotenv import load_dotenv

# -----------------------------------------------------------------------
# Load environment variables from .env
# -----------------------------------------------------------------------
load_dotenv()

TLE_FILE_PATH = "data/active_satellites_TLE_data.tle"
STATUS_FILE_PATH = "data/tle_update_status.json"
UPDATE_INTERVAL_HOURS = 4


# -----------------------------------------------------------------------
# Status file helpers
# -----------------------------------------------------------------------
def _write_status(success, message, satellite_count=None):
    status = {
        "success": success,
        "message": message,
        "satellite_count": satellite_count,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

    try:
        os.makedirs(os.path.dirname(STATUS_FILE_PATH), exist_ok=True)
        with open(STATUS_FILE_PATH, "w", encoding="utf-8") as file:
            json.dump(status, file)
    except OSError as e:
        print(f"[TLE Update] Could not write status file: {e}")


def get_last_update_status():
    """
    Reads data/tle_update_status.json and returns the last known update
    status, or None if the TLE data has never been updated yet in this
    environment.

    Returns:
        {
            "success": bool,
            "message": str,
            "satellite_count": int | None,
            "timestamp": str (ISO format, UTC)
        } | None
    """
    try:
        with open(STATUS_FILE_PATH, "r", encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return None


# -----------------------------------------------------------------------
# Download TLE data from source and overwrite the local file
# -----------------------------------------------------------------------
def get_data_from_source():
    """
    Downloads the latest active-satellite TLE data from the URL
    configured in the .env file (websource_url) and overwrites
    data/active_satellites_TLE_data.tle with the response.

    Also records the outcome (success/failure, timestamp, satellite
    count) to data/tle_update_status.json so the UI can show it.

    Returns:
        bool: True if the file was updated successfully, False otherwise.
    """
    try:
        url = os.environ["websource_url"]

        response = requests.get(url, timeout=30)
        response.raise_for_status()

        os.makedirs(os.path.dirname(TLE_FILE_PATH), exist_ok=True)

        with open(TLE_FILE_PATH, "w", encoding="utf-8") as file:
            file.write(response.text)

        # A TLE entry is 3 lines (name + 2 element lines)
        satellite_count = response.text.count("\n") // 3

        print(f"[TLE Update] Success at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        _write_status(True, "Updated successfully", satellite_count)
        return True

    except KeyError:
        print("[TLE Update] Failed: 'websource_url' not found in .env file")
        _write_status(False, "'websource_url' not found in .env file")
        return False

    except requests.RequestException as e:
        print(f"[TLE Update] Failed: {e}")
        _write_status(False, str(e))
        return False


# -----------------------------------------------------------------------
# Background loop that re-downloads the TLE file every N hours
# -----------------------------------------------------------------------
def _update_loop(interval_hours):
    interval_seconds = interval_hours * 60 * 60

    while True:
        get_data_from_source()
        time.sleep(interval_seconds)


# -----------------------------------------------------------------------
# Start the scheduler (singleton per app process via st.cache_resource)
# -----------------------------------------------------------------------
@st.cache_resource(show_spinner=False)
def start_tle_scheduler(interval_hours: int = UPDATE_INTERVAL_HOURS):
    """
    Starts a background daemon thread that automatically refreshes the
    TLE file every `interval_hours` hours.

    st.cache_resource guarantees this only ever runs once per running
    app process, no matter how many times Streamlit reruns the script
    or how many users/sessions hit the app.
    """
    thread = threading.Thread(
        target=_update_loop,
        args=(interval_hours,),
        daemon=True,
        name="TLEUpdaterThread"
    )
    thread.start()

    print(f"[TLE Update] Scheduler started - refreshing every {interval_hours} hours")

    return thread
