from injector import inject

from exiltool.backend.decorators import route
from exiltool.model.map import Sector, PlacesUpdate
from exiltool.mongo.sectors import SectorsRepository


class MapService:
    @inject
    def __init__(self, sectors: SectorsRepository):
        self.sectors = sectors

    @route('/api/map/g/<int:galaxy>/s/<int:sector>')
    def get_sector(self, galaxy: int, sector: int) -> Sector:
        return self.sectors.get_sector(galaxy, sector)

    @route('/api/map/places', method='POST')
    def update_places(self, data: PlacesUpdate):
        for place in data.places:
            self.sectors.update_place(place)
