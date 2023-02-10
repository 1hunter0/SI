import py2neo
from py2neo import Graph
import pandas as pd
import time

# 连接neo4j 数据库
graph = Graph('http://localhost:7474',auth=('neo4j','123456'))

class CVEEntity:
    CVE_ID: str = None
    Description: str = None
    CWE_ID: str = None
    cvssV3_vector: str = None
    cvssV3_attackVector: str = None
    cvssV3_attackComplexity: str = None
    cvssV3_privilegesRequired: str = None
    cvssV3_userInteraction: str = None
    cvssV3_confidentialityImpact: str = None
    cvssV3_integrityImpact: str = None
    cvssV3_availabilityImpact: str = None
    cvssV3_scope: str = None
    cvssV3_baseScore: str = None
    cvssV3_baseSeverity: str = None
    cvssV2_vector: str = None
    cvssV2_accessVector: str = None
    cvssV2_accessComplexity: str = None
    cvssV2_authentication: str = None
    cvssV2_confidentialityImpact: str = None
    cvssV2_integrityImpact: str = None
    cvssV2_availabilityImpact: str = None
    cvssV2_baseScore: str = None
    cvssV2_severity: str = None
    publishedDate: str = None
    lastModifiedDate: str = None
    Official_website: str = None

    def __init__(self,configReader):
        self.cveEntityFilePath = configReader["CVE_Entity_File_Path"]
        # 连接neo4j 数据库
        # 连接neo4j 数据库
        self.graph = Graph('http://localhost:7474',
                           auth=(configReader['neo4j_user_name'], configReader['neo4j_password']))

    def loadData(self):
        self.createCVEEntityFromDataSet(self.cveEntityFilePath)

    def clear(self):
        print("------------------------start clear CVE Entity------------------------")
        time_start = time.time()
        cypher ="OPTIONAL MATCH(n:CVE) - [r] - () DELETE n, r"
        graph.run(cypher)

        cypher = "OPTIONAL MATCH(n:CVE) DELETE n"
        graph.run(cypher)
        time_end = time.time()
        print('clear CVE Entity total use time:' + str(time_end - time_start))
        print("------------------------clear CVE Entity successfully------------------------")

    # -------------------------Create CVE Entity-----------------------------------------------
    def createCVEEntityFromDataSet(self,CVE_Entity_file_path: str):
        print("\n", "------------------------start create CVE Entity------------------------")
        time_start = time.time()

        # 提取CPE实体的各个属性
        CVE = pd.read_csv(CVE_Entity_file_path, encoding='UTF-8')
        columns = CVE.columns.values.tolist()
        columns.remove('CWE_ID')
        print(columns)

        # 创建cypher语句，使用LOAD CSV可大幅提高数据导入效率
        pre = '''USING PERIODIC COMMIT 5000
        LOAD CSV WITH HEADERS  
        FROM "file:///5CDataSet/Node/CVE_Entity.csv" AS line 
        MERGE(p:CVE{'''
        # pre=pre.replace("file:///CVE_Entity.csv",CVE_Entity_file_path)
        # print(pre)
        end = '''})'''

        mid = ""
        for i in columns:
            temp = i + ':line.' + i + ','
            mid = mid + temp
        mid = mid[:-1]

        create_node_cypher = pre + mid + end
        print(create_node_cypher)

        graph.run(create_node_cypher)

        #set score to float,将CVSS评分设为float类型，在查询时可以进行比较等数学运算
        set_float_cypher = '''
        MATCH (n:CVE)
        WHERE NOT (n.cvssV3_baseScore='N/A')
        SET n.cvssV3_baseScore = toFloat(n.cvssV3_baseScore)'''
        graph.run(set_float_cypher)

        set_float_cypher = '''
        MATCH (n:CVE)
        WHERE NOT (n.cvssV2_baseScore='N/A')
        SET n.cvssV2_baseScore = toInteger(n.cvssV2_baseScore)'''
        graph.run(set_float_cypher)


        time_end = time.time()
        print('create CVE Entity total use time:' + str(time_end - time_start))
        print("------------------------create CVE Entity successfully------------------------")

    def delete(self,CVE_ID:str):
        print("------------------------start search CVE node:"+CVE_ID+"------------------------")
        time_start = time.time()
        cypher = "OPTIONAL MATCH(n:CVE{CVE_ID=KEY}) - [r] - () DELETE n, r"
        cypher.replace("KEY", CVE_ID)
        graph.run(cypher)

        cypher = "OPTIONAL MATCH(n:CVE{CVE_ID=KEY}) DELETE n"
        cypher.replace("KEY", CVE_ID)
        graph.run(cypher)
        time_end = time.time()
        print('clear CVE node total use time:' + str(time_end - time_start))
        print("------------------------delete CVE node:"+CVE_ID+" successfully------------------------")



class CPEEntity:
    cpe23Uri: str = None
    lastModifiedDate: str = None
    cpe_version: str = None
    part: str = None
    vendor: str = None
    product: str = None
    version: str = None
    update: str = None
    edition: str = None
    language: str = None
    sw_edition: str = None
    target_sw: str = None
    target_hw: str = None
    other: str = None
    Official_website: str = None

    def __init__(self, configReader):
        self.cpeEntityNoQuoteFilePath = configReader["CPE_Entity_No_Quote_File_Path"]
        self.cpeEntityWithQuoteFilePath = configReader["CPE_Entity_With_Quote_File_Path"]
        # 连接neo4j 数据库
        self.graph = Graph('http://localhost:7474',
                           auth=(configReader['neo4j_user_name'], configReader['neo4j_password']))

    def loadData(self):
        self.createCPEEntityFromDataSet(self.cpeEntityNoQuoteFilePath, self.cpeEntityWithQuoteFilePath)

    def clear(self):
        print("------------------------start clear CPE Entity------------------------")
        time_start = time.time()
        cypher ="OPTIONAL MATCH(n:CPE) - [r] - () DELETE n, r"
        graph.run(cypher)

        cypher ="OPTIONAL MATCH(n:CPE) DELETE n"
        graph.run(cypher)
        time_end = time.time()
        print('clear CPE Entity total use time:' + str(time_end - time_start))
        print("------------------------clear CPE Entity successfully------------------------")

    # -------------------------Create CVE Entity-----------------------------------------------
    def createCPEEntityFromDataSet(self,CPE_Entity_no_quote_file_path: str,CPE_Entity_with_quote_file_path: str):
        print('\n', '------------------------start create CPE Entity------------------------')
        time_start = time.time()

        # 提取CPE实体的各个属性
        CPE = pd.read_csv(CPE_Entity_no_quote_file_path, encoding='utf-8')
        columns = CPE.columns.values.tolist()
        print(columns)

        # 创建cypher语句，使用LOAD CSV可大幅提高数据导入效率
        pre = '''USING PERIODIC COMMIT 5000
        LOAD CSV WITH HEADERS  
        FROM "file:///5CDataSet/Node/CPE_Entity_No_Quote.csv" AS line
        MERGE(p:CPE{'''
        # pre.replace("file:///CPE_Entity_No_Quote.csv", CPE_Entity_no_quote_file_path)
        end = '''})'''

        mid = ""
        for i in columns:
            temp = i + ':line.' + i + ','
            mid = mid + temp
        mid = mid[:-1]

        create_node_cypher = pre + mid + end
        print(create_node_cypher)
        graph.run(create_node_cypher)

        # 对于数据中存在‘”’的情况，使用python接口，不容易出错，可增强鲁棒性，且简单易懂
        # 缺点是速度稍慢，但对于少量数据足够
        CPE_Quote = pd.read_csv(CPE_Entity_with_quote_file_path, encoding='UTF-8')
        CPE_Quote.fillna('N/A', inplace=True)
        for index in range(len(CPE_Quote['cpe23Uri'])):
            node = py2neo.Node('CPE', cpe23Uri=str(CPE_Quote['cpe23Uri'][index]),
                               lastModifiedDate=str(CPE_Quote['lastModifiedDate'][index]),
                               cpe_version=str(CPE_Quote['cpe_version'][index]),
                               part=str(CPE_Quote['part'][index]),
                               vendor=str(CPE_Quote['vendor'][index]),
                               product=str(CPE_Quote['product'][index]),
                               version=str(CPE_Quote['version'][index]),
                               update=str(CPE_Quote['update'][index]),
                               edition=str(CPE_Quote['edition'][index]),
                               language=str(CPE_Quote['language'][index]),
                               sw_edition=str(CPE_Quote['sw_edition'][index]),
                               target_sw=str(CPE_Quote['target_sw'][index]),
                               target_hw=str(CPE_Quote['target_hw'][index]),
                               other=str(CPE_Quote['other'][index]),
                               Official_website=str(CPE_Quote['Official_website'][index]))
            graph.merge(node, 'CPE', 'cpe23Uri')

        time_end = time.time()
        print('create CPE Entity total use time:' + str(time_end - time_start))
        print('---------------------------create CPE Entity successful-------------------------')


    def delete(self,cpe23Uri:str):
        print("------------------------start search cve node:"+cpe23Uri+"------------------------")
        time_start = time.time()
        cypher = "OPTIONAL MATCH(n:CPE{cpe23Uri=KEY}) - [r] - () DELETE n, r"
        cypher.replace("KEY", cpe23Uri)
        graph.run(cypher)

        cypher = "OPTIONAL MATCH(n:CPE{cpe23Uri=KEY}) DELETE n"
        cypher.replace("KEY", cpe23Uri)
        graph.run(cypher)
        time_end = time.time()
        print('delete CPE node total use time:' + str(time_end - time_start))
        print("------------------------delete CPE node:"+cpe23Uri+" successfully------------------------")



class CWEEntity:
    CWE_ID: str = None
    Name: str = None
    Weakness_Abstraction: str = None
    Status: str = None
    Description: str = None
    Extended_Description: str = None
    Related_Weaknesses: str = None
    Applicable_Platforms: str = None
    Background_Details: str = None
    Common_Consequences: str = None
    Detection_Methods: str = None
    Potential_Mitigations: str = None
    Observed_Examples: str = None
    Functional_Areas: str = None
    Affected_Resources: str = None
    Related_Attack_Patterns: str = None
    Notes: str = None
    Official_website: str = None

    def __init__(self,configReader):
        self.cweEntityFilePath = configReader["CWE_Entity_File_Path"]
        # 连接neo4j 数据库
        self.graph = Graph('http://localhost:7474',
                           auth=(configReader['neo4j_user_name'], configReader['neo4j_password']))

    def loadData(self):
        self.createCWEEntityFromDataSet(self.cweEntityFilePath)

    def clear(self):
        print("------------------------start clear CWE Entity------------------------")
        time_start = time.time()
        cypher ="OPTIONAL MATCH(n:CWE) - [r] - () DELETE n, r"
        graph.run(cypher)
        cypher = "OPTIONAL MATCH(n:CWE) DELETE n"
        graph.run(cypher)
        time_end = time.time()
        print('clear CWE Entity total use time:' + str(time_end - time_start))
        print("------------------------clear CWE Entity successfully------------------------")

    # -------------------------Create CWE Entity-----------------------------------------------
    def createCWEEntityFromDataSet(self,CWE_Entity_file_path: str):
        print('\n', '------------------------start create CWE Entity------------------------')
        time_start = time.time()

        # 提取CWE实体的各个属性
        CWE = pd.read_csv(CWE_Entity_file_path, encoding='UTF-8')
        columns = CWE.columns.values.tolist()
        print(columns)

        # 创建cypher语句，使用LOAD CSV可大幅提高数据导入效率
        pre = '''USING PERIODIC COMMIT 5000
                        LOAD CSV WITH HEADERS  
                        FROM "file:///5CDataSet/Node/CWE_Entity.csv" AS line 
                        MERGE(p:CWE{'''
        # pre.replace("file:///CWE_Entity.csv", CWE_Entity_file_path)

        end = '''})'''

        mid = ""
        for i in columns:
            temp = i + ':line.' + i + ','
            mid = mid + temp
        mid = mid[:-1]
        # print(mid)

        create_node_cypher = pre + mid + end

        graph.run(create_node_cypher)
        time_end = time.time()
        print('create CWE total use time:' + str(time_end - time_start))
        print('------------------------create CWE Entity successfully------------------------')

    def delete(self,CWE_ID:str):
        print("------------------------start search CWE node:"+CWE_ID+"------------------------")
        time_start = time.time()
        cypher ="OPTIONAL MATCH(n:CWE{CWE_ID=KEY}) - [r] - () DELETE n, r"
        cypher.replace("KEY",CWE_ID)
        graph.run(cypher)
        cypher = "OPTIONAL MATCH(n:CWE{CWE_ID=KEY}) DELETE n"
        cypher.replace("KEY", CWE_ID)
        graph.run(cypher)
        time_end = time.time()
        print('clear CWE node total use time:' + str(time_end - time_start))
        print("------------------------delete CWE node:"+CWE_ID+" successfully------------------------")


class CAPECEntity:
    CAPEC_ID: str = None
    Name: str = None
    Abstraction: str = None
    Status: str = None
    Description: str = None
    Alternate_Terms: str = None
    Likelihood_Of_Attack: str = None
    Typical_Severity: str = None
    Related_Attack_Patterns: str = None
    Execution_Flow: str = None
    Prerequisites: str = None
    Skills_Required: str = None
    Resources_Required: str = None
    Indicators: str = None
    Consequences: str = None
    Mitigations: str = None
    Example_Instances: str = None
    Related_Weaknesses: str = None
    Taxonomy_Mappings: str = None
    Notes: str = None
    Official_website: str = None

    def __init__(self,configReader):
        self.capecEntityFilePath = configReader["CAPEC_Entity_File_Path"]
        # 连接neo4j 数据库
        self.graph = Graph('http://localhost:7474',
                           auth=(configReader['neo4j_user_name'], configReader['neo4j_password']))

    def loadData(self):
        self.createCAPECEntityFromDataSet(self.capecEntityFilePath)

    def clear(self):
        print("------------------------start clear CAPEC Entity------------------------")
        time_start = time.time()
        cypher ="OPTIONAL MATCH(n:CAPEC) - [r] - () DELETE n, r"
        graph.run(cypher)
        cypher = "OPTIONAL MATCH(n:CAPEC)DELETE n"
        graph.run(cypher)
        time_end = time.time()
        print('clear CAPEC Entity total use time:' + str(time_end - time_start))
        print("------------------------clear CAPEC Entity successfully------------------------")

    # -------------------------Create CVE Entity-----------------------------------------------
    def createCAPECEntityFromDataSet(self,CAPEC_Entity_file_path: str):
        print("\n", "------------------------start create CAPEC Entity------------------------")
        time_start = time.time()
        # 提取CAPEC实体的各个属性
        CAPEC = pd.read_csv(CAPEC_Entity_file_path, encoding='UTF-8')
        columns = CAPEC.columns.values.tolist()
        print(columns)

        # 创建cypher语句，使用LOAD CSV可大幅提高数据导入效率
        pre = '''USING PERIODIC COMMIT 5000
        LOAD CSV WITH HEADERS  
        FROM "file:///5CDataSet/Node/CAPEC_Entity.csv" AS line 
        MERGE(p:CAPEC{'''

        # pre.replace("file:///CAPEC_Entity.csv",CAPEC_Entity_file_path)

        end = '''})'''

        mid = ""
        for i in columns:
            temp = i + ':line.' + i + ','
            mid = mid + temp
        mid = mid[:-1]
        # print(mid)

        create_node_cypher = pre + mid + end
        print(create_node_cypher)

        graph.run(create_node_cypher)


        time_end = time.time()
        print('create CAPEC Entity total use time:' + str(time_end - time_start))
        print("------------------------create CAPEC Entity successfully------------------------")

    def delete(self,CAPEC_ID:str):
        print("------------------------start search CAPEC node:"+CAPEC_ID+"------------------------")
        time_start = time.time()
        cypher = "OPTIONAL MATCH(n:CAPEC{CAPEC_ID=KEY}) - [r] - () DELETE n, r"
        cypher.replace("KEY", CAPEC_ID)
        graph.run(cypher)
        cypher = "OPTIONAL MATCH(n:CAPEC{CAPEC_ID=KEY})DELETE n"
        cypher.replace("KEY", CAPEC_ID)
        graph.run(cypher)
        time_end = time.time()
        print('clear CAPEC node total use time:' + str(time_end - time_start))
        print("------------------------delete CAPEC node:"+CAPEC_ID+" successfully------------------------")