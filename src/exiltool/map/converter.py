from exiltool.map.model.domain import Sector, Place, Planet
from exiltool.map.model.ui import UiSector, UiPlace, UiPlanet
from exiltool.map.tools import compute_prod


class MapConverter:
    def convert(self, sector: Sector) -> UiSector:
        places = [self.convert_place(place) for place in sector.places]
        return UiSector(sector.galaxy, sector.sector, places)

    def convert_place(self, place: Place) -> UiPlace:
        planet = self.convert_planet(place.planet) if place.planet else None
        return UiPlace(place.position, planet)

    def convert_planet(self, planet: Planet) -> UiPlanet:
        return UiPlanet(planet.land, planet.space, planet.mineral, planet.hydrocarbon,
                        compute_prod(planet.land, planet.mineral),
                        compute_prod(planet.land, planet.hydrocarbon))
