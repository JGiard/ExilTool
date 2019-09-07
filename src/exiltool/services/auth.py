import logging

from flask import abort, session, redirect
from injector import inject
from werkzeug.security import check_password_hash

from exiltool.backend.decorators import route, noauth
from exiltool.model.user import LoginRequest, Registration
from exiltool.mongo.users import UserRepository

logger = logging.getLogger(__name__)


class AuthenticationService:
    @inject
    def __init__(self, users: UserRepository):
        self.users = users

    @noauth
    @route('/api/login', method='POST')
    def login(self, data: LoginRequest):
        potential_user = self.users.get_user(data.username)
        if not potential_user:
            logger.warning('user {} does not exists'.format(data.username))
            abort(401)
        if not potential_user.active:
            logger.warning('user {} is not active'.format(data.username))
            abort(401)
        if not check_password_hash(potential_user.crypted_password, data.password):
            logger.warning('user {} password does not match'.format(data.username))
            abort(401)

        session['username'] = potential_user.username

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
