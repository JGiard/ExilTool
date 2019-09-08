from typing import Optional
from uuid import uuid4

from injector import inject
from pyckson import parse, serialize
from pymongo import ASCENDING
from pymongo.database import Database
from werkzeug.security import generate_password_hash

from exiltool.model.user import User


class UserRepository:
    @inject
    def __init__(self, db: Database):
        self.collection = db['users']
        self.collection.create_index([('username', ASCENDING)], unique=True)

    def get_user(self, username) -> Optional[User]:
        doc = self.collection.find_one({'username': username})
        if doc:
            return parse(User, doc)

    def create(self, username: str, password: str):
        user = User(username, generate_password_hash(password), False, str(uuid4()))
        self.collection.insert(serialize(user))

    def get_by_apikey(self, apikey: str) -> Optional[User]:
        doc = self.collection.find_one({'apikey': apikey})
        if doc:
            return parse(User, doc)
