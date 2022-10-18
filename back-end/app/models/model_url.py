# coding: utf-8
from sqlalchemy import Column, DECIMAL, ForeignKey, Integer, TIMESTAMP
from sqlalchemy.dialects.mysql import VARCHAR
from sqlalchemy.orm import relationship
from app.database import Base
from model_dns import DnsEntity



class UrlEntity(Base):
    __tablename__ = 'url_entity'

    url = Column(VARCHAR(255), primary_key=True)
    history_dns = Column(ForeignKey('dns_entity.dns', ondelete='RESTRICT', onupdate='RESTRICT'), nullable=False, index=True, comment='历史dns')

    dns_url = relationship('DnsEntity', back_populates='related_url_entity', foreign_keys=[DnsEntity.related_url])
    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


