from typing import List
from pydantic import BaseModel


class User(BaseModel):
    room: str
    name: str
    messages: List[str] = []


class Message(BaseModel):
    text: str
    author: str

