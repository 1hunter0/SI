from typing import Union

from pydantic import BaseModel


class LoginIn(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    token: Union[str, None] = None


class UserInfo(BaseModel):
    username: str
