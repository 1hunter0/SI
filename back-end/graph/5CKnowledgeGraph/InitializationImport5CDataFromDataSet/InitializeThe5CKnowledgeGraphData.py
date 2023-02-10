import json
from py2neo import Graph
from createNode import NodeCreater
from createEdge import EdgeCreater



if __name__ == '__main__':
    with open("../config.json", "r", encoding="utf8") as f:
        configReader = json.load(f)
    # 连接neo4j 数据库
    graph = Graph('http://localhost:7474', auth=(configReader['neo4j_user_name'], configReader['neo4j_password']))

    # # 删除已有的所有内容
    # graph.delete_all()

    # 设置主码，加快速度
    try:
        print("------------------------start set unique key------------------------")
        unique_cypher1 = 'CREATE CONSTRAINT ON (a:CVE) ASSERT a.CVE_ID IS UNIQUE'
        unique_cypher2 = 'CREATE CONSTRAINT ON (b:CPE) ASSERT b.cpe23Uri IS UNIQUE'
        unique_cypher3 = 'CREATE CONSTRAINT ON (c:CWE) ASSERT c.CWE_ID IS UNIQUE'
        unique_cypher4 = 'CREATE CONSTRAINT ON (d:CAPEC) ASSERT d.CAPEC_ID IS UNIQUE'
        graph.run(unique_cypher1)
        graph.run(unique_cypher2)
        graph.run(unique_cypher3)
        graph.run(unique_cypher4)
        print("------------------------set unique key successfully------------------------")
    except:
        print("------------------------unique key already exist------------------------")
        pass

    nodeCreater=NodeCreater(configReader=configReader)
    nodeCreater.loadDataFromDataSet()
    edgeCreater=EdgeCreater(configReader=configReader)
    edgeCreater.loadDataFromDataSet()

