from math import atan2, cos, radians, sin, sqrt

from pyzcode import ZipCode


class DistanceCalculator:
    EARTH_RADIUS_KM = 6371.0  # Earth radius in kilometers

    @staticmethod
    def calculate_distance(zip_code1, zip_code2):
        # Retrieve latitude and longitude for both zip codes
        location1 = ZipCode(zip_code1)
        location2 = ZipCode(zip_code2)

        # Ensure the data is valid
        if (
            location1.lat is None
            or location1.lon is None
            or location2.lat is None
            or location2.lon is None
        ):
            raise ValueError("Invalid zip code(s) provided")

        lat1, lon1 = radians(location1.lat), radians(location1.lon)
        lat2, lon2 = radians(location2.lat), radians(location2.lon)

        # Haversine formula
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        distance_km = DistanceCalculator.EARTH_RADIUS_KM * c
        distance_km = round(distance_km, 3)

        return distance_km
