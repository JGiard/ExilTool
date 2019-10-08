from typing import List

from autovalue import autovalue


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
class JsShip:
    def __init__(self, id: str, quantity: int):
        self.id = id
        self.quantity = quantity


@autovalue
class JsResource:
    def __init__(self, id: int, quantity: int):
        self.id = id
        self.quantity = quantity


@autovalue
class JsFleet:
    def __init__(self, id: int, name: str, category: int, stance: int, size: int, signature: int, cargoload: int,
                 cargocapacity: int, action: str, endtime: int, commandername: str, position: JsPlanet,
                 destination: JsPlanet, ships: List[JsShip], resources: List[JsResource], shared: bool):
        self.id = id
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
