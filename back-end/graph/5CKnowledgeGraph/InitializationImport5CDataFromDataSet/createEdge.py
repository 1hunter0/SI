from py2neo import Graph
from Entities.Relations import CveCpeEdge,CveCweEdge,CweCapecEdge
import time


# 连接neo4j 数据库
graph = Graph('http://localhost:7474', auth=('neo4j', '123456'))


class EdgeCreater():
    def __init__(self, configReader):
        self.cveCpeEdgeCreater = CveCpeEdge(configReader=configReader)
        self.cveCweEdgeCreater = CveCweEdge(configReader=configReader)
        self.cweCapecEdgeCreater = CweCapecEdge(configReader=configReader)

    def loadDataFromDataSet(self):
        self.cveCpeEdgeCreater.loadData()
        self.cveCweEdgeCreater.loadData()
        self.cweCapecEdgeCreater.loadData()