from location.geo_service.geo_service import GeoService
from service_layer.exceptions import SearchQueryTooShortError


def sanitize(input):
    sanitized_value = input.strip().lower()
    if len(sanitized_value) < 3:
        raise SearchQueryTooShortError
    return sanitized_value


def recommend(seed_location, geo_service: GeoService):
    seed_location = sanitize(seed_location)
    return geo_service.recommend(seed_location)
