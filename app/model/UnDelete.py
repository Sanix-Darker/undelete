from app.model import *


class UnDelete(Model.Model):
    def __init__(self, json=None):
        super().__init__(json)
        if json is None:
            json = {"_id": "test"}
        self.json = json
        
        # We set the collection name
        self.set_collection("undelete")

        # We set our custom schema
        self.schema = {
            "type": "object",
            "required": ["chat_id", "origin", "replies"],
            "properties": {
                "origin": {"type": "object"},
                "chat_id": {"type": "string"},
                "replies": {
                    "type": ["array", "null"],
                    "items": {
                        "type": ["object", "null"],
                        "properties": {
                            "link": {
                                "type": ["string", "null"]
                            },
                            "avatar": {
                                "type": ["string", "null"]
                            },
                            "author-name": {
                                "type": ["string", "null"]
                            },
                            "author-link": {
                                "type": ["string", "null"]
                            },
                            "tweet-text": {
                                "type": ["string", "null"]
                            },
                        },
                    }
                }
            }
        }
