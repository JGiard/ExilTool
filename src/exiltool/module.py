from pathlib import Path

from flask import Flask
from injector import Module, provider, threadlocal, Binder
from pymongo import MongoClient
from pymongo.database import Database


class ExilModule(Module):
    def configure(self, binder: Binder):
        pass

    @provider
    @threadlocal
    def get_mongo(self) -> MongoClient:
        return MongoClient()

    @provider
    def get_database(self, client: MongoClient) -> Database:
        return client.get_database('exiltool')

    @provider
    def get_app(self) -> Flask:
        return Flask('ExilTool', template_folder=str(Path(__file__).parent / "templates"))
