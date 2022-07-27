from fastapi import FastAPI
from py2neo import *
from neo4j import GraphDatabase
from starlette.middleware.cors import CORSMiddleware

import schemas

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    # 允许跨域的源列表，例如 ["http://www.example.org"] 等等，["*"] 表示允许任何源
    allow_origins=["*"],
    # 跨域请求是否支持 cookie，默认是 False，如果为 True，allow_origins 必须为具体的源，不可以是 ["*"]
    allow_credentials=False,
    # 允许跨域请求的 HTTP 方法列表，默认是 ["GET"]
    allow_methods=["*"],
    # 允许跨域请求的 HTTP 请求头列表，默认是 []，可以使用 ["*"] 表示允许所有的请求头
    # 当然 Accept、Accept-Language、Content-Language 以及 Content-Type 总之被允许的
    allow_headers=["*"],
    # 可以被浏览器访问的响应头, 默认是 []，一般很少指定
    # expose_headers=["*"]
    # 设定浏览器缓存 CORS 响应的最长时间，单位是秒。默认为 600，一般也很少指定
    # max_age=1000
)

uri = 'neo4j://localhost:7687'
username = 'neo4j'
password = 'qazwsx'
neo4j_driver = GraphDatabase.driver(uri, auth=(username, password))


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.get("/q/{cypher_string}",
         response_model=schemas.Query,
         summary="Query the database with a custom Cypher string")
async def query(cypher_string: str):
    with neo4j_driver.session() as session:
        response = session.run(query=cypher_string)
        query_response = schemas.Query(response=response.data())
        return query_response
