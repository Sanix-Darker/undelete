from app.model import *


class WatchMe(Model.Model):
    def __init__(self, json=None):
        super().__init__(json)
        if json is None:
            json = {"_id": "test"}
        self.json = json
        
        # We set the collection name
        self.set_collection("watchme")

        # We set our custom schema
        self.schema = {
            "type": "object",
            "required": ["origin_id", "origin_url", "chat_ids"],
            "properties": {
                "origin_url": {"type": "string"},
                "replies": {
                    "type": ["array", "null"],
                    "items": {
                        "type": ["string", "null"],
                    }
                }
            }
        }
