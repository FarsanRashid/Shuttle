import json
from typing import List
from adapters.cache import AbstractCache
from adapters.geo_services import GeoService
from service_layer.exceptions import SearchQueryTooShortError


def sanitize(input):
    sanitized_value = input.strip().lower()
    if len(sanitized_value) < 3:
        raise SearchQueryTooShortError
    return sanitized_value


def recommend(seed_location, geo_service: GeoService, cache: AbstractCache) -> List:
    seed_location = sanitize(seed_location)
    recommendations = cache.get(seed_location)
    if recommendations is not None:
        return json.loads(recommendations)
    recommendations = geo_service.recommend(seed_location)
    cache.set(seed_location, json.dumps(recommendations))
    return recommendations
