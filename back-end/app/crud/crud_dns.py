from sqlalchemy.orm import Session
from app.models import models as model_dns


def get_dns_info(db: Session, dns: str):
    try:
        return db.query(model_dns.DnsEntity).filter(model_dns.DnsEntity.dns == dns).first()
    except Exception as e:
        print(e)
