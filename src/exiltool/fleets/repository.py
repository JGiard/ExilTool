from typing import List, Iterable

from injector import inject
from pyckson import serialize, parse
from pymongo import DeleteMany, InsertOne
from pymongo.database import Database

from exiltool.fleets.model.domain import Fleet, SourceType


class FleetsRepository:
    @inject
    def __init__(self, db: Database):
        self.collection = db['fleets']

    def update_player_fleets(self, username: str, fleets: List[Fleet]):
        requests = [
            DeleteMany({'username': username, 'sourceType': SourceType.fleet.name}),
        ]
        for fleet in fleets:
            requests.append(InsertOne(serialize(fleet)))
        self.collection.bulk_write(requests)

    def update_orbit(self, username: str, fleet: Fleet):
        self.collection.replace_one({'username': username,
                                     'sourceType': SourceType.planet.name,
                                     'sourceId': fleet.source_id
                                     }, serialize(fleet), upsert=True)

    def get_all(self) -> Iterable[Fleet]:
        for doc in self.collection.find():
            yield parse(Fleet, doc)

    def update_orbits(self, username: str, fleets: List[Fleet]):
        requests = [
            DeleteMany({'username': username, 'sourceType': SourceType.planet.name}),
        ]
        for fleet in fleets:
            requests.append(InsertOne(serialize(fleet)))
        self.collection.bulk_write(requests)
