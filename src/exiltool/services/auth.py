import logging

from flask import abort, session, redirect
from injector import inject

from exiltool.backend.auth import Authenticator
from exiltool.backend.decorators import route, noauth
from exiltool.model.user import LoginRequest, Registration
from exiltool.mongo.users import UserRepository

logger = logging.getLogger(__name__)


class AuthenticationService:
    @inject
    def __init__(self, users: UserRepository, auth: Authenticator):
        self.users = users
        self.auth = auth

    @noauth
    @route('/api/login', method='POST')
    def login(self, data: LoginRequest):
        user = self.auth.direct(data.username, data.password)

        session['username'] = user.username

    @noauth
    @route('/api/logout')
    def logout(self):
        session.clear()
        redirect('/')

    @noauth
    @route('/api/register', method='POST')
    def register(self, data: Registration):
        if self.users.get_user(data.username):
            logger.warning('user {} already exists'.format(data.username))
            abort(409)
        self.users.create(data.username, data.password)
