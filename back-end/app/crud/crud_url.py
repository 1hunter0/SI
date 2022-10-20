from sqlalchemy.orm import Session
from app.models import models as model_url


def get_url_info(db: Session, url: str):
    try:
        return db.query(model_url.UrlEntity).filter(model_url.UrlEntity == url).first()
    except Exception as e:
        print(e)
