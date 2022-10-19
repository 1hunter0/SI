# coding: utf-8
from sqlalchemy import Column, DECIMAL, ForeignKey, Integer, String, TIMESTAMP
from sqlalchemy.dialects.mysql import VARCHAR
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


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
    history_dns = Column(String(255), index=True)


class DnsEntity(Base):
    __tablename__ = 'dns_entity'

    dns = Column(String(255), primary_key=True)
    analysis_ip = Column(ForeignKey('ip_entity.ip', ondelete='SET NULL', onupdate='RESTRICT'), index=True, comment='解析ip')
    related_url = Column(ForeignKey('url_entity.url', ondelete='SET NULL', onupdate='RESTRICT'), index=True, comment='相关url')

    ip_entity = relationship('IpEntity')
    url_entity = relationship('UrlEntity')
