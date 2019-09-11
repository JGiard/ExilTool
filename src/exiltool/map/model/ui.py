from typing import Optional, List

from exiltool.map.model.domain import Place, Planet, Sector


class UiPlanet:
    def __init__(self, land: int, space: int, mineral: int, hydrocarbon: int,
                 mineral_prod: int, hydrocarbon_prod: int):
        self.land = land
        self.space = space
        self.mineral = mineral
        self.hydrocarbon = hydrocarbon
        self.mineral_prod = mineral_prod
        self.hydrocarbon_prod = hydrocarbon_prod


class UiPlace:
    def __init__(self, position: int, planet: Optional[UiPlanet] = None):
        self.position = position
        self.planet = planet


class UiSector:
    def __init__(self, galaxy: int, sector: int, places: List[UiPlace]):
        self.galaxy = galaxy
        self.sector = sector
        self.places = places
