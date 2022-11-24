import datetime
from typing import Union
from typing import List
from pydantic import BaseModel
import decimal
from .schema_file import FileBase


class IpBase(BaseModel):
    ip: Union[str, None] = None
    country: Union[str, None] = None
    province: Union[str, None] = None
    city: Union[str, None] = None
    isp: Union[str, None] = None
    latitude: Union[decimal.Decimal, None] = None
    longitude: Union[decimal.Decimal, None] = None
    degree: Union[str, None] = None
    confidence: Union[str, None] = None
    source: Union[str, None] = None


class AlarmBase(BaseModel):
    event_id: Union[int, None] = None
    ip_subject: Union[str, None] = None
    ip_object: Union[str, None] = None
    dev_info: Union[str, None] = None
    hostname: Union[str, None] = None
    timestamp: datetime.datetime = None


class Alarm(AlarmBase):
    attack_stage: Union[str, None] = None
    attack_status: Union[str, None] = None
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


class IpInner(BaseModel):
    subject_alarms: List[Alarm] = []
    object_alarms: List[Alarm] = []

    class Config:
        orm_mode = True


class IPInfoResponse(BaseModel):
    IpInfo: IpBase = None
    Alarms: IpInner = None
    Samples: FileBase = None


class IpListResponse(BaseModel):
    TotalNumber: int
    CurrentPage: int
    IPList: List[IpBase] = []


class PageResponse(BaseModel):
    PageNumber: int
