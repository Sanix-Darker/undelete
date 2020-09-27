from jsonschema import validate, ValidationError
from pymongo import MongoClient

from app.settings import *



class DATABASE:
    def __init__(self, database_name):
        # creation of MongoClient
        client = MongoClient()
        # Connect with the portnumber and host
        client = MongoClient(DATABASE_HOST)
        # Access database
        self.database_name = database_name
        self.db = client[self.database_name]


class Model:
    def __init__(self, json=None):
        if json is None:
            json = {"_id": "test"}
        self.json = json
        self.set_collection()
        self.schema = {}

    def set_collection(self, collection_name="model_example"):
        self.collection = DATABASE(DATABASE_NAME).db[collection_name]

    def set_json(self, json):
        self.json = json

    def save(self):
        if self.validate_input(self.json)[0]:
            self.collection.insert(self.json)
        else:
            print("[+] JSON not valid for save()")

    def update(self, param, json):
        if self.validate_input(json)[0]:
            self.collection.update_one(param, {"$set": json}, upsert=True)
        else:
            print("[+] JSON not valid for update()")

    def delete(self, param):
        self.collection.delete_many(param)

    def count(self, param):
        return self.collection.find(param).count()

    def find_by(self, param):
        return self.collection.find(param)

    def find_all(self):
        return self.collection.find()

    def close(self):
        self.collection.close()

    def validate_input(self, data):
        try:
            validate(data, self.schema)
            return True, ""
        except ValidationError as e:
            return False, str(e)
