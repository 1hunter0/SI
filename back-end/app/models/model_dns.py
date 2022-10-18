# coding: utf-8
from sqlalchemy import Column, DECIMAL, ForeignKey, Integer, TIMESTAMP
from sqlalchemy.dialects.mysql import VARCHAR
from sqlalchemy.orm import relationship
from app.database import Base
from model_ip import IpEntity
from model_url import UrlEntity


class DnsEntity(Base):
    __tablename__ = 'dns_entity'

    dns = Column(VARCHAR(255), primary_key=True)
    analysis_ip = Column(ForeignKey('ip_entity.ip', ondelete='RESTRICT', onupdate='RESTRICT'), nullable=False, index=True, comment='解析ip')
    history_ip = Column(ForeignKey('ip_entity.ip', ondelete='RESTRICT', onupdate='RESTRICT'), nullable=False, index=True, comment='历史ip')
    related_url = Column(ForeignKey('url_entity.url', ondelete='RESTRICT', onupdate='RESTRICT'), nullable=False, index=True, comment='相关url')
    
    analysis_ip_entity = relationship('IpEntity', back_populates="ip_dns_analysis", foreign_keys=[analysis_ip])
    history_ip_entity = relationship('IpEntity', back_populates='ip_dns_history', foreign_keys=[history_ip])
    related_url_entity = relationship('UrlEntity', back_populates='dns_url', foreign_keys=[related_url])



    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


