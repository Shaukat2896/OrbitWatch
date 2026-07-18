import numpy as np

MU = 398600.4418          # km³/s²
EARTH_RADIUS = 6378.137   # km


def extract_parameters(satellite):

    # NORAD ID
    norad = satellite.model.satnum

    # Inclination (radians -> degrees)
    inclination = np.degrees(satellite.model.inclo)

    # Mean Motion (rad/min -> rad/sec)
    mean_motion = satellite.model.no_kozai / 60

    # Semi-major axis (km)
    semi_major_axis = (MU / (mean_motion ** 2)) ** (1/3)

    # Mean altitude (km)
    altitude = semi_major_axis - EARTH_RADIUS

    # Orbit regime
    if altitude < 2000:
        orbit = "LEO"

    elif altitude < 35786:
        orbit = "MEO"

    elif abs(altitude - 35786) <= 500:
        orbit = "GEO"

    else:
        orbit = "HEO"

    return {
        "satellite": satellite,
        "norad": norad,
        "inclination": inclination,
        "altitude": altitude,
        "orbit": orbit
    }



from services import data_manager as dm


ALTITUDE_THRESHOLD = 100      # km
INCLINATION_THRESHOLD = 10    # degrees


def filter_objects(target_satellite):

    tle_dict = dm.load_tle_dictionary()

    target = extract_parameters(target_satellite)

    filtered = []

    for satellite in tle_dict.values():

        candidate = extract_parameters(satellite)

        # Skip itself
        if candidate["norad"] == target["norad"]:
            continue

        # Orbit regime
        if candidate["orbit"] != target["orbit"]:
            continue

        # Altitude difference
        altitude_difference = abs(
            candidate["altitude"] - target["altitude"]
        )

        if altitude_difference > ALTITUDE_THRESHOLD:
            continue

        # Inclination difference
        inclination_difference = abs(
            candidate["inclination"] - target["inclination"]
        )

        if inclination_difference > INCLINATION_THRESHOLD:
            continue

        filtered.append(candidate)

    return filtered



from skyfield.api import load

ts = load.timescale()


def find_closest_approach(target, candidate, hours):

    start_time = ts.now()

    minimum_distance = float("inf")
    closest_time = None

    total_minutes = int(hours * 60)

    for minute in range(0, total_minutes + 1, 5):

        t = ts.tt_jd(
            start_time.tt + minute / 1440
        )

        target_position = target.at(t).position.km

        candidate_position = candidate.at(t).position.km

        distance = np.linalg.norm(
            target_position - candidate_position
        )

        if distance < minimum_distance:

            minimum_distance = distance
            closest_time = t.utc_datetime()

    return {
        "Satellite Name": candidate.name,
        "NORAD": candidate.model.satnum,
        "Distance": minimum_distance,
        "Time": closest_time
    }


def evaluate_risk(distance):

    if distance < 1:
        return "Critical"

    elif distance < 5:
        return "High"

    elif distance < 10:
        return "Medium"

    elif distance < 25:
        return "Low"

    else:
        return "Safe"







def closest_objects_detector(selected_norad, hours):

    tle_dict = dm.load_tle_dictionary()

    try:
        target = tle_dict[selected_norad]

        candidates = filter_objects(target)

        risky = []
        safe = []

        for candidate in candidates:

            result = find_closest_approach(
                target,
                candidate["satellite"],
                hours
            )

            result["Risk"] = evaluate_risk(
                result["Distance"]
            )

            if result["Risk"] == "Safe":
                safe.append(result)

            else:
                risky.append(result)

        risky.sort(key=lambda x: x["Distance"])
        safe.sort(key=lambda x: x["Distance"])

        if len(risky) > 0:
            return risky

        return safe[:10]
    
    except:
        return []