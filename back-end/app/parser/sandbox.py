# 获取文件检测内容
import json
import requests
from conf.common import SANDBOX_URL, SANDBOX_APIKEY


class SandBox:

    def __init__(self, sha1: str):
        self.url = SANDBOX_URL
        self.apikey = SANDBOX_APIKEY
        self.param = {
            'apikey': self.apikey,
            'sha1': sha1
        }

    def parser(self):
        """
        :return:
        """
        response = requests.get(self.url, params=self.param)
        assert response.status_code==200

        data = response.json()['data']
        fields = {"file_name", "file_type", "sha1", "md5", "submit_time", "threat_level", "threat_score",
                  "multi_engines", "sandbox_type_list", "sandbox_behaviors", "multiengines_results"}
        values = {}

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
        threat_score = (data['summary']['threat_score'])
        multi_engines = data['summary']['multi_engines']
        # print("沙箱运行环境: ")
        list_env = []
        for i in data['summary']['sandbox_type_list']: list_env.append(i)

        # 反病毒引擎检测
        list_antvir = []
        for key, value in data['multiengines']['result'].items():
            # print("引擎:"+key+" 检出:"+value)
            list2 = [key, value]
            list_antvir.append(list2)
        # print("扫描时间: "+data['multiengines']['scan_time'])

        # 行为检测
        # 严重程度1为通用行为 2位可疑行为 3位高危行为
        # print('行为检测')
        list_behavior = []
        for item in data['signature']:
            des = json.loads(item['description'])
            list1 = [item['name'], des['cn'], str(item['severity'])]
            list_behavior.append(list1)
            # print('异常名称: '+item['name']+' \n说明: '+des['cn'] +'\n严重程度:'+str(item['severity'])+'\n')

        values['sha1'] = sha1
        values['file_name'] = file_name
        values['file_type'] = file_type
        values['md5'] = md5
        values['submit_time'] = submit_time
        values['threat_level'] = threat_level
        values['multi_engines'] = multi_engines
        list_env = ",".join([str(x) for x in list_env])
        values['sandbox_type_list'] = list_env
        values['threat_score'] = threat_score
        list_behavior = ",".join([str(x) for x in list_behavior])
        values['sandbox_behaviors'] = list_behavior
        list_antvir = ",".join([str(y) for y in list_antvir])
        values['multiengines_results'] = list_antvir
        return values


if __name__ == '__main__':
    sha1 = '9a6df3a428fa48f1605edd636c985fcc82d9293d'
    ans = SandBox(sha1).parser()
    print(ans)
