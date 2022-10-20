from sqlalchemy.orm import Session
from app.models import models as model_file
from app.schemas import schema_file


def get_file_info(db: Session, sha1: str):
    try:
        ans = db.query(model_file.SandboxFileEntity).filter(model_file.SandboxFileEntity.sha1 == sha1).first()
        return ans
    except Exception as e:
        print(e)


def create_file(db: Session, file: schema_file.FileBase):
    db_file = model_file.SandboxFileEntity()
    for k, v in file.dict().items():
        setattr(db_file, k, v)
    try:
        db.add(db_file)
        db.commit()
        db.refresh(db_file)
    except Exception as e:
        print(e)
    return db_file
