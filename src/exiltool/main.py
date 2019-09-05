from flask import Flask
from injector import Injector
from pyramid.response import Response

from exiltool.app import ExilApp
from exiltool.module import ExilModule


def hello_world(request):
    return Response('Hello World!')


def get_flask_app() -> Flask:
    injector = Injector(ExilModule())
    app = injector.create_object(ExilApp)
    return app.install()


app = get_flask_app()
