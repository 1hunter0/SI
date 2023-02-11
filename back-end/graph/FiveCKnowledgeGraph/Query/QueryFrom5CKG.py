import json
from py2neo import *
import time

# 连接数据库
graph = Graph('http://localhost:7474/', auth=('neo4j', '123456'))


def search_cve(dataType_source: str, key: str, value: str):
    # 定义nodes_data数组存储节点信息
    nodes_data = []
    # have_node 用来判断节点是否已经存在，避免重复加入相同的节点
    have_node = {}
    # 定义links_data数组存储关系信息
    links_data = []
    # have_link 用来判断关系是否已经存在，避免重复加入相同的边
    have_link = {}
    # 查询节点是否存在
    node = graph.run('MATCH(n:CVE' + "{" + key + ':"' + value + '"}) return n').data()
    # 如果节点存在len(node)的值为1,不存在的话len(node)的值为0
    if len(node):
        # 将节点信息的格式转化为json格式
        node = json.dumps(node, ensure_ascii=False)
        node = json.loads(node)
        cveNodeDic = node[0]['n']
        # cveNodeDic['name'] = value
        # cveNodeDic['symbolSize'] = 70
        # cveNodeDic['category'] = dataType_source
        nodes_data.append(cveNodeDic)
        have_node[value] = 1
        query = '''match (cve:CVE) where cve.CVE_ID="''' + value + '''" with cve 
        optional match (cve:CVE)-[r1:hasRelatedWeaknesses]->(cwe:CWE) with cve,r1,cwe 
        optional match(cwe:CWE)-[r2:hasRelatedAttackPattern]->(capec:CAPEC) with cve,r1,cwe,r2,capec 
        optional match(cve:CVE)-[r3:affectProducts]->(cpe:CPE) return r1,r2,r3 limit 6'''
        # print(query)
        # 查询的结果reps返回的是一个列表，列表内的每一项都是一个字典
        reps = graph.run(query).data()
        for rep in reps:
            # 每一个rep都是一个字典，其中的key是上面查询中r1,r2,r3中的一个，value是这个边的两个节点，是一个对象，具有start_node和end_node
            for key, value in rep.items():
                if value==None:
                    continue
                # print('key:', key)
                #                 print(type(value))
                start_node = value.start_node
                start_node = json.dumps(start_node, ensure_ascii=False)
                start_node = json.loads(start_node)
                start_node['symbolSize'] = 50

                end_node = value.end_node
                end_node = json.dumps(end_node, ensure_ascii=False)
                end_node = json.loads(end_node)
                end_node['symbolSize'] = 50
                if key == 'r1':
                    start_node['name'] = start_node['CVE_ID']
                    start_node['category'] = 'CVE'
                    end_node['name'] = end_node['CWE_ID']
                    end_node['category'] = 'CWE'

                    source = str(rep['r1'].start_node['CVE_ID'])
                    target = str(rep['r1'].end_node['CWE_ID'])
                    relationType = str(type(rep['r1']).__name__)
                    # print(source,'--'+relationType+'->',target)
                if key == 'r2':
                    start_node['name'] = start_node['CWE_ID']
                    start_node['category'] = 'CWE'
                    end_node['name'] = end_node['CAPEC_ID']
                    end_node['category'] = 'CAPEC'

                    source = str(rep['r2'].start_node['CWE_ID'])
                    target = str(rep['r2'].end_node['CAPEC_ID'])
                    relationType = str(type(rep['r2']).__name__)
                #   print(source,'--'+relationType+'->',target)
                if key == 'r3':
                    start_node['name'] = start_node['CVE_ID']
                    start_node['category'] = 'CVE'
                    end_node['name'] = end_node['cpe23Uri']
                    end_node['category'] = 'CPE'

                    source = str(rep['r3'].start_node['CVE_ID'])
                    target = str(rep['r3'].end_node['cpe23Uri'])
                    relationType = str(type(rep['r3']).__name__)
                #   print(source,'--'+relationType+'->',target)
                rel_dict = {
                    'source': source,
                    'target': target,
                    'name': relationType
                }
                # ---------------------------------------------------
                # 判断起始节点是否已经在节点池里，如果没在就加入新节点
                if start_node['name'] not in have_node:
                    have_node[start_node['name']] = 1
                    nodes_data.append(start_node)
                #                     print(start_node,'\n--------------------------------------------------------------------')
                if end_node['name'] not in have_node:
                    have_node[end_node['name']] = 1
                    nodes_data.append(end_node)
                #                     print(end_node,'\n--------------------------------------------------------------------')
                # 构造一个新变量temp，主要作用就是避免重复加入相同的边
                temp = source + '--' + relationType + '->' + target
                if temp not in have_link:
                    have_link[temp] = 1
                    links_data.append(rel_dict)
                    # print(temp)

        # 构造字典存储nodes_data和links_data
        search_neo4j_data = {
            'nodes_data': nodes_data,
            'links_data': links_data
        }
        # print(len(nodes_data))
        # print('******************************')
        # print(len(links_data))
        # 将dict转化为json格式
        search_neo4j_data = json.dumps(search_neo4j_data)
        return search_neo4j_data
    else:
        print("查无此节点")
        return []

def search_cwe(dataType_source: str, key: str, value: str):
    # 定义nodes_data数组存储节点信息
    nodes_data = []
    # have_node 用来判断节点是否已经存在，避免重复加入相同的节点
    have_node = {}
    # 定义links_data数组存储关系信息
    links_data = []
    # have_link 用来判断关系是否已经存在，避免重复加入相同的边
    have_link = {}
    # 查询节点是否存在
    node = graph.run('MATCH(n:CWE' + "{" + key + ':"' + value + '"}) return n').data()
    # 如果节点存在len(node)的值为1不存在的话len(node)的值为0
    if len(node):
        # 将节点信息的格式转化为json格式
        node = json.dumps(node, ensure_ascii=False)
        node = json.loads(node)
        cveNodeDic = node[0]['n']
        # cveNodeDic['name'] = value
        # cveNodeDic['symbolSize'] = 70
        # cveNodeDic['category'] = dataType_source
        nodes_data.append(cveNodeDic)
        have_node[value] = 1
        query = '''match (cwe:CWE) where cwe.CWE_ID="''' + value + '''" with cwe 
        optional match (cwe:CWE)-[r1:hasRelatedVulnerability]->(cve:CVE) with cwe,r1,cve 
        optional match(cwe:CWE)-[r2:hasRelatedAttackPattern]->(capec:CAPEC) with cve,r1,cwe,r2,capec 
        optional match(cve:CVE)-[r3:affectProducts]->(cpe:CPE) return r1,r2,r3 limit 9'''
        # print(query)
        # 查询的结果reps返回的是一个列表，列表内的每一项都是一个字典
        reps = graph.run(query).data()
        for rep in reps:
            # 每一个rep都是一个字典，其中的key是上面查询中r1,r2,r3中的一个，value是这个边的两个节点，是一个对象，具有start_node和end_node
            for key, value in rep.items():
                if value==None:
                    continue
                # print('key:', key)
                #                 print(type(value))
                start_node = value.start_node
                start_node = json.dumps(start_node, ensure_ascii=False)
                start_node = json.loads(start_node)
                start_node['symbolSize'] = 50

                end_node = value.end_node
                end_node = json.dumps(end_node, ensure_ascii=False)
                end_node = json.loads(end_node)
                end_node['symbolSize'] = 50
                if key == 'r1':
                    start_node['name'] = start_node['CWE_ID']
                    start_node['category'] = 'CWE'
                    end_node['name'] = end_node['CVE_ID']
                    end_node['category'] = 'CVE'

                    source = str(rep['r1'].start_node['CWE_ID'])
                    target = str(rep['r1'].end_node['CVE_ID'])
                    relationType = str(type(rep['r1']).__name__)
                #                     print(source,'--'+relationType+'->',target)
                if key == 'r2':
                    start_node['name'] = start_node['CWE_ID']
                    start_node['category'] = 'CWE'
                    end_node['name'] = end_node['CAPEC_ID']
                    end_node['category'] = 'CAPEC'

                    source = str(rep['r2'].start_node['CWE_ID'])
                    target = str(rep['r2'].end_node['CAPEC_ID'])
                    relationType = str(type(rep['r2']).__name__)
                #                     print(source,'--'+relationType+'->',target)
                if key == 'r3':
                    start_node['name'] = start_node['CVE_ID']
                    start_node['category'] = 'CVE'
                    end_node['name'] = end_node['cpe23Uri']
                    end_node['category'] = 'CPE'

                    source = str(rep['r3'].start_node['CVE_ID'])
                    target = str(rep['r3'].end_node['cpe23Uri'])
                    relationType = str(type(rep['r3']).__name__)
                #                     print(source,'--'+relationType+'->',target)
                rel_dict = {
                    'source': source,
                    'target': target,
                    'name': relationType
                }
                # ---------------------------------------------------
                # 判断起始节点是否已经在节点池里，如果没在就加入新节点
                if start_node['name'] not in have_node:
                    have_node[start_node['name']] = 1
                    nodes_data.append(start_node)
                #                     print(start_node,'\n--------------------------------------------------------------------')
                if end_node['name'] not in have_node:
                    have_node[end_node['name']] = 1
                    nodes_data.append(end_node)
                #                     print(end_node,'\n--------------------------------------------------------------------')
                # 构造一个新变量temp，主要作用就是避免重复加入相同的边
                temp = source + '--' + relationType + '->' + target
                if temp not in have_link:
                    have_link[temp] = 1
                    links_data.append(rel_dict)
                    # print(temp)

        # 构造字典存储data和links
        search_neo4j_data = {
            'nodes_data': nodes_data,
            'links_data': links_data
        }
        # print(len(nodes_data))
        # print('******************************')
        # print(len(links_data))
        # 将dict转化为json格式
        search_neo4j_data = json.dumps(search_neo4j_data)
        return search_neo4j_data
    else:
        # print("查无此节点")
        return []

def search_capec(dataType_source: str, key: str, value: str):
    # 定义nodes_data数组存储节点信息
    nodes_data = []
    # have_node 用来判断节点是否已经存在，避免重复加入相同的节点
    have_node = {}
    # 定义links_data数组存储关系信息
    links_data = []
    # have_link 用来判断关系是否已经存在，避免重复加入相同的边
    have_link = {}
    # 查询节点是否存在
    node = graph.run('MATCH(n:CAPEC' + "{" + key + ':"' + value + '"}) return n').data()
    # 如果节点存在len(node)的值为1不存在的话len(node)的值为0
    if len(node):
        # 将节点信息的格式转化为json格式
        node = json.dumps(node, ensure_ascii=False)
        node = json.loads(node)
        cveNodeDic = node[0]['n']
        # cveNodeDic['name'] = value
        # cveNodeDic['symbolSize'] = 70
        # cveNodeDic['category'] = dataType_source
        nodes_data.append(cveNodeDic)
        have_node[value] = 1
        query = '''match (capec:CAPEC) where capec.CAPEC_ID="''' + value + '''" with capec 
        optional match (capec:CAPEC)-[r1:hasRelatedWeakness]->(cwe:CWE) with capec,r1,cwe 
        optional match (cwe:CWE)-[r2:hasRelatedVulnerability]->(cve:CVE) with capec,r1,cwe,r2,cve 
        optional match(cve:CVE)-[r3:affectProducts]->(cpe:CPE) return r1,r2,r3 limit 9'''
        # print(query)
        # 查询的结果reps返回的是一个列表，列表内的每一项都是一个字典
        reps = graph.run(query).data()
        for rep in reps:
            # 每一个rep都是一个字典，其中的key是上面查询中r1,r2,r3中的一个，value是这个边的两个节点，是一个对象，具有start_node和end_node
            for key, value in rep.items():
                # print('key:', key)
                #                 print(type(value))
                start_node = value.start_node
                start_node = json.dumps(start_node, ensure_ascii=False)
                start_node = json.loads(start_node)
                start_node['symbolSize'] = 50

                end_node = value.end_node
                end_node = json.dumps(end_node, ensure_ascii=False)
                end_node = json.loads(end_node)
                end_node['symbolSize'] = 50
                if key == 'r1':
                    start_node['name'] = start_node['CAPEC_ID']
                    start_node['category'] = 'CAPEC'
                    end_node['name'] = end_node['CWE_ID']
                    end_node['category'] = 'CWE'

                    source = str(rep['r1'].start_node['CAPEC_ID'])
                    target = str(rep['r1'].end_node['CWE_ID'])
                    relationType = str(type(rep['r1']).__name__)
                #                     print(source,'--'+relationType+'->',target)
                if key == 'r2':
                    start_node['name'] = start_node['CWE_ID']
                    start_node['category'] = 'CWE'
                    end_node['name'] = end_node['CVE_ID']
                    end_node['category'] = 'CVE'

                    source = str(rep['r2'].start_node['CWE_ID'])
                    target = str(rep['r2'].end_node['CVE_ID'])
                    relationType = str(type(rep['r2']).__name__)
                #                     print(source,'--'+relationType+'->',target)
                if key == 'r3':
                    start_node['name'] = start_node['CVE_ID']
                    start_node['category'] = 'CVE'
                    end_node['name'] = end_node['cpe23Uri']
                    end_node['category'] = 'CPE'

                    source = str(rep['r3'].start_node['CVE_ID'])
                    target = str(rep['r3'].end_node['cpe23Uri'])
                    relationType = str(type(rep['r3']).__name__)
                #                     print(source,'--'+relationType+'->',target)
                rel_dict = {
                    'source': source,
                    'target': target,
                    'name': relationType
                }
                # ---------------------------------------------------
                # 判断起始节点是否已经在节点池里，如果没在就加入新节点
                if start_node['name'] not in have_node:
                    have_node[start_node['name']] = 1
                    nodes_data.append(start_node)
                #                     print(start_node,'\n--------------------------------------------------------------------')
                if end_node['name'] not in have_node:
                    have_node[end_node['name']] = 1
                    nodes_data.append(end_node)
                #                     print(end_node,'\n--------------------------------------------------------------------')
                # 构造一个新变量temp，主要作用就是避免重复加入相同的边
                temp = source + '--' + relationType + '->' + target
                if temp not in have_link:
                    have_link[temp] = 1
                    links_data.append(rel_dict)
                    # print(temp)

        # 构造字典存储data和links
        search_neo4j_data = {
            'nodes_data': nodes_data,
            'links_data': links_data
        }
        # 将dict转化为json格式
        search_neo4j_data = json.dumps(search_neo4j_data)
        return search_neo4j_data
    else:
        # print("查无此节点")
        return []

def search_cpe(dataType_source: str, key: str, value: str):
    # 定义nodes_data数组存储节点信息
    nodes_data = []
    # have_node 用来判断节点是否已经存在，避免重复加入相同的节点
    have_node = {}
    # 定义links_data数组存储关系信息
    links_data = []
    # have_link 用来判断关系是否已经存在，避免重复加入相同的边
    have_link = {}
    # 查询节点是否存在
    node = graph.run('MATCH(n:CPE' + "{" + key + ':"' + value + '"}) return n').data()
    # 如果节点存在len(node)的值为1不存在的话len(node)的值为0
    if len(node):
        # 将节点信息的格式转化为json格式
        node = json.dumps(node, ensure_ascii=False)
        node = json.loads(node)
        cveNodeDic = node[0]['n']
        # cveNodeDic['name'] = value
        # cveNodeDic['symbolSize'] = 70
        # cveNodeDic['category'] = dataType_source
        nodes_data.append(cveNodeDic)
        have_node[value] = 1
        query = '''match (cpe:CPE) where cpe.cpe23Uri="''' + value + '''" with cpe 
        optional match (cpe:CPE)-[r1:hasRelatedVulnerability]->(cve:CVE) with cpe,r1,cve 
        optional match (cve:CVE)-[r2:hasRelatedWeaknesses]->(cwe:CWE) with cpe,r1,cve,r2,cwe 
        optional match(cwe:CWE)-[r3:hasRelatedAttackPattern]->(capec:CAPEC) return r1,r2,r3 limit 6'''
        # print(query)
        # 查询的结果reps返回的是一个列表，列表内的每一项都是一个字典
        reps = graph.run(query).data()
        for rep in reps:
            # 每一个rep都是一个字典，其中的key是上面查询中r1,r2,r3中的一个，value是这个边的两个节点，是一个对象，具有start_node和end_node
            for key, value in rep.items():
                # print('key:', key)
                #                 print(type(value))
                start_node = value.start_node
                start_node = json.dumps(start_node, ensure_ascii=False)
                start_node = json.loads(start_node)
                start_node['symbolSize'] = 50

                end_node = value.end_node
                end_node = json.dumps(end_node, ensure_ascii=False)
                end_node = json.loads(end_node)
                end_node['symbolSize'] = 50
                if key == 'r1':
                    start_node['name'] = start_node['cpe23Uri']
                    start_node['category'] = 'CPE'
                    end_node['name'] = end_node['CVE_ID']
                    end_node['category'] = 'CVE'

                    source = str(rep['r1'].start_node['cpe23Uri'])
                    target = str(rep['r1'].end_node['CVE_ID'])
                    relationType = str(type(rep['r1']).__name__)
                #                     print(source,'--'+relationType+'->',target)
                if key == 'r2':
                    start_node['name'] = start_node['CVE_ID']
                    start_node['category'] = 'CVE'
                    end_node['name'] = end_node['CWE_ID']
                    end_node['category'] = 'CWE'

                    source = str(rep['r2'].start_node['CVE_ID'])
                    target = str(rep['r2'].end_node['CWE_ID'])
                    relationType = str(type(rep['r2']).__name__)
                #                     print(source,'--'+relationType+'->',target)
                if key == 'r3':
                    start_node['name'] = start_node['CWE_ID']
                    start_node['category'] = 'CWE'
                    end_node['name'] = end_node['CAPEC_ID']
                    end_node['category'] = 'CAPEC'

                    source = str(rep['r3'].start_node['CWE_ID'])
                    target = str(rep['r3'].end_node['CAPEC_ID'])
                    relationType = str(type(rep['r3']).__name__)
                #                     print(source,'--'+relationType+'->',target)
                rel_dict = {
                    'source': source,
                    'target': target,
                    'name': relationType
                }
                # ---------------------------------------------------
                # 判断起始节点是否已经在节点池里，如果没在就加入新节点
                if start_node['name'] not in have_node:
                    have_node[start_node['name']] = 1
                    nodes_data.append(start_node)
                #                     print(start_node,'\n--------------------------------------------------------------------')
                if end_node['name'] not in have_node:
                    have_node[end_node['name']] = 1
                    nodes_data.append(end_node)
                #                     print(end_node,'\n--------------------------------------------------------------------')
                # 构造一个新变量temp，主要作用就是避免重复加入相同的边
                temp = source + '--' + relationType + '->' + target
                if temp not in have_link:
                    have_link[temp] = 1
                    links_data.append(rel_dict)
                    print(temp)

        # 构造字典存储data和links
        search_neo4j_data = {
            'nodes_data': nodes_data,
            'links_data': links_data
        }
        # 将dict转化为json格式
        search_neo4j_data = json.dumps(search_neo4j_data)
        return search_neo4j_data
    else:
        # print("查无此节点")
        return []

def search_5cKG_data(node_name: str):
    time_start = time.time()
    # 接收前端传过来的查询值
    if node_name.find('CVE') != -1:
        search_neo4j_data = search_cve(dataType_source='CVE', key='CVE_ID', value=node_name)
        time_end = time.time()
        print('search cve total use time:' + str(time_end - time_start))
    elif node_name.find('CWE') != -1:
        search_neo4j_data = search_cwe(dataType_source='CWE', key='CWE_ID', value=node_name)
        time_end = time.time()
        print('search cwe total use time:' + str(time_end - time_start))
    elif node_name.find('cpe') != -1:
        search_neo4j_data = search_cpe(dataType_source='CPE', key='cpe23Uri', value=node_name)
        time_end = time.time()
        print('search cpe total use time:' + str(time_end - time_start))
    elif node_name.find('CAPEC') != -1:
        search_neo4j_data = search_capec(dataType_source='CAPEC', key='CAPEC_ID', value=node_name)
        time_end = time.time()
        print('search capece total use time:' + str(time_end - time_start))
    else:
        search_neo4j_data = []
    # print(search_neo4j_data)
    return search_neo4j_data


