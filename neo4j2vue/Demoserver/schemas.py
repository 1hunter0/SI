from pydantic import BaseModel
from uuid import UUID
from typing import Union


class Query(BaseModel):
    response: list


class GUID(BaseModel):
    id: str


class Message(BaseModel):
    message: str
