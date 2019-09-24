from typing import List

from injector import inject
from pyckson import parse, rename, serialize
from pymongo import ReplaceOne
from pymongo.database import Database

from exiltool.map.model.domain import Place, Sector


@rename(id='_id')
class MongoPlace:
    def __init__(self, id: str, place: Place):
        self.id = id
        self.place = place

    @staticmethod
    def make_id(galaxy: int, sector: int, position: int) -> str:
        return 'g{}s{}p{}'.format(galaxy, sector, position)

    @staticmethod
    def from_place(place: Place) -> 'MongoPlace':
        return MongoPlace(MongoPlace.make_id(place.galaxy, place.sector, place.position), place)


class MapRepository:
    @inject
    def __init__(self, db: Database):
        self.collection = db['sectors']

    def get_place(self, galaxy: int, sector: int, position: int) -> Place:
        doc = self.collection.find_one({'_id': MongoPlace.make_id(galaxy, sector, position)})
        if doc is None:
            return Place(galaxy, sector, position)
        mongo_place = parse(MongoPlace, doc)
        return mongo_place.place

    def get_sector(self, galaxy: int, sector: int) -> Sector:
        docs = self.collection.find({'place.galaxy': galaxy, 'place.sector': sector})
        places = [parse(MongoPlace, doc).place for doc in docs]
        places_by_pos = {place.position: place for place in places}
        ordered_places = []
        for i in range(1, 26):
            if i in places_by_pos:
                ordered_places.append(places_by_pos[i])
            else:
                ordered_places.append(Place(galaxy, sector, i))
        return Sector(galaxy, sector, ordered_places)

    def update_places(self, places: List[Place]):
        mongo_places = [MongoPlace.from_place(place) for place in places]
        requests = [ReplaceOne({'_id': place.id}, serialize(place), upsert=True) for place in mongo_places]
        self.collection.bulk_write(requests)
