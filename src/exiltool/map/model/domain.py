from enum import Enum
from typing import Optional, List

from autovalue import autovalue


@autovalue
class Planet:
    def __init__(self, land: int, space: int, mineral: int, hydrocarbon: int, image: Optional[str] = '01'):
        self.land = land
        self.space = space
        self.mineral = mineral
        self.hydrocarbon = hydrocarbon
        self.image = image


class PlaceType(Enum):
    empty = 1
    vortex = 2
    asteroids = 3
    planet = 4
    merchant = 5
    unknown = 6


@autovalue
class Place:
    def __init__(self, galaxy: int, sector: int, position: int,
                 category: Optional[PlaceType] = PlaceType.unknown,
                 planet: Optional[Planet] = None):
        self.galaxy = galaxy
        self.sector = sector
        self.position = position
        self.category = category
        self.planet = planet


@autovalue
class Sector:
    def __init__(self, galaxy: int, sector: int, places: List[Place]):
        self.galaxy = galaxy
        self.sector = sector
        self.places = places
