from pathlib import Path

from flask import Flask
from injector import Module, provider, threadlocal, Binder
from pymongo import MongoClient
from pymongo.database import Database

from exiltool.configuration import Configuration


class ExilModule(Module):
    def configure(self, binder: Binder):
        binder.bind(Configuration, to=Configuration())

    @provider
    @threadlocal
    def get_mongo(self, conf: Configuration) -> MongoClient:
        if conf.mongo_uri:
            return MongoClient(conf.mongo_uri)
        else:
            return MongoClient(conf.mongo_host, conf.mongo_port, username=conf.mongo_user, password=conf.mongo_password)

    @provider
    def get_database(self, client: MongoClient, conf: Configuration) -> Database:
        return client.get_database(conf.mongo_db)

    @provider
    def get_app(self) -> Flask:
        return Flask('ExilTool', template_folder=str(Path(__file__).parent / "templates"))
