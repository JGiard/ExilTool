from flask import render_template, request, make_response
from injector import inject

from exiltool.backend.decorators import route, noauth
from exiltool.mongo.sectors import SectorsRepository


class HealthService:
    @noauth
    @route('/health')
    def health(self):
        return '', 200
