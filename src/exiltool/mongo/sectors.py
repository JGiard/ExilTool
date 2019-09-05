from injector import inject
from pyckson import parse, rename, serialize
from pymongo.database import Database

from exiltool.model.map import Place


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


class SectorsRepository:
    @inject
    def __init__(self, db: Database):
        self.collection = db['sectors']

    def get_place(self, galaxy: int, sector: int, position: int) -> Place:
        doc = self.collection.find_one({'_id': MongoPlace.make_id(galaxy, sector, position)})
        if doc is None:
            return Place(galaxy, sector, position)
        mongo_place = parse(MongoPlace, doc)
        return mongo_place.place

    def update_place(self, place: Place):
        print(place)
        print(self.collection)
        mongo_place = MongoPlace.from_place(place)
        self.collection.update({'_id': mongo_place.id}, serialize(mongo_place), upsert=True)
