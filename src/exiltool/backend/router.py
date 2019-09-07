import inspect
from typing import Iterable, Callable

from flask import Flask
from injector import inject

from exiltool.backend.decorators import ROUTE_ATTR, ROUTE_METHOD_ATTR
from exiltool.backend.runner import ServiceRunner


class ServiceRouter:
    @inject
    def __init__(self, runner: ServiceRunner):
        self.runner = runner

    def route(self, flask: Flask, cls):
        for method in self.find_routed_methods(cls):
            path = getattr(method, ROUTE_ATTR)
            methods = [getattr(method, ROUTE_METHOD_ATTR)]
            endpoint = '{}.{}'.format(cls.__name__, method.__name__)

            flask.route(path, methods=methods, endpoint=endpoint)(self.runner.get_runner(cls, method))

    def find_routed_methods(self, cls) -> Iterable[Callable]:
        for name, method in inspect.getmembers(cls):
            if hasattr(method, ROUTE_ATTR):
                yield method
