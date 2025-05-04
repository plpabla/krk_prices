from math import radians, cos, sin, asin, sqrt


def _haversine(lat1, lon1, lat2, lon2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees).
    Returns distance in kilometers.
    """
    # Convert decimal degrees to radians
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    r = 6371  # Radius of Earth in kilometers
    return c * r


def calc_distance_from_center(lat, lon):
    center_lat = 50.055
    center_lon = 19.94
    return _haversine(lat, lon, center_lat, center_lon)


def calc_distance_from_other_expensive(lat, lon):
    area_lat = 50.065
    area_lon = 19.93
    return _haversine(lat, lon, area_lat, area_lon)
