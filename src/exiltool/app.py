from flask import Flask
from injector import inject

from exiltool.services.auth import AuthenticationService
from exiltool.services.health import HealthService
from exiltool.services.map import MapService
from exiltool.services.script import ScriptService
from exiltool.services.web import WebService
from exiltool.setup.extensions import FlaskExtInstaller
from exiltool.setup.service import ServiceInstaller


class ExilApp:
    @inject
    def __init__(self, flask: Flask, services: ServiceInstaller, extensions: FlaskExtInstaller):
        self.flask = flask
        self.services = services
        self.extensions = extensions

    def install(self) -> Flask:
        self.extensions.install_session(self.flask)
        self.extensions.install_mongo(self.flask)
        self.services.install(self.flask, MapService)
        self.services.install(self.flask, ScriptService)
        self.services.install(self.flask, WebService)
        self.services.install(self.flask, AuthenticationService)
        self.services.install(self.flask, HealthService)
        return self.flask
