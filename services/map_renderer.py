from PIL import Image, ImageDraw
import streamlit as st
from services import satellite_locator

def latlon_to_pixel(latitude, longitude, width, height):
    """
    Convert latitude and longitude to pixel coordinates
    on an equirectangular world map.
    """

    x = (longitude + 180) * width / 360
    y = (90 - latitude) * height / 180

    return int(x), int(y)


def draw_all_satellites(
    world_map_path,
    locations,
    selected_norad=None
):
    """
    Draw all satellites on the world map.

    Parameters
    ----------
    world_map_path : str
        Path to the world map image.

    locations : list
        List of satellite dictionaries.

    selected_norad : int | None
        NORAD ID of the selected satellite.
    """

    image = Image.open(world_map_path).convert("RGB")

    draw = ImageDraw.Draw(image)

    width, height = image.size

    normal_radius = 3
    selected_radius = 6

    for satellite in locations:

        x, y = latlon_to_pixel(
            satellite["latitude"],
            satellite["longitude"],
            width,
            height
        )

        # Highlight selected satellite
        if satellite["NORAD ID"] == selected_norad:

            draw.ellipse(
                (
                    x - selected_radius,
                    y - selected_radius,
                    x + selected_radius,
                    y + selected_radius
                ),
                fill="red",
                width=4
            )

        # Draw remaining satellites
        else:

            draw.ellipse(
                (
                    x - normal_radius,
                    y - normal_radius,
                    x + normal_radius,
                    y + normal_radius
                ),
                fill="yellow",
                width=0.5
            )

    return image

#@st.fragment(run_every="10s")
def live_map(df):
    locations = satellite_locator.locate_all_satellites(df)

    image = draw_all_satellites(
        "assets/World_Map.jpg",
        locations,
        st.session_state.selected_norad
    )

    st.image(image, width="stretch")


# ===========================================================================
# Orbit Predictor map rendering
# ===========================================================================

def _draw_ground_track(draw, track, width, height, color=(0, 229, 255), line_width=2):
    """
    Draws a satellite ground track on the map, breaking the line whenever
    it crosses the antimeridian (i.e. wraps around from +180 to -180
    longitude) so it doesn't draw a wrong horizontal line across the map.
    """

    segment = []
    prev_x = None

    for latitude, longitude in track:

        x, y = latlon_to_pixel(latitude, longitude, width, height)

        if prev_x is not None and abs(x - prev_x) > width / 2:
            # Longitude wrap detected -> end current segment, start a new one
            if len(segment) > 1:
                draw.line(segment, fill=color, width=line_width)
            segment = [(x, y)]
        else:
            segment.append((x, y))

        prev_x = x

    if len(segment) > 1:
        draw.line(segment, fill=color, width=line_width)


def draw_prediction_map(
    world_map_path,
    current=None,
    future=None,
    track=None
):
    """
    Draws the Orbit Predictor map.

    Parameters
    ----------
    world_map_path : str
        Path to the base world map image.
    current : dict | None
        {"latitude": float, "longitude": float} - satellite's current position.
    future : dict | None
        {"latitude": float, "longitude": float} - satellite's predicted position.
    track : list | None
        List of (latitude, longitude) tuples describing the ground track
        between the current and future positions.

    Returns
    -------
    PIL.Image
        If current/future/track are all None, the plain base map is returned.
    """

    image = Image.open(world_map_path).convert("RGB")

    draw = ImageDraw.Draw(image)

    width, height = image.size

    marker_radius = 7

    if track:
        _draw_ground_track(draw, track, width, height)

    if current is not None:

        x, y = latlon_to_pixel(current["latitude"], current["longitude"], width, height)

        draw.ellipse(
            (x - marker_radius, y - marker_radius, x + marker_radius, y + marker_radius),
            fill="lime",
            outline="white",
            width=2
        )

    if future is not None:

        x, y = latlon_to_pixel(future["latitude"], future["longitude"], width, height)

        draw.ellipse(
            (x - marker_radius, y - marker_radius, x + marker_radius, y + marker_radius),
            fill="red",
            outline="white",
            width=2
        )

    return image
