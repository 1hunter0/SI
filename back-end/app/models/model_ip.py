# coding: utf-8
from sqlalchemy import Column, DECIMAL, ForeignKey, Integer, TIMESTAMP
from sqlalchemy.dialects.mysql import VARCHAR
from sqlalchemy.orm import relationship
from app.database import Base
from model_dns import DnsEntity

class IpAlarmEvent(Base):
    __tablename__ = 'ip_alarm_event'

    event_id = Column(Integer, primary_key=True)
    ip_subject = Column(ForeignKey('ip_entity.ip', ondelete='RESTRICT', onupdate='RESTRICT'), nullable=False, index=True, comment='攻击者ip')
    ip_object = Column(ForeignKey('ip_entity.ip', ondelete='RESTRICT', onupdate='RESTRICT'), nullable=False, index=True, comment='受害者ip')
    dev_info = Column(VARCHAR(255), nullable=False, comment='告警来源设备')
    hostname = Column(VARCHAR(255), nullable=False, comment='告警来源ip')
    timestamp = Column(TIMESTAMP, nullable=False, comment='告警发生时间')
    attack_stage = Column(VARCHAR(255), comment='攻击阶段')
    attack_status = Column(Integer, comment='攻击状态')
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

    ip_subject_entity = relationship('IpEntity', back_populates="subject_alarms", foreign_keys=[ip_subject])
    ip_object_entity = relationship('IpEntity', back_populates='object_alarms', foreign_keys=[ip_object])

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class IpEntity(Base):
    __tablename__ = 'ip_entity'

    ip = Column(VARCHAR(255), primary_key=True)
    country = Column(VARCHAR(255))
    province = Column(VARCHAR(255))
    city = Column(VARCHAR(255))
    isp = Column(VARCHAR(255))
    latitude = Column(DECIMAL(10, 6))
    longitude = Column(DECIMAL(10, 6))

    subject_alarms = relationship("IpAlarmEvent", back_populates="ip_subject_entity", foreign_keys=[IpAlarmEvent.ip_subject])
    object_alarms = relationship("IpAlarmEvent", back_populates="ip_object_entity", foreign_keys=[IpAlarmEvent.ip_object])
