from flask import render_template, request

from exiltool.backend.decorators import route


class WebService:
    @route('/')
    def home(self):
        return render_template('index.html')

    @route('/login')
    def login(self):
        return render_template('login.html')
