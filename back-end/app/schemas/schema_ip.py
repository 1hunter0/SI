import datetime
from typing import Union
from typing import List
from pydantic import BaseModel
import decimal


class IpBase(BaseModel):
    ip: str
    country: Union[str, None] = None
    province: Union[str, None] = None
    city: Union[str, None] = None
    isp: Union[str, None] = None
    latitude: Union[decimal.Decimal, None] = None
    longitude: Union[decimal.Decimal, None] = None


class AlarmBase(BaseModel):
    event_id: int
    ip_subject: str
    ip_object: str
    dev_info: str
    hostname: str
    timestamp: datetime.datetime


class Alarm(AlarmBase):
    attack_stage: Union[str, None] = None
    attack_status: Union[int, None] = None
    dev_category: Union[str, None] = None
    dev_rule: Union[str, None] = None
    degree: Union[str, None] = None
    forbid_status: Union[str, None] = None
    req_method: Union[str, None] = None
    threat_phase: Union[str, None] = None
    kill_chain: Union[str, None] = None
    kill_chain_all: Union[str, None] = None
    attack_type: Union[str, None] = None
    attack_type_all: Union[str, None] = None
    att_ck_all: Union[str, None] = None
    att_ck: Union[str, None] = None

    class Config:
        orm_mode = True


class IpInner(IpBase):
    subject_alarms: List[Alarm] = []
    object_alarms: List[Alarm] = []

    class Config:
        orm_mode = True