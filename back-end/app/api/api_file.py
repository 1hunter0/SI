import datetime
import json
from typing import List
from fastapi import APIRouter, Depends, UploadFile
from app.schemas import schema_ip
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.crud import crud_file
from app.schemas import schema_file, schema_response
from app.global_variable import *
from app.parser.sandbox import SandBox
from graph.sandbox_neo4j import *

router_file = APIRouter(
    prefix="/files",
    tags=["files"]
)


###############
# dev
@router_file.get("/inner")
def get_inner_file(file: str):
    file_info = json.load(open('app/api/FILE.json', 'r', encoding="utf-8"))
    return file_info


def filehelper(data: dict):
    file = schema_file.FileBase()
    file.sha1 = data['sha1']
    file.file_type = data['file_type']
    file.file_name = data['file_name']
    file.threat_score = data['threat_score']
    file.multi_engines = data['multi_engines']
    file.threat_level = data['threat_level']
    file.submit_time = data['submit_time']
    file.sandbox_type_list = data['sandbox_type_list']
    file.sandbox_behaviors = data['sandbox_behaviors']
    file.multiengines_results = data['multiengines_results']

    return file


################
@router_file.get("/info", response_model=schema_response.MyResponse)
def get_file(sha1: str, db: Session = Depends(get_db)):
    print(sha1)
    file_info = crud_file.get_file_info(db, sha1)
    print(file_info)
    if file_info:
        return schema_response.MyResponse(
            ErrCode=SUCCESS,
            Data=file_info
        )
    # 不在数据库
    data = {}
    try:
        data = SandBox(sha1).parser()
    except Exception as e:
        print(e)
    file = filehelper(data)
    file_info = crud_file.create_file(db, file)
    if not file_info:
        return schema_response.MyResponse(ErrCode=FAIL, ErrMessage="数据插入失败")
    return schema_response.MyResponse(
        ErrCode=SUCCESS,
        Data=file_info
    )


@router_file.post("/upload", response_model=schema_response.MyResponse)
def get_info_from_file(file: UploadFile, db: Session = Depends(get_db)):
    """
    TODO: 直接传输文件到沙箱中
    1.判断sha1是否在数据库中
        1.1 若在直接返回数据库中结果
        1.2 若不在则需要进行对应的沙箱分析后加入到数据库中
    :param file:
    :param db:
    :return:
    """
    return

################
#将文件网络信息加入图数据库 api  没有检查是否重复 使用的前提是先检查数据库中没有再调用
# 返回 "detail": "Not Found" 说明该文件没有网络行为
@router_file.get("/updatenetgraph", response_model=schema_response.MyResponse)
def update_graph(sha1: str):
    """
    :param sha:文件sha256值
    :return:bool 是否成功
    """
    print(sha1)
    # file_info = crud_file.get_file_info(db, sha1)
    done = False
    message = "文件网络信息更新至图数据库成功"
    graph = Graph('bolt://localhost:7687',auth='neo4j',password='123456')
    try:
        done = update_file_network(sha1,graph=graph)
    except Exception as e:
        print(e)
    if not done:
        return schema_response.MyResponse(ErrCode=FAIL, ErrMessage="数据插入失败")
    return schema_response.MyResponse(
        ErrCode=SUCCESS,
        Data=message
    )
    
################
#从图数据库根据文件sha 返回文件网络信息 api  
@router_file.get("/getnetgraph", response_model=schema_response.MyResponse)
def get_graph(sha: str):
    """
    :param sha: 文件sha值
    :return: nodes_data,links_data 图数据 分别是结点与连接的两个字典列表
    """
    graph = Graph('bolt://localhost:7687',auth='neo4j',password='123456')
    nodes_data = []
    links_data = []
    try:
        (nodes_data,links_data) = get_gragh(sha,graph)
    except Exception as e:
        print(e)
    data1 = {'nodes':nodes_data,'links':links_data}
    if nodes_data == []:
        return schema_response.MyResponse(ErrCode=FAIL, ErrMessage="查询不到该文件")
    return schema_response.MyResponse(
        ErrCode=SUCCESS,
        Data=data1
    )
################
#根据ip返回对应关联样本网络图 api  
@router_file.get("/getfilebyip", response_model=schema_response.MyResponse)
def get_graph(ip: str):
    """
    :param ip: ipstr
    :return: nodes_data,links_data 图数据 分别是结点与连接的两个字典列表
    """
    graph = Graph('bolt://localhost:7687',auth='neo4j',password='123456')
    nodes_data = []
    links_data = []
    try:
        (nodes_data,links_data)= get_gragh_byip(ip,graph)
    except Exception as e:
        print(e)
    data1 = {'nodes':nodes_data,'links':links_data}
    if nodes_data == []:
        return schema_response.MyResponse(ErrCode=FAIL, ErrMessage="查询不到相关样本")
    return schema_response.MyResponse(
        ErrCode=SUCCESS,
        Data=data1
    )









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
