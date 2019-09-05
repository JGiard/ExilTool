from functools import wraps

from flask import request
from injector import Injector, inject
from pyckson import serialize, parse

from exiltool.backend.decorators import ROUTE_DATA_TYPE_ATTR


class ServiceRunner:
    @inject
    def __init__(self, injector: Injector):
        self.injector = injector

    def run(self, cls, method, *args, **kwargs):
        instance = self.injector.create_object(cls)
        if request.method == 'POST' and hasattr(method, ROUTE_DATA_TYPE_ATTR):
            kwargs['data'] = parse(getattr(method, ROUTE_DATA_TYPE_ATTR), request.get_json(force=True))

        reply = method(instance, *args, **kwargs)
        if reply is None:
            return '', 200
        elif isinstance(reply, dict):
            return reply
        elif isinstance(reply, str):
            return reply
        else:
            return serialize(reply)

    def wraps(self, cls, method):
        @wraps(method)
        def wrapper(*args, **kwargs):
            return self.run(cls, method, *args, **kwargs)

        return wrapper
