from typing import Union

from pydantic import BaseModel

#情报模型层次
class IP(BaseModel):
    name: str
    description: Union[str, None] = None


class DNS(BaseModel):
    name: str
    description: Union[str, None] = None


class FILE(BaseModel):
    name: str
    description: Union[str, None] = None