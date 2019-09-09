from flask import Flask
from flask_session import Session
from injector import inject
from pymongo import MongoClient

from exiltool.configuration import Configuration


class FlaskExtInstaller:
    @inject
    def __init__(self, mongo: MongoClient, conf: Configuration):
        self.mongo = mongo
        self.conf = conf

    def install_session(self, flask: Flask):
        flask.config['SESSION_TYPE'] = 'mongodb'
        flask.config['SESSION_MONGODB'] = self.mongo
        flask.config['SESSION_MONGODB_DB'] = self.conf.mongo_db
        Session().init_app(flask)
