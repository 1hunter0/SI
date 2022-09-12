from sqlalchemy.orm import Session
from app.models import model_ip
from app.schemas import schema_ip


def get_inner_ip(db: Session, ip: str):
    try:
        return db.query(model_ip.IpEntity).filter(model_ip.IpEntity.ip == ip).first()
    except Exception as e:
        print(e)


def create_alarm(db: Session, alarm: schema_ip.Alarm):
    db_alarm = model_ip.IpAlarmEvent()
    for k, v in alarm.dict().items():
        setattr(db_alarm, k, v)
    try:
        db.add(db_alarm)
        db.commit()
        db.refresh(db_alarm)
    except Exception as e:
        print(e)
    return db_alarm


def create_ip(db: Session, ip: schema_ip.IpBase):
    db_ip = model_ip.IpEntity()
    for k, v in ip.dict().items():
        setattr(db_ip, k, v)
    try:
        db.add(db_ip)
        db.commit()
        db.refresh(db_ip)
    except Exception as e:
        print(e)
    return db_ip


