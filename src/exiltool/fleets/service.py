from operator import attrgetter
from typing import List

from injector import inject

from exiltool.backend.decorators import route
from exiltool.fleets.converter import FleetConverter
from exiltool.fleets.model.domain import Fleet, SourceType
from exiltool.fleets.model.js import JsFleet, JsShip, JsOrbit
from exiltool.fleets.repository import FleetsRepository
from exiltool.model.user import User


class FleetsService:
    @inject
    def __init__(self, repository: FleetsRepository, converter: FleetConverter):
        self.repository = repository
        self.converter = converter

    @route('/api/fleets', method='POST')
    def update_fleets(self, user: User, data: List[JsFleet]):
        fleets = (self.converter.fleet_from_js(user, f) for f in data)
        fleets = filter(attrgetter('ships'), fleets)
        self.repository.update_player_fleets(user.username, list(fleets))

    @route('/api/orbit/<int:planet_id>', method='POST')
    def update_orbit_ships(self, user: User, planet_id: int, data: List[JsShip]):
        ships = list(self.converter.ships_from_js(data))
        fleet = Fleet(user.username, planet_id, SourceType.planet, ships)
        self.repository.update_orbit(user.username, fleet)

    @route('/api/orbits', method='POST')
    def update_all_orbits(self, user: User, data: List[JsOrbit]):
        fleets = (self.converter.orbit_from_js(user, o) for o in data)
        fleets = filter(attrgetter('ships'), fleets)
        self.repository.update_orbits(user.username, list(fleets))
