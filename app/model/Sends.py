from app.model import *


class Sends(Model.Model):
    def __init__(self, json=None):
        super().__init__(json)
        if json is None:
            json = {"_id": "test"}
        self.json = json
        
        # We set the collection name
        self.set_collection("sends")

        # We set our custom schema
        self.schema = {
            "type": "object",
            "required": ["hash", "chat-ids"],
            "properties": {
                "hash": {"type": "string"},
                "chat-ids": {
                    "type": ["array", "null"],
                    "items": {
                        "type": ["string", "null"],
                    }
                }
            }
        }
