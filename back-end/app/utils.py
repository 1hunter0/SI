from typing import Optional

from passlib.context import CryptContext
from jose import JWTError, jwt

from datetime import datetime, timedelta

from sqlalchemy.orm import class_mapper

SECRET_KEY = "34b07e82a13f987e00150782965d59e196376a9bc8ad2a6fbdf33830749ae4a2"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# 使用的算法是Bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str):
    """
    对密码进行加密
    :param password: 原生密码
    :return: 加密后的密码
    """
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password) -> bool:
    """
    校验密码是否正确
    :param plain_password:
    :param hashed_password:
    :return:
    """
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """

    :param data: 需要进行JWT令牌加密的数据（解密的时候会用到）
    :param expires_delta: 令牌有效期
    :return: token
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    # 添加失效时间
    to_encode.update({"exp": expire})
    # SECRET_KEY：密钥
    # ALGORITHM：JWT令牌签名算法
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def serialize(model):
    """Transforms a model into a dictionary which can be dumped to JSON."""
    # first we get the names of all the columns on your model
    columns = [c.key for c in class_mapper(model.__class__).columns]
    # then we return their values in a dict
    return dict((c, getattr(model, c)) for c in columns)


from app.global_variable import THREAT_LEVEL


def threat_comparison(threat1: str, threat2: str):
    """
    # compare threat level by THREAT_LEVEL in global_variable
    :param threat1:
    :param threat2:
    :return: threat1 level >  threat2 level
    """
    if threat1 is None:
        return False
    if threat2 is None:
        return True
    return THREAT_LEVEL[threat1] > THREAT_LEVEL[threat2]


if __name__ == '__main__':  # 测试
    print(get_password_hash("123456"))
    print(verify_password("123456", "$2b$12$DYN8BofHRXwFdVkG.QQH1uG5PnHeEVFhTT.Nq1.HU3LKQtBEC4KWG"))
    print(threat_comparison('high',None))
