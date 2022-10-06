from typing import Union
from enum import Enum

from pydantic import BaseModel

class level(Enum):
    high = 3
    mideum = 2
    low = 1
    unkonwn = 0

class base(BaseModel):
    threat_level: level
    Confidence: level
    source: str


#情报模型层次
class IP(BaseModel):
    ip: str
    country: str
    province: str
    city: str
    latitude: float
    longitude: float


class IP_threat(BaseModel):
    #todo
    pass



class DNS(BaseModel):
    name: str
    description: Union[str, None] = None


class FILE(BaseModel):
    name: str
    description: Union[str, None] = None