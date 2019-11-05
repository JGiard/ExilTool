from typing import List

from injector import inject

from exiltool.backend.decorators import route
from exiltool.model.resa import Resa, ResaErrorCode, ResaResult
from exiltool.model.user import User
from exiltool.mongo.resa import ResaRepository


class ResaService:
    @inject
    def __init__(self, repository: ResaRepository):
        self.repository = repository

    @route('/api/resa')
    def get(self) -> List[Resa]:
        resas = sorted(list(self.repository.get_all()))
        return resas

    @route('/api/resa/g/<int:galaxy>/s/<int:sector>/p/<int:position>', method='POST')
    def claim(self, user: User, galaxy: int, sector: int, position: int):
        if len(list(self.repository.get_by_user(user.username))) >= 4:
            return ResaResult(False, ResaErrorCode.limit_reached.value)
        if self.repository.get_by_pos(galaxy, sector, position) is not None:
            return ResaResult(False, ResaErrorCode.already_taken.value)
        self.repository.save(Resa(user.username, galaxy, sector, position))
        return ResaResult(True)

    @route('/api/resa/g/<int:galaxy>/s/<int:sector>/p/<int:position>', method='DELETE')
    def remove(self, user: User, galaxy: int, sector: int, position: int):
        resa = self.repository.get_by_pos(galaxy, sector, position)
        assert resa is not None and resa.username == user.username
        self.repository.remove(resa)
