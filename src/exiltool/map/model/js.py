from typing import List, Optional

from autovalue import autovalue
from pyckson import rename


@autovalue
class JsPlanet:
    def __init__(self, land: int, space: int, mineral: int, hydrocarbon: int,
                 alliance: Optional[str] = None, owner: Optional[str] = None):
        self.land = land
        self.space = space
        self.mineral = mineral
        self.hydrocarbon = hydrocarbon
        self.alliance = alliance
        self.owner = owner


@autovalue
@rename(fleet_id='id')
class JsOrbitFleet:
    def __init__(self, fleet_id: int, name: str, tag: str, player: str, stance: int, signature: str):
        self.fleet_id = fleet_id
        self.name = name
        self.tag = tag
        self.player = player
        self.stance = stance
        self.signature = signature


@autovalue
class JsPlace:
    def __init__(self, galaxy: int, sector: int, position: int, img: Optional[str] = '01',
                 planet: Optional[JsPlanet] = None, elements: Optional[List[str]] = None,
                 orbit: Optional[List[JsOrbitFleet]] = None):
        self.galaxy = galaxy
        self.sector = sector
        self.position = position
        self.img = img
        self.planet = planet
        self.elements = elements
        self.orbit = orbit


@autovalue
class JsSector:
    def __init__(self, places: List[JsPlace], galaxy: Optional[int] = None, sector: Optional[int] = None):
        self.places = places
        self.galaxy = galaxy
        self.sector = sector
