from sqlalchemy.orm import Session
from app.models import models as model_user
from ..utils import get_password_hash as pwdhash


def get_user(db: Session, username: str):
    try:
        return db.query(model_user.User).filter(model_user.User.username == username).first()
    except Exception as e:
        print(e)


def create_user(db: Session, username: str, password: str):
    user_ = model_user.User()
    user_.username = username
    user_.password = pwdhash(password)
    try:
        db.add(user_)
        db.commit()
        db.refresh(user_)
    except Exception as e:
        print(e)
    return user_
