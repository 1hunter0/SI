import json
import requests
from py2neo import Graph,Node,Relationship
#neo4j 连接图数据库

#实体：文件 进程 ip 域名 dns
#关系：启动 连接 释放（暂无） [域名]解析[ip]
def create_file_node(name,sha,graph):
  file=Node('文件',name=name,sha=sha)
  graph.create(file)
  return file
def create_process_node(name,pid,comline,graph):
  process=Node('进程',name=name,pid=pid,comline=comline)
  graph.create(process)
  return process
  
def create_ip_node(ip,graph):
  ip = Node('ip',ip=ip)
  graph.create(ip)
  return ip
  
def create_domain_node(domain,graph):
  domain = Node('域名',donmain=domain)
  graph.create(domain)
  return domain
  
def create_dns_node(dns,graph):
  dns = Node('dns',dns=dns)
  graph.create(dns)
  return dns

def create_start_rela(head,tail,graph):
  rela = Relationship(head,"启动",tail)
  graph.create(rela)
  
def create_link_rela(head,tail,graph):
  rela = Relationship(head,"连接",tail)
  graph.create(rela)
  
def create_drop_rela(head,tail,graph):
  rela = Relationship(head,"释放",tail)
  graph.create(rela)

def create_parse_rela(head,tail,graph):
  rela = Relationship(head,"解析",tail)
  graph.create(rela)
# graph = Graph('bolt://localhost:7687',auth='neo4j',password='123456')
res_name =[]
res_pid  = []
res_comline =[]
def pre(tn):
    global res_name,res_pid ,res_comline
    if not tn:
        return
    res_name.append(tn.val)
    res_pid.append(str(tn.pid))
    res_comline.append(tn.comline)
    for i in tn.l_child:
        pre(i)
    return(res_name,res_pid)
#遍历多叉树获取文件名
def tree(list,root):
  if len(list)!=0:
    for i in range(len(list)):
      j = Node_process(list[i]['process_name'],list[i]['pid'],list[i]['command_line'])
      root.add_child(j)
      if len(list[i]['children'])!=0:
        tree(list[i]['children'],j) 
class Node_process():
    # 初始化一个节点
    def __init__(self,val,pid,comline = None):
        self.val = val       # 节点值
        self.pid = pid       #进程pid值
        self.comline = comline
        self.l_child = []    # 子节点列表
    # 添加子节点
    def add_child(self,node):
        self.l_child.append(node)
#没有network响应 考虑换沙盒环境 'sandbox_type'
def update_file_network(sha,graph):
  url = 'https://api.threatbook.cn/v3/file/report'
  # sha = 'bcd9aa6199612ec0ebec498222221e94b47ec23c2eba425791f753eae444b552'
  params = {
      'apikey': '44a4838848ac4f5799d1ccf1cf18519a130f43810ee0413c9a93a9acf4ed684b',
      #'sandbox_type': 'win10_sp1_enx86_office2016',
      #'query_fields':'network',
      'sha256': sha
        # 'df6ef08c7f15923c029a8aedf16daf5a5fb56a49942c314bf4e7bc3f3d1139d3'
  }
  response = requests.get(url, params=params)
  data =response.json()
  name_file = (data['data']['summary']['file_name'])
  sha_file  = (data['data']['summary']['sample_sha256'])
  data_net = data['data']['network']
  data_drop = data['data']['dropped']
  data_ps = data['data']['pstree']
  # print(data_net)
  #读json文件
  # with open('/Users/ztxx/Desktop/HWexploit-main.zip.json') as f:
  #   data = json.load(f)

  root1 = Node_process('root',0,'')   
  res_name.clear() #进程名
  res_pid.clear() #进程pid
  res_comline.clear() #进程路径
  tree(data_ps['children'],root1)
  
  pre(root1)
  # print(res_name)
  # print(res_pid)
  # print(res_comline)
  process_count = len(res_name)
  ip_count = len(data_net['domains'])
  domain_count = len(data_net['domains'])
  dns_count = len(data_net['dns_servers'])
  # process_one = create_process_node(name_file,0,'none',graph)
  print('载入进程:',res_name)
  # print(res_pid)
  # process_one = create_process_node(res_name[1],res_pid[1],res_comline[1],graph)
  process_one  = create_file_node(name_file,sha_file,graph)
  for i in range(1,process_count):
    #print(res_name[i]+res_pid[i]+res_comline[i])
    if(res_name[i] != '' and res_pid[i] != '' and res_comline[i] != '' ):
        j = create_process_node(res_name[i],res_pid[i],res_comline[i],graph)
        create_start_rela(process_one,j,graph)
  # create_start_rela(ff,process_one,graph)
  for i in data_net['domains']:
    if(i['ip'] != '' ):
      print('关联ip:',i['ip'])
      iipp = "'"+i['ip']+"'"
      cypher_3 = "MATCH (n{ip:"+iipp+"})  RETURN n"
      ip_data = graph.run(cypher_3 ).data()
      # print(ip_data)
      if ip_data == []:
        j = create_ip_node(i['ip'],graph)
        # print('aaaa',j)
        create_link_rela(process_one,j,graph)
      else:
        create_link_rela(process_one,ip_data[0]['n'],graph)
    else:
      j = create_ip_node('---',graph)
      create_link_rela(process_one,j,graph)
    k = create_domain_node(i['domain'],graph)
    create_link_rela(process_one,k,graph)
    create_parse_rela(k,j,graph)

  for i in data_net['dns_servers']:
    # dns如果去重 将子图拼起来很乱 而且影响由ip返回样本
    # ddns = "'"+i+"'"      
    # cypher_3 = "MATCH (n{dns:"+ddns+"})  RETURN n"
    # dns_data = graph.run(cypher_3 ).data()
    # if dns_data == []:
    #   m = create_dns_node(i,graph)
    #   create_link_rela(process_one,m,graph)
    # else:
    #   create_link_rela(process_one,dns_data[0]['n'],graph)
    m = create_dns_node(i,graph)
    create_link_rela(process_one,m,graph)
      

  print("数据导入完成")
  return True

def clean_data(graph):
  #清空数据库
  graph.delete_all() 
  print("旧数据已删除")
  
def get_gragh_byip(ip,graph):
  ip = "'"+ip+"'"
  nodes_list = []
  links_list = []
  dns_list = []
  cypher_3 = "MATCH p=(nn)-[r:`连接`]->(n{ip:"+ip+"})  RETURN nn"
  nodes_data = graph.run(cypher_3 ).data()
  # print(nodes_data)
  for file in nodes_data:
    nodes1_list,links1_list = get_gragh(file['nn']['sha'],graph)
    # print(nodes1_list)
    for i in nodes1_list:
      if i['node']['dns'] != None:
        if i['node']['dns'] not in dns_list:
          dns_list.append(i['node']['dns'])
          nodes_list.append(i)
      # print('i是',i,'    list:',nodes_list,'\n',i not in nodes_list)
      elif i not in nodes_list:
        nodes_list.append(i)
    for i in links1_list:
      if i not in links_list:
        links_list.append(i)
  # print((nodes_list))
  return nodes_list,links_list

#获取文件网络行文详情
def get_gragh(sha1,graph):
  # name1 = "'hh3.0.exe'"
  # name1 = "'"+name1+"'"
  sha1 = "'"+sha1+"'"
  cypher_1 = "MATCH (node{sha:"+sha1+"}) RETURN node "
  cypher_11 = "MATCH (node1{sha:"+sha1+"})-->(node) RETURN node "

  cypher_2 = "match data=(node1:文件{sha:"+sha1+"})-[link]->(node2) return node1,type(link),node2"
  cypher_22 = "match (node:文件{sha:"+sha1+"})-[link1]->(node1)-[link2]->(node2) return node1,type(link2),node2"
  # "MATCH (a)-[r]->(b) RETURN id(a) as a_id, r.funded_amount, r.funded_rate, type(r), id(b) as b_id LIMIT 10"
  # cypher_2 ="MATCH p=()-->() RETURN p LIMIT 25"
  # 连接数据库
  # 查询，并使用.data()序列化数据
  
  nodes_data = graph.run(cypher_1 ).data()
  nodes_data += graph.run(cypher_11 ).data()
  # da = graph.run(cypher_1).to_data_frame()
  
  links_data = graph.run(cypher_2 ).data()
  links_data += graph.run(cypher_22 ).data()
  # print('aa',links_data,nodes_data)
  # print(da)
  # for node in nodes_data:
  #     print(node)

  # for link in links_data:
  #     print(link)
  return (nodes_data,links_data)


if __name__ == '__main__':
  graph = Graph('bolt://localhost:7687',auth='neo4j',password='123456')
  clean_data(graph)
  sha_list = ['bcd9aa6199612ec0ebec498222221e94b47ec23c2eba425791f753eae444b552',
              '08afebd78cb63025988d19587fd6edbb46460b890c4cc73e7e9ce82fbfa4f03f',
              '273b04eb37269be2b9ca465e4da755a8fdfbff65049bd21879234fc4e66e4953',
              '515987734680f578fdd05e47f599091e9bcf9648f38eadb22abf75b9c5726a5d',
              '9616ae6194d02e44f1cc5b55fc63ce6ab7af2d1cb92941b9bc754cd5adefc6da',
              'ed84f99a2ccf53e6b55c7987766354cb44e7d7a196417dcbce6d9d4c9bdac87c',
              '948b9943a900bba5dcd6fbace5b57ff83d8ee733e4858668695b923009cd72f8',
              '32494bb6dbf9bf8e13d8b740d7ed9485f6504f60ca6504d7b27dab7036eb3578',
              '9376c6c51115f58e865eb81abba2542baf3ce43636012491ef9b08e2129f362e',
              '707e92a1fb41885fd84e1561a88f7c183953f9256a00570777aea6cf425fb5eb',
              '85945a04af106e06d88248e94b03b6e88a247daff74ff36c925664b77e36ba89',
              'fadf85ad82a2ab73a97e0d1f4afd4baea81ac06be1dd23b2b5bb11b885f022fd',
              '3abe2e37b126cff858a0aa8385c0703d3a57aa2b2564f7ae5efc6fcc78d0c0ec']
  sha_list.append('df6ef08c7f15923c029a8aedf16daf5a5fb56a49942c314bf4e7bc3f3d1139d3')

  for sha in sha_list:
    update_file_network(sha,graph)
    
  # li1,li2 = get_gragh_byip('43.248.129.49',graph)
  # li1,li2 = get_gragh_byip('99.84.140.81',graph)
  # print('222',li1)
  # a = [{'node': Node('dns', dns='8.8.8.8')}]
  # b = {'node': Node('dns', dns='8.8.8.8')}
  # print ( b['node']['ip'])
  # nodes_data,links_data = get_gragh('3abe2e37b126cff858a0aa8385c0703d3a57aa2b2564f7ae5efc6fcc78d0c0ec',graph)
  # for node in nodes_data:
  #     print(node)

  # for link in links_data:
  #     print(link)