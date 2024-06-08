from abc import ABC, abstractmethod
import logging
import os
from typing import Dict, List

import requests

logger = logging.getLogger(__name__)


class GeoService(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def recommend(self, seed_location) -> List:
        pass


class BariKoi(GeoService):
    def __init__(self):
        pass

    def recommend(self, seed_location) -> List:
        response = requests.get(
            "https://barikoi.xyz/v2/api/search/autocomplete/place",
            params={'q': seed_location,
                    'city': 'dhaka',
                    'api_key': os.environ.get('BARIKOI_API_KEY')
                    },
            timeout=5
        )
        if response.json()["status"] != 200:
            logger.exception(response.json())
            raise Exception
        return response.json()["places"]


class FakeGeoService(GeoService):
    def __init__(self):
        pass

    def recommend(self, seed_location) -> List:
        return []
