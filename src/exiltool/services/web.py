from flask import render_template, request
from injector import inject

from exiltool.backend.decorators import route, noauth
from exiltool.mongo.sectors import SectorsRepository


class WebService:
    @inject
    def __init__(self, sectors: SectorsRepository):
        self.sectors = sectors

    @route('/')
    def home(self):
        return render_template('index.html')

    @noauth
    @route('/login')
    def login(self):
        return render_template('login.html')

    @noauth
    @route('/register')
    def register(self):
        return render_template('register.html')

    @noauth
    @route('/map')
    def map(self):
        galaxy = int(request.args.get('g', 1))
        sector = int(request.args.get('s', 1))
        return render_template('map.html', sector=self.sectors.get_sector(galaxy, sector))
