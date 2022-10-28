import datetime
import json
from typing import List
from fastapi import APIRouter, Depends, UploadFile
from app.schemas import schema_ip,schema_response
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.crud import crud_ip
import requests
from app.global_variable import *
import json
fake_dns = {}

router_dns = APIRouter(
    prefix="/domains",
    tags=["domains"]
)
# 读打开文件
with open('app/api/fake_dns.json', encoding='utf-8') as a:
    # 读取文件
    fake_dns = json.load(a)

###############
# dev
@router_dns.get("/inner/{domain}")
def get_inner_domain(domain: str):
    domain_info = json.load(open('app/api/DNS.json', 'r', encoding="utf-8"))
    return domain_info

################
@router_dns.get("/info", response_model=schema_response.MyResponse)
def get_dns(dns: str, db: Session = Depends(get_db)):
    url = "https://api.threatbook.cn/v3/domain/query"
    query = {
        "apikey":"44a4838848ac4f5799d1ccf1cf18519a130f43810ee0413c9a93a9acf4ed684b",
        "resource":dns
        }
    response = requests.request("GET", url, params=query)
    print(response.json())
    return schema_response.MyResponse(
        ErrCode=SUCCESS,
        Data=fake_dns['data']
    )
