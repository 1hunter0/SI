import json
import re
import copy
import datetime
from conf import common
from app.schemas import schema_ip, schema_dns, schema_url


class InnerParser:
    def __init__(self, alarm):
        self.alarm = alarm
        self.ip = []
        self.ip_alarm = schema_ip.Alarm()
        self.dns = schema_dns.DnsBase()
        self.url = schema_url.UrlBase()
        self.parser()

    def ip_parser(self):
        if self.alarm.get("src_ip"):
            ip_ = schema_ip.IpBase()
            for k in common.IPFIELD.keys():
                setattr(ip_, k, self.alarm.get(common.IPFIELD[k]))
            self.ip.append(ip_)

        dstdata = self.alarm.get("dst_ip")
        if dstdata is not None:
            dst_ip = schema_ip.IpBase(ip=self.alarm.get("dst_ip"))
            self.ip.append(dst_ip)

    def alarm_parser(self):
        for k in common.ALARMNOTNULL.keys():
            if self.alarm.get(common.ALARMNOTNULL[k]) is None:
                self.ip_alarm = None
                return

        for k in common.IPALARMFIELD.keys():
            value = self.alarm.get(common.IPALARMFIELD[k])
            if k == "timestamp":
                value = datetime.datetime.fromtimestamp(int(value) / 1000)
            value = str(value)
            if len(value) > 250:
                value = value[:250]
            setattr(self.ip_alarm, k, str(value))

    def dns_parser(self):
        pass

    def url_parser(self):
        pass

    def parser(self):
        self.ip_parser()
        self.dns_parser()
        self.url_parser()
        self.alarm_parser()


if __name__ == '__main__':
    f = open("/Users/corazon/Code/PycharmProjects/SI/back-end/parser/data.json", encoding="utf-8")
    a = {}
    for line in f:
        data = json.loads(line)
        b = InnerParser(data)
        if b.ip_alarm is not None:
            print(b.ip_alarm.dict())
