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

IPALARMFIELD = {"ip_subject": "src_ip",
                "ip_object": "dst_ip",
                "dev_info": "dev_info",
                "hostname": "hostname",
                "timestamp": "timestamp",
                "attack_stage": "ATTACKSTAGE",
                "attack_status": "ATTACKSTATUS",
                "dev_category": "dev_category",
                "dev_rule": "dev_rule",
                "degree": "degree",
                "forbid_status": "forbid_status",
                "req_method": "req_method",
                "kill_chain": "kill_chain",
                "kill_chain_all": "kill_chain_all",
                "attack_type": "attack_type",
                "attack_type_all": "attack_type_all",
                "att_ck_all": "att_ck_all",
                "att_ck": "att_ck",
                "threat_phase": "threat.phase"}

ALARMNOTNULL = {"ip_subject": "src_ip",
                "ip_object": "dst_ip",
                "dev_info": "dev_info",
                "hostname": "hostname",
                "timestamp": "timestamp"}

DNSFIELD = {}
URLFIELD = {}
