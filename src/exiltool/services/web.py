from flask import render_template, request
from injector import inject

from exiltool.backend.decorators import route, noauth
from exiltool.map.converter import MapConverter
from exiltool.map.repository import MapRepository
from exiltool.model.user import User
from exiltool.mongo.resa import ResaRepository


class WebService:
    @inject
    def __init__(self, sectors: MapRepository, converter: MapConverter, resas: ResaRepository):
        self.sectors = sectors
        self.converter = converter
        self.resas = resas

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

    @route('/map')
    def map(self):
        galaxy = int(request.args.get('g', 1))
        sector = int(request.args.get('s', 1))
        sector = self.converter.sector_to_ui(self.sectors.get_sector(galaxy, sector))
        return render_template('map.html', sector=sector)

    @route('/resa')
    def resa(self, user: User):
        all_resa = sorted(list(self.resas.get_all()))
        return render_template('resa.html', resas=all_resa, username=user.username)
