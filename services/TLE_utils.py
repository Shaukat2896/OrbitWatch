import os
import time
import threading
from datetime import datetime

import requests
import streamlit as st
from dotenv import load_dotenv

# -----------------------------------------------------------------------
# Load environment variables from .env
# -----------------------------------------------------------------------
load_dotenv()

TLE_FILE_PATH = "data/active_satellites_TLE_data.tle"
UPDATE_INTERVAL_HOURS = 4


# -----------------------------------------------------------------------
# Download TLE data from source and overwrite the local file
# -----------------------------------------------------------------------
def get_data_from_source():
    """
    Downloads the latest active-satellite TLE data from the URL
    configured in the .env file (websource_url) and overwrites
    data/active_satellites_TLE_data.tle with the response.

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

        print(f"[TLE Update] Success at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        return True

    except KeyError:
        print("[TLE Update] Failed: 'websource_url' not found in .env file")
        return False

    except requests.RequestException as e:
        print(f"[TLE Update] Failed: {e}")
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
