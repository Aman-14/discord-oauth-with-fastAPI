from decouple import config
from motor.motor_asyncio import AsyncIOMotorClient


class Database:
    def __init__(self):
        self._initialized = False
        self._pool = None
        self._models = {}

    def connect(self):
        try:
            self._pool = AsyncIOMotorClient(config("DATABASE_URI")).fastapidb
        except Exception as err:
            print(err)
            exit()
        else:
            self._initialized = True
            print("db initalized", self._models)
            # attaching collection object to their respective model
            for model, collection in self._models.items():
                model.collection = self.pool[collection]

    @property
    def pool(self):
        return self._pool

    # registers models so later we can attach collection object to them
    def register(self, collection):
        def function(cls):
            self._models[cls] = collection
            return cls

        return function


db = Database()
