from enum import Enum
from typing import List


class Ship(Enum):
    chasseur = ('Chasseur', 4)
    inter = ('Intercepteur', 5)
    predateur = ('Prédateur', 5)
    corv_legere = ('Corvette légère', 7)
    corv_lourde = ('Corvette lourde', 9)
    fa = ('Frégate d\'assaut', 28)
    fi = ('Frégate à canon ionique', 32)
    fm = ('Frégate à missiles', 50)
    croiseur = ('Croiseur', 68)
    cc = ('Croiseur de combat', 120)

    def __init__(self, display_name: str, signature: int):
        self.display_name = display_name
        self.signature = signature


class SourceType(Enum):
    fleet = 1
    planet = 2


class FleetShips:
    def __init__(self, ship: Ship, quantity: int):
        self.ship = ship
        self.quantity = quantity


class Fleet:
    def __init__(self, username: str, source_id: int, source_type: SourceType, ships: List[FleetShips]):
        self.username = username
        self.source_id = source_id
        self.source_type = source_type
        self.ships = ships
