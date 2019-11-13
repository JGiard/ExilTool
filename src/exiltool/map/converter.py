from typing import Optional

from exiltool.map.model.domain import Sector, Place, Planet, PlaceType, PlaceOwner, OrbitFleet
from exiltool.map.model.js import JsPlace, JsPlanet, JsOrbitFleet
from exiltool.map.model.ui import UiSector, UiPlace, UiPlanet
from exiltool.map.tools import compute_prod

ignored_specials = ['Filon de minerai', 'Gisements d\'hydrocarbure']


class MapConverter:
    def sector_to_ui(self, sector: Sector) -> UiSector:
        places = [self.place_to_ui(place) for place in sector.places]
        return UiSector(sector.galaxy, sector.sector, places)

    def place_to_ui(self, place: Place) -> UiPlace:
        planet = self.planet_to_ui(place.planet) if place.planet else None
        foss = None
        if place.orbit:
            for fleet in place.orbit:
                if fleet.name == 'Les fossoyeurs':
                    foss = fleet.signature
        return UiPlace(place.galaxy, place.sector, place.position, place.category.name, planet, place.specials, foss)

    def planet_to_ui(self, planet: Planet) -> UiPlanet:
        owner = ''
        if planet.owner:
            if planet.owner.alliance:
                owner = '[{}] {}'.format(planet.owner.alliance, planet.owner.name)
            else:
                owner = planet.owner.name
        return UiPlanet(planet.land, planet.space, planet.mineral, planet.hydrocarbon,
                        compute_prod(planet.land, planet.mineral),
                        compute_prod(planet.land, planet.hydrocarbon),
                        planet.image, owner)

    def place_from_js(self, place: JsPlace) -> Place:
        place_type = PlaceType.planet
        if place.img == 'vortex':
            place_type = PlaceType.vortex
        elif place.img == 'asteroids':
            place_type = PlaceType.asteroids
        elif place.img == 'merchant':
            place_type = PlaceType.merchant
        elif place.img == '' and not place.planet:
            place_type = PlaceType.empty
        planet = self.planet_from_js(place.planet, place.img) if place_type == PlaceType.planet else None
        specials = [el for el in place.elements if el not in ignored_specials] if place.elements is not None else None
        orbits = [self.orbit_from_js(o) for o in place.orbit] if place.orbit else None
        return Place(place.galaxy, place.sector, place.position, place_type, planet, specials, orbits)

    def orbit_from_js(self, orbit: JsOrbitFleet) -> OrbitFleet:
        return OrbitFleet(
            fleet_id=orbit.fleet_id,
            name=orbit.name,
            tag=orbit.tag,
            player=orbit.player,
            stance=orbit.stance,
            signature=orbit.signature
        )

    def planet_from_js(self, planet: Optional[JsPlanet], img: str) -> Planet:
        if planet is None:
            return Planet(-1, -1, -1, -1, img)
        owner = None
        if planet.owner:
            alliance = planet.alliance if planet.alliance else None
            owner = PlaceOwner(planet.owner, alliance)
        return Planet(planet.land, planet.space, planet.mineral, planet.hydrocarbon, img, owner)
