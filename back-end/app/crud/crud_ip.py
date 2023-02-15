from sqlalchemy.orm import Session
from sqlalchemy import func, distinct
from app.models import models as model_ip
from app.schemas import schema_ip
from app.utils import threat_comparison
from conf.riskconf import RISKNUM, REASON_FREQUENT


def get_inner_ip(db: Session, ip: str):
    try:
        return db.query(model_ip.IpEntity).filter(model_ip.IpEntity.ip == ip,
                                                  model_ip.IpEntity.country.isnot(None)).first()
    except Exception as e:
        print(e)


def get_ip(db: Session, ip: str):
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


def get_risk_alarm_num(db: Session, query=None):
    try:
        if query is None:
            count = db.query(func.count(distinct(model_ip.RiskIpAlarmEvent.ip_subject))).scalar()
        else:
            count = db.query(func.count(distinct(model_ip.RiskIpAlarmEvent.ip_subject))) \
                .filter(model_ip.RiskIpAlarmEvent.ip_subject.like("%" + query + "%")).scalar()
        return count
    except Exception as e:
        print(e)


def get_ip_info_by_offset(db: Session, page_size: int, curpage: int, query=None):
    offset = (curpage - 1) * page_size
    try:
        if query is None:
            return db.query(model_ip.IpEntity) \
                .filter(model_ip.IpEntity.country.isnot(None)) \
                .order_by(model_ip.IpEntity.id) \
                .limit(page_size) \
                .offset(offset) \
                .all()
        else:
            return db.query(model_ip.IpEntity) \
                .filter(model_ip.IpEntity.country.isnot(None)) \
                .filter(model_ip.IpEntity.ip.like("%" + query + "%")) \
                .order_by(model_ip.IpEntity.id) \
                .limit(page_size) \
                .offset(offset) \
                .all()
    except Exception as e:
        print(e)


def get_riskalarm_by_offset(db: Session, page_size: int, curpage: int, query=None):
    offset = (curpage - 1) * page_size
    try:
        if query is None:
            return db.query(model_ip.RiskIpAlarmEvent) \
                .limit(page_size) \
                .offset(offset) \
                .all()
        else:
            return db.query(model_ip.RiskIpAlarmEvent) \
                .filter(model_ip.RiskIpAlarmEvent.ip_subject.like("%" + query + "%")) \
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


def get_ip_relevant_risk_alarm(db: Session, ip: str):
    try:
        query_res_sub = db.query(model_ip.RiskIpAlarmEvent).filter(model_ip.RiskIpAlarmEvent.ip_subject == ip)
        query_res_obj = db.query(model_ip.RiskIpAlarmEvent).filter(model_ip.RiskIpAlarmEvent.ip_object == ip)
        return query_res_sub.union(query_res_obj).all()
    except Exception as e:
        print(e)


def get_topk_attack_type(db: Session, ip: str, k: int):
    try:
        attack_type_list = db.query(model_ip.IpAlarmEvent.attack_type,
                                    func.count(model_ip.IpAlarmEvent.attack_type)) \
            .filter(model_ip.IpAlarmEvent.ip_subject == ip) \
            .group_by(model_ip.IpAlarmEvent.attack_type) \
            .order_by(func.count(model_ip.IpAlarmEvent.attack_type).desc()) \
            .all()
        #print(attack_type_list[0][0])
        if attack_type_list[0][0] == 'None':
            return attack_type_list[1:k+1]
        return attack_type_list[:k]
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
        if db_alarm.count >= RISKNUM:
            create_risk_alarm(db, db_alarm, REASON_FREQUENT)
        db.merge(db_alarm)
        db.commit()
        # db.refresh(db_alarm)
        return db_alarm
    except Exception as e:
        print(e)


def create_risk_alarm(db: Session, alarm: schema_ip.Alarm, riskreason: str):
    try:
        db_alarm = db.query(model_ip.RiskIpAlarmEvent).filter(model_ip.RiskIpAlarmEvent.ip_object == alarm.ip_object,
                                                              model_ip.RiskIpAlarmEvent.ip_subject == alarm.ip_subject,
                                                              model_ip.RiskIpAlarmEvent.attack_type == alarm.attack_type) \
            .first()
        if db_alarm is not None:
            return db_alarm
        db_alarm = model_ip.RiskIpAlarmEvent()
        setattr(db_alarm, "ip_object", alarm.ip_object)
        setattr(db_alarm, "ip_subject", alarm.ip_subject)
        setattr(db_alarm, "attack_type", alarm.attack_type)
        setattr(db_alarm, "reason", riskreason)
        db.add(db_alarm)
        db.commit()
        # db.refresh(db_alarm)
        return db_alarm
    except Exception as e:
        print(e)


def create_ip(db: Session, ip: schema_ip.IpBase):
    db_ip = model_ip.IpEntity()
    crrip = get_ip(db, ip.ip)
    if crrip:
        if crrip.country is None:
            try:
                # set highest alarm degree as ip degree
                if threat_comparison(crrip.degree, ip.degree):
                    ip.degree = crrip.degree
                db_ip = db.query(model_ip.IpEntity).filter(model_ip.IpEntity.ip == ip.ip).update(ip.dict())
                db.commit()
                db.refresh(db_ip)
            except Exception as e:
                print(e)
        else:
            try:
                if threat_comparison(ip.degree, crrip.degree):
                    # ip higher than crrip
                    db_ip = db.query(model_ip.IpEntity).filter(model_ip.IpEntity.ip == ip.ip).update(
                        {"degree": ip.degree})
                    db.commit()
                    db.refresh(db_ip)
            except Exception as e:
                print(e)
        return db_ip
    for k, v in ip.dict().items():
        setattr(db_ip, k, v)
    try:
        db.add(db_ip)
        db.commit()
        db.refresh(db_ip)
    except Exception as e:
        print(e)
    return db_ip
