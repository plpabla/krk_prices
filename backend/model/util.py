from geopy.geocoders import Nominatim

from .distanse_calc import (
    calc_distance_from_center,
    calc_distance_from_other_expensive,
)


def calculate_lat_lon(address: str) -> tuple:
    geolocator = Nominatim(
        user_agent="geo_locator"
    )  # Tworzymy obiekt geolokatora (identyfikator user_agent jest wymagany)
    location = geolocator.geocode(
        address
    )  # Pobieramy dane lokalizacji dla podanego adresu

    if location:
        return (
            location.latitude,
            location.longitude,
        )  # Zwracamy szerokość i długość geograficzną
    else:
        return (50.0647, 19.9450)


__all__ = [
    "calc_distance_from_center",
    "calc_distance_from_other_expensive",
    "calculate_lat_lon",
]
