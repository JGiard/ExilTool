import os


class Configuration:
    def __init__(self):
        self.mongo_host = os.environ.get('MONGO_HOST', os.environ.get('MONGODB_ADDON_HOST', 'localhost'))
        self.mongo_port = int(os.environ.get('MONGO_PORT', os.environ.get('MONGODB_ADDON_PORT', 27017)))
        self.mongo_db = os.environ.get('MONGO_DB', os.environ.get('MONGODB_ADDON_DB', 'exiltool'))
        self.mongo_user = os.environ.get('MONGO_USER', os.environ.get('MONGODB_ADDON_USER', None))
        self.mongo_password = os.environ.get('MONGO_PASSWORD', os.environ.get('MONGODB_ADDON_PASSWORD', None))
        self.mongo_uri = os.environ.get('MONGO_URI', os.environ.get('MONGODB_ADDON_URI', None))
