from functools import wraps
from inspect import signature
from typing import Optional

from flask import request
from injector import Injector, inject
from pyckson import serialize, parse

from exiltool.backend.auth import AuthenticationProxy
from exiltool.backend.decorators import NO_AUTH_ATTR
from exiltool.model.user import User


class ServiceRunner:
    @inject
    def __init__(self, injector: Injector, auth: AuthenticationProxy):
        self.injector = injector
        self.auth = auth

    def run(self, cls, method, flask_params: dict):
        instance = self.injector.create_object(cls)
        user = None
        if not getattr(method, NO_AUTH_ATTR, False):
            user = self.auth.check_login()

        reply = method(instance, flask_params, user)
        return self.handle_reply(reply)

    def handle_reply(self, reply):
        if reply is None:
            return '', 204
        elif isinstance(reply, dict):
            return reply
        elif isinstance(reply, str):
            return reply
        elif isinstance(reply, tuple):
            return reply
        else:
            return serialize(reply)

    def get_runner(self, cls, method):
        @wraps(method)
        def wrapper(**flask_params):
            return self.run(cls, self.prepare(method), flask_params)

        return wrapper

    def prepare(self, method):
        parameters = signature(method).parameters

        @wraps(method)
        def wrapper(instance, flask_params: dict, user: Optional[User]):
            fargs = flask_params.copy()
            if 'data' in parameters and request.method == 'POST':
                data = request.get_json(force=True)
                self.fix_arrays(data)
                fargs['data'] = parse(parameters['data'].annotation, data)
            if user and 'user' in parameters and parameters['user'].annotation == User:
                fargs['user'] = user
            return method(instance, **fargs)

        return wrapper

    def fix_arrays(self, data):
        if type(data) is list:
            if data[0] == 0:
                del data[0]
            for item in data:
                self.fix_arrays(item)
        if type(data) is dict:
            for item in data.values():
                self.fix_arrays(item)
