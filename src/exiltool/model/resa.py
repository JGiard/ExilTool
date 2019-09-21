from enum import Enum
from typing import Optional

from autovalue import autovalue


@autovalue
class Resa:
    def __init__(self, username: str, galaxy: int, sector: int, position: int):
        self.username = username
        self.galaxy = galaxy
        self.sector = sector
        self.position = position

    def __lt__(self, other: 'Resa'):
        return (self.galaxy, self.sector, self.position) < (other.galaxy, other.sector, other.position)


class ResaErrorCode(Enum):
    limit_reached = 1
    already_taken = 2


class ResaResult:
    def __init__(self, success: bool, code: Optional[int] = None):
        self.success = success
        self.code = code
