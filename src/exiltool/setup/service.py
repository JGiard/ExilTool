from flask import Flask
from injector import inject, singleton

from exiltool.backend.router import ServiceRouter


class ServiceInstaller:
    @inject
    def __init__(self, router: ServiceRouter):
        self.router = router

    def install(self, flask: Flask, service):
        singleton(service)
        self.router.route(flask, service)
