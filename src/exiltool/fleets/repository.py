from typing import Dict, Iterable

from injector import inject
from pyckson import serialize, parse
from pymongo.database import Database

from exiltool.fleets.model.domain import Ship, PlayerShips, PlayerShipCount


class ShipsRepository:
    @inject
    def __init__(self, db: Database):
        self.collection = db['ships']

    def update_player(self, username: str, ships: Dict[Ship, int]):
        ships = [PlayerShipCount(key, value) for key, value in ships.items()]
        doc = serialize(PlayerShips(username, ships))
        self.collection.update({'username': username}, doc, upsert=True)

    def get_all(self) -> Iterable[PlayerShips]:
        for doc in self.collection.find():
            yield parse(PlayerShips, doc)
