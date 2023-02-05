import py2neo
from py2neo import Graph,NodeMatcher
import pandas as pd
import time

# 连接neo4j 数据库
graph = Graph('http://localhost:7474',auth=('neo4j','123456'))

class EdgeBase:
    start_node: dict = None
    end_node: dict = None
    relation: str = None


class CveCpeEdge(EdgeBase):
    def __init__(self, configReader):
        self.CveCpeNoQuoteFilePath = configReader["CVE_CPE_Relation_File_Path_No_Quote"]
        self.CveCpeWithQuoteFilePath = configReader["CVE_CPE_Relation_File_Path_With_Quote"]

    def loadData(self):
        self.createCveCpeEdge(self.CveCpeNoQuoteFilePath, self.CveCpeWithQuoteFilePath)

    def createCveCpeEdgeFromDataSet(self, CVE_contact_CPE_No_Quote: str, CVE_contact_CPE_With_Quote: str):
        print('\n', '------------------------start create edge between CVE and CPE------------------------')
        time_start = time.time()

        create_CVE_CPE_Relation_cypher = '''USING PERIODIC COMMIT 5000
        LOAD CSV WITH HEADERS  
        FROM "file:///Origin/Relation/CVE_contact_CPE_No_Quote.csv" AS line
        match (from:CVE{CVE_ID:line.CVE_ID})
        match (to:CPE{cpe23Uri:line.cpe23Uri})
        MERGE (from)-[r:affectProducts]->(to)
        MERGE (to)-[r1:hasRelatedVulnerability]->(from)'''
        create_CVE_CPE_Relation_cypher.replace("file:///Origin/Relation/CVE_contact_CPE_No_Quote.csv",
                                               CVE_contact_CPE_No_Quote)

        print(create_CVE_CPE_Relation_cypher)

        graph.run(create_CVE_CPE_Relation_cypher)

        # 有‘“’的部分，使用python接口创建关系
        CVE_contact_CPE_With_Quote = pd.read_csv(CVE_contact_CPE_With_Quote,encoding='utf-8')
        columns = CVE_contact_CPE_With_Quote.columns.values.tolist()
        print(columns)

        # 判断节点是否已经存在
        graph.schema.node_labels
        graph.schema.relationship_types
        node_matcher = NodeMatcher(graph)
        for index in range(len(CVE_contact_CPE_With_Quote['CVE_ID'])):
            cveid, cpe23Uri = CVE_contact_CPE_With_Quote['CVE_ID'][index], CVE_contact_CPE_With_Quote['cpe23Uri'][index]
            cve_node = node_matcher.match('CVE').where(CVE_ID=cveid).first()
            cpe_node = node_matcher.match('CPE').where(cpe23Uri=cpe23Uri).first()
            r1 = py2neo.Relationship(cve_node, 'affectProducts', cpe_node)
            r2 = py2neo.Relationship(cpe_node, 'hasRelatedVulnerability', cve_node)
            graph.merge(r1)
            graph.merge(r2)
        time_end = time.time()
        print('create edge between CVE and CPE total use time:' + str(time_end - time_start))
        print('------------------------create edge between CVE and CPE successfully------------------------')


class CveCweEdge(EdgeBase):
    def __init__(self, configReader):
        self.CveCweFilePath = configReader["CVE_CWE_Relation_File_Path"]

    def loadData(self):
        self.createCveCweEdge(self.CveCweFilePath)

    def createCveCweEdgeFromDataSet(self, CVE_contact_CWE: str):
        print('\n', '------------------------start create edge between CVE and CWE------------------------')
        time_start = time.time()

        create_CVE_CWE_Relation_cypher = '''USING PERIODIC COMMIT 5000
        LOAD CSV WITH HEADERS  
        FROM "file:///Origin/Relation/CVE_contact_CWE.csv" AS line 
        match (from:CVE{CVE_ID:line.CVE_ID})
        match (to:CWE{CWE_ID:line.CWE_ID})
        MERGE (from)-[r:hasRelatedWeaknesses]->(to)
        MERGE (to)-[r1:hasRelatedVulnerability]->(from)'''
        create_CVE_CWE_Relation_cypher.replace("file:///Origin/Relation/CVE_contact_CWE.csv",CVE_contact_CWE)

        print(create_CVE_CWE_Relation_cypher)

        graph.run(create_CVE_CWE_Relation_cypher)
        time_end = time.time()
        print('create edge between CVE and CWE total use time:' + str(time_end - time_start))
        print('------------------------create edge between CVE and CWE successfully------------------------')


class CweCapecEdge(EdgeBase):
    def __init__(self, configReader):
        self.CveCapecFilePath = configReader["CWE_CAPEC_Relation_File_Path"]

    def loadData(self):
        self.createCweCapecEdge(self.CveCapecFilePath)

    def createCweCapecEdgeFromDataSet(self, CWE_contact_CAPEC: str):
        print('\n', '------------------------start create edge between CWE and CAPEC------------------------')
        time_start = time.time()

        create_CWE_CAPEC_Relation_cypher = '''USING PERIODIC COMMIT 5000
        LOAD CSV WITH HEADERS  
        FROM "file:///Origin/Relation/CWE_contact_CAPEC.csv" AS line 
        match (from:CVE{CVE_ID:line.CVE_ID})
        match (to:CWE{CWE_ID:line.CWE_ID})
        MERGE (from)-[r:hasRelatedWeaknesses]->(to)
        MERGE (to)-[r1:hasRelatedVulnerability]->(from)'''
        create_CWE_CAPEC_Relation_cypher.replace("file:///Origin/Relation/CWE_contact_CAPEC.csv",CWE_contact_CAPEC)

        print(create_CWE_CAPEC_Relation_cypher)

        graph.run(create_CWE_CAPEC_Relation_cypher)
        time_end = time.time()
        print('create edge between CWE and CAPEC total use time:' + str(time_end - time_start))
        print('------------------------create edge between CWE and CAPEC successfully------------------------')

