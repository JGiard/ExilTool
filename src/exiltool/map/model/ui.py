from typing import Optional, List


class UiPlanet:
    def __init__(self, land: int, space: int, mineral: int, hydrocarbon: int,
                 mineral_prod: int, hydrocarbon_prod: int, image: str,
                 owner: str):
        self.land = land
        self.space = space
        self.mineral = mineral
        self.hydrocarbon = hydrocarbon
        self.mineral_prod = mineral_prod
        self.hydrocarbon_prod = hydrocarbon_prod
        self.image = image
        self.owner = owner


class UiPlace:
    def __init__(self, galaxy: int, sector: int, position: int, category: str, planet: Optional[UiPlanet] = None,
                 specials: List[str] = None, foss: Optional[int] = None, resa: Optional[str] = None):
        self.galaxy = galaxy
        self.sector = sector
        self.position = position
        self.category = category
        self.planet = planet
        self.specials = specials or []
        self.foss = foss
        self.resa = resa

    @property
    def name(self) -> str:
        return '{}.{}.{}'.format(self.galaxy, self.sector, self.position)


class UiSector:
    def __init__(self, galaxy: int, sector: int, places: List[UiPlace]):
        self.galaxy = galaxy
        self.sector = sector
        self.places = places
