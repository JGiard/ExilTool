from injector import inject

from exiltool.backend.decorators import route
from exiltool.map.converter import MapConverter
from exiltool.map.model.domain import Sector
from exiltool.map.model.js import JsSector
from exiltool.mongo.sectors import SectorsRepository


class MapService:
    @inject
    def __init__(self, sectors: SectorsRepository, converter: MapConverter):
        self.sectors = sectors
        self.converter = converter

    @route('/api/map/g/<int:galaxy>/s/<int:sector>')
    def get_sector(self, galaxy: int, sector: int) -> Sector:
        return self.sectors.get_sector(galaxy, sector)

    @route('/api/map/places', method='POST')
    def update_places(self, data: JsSector):
        for place in data.places:
            self.sectors.update_place(self.converter.place_from_js(place))
