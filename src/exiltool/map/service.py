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
                if place.planet.mineral == -1 and places[place.position].planet is not None:
                    old_place = places[place.position]
                    planet = old_place.planet.update(image=place.planet.image)
                    if place.planet.owner.name != 'Occupée':
                        planet = planet.update(owner=place.planet.owner)
                    places[place.position] = old_place.update(planet=planet)
                else:
                    places[place.position] = place
            else:
                places[place.position] = place

        self.repository.update_places(list(places.values()))