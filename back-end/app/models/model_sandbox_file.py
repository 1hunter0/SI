# coding: utf-8
from sqlalchemy import Column, DECIMAL, ForeignKey, Integer, TIMESTAMP
from sqlalchemy.dialects.mysql import VARCHAR
from sqlalchemy.orm import relationship
from app.database import Base


class SandboxFile(Base):
    __tablename__ = 'sandbox_file'

    sha1 = Column(VARCHAR(255), primary_key=True)
    file_name = Column(VARCHAR(255), nullable=False, comment='文件名')
    file_type = Column(VARCHAR(255), nullable=False, comment='文件类型')
    md5 = Column(VARCHAR(255), comment='文件md5值')
    submit_time = Column(TIMESTAMP, nullable=False, comment='提交时间')
    threat_level = Column(VARCHAR(255), comment='威胁等级')
    multi_engines = Column(VARCHAR(255), comment='反病毒扫描引擎检出率')
    sandbox_type_list = Column(VARCHAR(255), comment='沙箱运行环境')
    threat_score = Column(Integer, comment='文件威胁分值')
    sandbox_behaviors = Column(VARCHAR(2055), comment='文件行为检测')
    multiengines_results = Column(VARCHAR(255), comment='反病毒引擎检测结果')

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


