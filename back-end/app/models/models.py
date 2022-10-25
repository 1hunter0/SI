# coding: utf-8
from sqlalchemy import Column, DECIMAL, ForeignKey, Integer, String, TIMESTAMP
from sqlalchemy.dialects.mysql import TINYINT, VARCHAR
from sqlalchemy.orm import relationship
from app.database import Base
metadata = Base.metadata


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String(255))
    password = Column(String(255))

class IpEntity(Base):
    __tablename__ = 'ip_entity'

    ip = Column(VARCHAR(255), primary_key=True)
    country = Column(VARCHAR(255))
    province = Column(VARCHAR(255))
    city = Column(VARCHAR(255))
    isp = Column(VARCHAR(255))
    latitude = Column(DECIMAL(10, 6))
    longitude = Column(DECIMAL(10, 6))


class SandboxFileEntity(Base):
    __tablename__ = 'sandbox_file_entity'

    sha1 = Column(VARCHAR(255), primary_key=True)
    file_name = Column(VARCHAR(255))
    file_type = Column(VARCHAR(255))
    md5 = Column(VARCHAR(255))
    submit_time = Column(TIMESTAMP, nullable=False, comment='提交时间时间')
    threat_level = Column(VARCHAR(255), comment='威胁等级')
    multi_engines = Column(VARCHAR(255), comment='反病毒扫描引擎检出率')
    sandbox_type_list = Column(VARCHAR(255), comment='沙箱运行环境')
    threat_score = Column(Integer, comment='文件威胁分值')
    sandbox_behaviors = Column(VARCHAR(2055), comment='文件行为检测')
    multiengines_results = Column(VARCHAR(2055), comment='反病毒引擎检测结果')


class UrlEntity(Base):
    __tablename__ = 'url_entity'

    url = Column(String(255), primary_key=True)
    history_dns = Column(VARCHAR(255), index=True, comment='历史dns')
    severity = Column(TINYINT, comment='威胁等级')


class DnsEntity(Base):
    __tablename__ = 'dns_entity'

    dns = Column(String(255), primary_key=True)
    analysis_ip = Column(ForeignKey('ip_entity.ip', ondelete='SET NULL', onupdate='RESTRICT'), index=True,
                         comment='解析ip')
    related_url = Column(ForeignKey('url_entity.url', ondelete='SET NULL', onupdate='RESTRICT'), index=True,
                         comment='相关url')
    severity = Column(TINYINT, comment='威胁等级')
    sample = Column(String(255), comment='相关样本')
    confidence = Column(String(255), comment='置信度')
    scene = Column(String(255), comment='应用场景')
    open_source = Column(String(255), comment='开源情报')

    ip_entity = relationship('IpEntity')
    url_entity = relationship('UrlEntity')


class IpAlarmEvent(Base):
    __tablename__ = 'ip_alarm_event'

    event_id = Column(Integer, primary_key=True)
    ip_subject = Column(ForeignKey('ip_entity.ip', ondelete='RESTRICT', onupdate='RESTRICT'), nullable=False,
                        index=True, comment='攻击者ip')
    ip_object = Column(ForeignKey('ip_entity.ip', ondelete='RESTRICT', onupdate='RESTRICT'), nullable=False, index=True,
                       comment='受害者ip')
    dev_info = Column(VARCHAR(255), nullable=False, comment='告警来源设备')
    hostname = Column(VARCHAR(255), nullable=False, comment='告警来源ip')
    timestamp = Column(TIMESTAMP, nullable=False, comment='告警发生时间')
    attack_stage = Column(VARCHAR(255), comment='攻击阶段')
    attack_status = Column(VARCHAR(255), comment='攻击状态')
    dev_category = Column(VARCHAR(255), comment='触发告警的规则类型')
    dev_rule = Column(VARCHAR(255), comment='触发告警的规则')
    degree = Column(VARCHAR(255), comment='程度')
    forbid_status = Column(VARCHAR(255), comment='该请求是否被防火墙阻断')
    req_method = Column(VARCHAR(255), comment='http请求方式')
    threat_phase = Column(VARCHAR(255), comment='威胁的阶段')
    kill_chain = Column(VARCHAR(255), comment='单个杀伤链')
    kill_chain_all = Column(VARCHAR(255), comment='全杀伤链')
    attack_type = Column(VARCHAR(255), comment='攻击类型及编号')
    attack_type_all = Column(VARCHAR(255), comment='攻击类型及编号')
    att_ck_all = Column(VARCHAR(255), comment='攻击类型及编号')
    att_ck = Column(VARCHAR(255), comment='攻击类型及编号')

    ip_entity = relationship('IpEntity', primaryjoin='IpAlarmEvent.ip_object == IpEntity.ip')
    ip_entity1 = relationship('IpEntity', primaryjoin='IpAlarmEvent.ip_subject == IpEntity.ip')
