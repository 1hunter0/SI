import json
import requests
from py2neo import Graph,Node,Relationship
#neo4j 连接图数据库
graph = Graph('bolt://localhost:7687',auth='neo4j',password='123456')

#实体：进程 ip 域名 dns
#关系：启动 连接 释放（暂无） [域名]解析[ip]
def create_process_node(name,pid,comline):
  process=Node('进程',name=name,pid=pid,comline=comline)
  graph.create(process)
  return process
  
def create_ip_node(ip):
  ip = Node('ip',ip=ip)
  graph.create(ip)
  return ip
  
def create_domain_node(domain):
  domain = Node('域名',donmain=domain)
  graph.create(domain)
  return domain
  
def create_dns_node(dns):
  dns = Node('dns',dns=dns)
  graph.create(dns)
  return dns

def create_start_rela(head,tail):
  rela = Relationship(head,"启动",tail)
  graph.create(rela)
  
def create_link_rela(head,tail):
  rela = Relationship(head,"连接",tail)
  graph.create(rela)
  
def create_drop_rela(head,tail):
  rela = Relationship(head,"释放",tail)
  graph.create(rela)

def create_parse_rela(head,tail):
  rela = Relationship(head,"解析",tail)
  graph.create(rela)
#没有network响应 考虑换沙盒环境 'sandbox_type'
url = 'https://api.threatbook.cn/v3/file/report'
params = {
    'apikey': '44a4838848ac4f5799d1ccf1cf18519a130f43810ee0413c9a93a9acf4ed684b',
    #'sandbox_type': 'win10_sp1_enx86_office2016',
    #'query_fields':'network',
    'sha256': 'df6ef08c7f15923c029a8aedf16daf5a5fb56a49942c314bf4e7bc3f3d1139d3'
}
response = requests.get(url, params=params)
data =response.json()
data_net = data['data']['network']
data_drop = data['data']['dropped']
data_ps = data['data']['pstree']

#读json文件
# with open('/Users/ztxx/Desktop/HWexploit-main.zip.json') as f:
#   data = json.load(f)
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
root1 = Node_process('root',0,'')
#遍历多叉树获取文件名
def tree(list,root):
  if len(list)!=0:
    for i in range(len(list)):
      j = Node_process(list[i]['process_name'],list[i]['pid'],list[i]['command_line'])
      root.add_child(j)
      if len(list[i]['children'])!=0:
        tree(list[i]['children'],j) 
      
res_name = [] #进程名
res_pid = [] #进程pid
res_comline = [] #进程路径
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

#每次运行先清空数据库
graph.delete_all()
print("旧数据已删除")

process_one = create_process_node(res_name[1],res_pid[1],res_comline[1])
for i in range(2,process_count):
  #print(res_name[i]+res_pid[i]+res_comline[i])
  j = create_process_node(res_name[i],res_pid[i],res_comline[i])
  create_start_rela(process_one,j)
  
for i in data_net['domains']:
  j = create_ip_node(i['ip'])
  k = create_domain_node(i['domain'])
  create_link_rela(process_one,j)
  create_link_rela(process_one,k)
  create_parse_rela(k,j)

for i in data_net['dns_servers']:
  create_dns_node(i)

print("数据导入完成")