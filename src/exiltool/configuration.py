import os


class Configuration:
    def __init__(self):
        self.mongo_host = os.environ.get('MONGO_HOST', 'localhost')
        self.mongo_port = int(os.environ.get('MONGO_PORT', 27017))
        self.mongo_db = os.environ.get('MONGO_DB', 'exiltool')
