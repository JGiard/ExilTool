from flask import Flask, render_template
from injector import inject

from exiltool.backend.router import ServiceRouter
from exiltool.services.map import MapService
from exiltool.services.script import ScriptService
from exiltool.services.web import WebService


class ExilApp:
    @inject
    def __init__(self, flask: Flask, router: ServiceRouter):
        self.flask = flask
        self.router = router

    def install(self) -> Flask:
        self.router.install(self.flask, MapService)
        self.router.install(self.flask, ScriptService)
        self.router.install(self.flask, WebService)
        return self.flask
