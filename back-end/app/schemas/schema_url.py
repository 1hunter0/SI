from typing import Union
from pydantic import BaseModel


class UrlBase(BaseModel):
    url: Union[str, None] = None
    history_dns: Union[str, None] = None
    severity: Union[int, None] = None
