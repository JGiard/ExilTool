from collections import Counter
from typing import List

from injector import inject

from exiltool.backend.decorators import route
from exiltool.fleets.model.domain import Ship
from exiltool.fleets.model.js import JsFleet
from exiltool.fleets.repository import ShipsRepository
from exiltool.model.user import User


class FleetsService:
    @inject
    def __init__(self, repository: ShipsRepository):
        self.repository = repository

    @route('/api/fleets', method='POST')
    def update_fleets(self, user: User, data: List[JsFleet]):
        ships = Counter()
        for fleet in data:
            for ship in fleet.ships:
                for model in Ship:
                    if ship.id == model.display_name:
                        ships[model] += ship.quantity
        self.repository.update_player(user.username, ships)
