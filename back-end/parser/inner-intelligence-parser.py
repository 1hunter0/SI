import json
import MySQLdb
import re
import datetime
import constants

necessaryFields = {"hostname", "dev_info", "source", "timestamp", "src_ip", "dst_ip"}
alarmFieldMap = {"ip_subject": "src_ip", "ip_object": "dst_ip"}


def initializeDB():
    """
    初始化MySQL数据库连接, 建表
    :return: csr, 数据库cursor
    """
    conn = MySQLdb.connect(constants.HOST, constants.USER, constants.PWD)
    csr = conn.cursor()
    csr.execute("USE " + constants.DB)
    with open('../db/ip_entity.sql', encoding="utf-8") as f:
        csr.execute(f.read())
    with open('../db/ip_alarm_event.sql', encoding="utf-8") as f:
        csr.execute(f.read().encode('utf8'))
    return csr, conn


def filter(alarm):
    """
    Decide whether filter an alarm or not
    :param alarm: the alarm to be filtered
    :return: true for filtering this alarm
    """
    for field in necessaryFields:
        if field not in alarm:
            return true


def loadTable(fileName):
    """
    Load table's fields from .sql file
    :param fileName: the name of the sql file
    :return: the table's fields
    """
    fields = []
    with open(fileName, encoding="utf-8") as f:
        lst = ""
        cnt = 0
        for word in f.read().split():
            if word.upper() == "PRIMARY":
                break
            if re.match('`([^"]*)`', lst):
                if cnt > 1:
                    fields.append([lst.replace("`", ""), word.split('(')[0]])
                cnt += 1
            lst = word
    return fields

def insertIP(alarm, ipFields, csr):
    values = []
    for field in ipFields:
        mapField = "src" + ("_" if field == "ip" else ".") + field

def insertIntoTable(alarm, fields, csr, table):
    """
    Insert alarm event or ip info into corresponding table.
    :param alarm: alarm event
    :param fields: fields of corresponding table
    :param csr: mysqldb cursor
    :return:
    """
    values = []
    for field in fields:
        if table == "ip_alarm_event":
            mapField = alarmFieldMap[field[0]] if field[0] in alarmFieldMap else field[0]
        else:
            mapField = "src" + ("_" if field[0] == "ip" else ".") + field[0]
        if mapField in alarm:
            value = str(alarm[mapField])
            if field[1].lower() == "varchar":
                value = "\"" + value + "\""
            elif field[1].lower() == "timestamp":
                value = datetime.datetime.fromtimestamp(int(value)/1000)
                value = "\"" + str(value) + "\""
            values.append(value)
        else:
            values.append("NULL")
    strValues = ""
    for value in values:
        strValues += str(value) + ','
    strValues = strValues[:-1]
    sql = ("INSERT INTO " + table + " values(" + strValues + ")")
    try:
        csr.execute(sql.encode("utf8"))  # TODO: there is problem in the first record 阻止HTTP协议头部X-Forwarded-For字段è'
    except:
        pass


if __name__ == "__main__":
    csr, conn = initializeDB()
    alarmFields = loadTable("../db/ip_alarm_event.sql")
    ipFields = loadTable("../db/ip_entity.sql")

    f = open("data.json", encoding="utf-8")
    for line in f:
        alarm = json.loads(line)
        insertIntoTable(alarm, ipFields, csr, "ip_entity")
        insertIntoTable(alarm, alarmFields, csr, "ip_alarm_event")
    conn.commit()