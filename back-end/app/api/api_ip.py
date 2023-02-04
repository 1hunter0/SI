import datetime
import json
import math
from typing import List
from fastapi import APIRouter, Depends, UploadFile
from pymysql import IntegrityError

import app.models.models
import model.models
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
from app.utils import serialize


def model2alarmlist(ipalarm):
    alarmlist = []
    for alarm in ipalarm:
        thedict = serialize(alarm)
        alarmlist.append(schema_ip.Alarm(**thedict))
    return alarmlist


@router_ip.get("/info", response_model=schema_response.MyResponse)
def get_file(ip: str, db: Session = Depends(get_db)):
    """
    单个ip的详细信息，包括相关告警以及相关样本
    :param ip:
    :param db:
    :return:
    """
    print(ip)
    ip_info = crud_ip.get_inner_ip(db, ip)
    if not ip_info:
        return schema_response.MyResponse(
            ErrCode=FAIL,
            ErrMessage="数据库中未找到相关IP"
        )
    ipalarm_sub, ipalarm_obj = crud_ip.get_ip_relevant_alarm(db, ip)
    sub_list = model2alarmlist(ipalarm_sub)
    obj_list = model2alarmlist(ipalarm_obj)
    alarm_list = schema_ip.IpInner(subject_alarms=sub_list, object_alarms=obj_list)
    sample_list = None
    # todo add sample_list
    ip_merged = schema_ip.IPInfoResponse(Alarms=alarm_list, Sample=sample_list,
                                         IpInfo=schema_ip.IpBase(**serialize(ip_info)))

    return schema_response.MyResponse(
        ErrCode=SUCCESS,
        Data=ip_merged
    )


def calculate_page(page_size: int, index_num: int):
    page_total = math.ceil(index_num / page_size)
    return page_total


@router_ip.get("/pagenum", response_model=schema_response.MyResponse)
def get_page_num(page_size: int, query=None, db: Session = Depends(get_db)):
    """
    :param query: 模糊查询
    :param page_size: 每页包含ip个数
    :param db:
    :return: 总页面数
    """
    count = crud_ip.get_ip_num(db, query)
    page_total = calculate_page(page_size=page_size, index_num=count)
    page_res = schema_ip.PageResponse(PageNumber=page_total)
    return schema_response.MyResponse(
        ErrCode=SUCCESS,
        Data=page_res
    )


@router_ip.get("/query", response_model=schema_response.MyResponse)
def query_ip(page_size: int, curr_page: int, query=None, db: Session = Depends(get_db)):
    """
    分页查询
    :param curr_page: 当前页码 最小为1
    :param db:
    :param page_size: 每页包含ip个数
    :param query: 模糊查询
    :return:
    """
    ip_total = crud_ip.get_ip_num(db, query)
    page_total = calculate_page(page_size, index_num=ip_total)
    if curr_page <= 0 or (curr_page > page_total and curr_page != 1):
        return schema_response.MyResponse(
            ErrCode=FAIL,
            ErrMessage="页码越界"
        )
    ip_info = crud_ip.get_ip_info_by_offset(db, page_size, curr_page, query)
    ip_list = []
    for ip in ip_info:
        thedict = serialize(ip)
        ip_list.append(schema_ip.IpBase(**thedict))
    ipres = schema_ip.IpListResponse(
        TotalNumber=ip_total,
        IPList=ip_list,
        CurrentPage=curr_page
    )
    return schema_response.MyResponse(
        ErrCode=SUCCESS,
        Data=ipres
    )


@router_ip.get("/query_risk_alarm", response_model=schema_response.MyResponse)
def query_risk_alarm(page_size: int, curr_page: int, query=None, db: Session = Depends(get_db)):
    """
    分页查询
    :param curr_page: 当前页码 最小为1
    :param db:
    :param page_size: 每页包含alarm
    :param query: 模糊查询
    :return:
    """
    alarm_total = crud_ip.get_risk_alarm_num(db, query)
    page_total = calculate_page(page_size, index_num=alarm_total)
    if curr_page <= 0 or (curr_page > page_total and curr_page != 1):
        return schema_response.MyResponse(
            ErrCode=FAIL,
            ErrMessage="页码越界"
        )
    risk_alarm_info = crud_ip.get_riskalarm_by_offset(db, page_size, curr_page, query)
    risk_alarm_list = []
    for risk_alarm in risk_alarm_info:
        thedict = serialize(risk_alarm)
        risk_alarm_list.append(schema_ip.RiskAlarm(**thedict))
    riskalarmres = schema_ip.RiskAlarmListResponse(
        TotalNumber=alarm_total,
        RiskAlarmList=risk_alarm_list,
        CurrentPage=curr_page
    )
    return schema_response.MyResponse(
        ErrCode=SUCCESS,
        Data=riskalarmres
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


@router_ip.get("/topk_attack_type", response_model=schema_response.MyResponse)
def get_topk_attck_type(ip: str, k: int, db: Session = Depends(get_db)):
    print(ip, k)
    attackTypeInfo = crud_ip.get_topk_attack_type(db, ip, k)
    attackTypeList = []
    for mtype in attackTypeInfo:
        attackTypeList.append(mtype[0])

    # todo add virusFamilylist
    virusFamilyList = []
    attackGangsList = []
    return schema_response.MyResponse(
        ErrCode=SUCCESS,
        Data=schema_ip.TopkAttckTypeResponse(
            AttackTypeList=attackTypeList,
            VirusFamilyList=virusFamilyList,
            AttackGangsList=attackGangsList
        )
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
