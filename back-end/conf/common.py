# 动态沙箱
SANDBOX_URL = 'https://api.threatbook.cn/v3/file/report'
SANDBOX_APIKEY = '44a4838848ac4f5799d1ccf1cf18519a130f43810ee0413c9a93a9acf4ed684b'
FILEFIELD = {}

# 内生情报map   原始数据 to model
IPFIELD = {"ip": "src_ip",
           "province": "src.province",
           "city": "src.city",
           "isp": "src.isp",
           "country": "src.country",
           "degree": "degree"}

IPALARMFIELD = {"src_ip": "ip_subject",
                "dst_ip": "ip_object",
                "dev_info": "dev_info",
                "hostname": "hostname",
                "timestamp": "timestamp",
                "ATTACKSTAGE": "attack_stage",
                "ATTACKSTATUS": "attack_status",
                "dev_category": "dev_category",
                "dev_rule": "dev_rule",
                "degree": "degree",
                "forbid_status": "forbid_status",
                "req_method": "req_method",
                "kill_chain": "kill_chain",
                "kill_chain_all": "kill_chain_all",
                "attack_type": "attack_type",
                "attack_type_all": "attack_type",
                "att_ck_all": "attack_type",
                "att_ck": "attack_type",
                "threat.phase": "threat_phase"}

ALARMNOTNULL = {"ip_subject": "src_ip",
                "ip_object": "dst_ip",
                "dev_info": "dev_info",
                "hostname": "hostname",
                "timestamp": "timestamp"}

DNSFIELD = {}
URLFIELD = {}
