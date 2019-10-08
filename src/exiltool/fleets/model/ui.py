from typing import Dict, List


class UiPlayerShips:
    def __init__(self, username: str, ships: Dict[str, int], total_sig: int):
        self.username = username
        self.ships = ships
        self.total_sig = total_sig


class UiFleets:
    def __init__(self, players: List[UiPlayerShips]):
        self.players = players
