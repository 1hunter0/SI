import datetime
import json
from typing import List
from fastapi import APIRouter, Depends, UploadFile
from app.dependencies import get_db
from app.schemas import schema_file, schema_response
from app.global_variable import *
from py2neo import Graph
from graph.FiveCKnowledgeGraph.Query.QueryFrom5CKG import search_5cKG_data

router_5c = APIRouter(
    prefix="/5c",
    tags=["5c"]
)



################
# 从图数据库返回5C信息 api
@router_5c.get("/get5cgraph", response_model=schema_response.MyResponse)
def get_graph(node_name: str):
    """
    :param node_name: 节点的名字，通过主码确定，例如"CVE-2006-0207"、"CWE-94"、"CAPEC-111"等
    :return: nodes_data,links_data 图数据 分别是结点与连接的两个字典列表
    """
    try:
        print('start_search:', node_name)
        search_neo4j_data = search_5cKG_data(node_name)
    except Exception as e:
        print(e)
    if search_neo4j_data == []:
        print('数据库中暂未添加该实体')
        return schema_response.MyResponse(ErrCode=FAIL, ErrMessage="数据库中暂未添加该实体")
    return schema_response.MyResponse(
        ErrCode=SUCCESS,
        Data=search_neo4j_data
    )
