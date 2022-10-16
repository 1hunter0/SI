import datetime
import json
from typing import List
from fastapi import APIRouter, Depends, UploadFile
from app.schemas import schema_ip
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.crud import crud_ip

router_url = APIRouter(
    prefix="/urls",
    tags=["urls"]
)

###############
# dev
@router_url.get("/inner/{url}")
def get_inner_url(url: str):
    url_info = json.load(open('app/api/URL.json', 'r', encoding="utf-8"))
    return url_info

################

#
# @router_ip.get("/inner/{ip}", response_model=schema_ip.IpInner)
# def get_inner_ip(ip: str, db: Session = Depends(get_db)):
#     db_ip = crud_ip.get_inner_ip(db, ip)
#     return db_ip
#
#
# @router_ip.post("/upload", response_model=dict)
# def create_alarms_by_file(file: UploadFile, db: Session = Depends(get_db)):
#     add_dict = {
#         'ip_list': [],
#         'alarm_list': []
#     }
#     for line in file.file:
#         log_json = json.loads(line)
#         alarm = schema_ip.Alarm()
#         ip = schema_ip.IpBase()
#         # todo: 解析该行日志，填充ip对象和alarm对象，调用create_ip和create_alarm持久化；填充ip_list和alarm_list并返回
#
#     return add_dict
#
#
# @router_ip.get("/test/alarm")
# def test_add_alarm(db: Session = Depends(get_db)):
#     alarm = schema_ip.Alarm(event_id=1, ip_subject='22.11.1.158', ip_object='22.11.1.158', dev_info='asd',
#                             hostname='klljkh', timestamp=datetime.datetime.now())
#     db_alarm = crud_ip.create_alarm(db, alarm)
#     return db_alarm
#
#
# @router_ip.get("/test/ip")
# def test_add_ip(db: Session = Depends(get_db)):
#     ip = schema_ip.IpBase(ip='1.2.3.4', country='中国')
#     db_ip = crud_ip.create_ip(db, ip)
#     return db_ip
