from typing import List, Iterable

from exiltool.fleets.model.domain import Fleet, SourceType, FleetShips, Ship
from exiltool.fleets.model.js import JsFleet, JsShip, JsOrbit
from exiltool.model.user import User


class FleetConverter:
    def fleet_from_js(self, user: User, fleet: JsFleet) -> Fleet:
        return Fleet(
            username=user.username,
            source_id=fleet.fleet_id,
            source_type=SourceType.fleet,
            ships=list(self.ships_from_js(fleet.ships))
        )

    def ships_from_js(self, ships: List[JsShip]) -> Iterable[FleetShips]:
        for ship in ships:
            for model in Ship:
                if ship.name.replace('&#39;', "'") == model.display_name:
                    yield FleetShips(model, ship.quantity)

    def orbit_from_js(self, user: User, orbit: JsOrbit) -> Fleet:
        return Fleet(
            username=user.username,
            source_id=orbit.planet_id,
            source_type=SourceType.planet,
            ships=list(self.ships_from_js(orbit.ships))
        )
