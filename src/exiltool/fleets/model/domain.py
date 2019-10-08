from enum import Enum
from typing import List


class Ship(Enum):
    chasseur = ('Chasseur', 4)
    inter = ('Intercepteur', 5)
    corv_legere = ('Corvette légère', 7)
    corv_lourde = ('Corvette lourde', 9)
    fa = ('Frégate d&#39;assaut', 28)
    croiseur = ('Croiseur', 68)
    cc = ('Croiseur de combat', 120)

    def __init__(self, display_name: str, signature: int):
        self.display_name = display_name
        self.signature = signature


class PlayerShipCount:
    def __init__(self, ship: Ship, quantity: int):
        self.ship = ship
        self.quantity = quantity


class PlayerShips:
    def __init__(self, username: str, ships: List[PlayerShipCount]):
        self.username = username
        self.ships = ships
