from flask import render_template

from exiltool.backend.decorators import route, noauth


class WebService:
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
