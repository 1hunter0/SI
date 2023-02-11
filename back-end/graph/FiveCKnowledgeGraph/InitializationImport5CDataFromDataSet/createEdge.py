
from Entities.Relations import CveCpeEdge,CveCweEdge,CweCapecEdge






class EdgeCreater():

    def __init__(self, configReader):
        self.cveCpeEdgeCreater = CveCpeEdge(configReader=configReader)
        self.cveCweEdgeCreater = CveCweEdge(configReader=configReader)
        self.cweCapecEdgeCreater = CweCapecEdge(configReader=configReader)

    def loadDataFromDataSet(self):
        self.cveCpeEdgeCreater.loadData()
        self.cveCweEdgeCreater.loadData()
        self.cweCapecEdgeCreater.loadData()