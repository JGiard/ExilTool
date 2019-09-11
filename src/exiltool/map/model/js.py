from typing import List

from exiltool.map.model.domain import Place


class PlacesUpdate:
    def __init__(self, places: List[Place]):
        self.places = places
