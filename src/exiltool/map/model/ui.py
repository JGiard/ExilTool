from typing import Optional, List

from exiltool.map.model.domain import PlaceType


class UiPlanet:
    def __init__(self, land: int, space: int, mineral: int, hydrocarbon: int,
                 mineral_prod: int, hydrocarbon_prod: int, image: str):
        self.land = land
        self.space = space
        self.mineral = mineral
        self.hydrocarbon = hydrocarbon
        self.mineral_prod = mineral_prod
        self.hydrocarbon_prod = hydrocarbon_prod
        self.image = image


class UiPlace:
    def __init__(self, position: int, category: str, planet: Optional[UiPlanet] = None):
        self.position = position
        self.category = category
        self.planet = planet


class UiSector:
    def __init__(self, galaxy: int, sector: int, places: List[UiPlace]):
        self.galaxy = galaxy
        self.sector = sector
        self.places = places
