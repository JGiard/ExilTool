from typing import List, Optional

from autovalue import autovalue


@autovalue
class JsPlanet:
    def __init__(self, land: int, space: int, mineral: int, hydrocarbon: int):
        self.land = land
        self.space = space
        self.mineral = mineral
        self.hydrocarbon = hydrocarbon


@autovalue
class JsPlace:
    def __init__(self, galaxy: int, sector: int, position: int, img: Optional[str] = '01',
                 planet: Optional[JsPlanet] = None):
        self.galaxy = galaxy
        self.sector = sector
        self.position = position
        self.img = img
        self.planet = planet


@autovalue
class JsSector:
    def __init__(self, places: List[JsPlace]):
        self.places = places
