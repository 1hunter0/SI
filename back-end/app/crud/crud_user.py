from sqlalchemy.orm import Session
from app.models import models as model_user


def get_user(db: Session, username: str):
    try:
        return db.query(model_user.User).filter(model_user.User.username == username).first()
    except Exception as e:
        print(e)
