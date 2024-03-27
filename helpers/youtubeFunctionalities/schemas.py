from pydantic import BaseModel
from typing import List
import json

class JsonModel(BaseModel):
    def toJson(cls):
        return json.loads(cls.model_dump_json())
    
class Message(JsonModel):
    id: str
    userId: str
    text: str
    pubTime: str
    
class Chat(JsonModel):
    messages: List[Message]
    nextPage: str