from typing import Union
from pydantic import BaseModel


class DnsBase(BaseModel):
    dns: Union[str, None] = None
    analysis_ip: Union[str, None] = None
    related_url: Union[str, None] = None
    severity: Union[str, None] = None
    sample: Union[str, None] = None
    confidence: Union[str, None] = None
    scene: Union[str, None] = None
    open_source: Union[str, None] = None
