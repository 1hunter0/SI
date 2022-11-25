from sqlalchemy.orm import Session
from sqlalchemy import func, distinct
from app.models import models as model_ip
from app.schemas import schema_ip
from app.utils import threat_comparison


def get_inner_ip(db: Session, ip: str):
    try:
        return db.query(model_ip.IpEntity).filter(model_ip.IpEntity.ip == ip).first()
    except Exception as e:
        print(e)


def get_ip_num(db: Session, query=None):
    try:
        if query is None:
            count = db.query(func.count(distinct(model_ip.IpEntity.ip))).scalar()
        else:
            count = db.query(func.count(distinct(model_ip.IpEntity.ip))) \
                .filter(model_ip.IpEntity.ip.like("%" + query + "%")).scalar()
        return count
    except Exception as e:
        print(e)


def get_ip_info_by_offset(db: Session, page_size: int, curpage: int, query=None):
    offset = (curpage - 1) * page_size
    try:
        if query is None:
            return db.query(model_ip.IpEntity) \
                .order_by(model_ip.IpEntity.id). \
                limit(page_size) \
                .offset(offset) \
                .all()
        else:
            return db.query(model_ip.IpEntity) \
                .filter(model_ip.IpEntity.ip.like("%" + query + "%")) \
                .order_by(model_ip.IpEntity.id) \
                .limit(page_size) \
                .offset(offset) \
                .all()
    except Exception as e:
        print(e)


def get_ip_relevant_alarm(db: Session, ip: str):
    try:
        query_res_sub = db.query(model_ip.IpAlarmEvent).filter(model_ip.IpAlarmEvent.ip_subject == ip).all()
        query_res_obj = db.query(model_ip.IpAlarmEvent).filter(model_ip.IpAlarmEvent.ip_object == ip).all()
        return query_res_sub, query_res_obj
    except Exception as e:
        print(e)


def create_alarm(db: Session, alarm: schema_ip.Alarm):
    try:
        db_alarm = db.query(model_ip.IpAlarmEvent).filter(model_ip.IpAlarmEvent.ip_object == alarm.ip_object,
                                                          model_ip.IpAlarmEvent.ip_subject == alarm.ip_subject,
                                                          model_ip.IpAlarmEvent.attack_type == alarm.attack_type) \
            .first()
        if db_alarm is None:
            db_alarm = model_ip.IpAlarmEvent()
            for k, v in alarm.dict().items():
                setattr(db_alarm, k, v)
        db_alarm.count += 1
        db.merge(db_alarm)
        db.commit()
        # db.refresh(db_alarm)
        return db_alarm
    except Exception as e:
        print(e)


def create_ip(db: Session, ip: schema_ip.IpBase):
    db_ip = model_ip.IpEntity()
    for k, v in ip.dict().items():
        setattr(db_ip, k, v)
    crrip = get_inner_ip(db, ip.ip)
    if crrip:
        if crrip.country is None:
            # set highest alarm degree as ip degree
            if threat_comparison(crrip.degree, db_ip.degree):
                db_ip.degree = crrip.degree
        else:
            if threat_comparison(db_ip.degree, crrip.degree):
                crrip.degree = db_ip.degree
            db_ip = crrip
    try:
        db.merge(db_ip)
        db.commit()
    except Exception as e:
        print(e)
    return db_ip
