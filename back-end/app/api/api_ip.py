import datetime
import json
from typing import List
from fastapi import APIRouter, Depends, UploadFile
from pymysql import IntegrityError

import app.models.models
from app.schemas import schema_ip, schema_response, schema_url, schema_dns
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.crud import crud_ip
from app.global_variable import *
from app.parser import innerparser

router_ip = APIRouter(
    prefix="/ips",
    tags=["ips"]
)


###############
# dev
@router_ip.get("/inner/{ip}")
def get_inner_ip(ip: str):
    ip_info = json.load(open('app/api/IP.json', 'r', encoding="utf-8"))
    return ip_info


################

@router_ip.get("/info", response_model=schema_response.MyResponse)
def get_file(ip: str, db: Session = Depends(get_db)):
    print(ip)
    ip_info = crud_ip.get_inner_ip(db, ip)
    if not ip_info:
        return schema_response.MyResponse(
            ErrCode=FAIL,
            ErrMessage="数据库中未找到相关IP"
        )
    return schema_response.MyResponse(
        ErrCode=SUCCESS,
        Data=ip_info
    )


@router_ip.post("/upload", response_model=schema_response.MyResponse)
def create_alarms_by_file(file: UploadFile, db: Session = Depends(get_db)):
    print(file.filename)
    create_ip_num = 0
    create_alarm_num = 0
    for line in file.file:
        data = json.loads(line)
        dataParser = innerparser.InnerParser(data)
        for ip_ in dataParser.ip:
            if ip_.ip is not None:
                try:
                    ipinfo = crud_ip.create_ip(db, ip_)
                    if ipinfo.ip:
                        create_ip_num += 1
                except Exception as e:
                    print(e)
        if dataParser.ip_alarm is not None:
            try:
                alarminfo = crud_ip.create_alarm(db, dataParser.ip_alarm)
                if alarminfo.ip_object:
                    create_alarm_num += 1
            except Exception as e:
                print(e)

        """
        todo: dns+url
        """
    message = "插入ip:" + str(create_ip_num) + "插入alarm:" + str(create_alarm_num)
    return schema_response.MyResponse(
        ErrCode=SUCCESS,
        Data=message
    )
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
