import os
from abc import ABC, abstractmethod
from typing import Dict

import requests


class GeoService(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def recommend(self, seed_location) -> Dict:
        pass


class BariKoi(GeoService):
    def __init__(self):
        pass

    def recommend(self, seed_location):
        response = requests.get(
            "https://barikoi.xyz/v2/api/search/autocomplete/place",
            params={'q': seed_location,
                    'city': 'dhaka',
                    'api_key': os.environ.get('BARIKOI_API_KEY')
                    },
            timeout=5
        )
        return response.json()


class FakeGeoService(GeoService):
    def __init__(self):
        pass

    def recommend(self, seed_location) -> Dict:
        return {"places": []}
