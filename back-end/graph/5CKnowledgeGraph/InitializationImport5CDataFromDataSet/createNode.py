from py2neo import Graph
from Entities.Entities import CVEEntity,CPEEntity,CWEEntity,CAPECEntity

# 连接neo4j 数据库
graph = Graph('http://localhost:7474', auth=('neo4j', '123456'))
class NodeCreater():
    def __init__(self, configReader):
        self.cveNodeCreater = CVEEntity(configReader=configReader)
        self.cpeNodeCreater = CPEEntity(configReader=configReader)
        self.cweNodeCreater = CWEEntity(configReader=configReader)
        self.capecNodeCreater = CAPECEntity(configReader=configReader)

    def loadDataFromDataSet(self):
        self.cveNodeCreater.loadData()
        self.cpeNodeCreater.loadData()
        self.cweNodeCreater.loadData()
        self.capecNodeCreater.loadData()