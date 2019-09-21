from flask import Flask
from injector import inject

from exiltool.map.service import MapService
from exiltool.services.auth import AuthenticationService
from exiltool.services.health import HealthService
from exiltool.services.resa import ResaService
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
        self.services.install(self.flask, MapService)
        self.services.install(self.flask, ScriptService)
        self.services.install(self.flask, WebService)
        self.services.install(self.flask, AuthenticationService)
        self.services.install(self.flask, HealthService)
        self.services.install(self.flask, ResaService)
        return self.flask
