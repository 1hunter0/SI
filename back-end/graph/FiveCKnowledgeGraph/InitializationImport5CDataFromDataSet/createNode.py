
from Entities.Entities import CVEEntity,CPEEntity,CWEEntity,CAPECEntity


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