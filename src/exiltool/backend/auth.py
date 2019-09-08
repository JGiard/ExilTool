import logging
from typing import Optional

from flask import session, request, redirect, abort
from injector import inject
from werkzeug.exceptions import HTTPException
from werkzeug.security import check_password_hash

from exiltool.model.user import User
from exiltool.mongo.users import UserRepository

logger = logging.getLogger(__name__)


class Authenticator:
    @inject
    def __init__(self, users: UserRepository):
        self.users = users

    def session(self) -> Optional[User]:
        if 'username' in session:
            user = self.users.get_user(session['username'])
            return user

    def direct(self, username: str, password: str) -> Optional[User]:
        potential_user = self.users.get_user(username)
        if not potential_user:
            logger.warning('user {} does not exists'.format(username))
            abort(401)
        if not potential_user.active:
            logger.warning('user {} is not active'.format(username))
            abort(401)
        if not check_password_hash(potential_user.crypted_password, password):
            logger.warning('user {} password does not match'.format(username))
            abort(401)

        return potential_user

    def apikey(self, apikey: str):
        potential_user = self.users.get_by_apikey(apikey)
        if not potential_user:
            logger.warning('invalid api key {}'.format(apikey))
            abort(401)

        return potential_user

    def get_user(self) -> User:
        user = self.session()
        if user:
            return user
        if request.authorization:
            user = self.direct(request.authorization.username, request.authorization.password)
            if user:
                return user
        if 'ApiKey' in request.headers:
            user = self.apikey(request.headers['ApiKey'])
            if user:
                return user

        logger.warning('Could not authenticate request')
        abort(401)


class AuthenticationProxy:
    @inject
    def __init__(self, auth: Authenticator):
        self.auth = auth

    def check_login(self) -> User:
        try:
            user = self.auth.get_user()
            session['username'] = user.username
            return user
        except HTTPException:
            if not request.path.startswith('/api'):
                abort(redirect('/login'))
            else:
                raise
