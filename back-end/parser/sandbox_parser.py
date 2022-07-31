
# 准备json文件，里边内容为：{"name": "tom", "age": "28"}

import json
import pymysql



#获取文件检测内容
import json
import requests
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
data = data['data']

#print(data['network']['hosts'])
#读json文件
# with open('/Users/ztxx/Desktop/HWexploit-main.zip.json') as f:
#   data = json.load(f)
fields = {"file_name","file_type","sha1","md5","submit_time","threat_level","threat_score","multi_engines"
          ,"sandbox_type_list","sandbox_behaviors","multiengines_results"}
values = []

# 查看文件基本信息
# print('文件名称: '+data['summary']['file_name'])
# print("文件类型: "+data['summary']['file_type'])
# print("sha1: "+data['summary']['sha1'])
# print("md5: "+data['summary']['md5'])
# print("文件提交时间: "+data['summary']['submit_time'])
# print("文件威胁等级: "+data['summary']['threat_level'])
# print("文件威胁分值: "+str(data['summary']['threat_score']))
# print("反病毒扫描引擎检出率: "+data['summary']['multi_engines'])

file_name = data['summary']['file_name']
file_type = data['summary']['file_type']
sha1 = data['summary']['sha1']
md5 = data['summary']['md5']
submit_time = data['summary']['submit_time']
threat_level = data['summary']['threat_level']
threat_score = str(data['summary']['threat_score'])
multi_engines = data['summary']['multi_engines']
print("沙箱运行环境: ")
list_env = []
for i in data['summary']['sandbox_type_list']: list_env.append(i)


# 反病毒引擎检测
list_antvir=[]
for key,value in data['multiengines']['result'].items():
    #print("引擎:"+key+" 检出:"+value)
    list2 =[]
    list2.append(key)
    list2.append(value)
    list_antvir.append(list2)
#print("扫描时间: "+data['multiengines']['scan_time'])

# 行为检测
# 严重程度1为通用行为 2位可疑行为 3位高危行为
print('行为检测')
list_behavior =[]
for item in data['signature']:
  des = json.loads(item['description'])
  list1 = []
  list1.append(item['name'])
  list1.append(des['cn'])
  list1.append(str(item['severity']))
  list_behavior.append(list1)
  #print('异常名称: '+item['name']+' \n说明: '+des['cn'] +'\n严重程度:'+str(item['severity'])+'\n')

values.append(sha1)
values.append(file_name)
values.append(file_type)
values.append(md5)
#values.append(submit_time)
values.append("2232523525")
values.append(threat_level)
values.append(multi_engines)
list_env = ",".join([str(x) for x in list_env])
#values.append(list_env)
values.append(threat_score)
list_behavior= ",".join([str(x) for x in list_behavior])
#values.append(list_behavior)
list_antivir= ",".join([str(x) for x in list_antvir])
#values.append(list_antvir)
values.append("test1")
values.append("test1")
values.append("test1")
valuesTuple = tuple(values)
print(list_antivir)
#json文件 (非api版！！没用。。)keys值：info  behavior tsmam metadata screenshots static strings sigma target network signatures tags

values.append("test1")
values.append("test1")
values.append("test1")

# 连接数据库
conn = pymysql.connect(
        host = 'localhost',
    #端口号
        port = 3306,
    #用户名
        user = 'root',
    #密码
        passwd = '12345678',
    #数据库名称
        db = 'test_sandbox',
    #字符编码格式
        charset = 'utf8')
cur = conn.cursor()

# with open('../db/sandbox_file_entity.sql', encoding="utf-8") as f:
#         cur.execute(f.read().encode('utf8'))
# 拼接values为：%s, %s
values = ', '.join(['%s']*len(fields)) 

# 插入的表名
table = 'sandbox_file_entity'

# 插入sql语句
insertSql = 'INSERT INTO {table} VALUES ({values})'.format(table=table,  values=values)
print(insertSql)
#执行建表与插入sql
#cur.execute(createTableSql)
cur.execute(insertSql,valuesTuple)

# 提交commit
conn.commit()

# 关闭数据库连接
conn.close()
    

print("数据更新完毕!!!")

