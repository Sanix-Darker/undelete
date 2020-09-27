from pymongo import MongoClient

from settings import *

class DATABASE:
    def __init__(self, database_name):
        # creation of MongoClient
        client = MongoClient()
        # Connect with the portnumber and host
        client = MongoClient(DATABASE_HOST)
        # Access database
        self.database_name = database_name
        self.db = client[self.database_name]


def get_db():
    DB = DATABASE(DATABASE_NAME)
    return DB.db
