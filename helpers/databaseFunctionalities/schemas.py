from pydantic import BaseModel
from datetime import datetime
import json

class JsonModel(BaseModel):
    def toJson(cls):
        return json.loads(cls.model_dump_json())
    
class Viewer(JsonModel):
    name: str
    channelId: str
    points: int
    mod: bool
    lastUpdate: datetime
    newMessage: bool = False