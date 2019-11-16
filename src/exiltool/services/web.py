from collections import Counter, defaultdict

from flask import render_template, request
from injector import inject

from exiltool.backend.decorators import route, noauth
from exiltool.fleets.model.ui import UiPlayerShips, UiFleets
from exiltool.fleets.repository import FleetsRepository
from exiltool.map.converter import MapConverter
from exiltool.map.model.domain import Place
from exiltool.map.repository import MapRepository
from exiltool.model.user import User
from exiltool.mongo.resa import ResaRepository


class WebService:
    @inject
    def __init__(self, sectors: MapRepository, converter: MapConverter, resas: ResaRepository,
                 fleets: FleetsRepository):
        self.sectors = sectors
        self.converter = converter
        self.resas = resas
        self.fleets = fleets

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
        all_resa = list(self.resas.get_all())
        sector = self.converter.sector_to_ui(self.sectors.get_sector(galaxy, sector), all_resa)
        return render_template('map.html', sector=sector)

    @route('/resa')
    def resa(self, user: User):
        all_resa = sorted(list(self.resas.get_all()))
        return render_template('resa.html', resas=all_resa, username=user.username)

    def is_spe(self, place: Place):
        return 'Planète extraordinaire' in place.specials or 'Présence de vers de sable' in place.specials

    @route('/tops')
    def tops(self, user: User):
        galaxy = int(request.args.get('g', 1))
        top_mineral = [self.converter.place_to_ui(place) for place in self.sectors.top_mineral(galaxy)]
        top_mineral = sorted(top_mineral, key=lambda x: x.planet.mineral_prod, reverse=True)[:50]
        top_hydro = [self.converter.place_to_ui(place) for place in self.sectors.top_hydro(galaxy)]
        top_hydro = sorted(top_hydro, key=lambda x: x.planet.hydrocarbon_prod, reverse=True)[:50]
        top_land = [self.converter.place_to_ui(place) for place in self.sectors.top_land(galaxy)]
        top_land = sorted(top_land, key=lambda x: x.planet.land, reverse=True)[:50]
        top_spe = [self.converter.place_to_ui(place) for place in self.sectors.top_spe(galaxy)]
        top_spe = sorted(top_spe, key=lambda x: x.planet.land, reverse=True)
        top_spe = list(filter(lambda p: self.is_spe(p), top_spe))[:100]
        resas = self.resas.get_all()
        resas = {'{}.{}.{}'.format(r.galaxy, r.sector, r.position): r.username for r in resas}
        return render_template('tops.html', galaxy=galaxy, top_mineral=top_mineral, top_hydro=top_hydro,
                               top_land=top_land, resas=resas, top_spe=top_spe)

    @route('/fleets')
    def fleets(self):
        ships_by_player = defaultdict(Counter)
        sig_by_player = Counter()
        for fleet in self.fleets.get_all():
            for ship in fleet.ships:
                ships_by_player[fleet.username][ship.ship.name] += ship.quantity
                ships_by_player['Total'][ship.ship.name] += ship.quantity
                sig_by_player[fleet.username] += ship.ship.signature * ship.quantity
                sig_by_player['Total'] += ship.ship.signature * ship.quantity

        data = [UiPlayerShips(player, ships, sig_by_player[player]) for player, ships in ships_by_player.items()]
        return render_template('fleets.html', fleets=UiFleets(data))
