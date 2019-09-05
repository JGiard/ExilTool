from typing import Optional, List


class Planet:
    def __init__(self, land: int, space: int, mineral: int, hydrocarbon: int):
        self.land = land
        self.space = space
        self.mineral = mineral
        self.hydrocarbon = hydrocarbon


class Place:
    def __init__(self, galaxy: int, sector: int, position: int, planet: Optional[Planet] = None):
        self.galaxy = galaxy
        self.sector = sector
        self.position = position
        self.planet = planet


class Sector:
    def __init__(self, galaxy: int, sector: int, places: List[Place]):
        self.galaxy = galaxy
        self.sector = sector
        self.places = places


class PlacesUpdate:
    def __init__(self, places: List[Place]):
        self.places = places
