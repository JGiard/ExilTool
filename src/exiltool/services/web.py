from collections import Counter

from flask import render_template, request
from injector import inject

from exiltool.backend.decorators import route, noauth
from exiltool.fleets.model.ui import UiPlayerShips, UiFleets
from exiltool.fleets.repository import ShipsRepository
from exiltool.map.converter import MapConverter
from exiltool.map.repository import MapRepository
from exiltool.model.user import User
from exiltool.mongo.resa import ResaRepository


class WebService:
    @inject
    def __init__(self, sectors: MapRepository, converter: MapConverter, resas: ResaRepository,
                 ships: ShipsRepository):
        self.sectors = sectors
        self.converter = converter
        self.resas = resas
        self.ships = ships

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

    @route('/tops')
    def tops(self, user: User):
        galaxy = int(request.args.get('g', 1))
        top_mineral = [self.converter.place_to_ui(place) for place in self.sectors.top_mineral(galaxy)]
        top_mineral = sorted(top_mineral, key=lambda x: x.planet.mineral_prod, reverse=True)[:50]
        top_hydro = [self.converter.place_to_ui(place) for place in self.sectors.top_hydro(galaxy)]
        top_hydro = sorted(top_hydro, key=lambda x: x.planet.hydrocarbon_prod, reverse=True)[:50]
        top_land = [self.converter.place_to_ui(place) for place in self.sectors.top_land(galaxy)]
        top_land = sorted(top_land, key=lambda x: x.planet.land, reverse=True)[:50]
        resas = self.resas.get_all()
        resas = {'{}.{}.{}'.format(r.galaxy, r.sector, r.position): r.username for r in resas}
        return render_template('tops.html', galaxy=galaxy, top_mineral=top_mineral, top_hydro=top_hydro,
                               top_land=top_land, resas=resas)

    @route('/fleets')
    def fleets(self):
        players = []
        total_ships = Counter()
        total_sig = 0
        for player in self.ships.get_all():
            ships = {}
            player_sig = 0
            for player_ship in player.ships:
                ships[player_ship.ship.name] = player_ship.quantity
                total_ships[player_ship.ship.name] += player_ship.quantity
                player_sig += player_ship.ship.signature * player_ship.quantity
            total_sig += player_sig
            players.append(UiPlayerShips(player.username, ships, player_sig))
        total = UiPlayerShips('Total', total_ships, total_sig)
        return render_template('fleets.html', fleets=UiFleets([total] + players))
