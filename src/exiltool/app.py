from flask import Flask, render_template
from injector import inject

from exiltool.backend.router import ServiceRouter
from exiltool.services.map import MapService
from exiltool.services.script import ScriptService


class ExilApp:
    @inject
    def __init__(self, flask: Flask, router: ServiceRouter):
        self.flask = flask
        self.router = router

    def install(self) -> Flask:
        self.router.install(self.flask, MapService)
        self.router.install(self.flask, ScriptService)
        return self.flask
