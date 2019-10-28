from injector import inject

from exiltool.backend.decorators import route
from exiltool.map.converter import MapConverter
from exiltool.map.model.domain import Sector, PlaceType
from exiltool.map.model.js import JsSector
from exiltool.map.repository import MapRepository


class MapService:
    @inject
    def __init__(self, repository: MapRepository, converter: MapConverter):
        self.repository = repository
        self.converter = converter

    @route('/api/map/g/<int:galaxy>/s/<int:sector>')
    def get_sector(self, galaxy: int, sector: int) -> Sector:
        return self.repository.get_sector(galaxy, sector)

    @route('/api/map/places', method='POST')
    def update_places(self, data: JsSector):
        galaxy = data.galaxy or data.places[0].galaxy
        sector = data.sector or data.places[0].sector
        new_places = [self.converter.place_from_js(place) for place in data.places]
        places = {place.position: place for place in self.repository.get_sector(galaxy, sector).places}
        for place in new_places:
            if place.position not in places:
                places[place.position] = place
                continue
            if place.category == PlaceType.planet:
                if places[place.position].planet is None:
                    places[place.position] = place
                else:
                    new_planet = places[place.position].planet.update(image=place.planet.image)
                    if place.planet.mineral != -1:
                        new_planet = new_planet.update(mineral=place.planet.mineral,
                                                       hydrocarbon=place.planet.hydrocarbon,
                                                       land=place.planet.land,
                                                       space=place.planet.space)
                        if place.specials is not None:
                            places[place.position] = places[place.position].update(specials=place.specials)
                        if place.orbit is not None:
                            places[place.position] = places[place.position].update(orbit=place.orbit)
                    if place.planet.mineral != -1 or (place.planet and place.planet.owner and place.planet.owner.name != 'Occupée'):
                        new_planet = new_planet.update(owner=place.planet.owner)
                    places[place.position] = places[place.position].update(planet=new_planet)
            else:
                places[place.position] = places[place.position].update(category=place.category)
                if place.orbit and len(place.orbit) > 0:
                    places[place.position] = places[place.position].update(orbit=place.orbit)

        self.repository.update_places(list(places.values()))
