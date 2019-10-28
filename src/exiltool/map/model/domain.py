from enum import Enum
from typing import Optional, List

from autovalue import autovalue
from pyckson import rename


@autovalue
class PlaceOwner:
    def __init__(self, name: str, alliance: Optional[str] = None):
        self.name = name
        self.alliance = alliance


@autovalue
class Planet:
    def __init__(self, land: int, space: int, mineral: int, hydrocarbon: int, image: Optional[str] = '01',
                 owner: Optional[PlaceOwner] = None):
        self.land = land
        self.space = space
        self.mineral = mineral
        self.hydrocarbon = hydrocarbon
        self.image = image
        self.owner = owner


class PlaceType(Enum):
    empty = 1
    vortex = 2
    asteroids = 3
    planet = 4
    merchant = 5
    unknown = 6


@autovalue
@rename(fleet_id='id')
class OrbitFleet:
    def __init__(self, fleet_id: int, name: str, tag: str, player: str, stance: int, signature: str):
        self.fleet_id = fleet_id
        self.name = name
        self.tag = tag
        self.player = player
        self.stance = stance
        self.signature = signature


@autovalue
class Place:
    def __init__(self, galaxy: int, sector: int, position: int,
                 category: Optional[PlaceType] = PlaceType.unknown,
                 planet: Optional[Planet] = None, specials: Optional[List[str]] = None,
                 orbit: Optional[List[OrbitFleet]] = None):
        self.galaxy = galaxy
        self.sector = sector
        self.position = position
        self.category = category
        self.planet = planet
        self.specials = specials
        self.orbit = orbit


@autovalue
class Sector:
    def __init__(self, galaxy: int, sector: int, places: List[Place]):
        self.galaxy = galaxy
        self.sector = sector
        self.places = places
