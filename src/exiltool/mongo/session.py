from injector import inject
from pymongo.database import Database


class SessionRepository:
    @inject
    def __init__(self, db: Database):
        pass
