from typing import List

from autovalue import autovalue
from pyckson import rename


@autovalue
class JsPlanet:
    def __init__(self, id: int, name: str, relation: int, g: str, s: str, p: str):
        self.id = id
        self.name = name
        self.relation = relation
        self.g = g
        self.s = s
        self.p = p


@autovalue
@rename(name='id')
class JsShip:
    def __init__(self, name: str, quantity: int):
        self.name = name
        self.quantity = quantity


@autovalue
class JsOrbit:
    def __init__(self, planet_id: int, ships: List[JsShip]):
        self.planet_id = planet_id
        self.ships = ships


@autovalue
class JsResource:
    def __init__(self, id: int, quantity: int):
        self.id = id
        self.quantity = quantity


@autovalue
@rename(fleet_id='id')
class JsFleet:
    def __init__(self, fleet_id: int, name: str, category: int, stance: int, size: int, signature: int, cargoload: int,
                 cargocapacity: int, action: str, endtime: int, commandername: str, position: JsPlanet,
                 destination: JsPlanet, ships: List[JsShip], resources: List[JsResource], shared: bool):
        self.fleet_id = fleet_id
        self.name = name
        self.category = category
        self.stance = stance
        self.size = size
        self.signature = signature
        self.cargoload = cargoload
        self.cargocapacity = cargocapacity
        self.action = action
        self.endtime = endtime
        self.commandername = commandername
        self.position = position
        self.destination = destination
        self.ships = ships
        self.resources = resources
        self.shared = shared
