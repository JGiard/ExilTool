from flask import session, request, redirect, abort
from injector import inject

from exiltool.model.user import User
from exiltool.mongo.users import UserRepository


class AuthenticationProxy:
    @inject
    def __init__(self, users: UserRepository):
        self.users = users

    def check_login(self) -> User:
        if 'username' in session:
            user = self.users.get_user(session['username'])
            return user

        if request.path.startswith('/api'):
            abort(401)
        else:
            abort(redirect('/login'))
