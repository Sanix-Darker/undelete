from app.model import Database
from jsonschema import validate, ValidationError


class Model:
    def __init__(self, json=None):
        if json is None:
            json = {"_id": "test"}
        self.json = json
        self.database = Database
        self.collection = self.database.get_db()["model_example"]
        self.schema = {}

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