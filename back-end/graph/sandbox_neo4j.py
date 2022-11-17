import json
import requests
from py2neo import Graph,Node,Relationship
#neo4j 连接图数据库

#实体：进程 ip 域名 dns
#关系：启动 连接 释放（暂无） [域名]解析[ip]
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
  # print(data)
  data_net = data['data']['network']
  data_drop = data['data']['dropped']
  data_ps = data['data']['pstree']
  # print(data_net)
  #读json文件
  # with open('/Users/ztxx/Desktop/HWexploit-main.zip.json') as f:
  #   data = json.load(f)

  root1 = Node_process('root',0,'')   
  # res_name = [] #进程名
  # res_pid = [] #进程pid
  # res_comline = [] #进程路径
  tree(data_ps['children'],root1)
  pre(root1)
  # print(res_name)
  # print(res_pid)
  # print(res_comline)
  process_count = len(res_name)
  ip_count = len(data_net['domains'])
  domain_count = len(data_net['domains'])
  dns_count = len(data_net['dns_servers'])
  #print(data_drop)
  #print(data_net['domains'])
  #print(data_net['tcp'])
  #print(data_net['dns_servers'])
  process_one = create_process_node(res_name[1],res_pid[1],res_comline[1],graph)
  for i in range(2,process_count):
    #print(res_name[i]+res_pid[i]+res_comline[i])
    j = create_process_node(res_name[i],res_pid[i],res_comline[i],graph)
    create_start_rela(process_one,j,graph)
    
  for i in data_net['domains']:
    j = create_ip_node(i['ip'],graph)
    k = create_domain_node(i['domain'],graph)
    create_link_rela(process_one,j,graph)
    create_link_rela(process_one,k,graph)
    create_parse_rela(k,j,graph)

  for i in data_net['dns_servers']:
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
  cypher_3 = "MATCH p=(nn)-[r:`连接`]->(n{ip:"+ip+"})  RETURN nn"
  nodes_data = graph.run(cypher_3 ).data()
  print(nodes_data)
  return nodes_data

def get_gragh(name1,graph):
  # name1 = "'hh3.0.exe'"
  name1 = "'"+name1+"'"
  cypher_1 = "MATCH (node{name:"+name1+"}) RETURN node "
  cypher_11 = "MATCH (node1{name:"+name1+"})-->(node) RETURN node "

  cypher_2 = "match data=(node1:进程{name:"+name1+"})-[link]->(node2) return node1,type(link),node2"
  cypher_22 = "match (node:进程{name:"+name1+"})-[link1]->(node1)-[link2]->(node2) return node1,type(link2),node2"
  # "MATCH (a)-[r]->(b) RETURN id(a) as a_id, r.funded_amount, r.funded_rate, type(r), id(b) as b_id LIMIT 10"
  # cypher_2 ="MATCH p=()-->() RETURN p LIMIT 25"
  # 连接数据库
  # 查询，并使用.data()序列化数据
  nodes_data = graph.run(cypher_1 ).data()
  nodes_data += graph.run(cypher_11 ).data()
  # da = graph.run(cypher_1).to_data_frame()
  
  links_data = graph.run(cypher_2 ).data()
  links_data += graph.run(cypher_22 ).data()
  # print('aa',links_data)
  # print(da)
  # for node in nodes_data:
  #     print(node)

  # for link in links_data:
  #     print(link)
  return (nodes_data,links_data)


if __name__ == '__main__':
  graph = Graph('bolt://localhost:7687',auth='neo4j',password='123456')
  # clean_data(graph)
  # sha = 'df6ef08c7f15923c029a8aedf16daf5a5fb56a49942c314bf4e7bc3f3d1139d3'
  # sha = 'bcd9aa6199612ec0ebec498222221e94b47ec23c2eba425791f753eae444b552'
  sha ='08afebd78cb63025988d19587fd6edbb46460b890c4cc73e7e9ce82fbfa4f03f'
  update_file_network(sha,graph)
  # nodes_data,links_data = get_gragh('hh3.0.exe',graph)
  # for node in nodes_data:
  #     print(node)

  # for link in links_data:
  #     print(link)