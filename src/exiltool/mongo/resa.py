from typing import Iterable, Optional

from injector import inject
from pyckson import serialize, parse
from pymongo.database import Database

from exiltool.model.resa import Resa


class ResaRepository:
    @inject
    def __init__(self, db: Database):
        self.collection = db['resa']

    def save(self, resa: Resa):
        self.collection.update({'galaxy': resa.galaxy, 'sector': resa.sector, 'position': resa.position},
                               serialize(resa), upsert=True)

    def remove(self, resa: Resa):
        self.collection.remove({'galaxy': resa.galaxy, 'sector': resa.sector, 'position': resa.position})

    def get_by_user(self, username: str) -> Iterable[Resa]:
        for doc in self.collection.find({'username': username}):
            yield parse(Resa, doc)

    def get_by_pos(self, galaxy: int, sector: int, position: int) -> Optional[Resa]:
        doc = self.collection.find_one({'galaxy': galaxy, 'sector': sector, 'position': position})
        if doc is not None:
            return parse(Resa, doc)

    def get_all(self) -> Iterable[Resa]:
        for doc in self.collection.find():
            yield parse(Resa, doc)
