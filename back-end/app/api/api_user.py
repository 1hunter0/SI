from fastapi import APIRouter, Depends, Response
from app.schemas import schema_user, schema_response
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.crud import crud_user
from datetime import timedelta
import app.utils as utils
from app.global_variable import *
from jose import jwt

router_user = APIRouter(
    prefix="/users",
    tags=["users"]
)


@router_user.post("/login", response_model=schema_response.MyResponse)
def login(LoginForm: schema_user.LoginIn, response: Response, db: Session = Depends(get_db)):
    username, password = LoginForm.username, LoginForm.password
    user = crud_user.get_user(db, username)
    if not user:
        # response.status_code = status.HTTP_404_NOT_FOUND
        return schema_response.MyResponse(ErrCode=FAIL, ErrMessage="没有该用户信息")

    verify_result = False
    try:
        verify_result = utils.verify_password(password, user.password)
    except Exception as e:
        print(e)

    if not verify_result:
        # response.status_code = status.HTTP_400_BAD_REQUEST
        return schema_response.MyResponse(ErrCode=FAIL, ErrMessage="用户密码错误")

    # 过期时间
    access_token_expires = timedelta(minutes=utils.ACCESS_TOKEN_EXPIRE_MINUTES)
    # 加密，要使用str类型
    access_token = utils.create_access_token(
        data={"username": user.username, "id": user.id}, expires_delta=access_token_expires
    )
    return schema_response.MyResponse(
        ErrCode=SUCCESS,
        Data=schema_user.Token(token=access_token)
    )


@router_user.get("/info", response_model=schema_response.MyResponse)
def info(token: str, db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, utils.SECRET_KEY, algorithms=utils.ALGORITHM)
        username: str = payload.get("username")
    except jwt.ExpiredSignatureError:
        return schema_response.MyResponse(ErrCode=TOKENEXPIRED, ErrMessage="token已经过期，请重新登录")
    except Exception:
        return schema_response.MyResponse(ErrCode=TOKENFAIL, ErrMessage="token验证失败")

    user = crud_user.get_user(db, username)
    if not user:
        return schema_response.MyResponse(ErrCode=FAIL, ErrMessage="没有该用户信息")
    return schema_response.MyResponse(
        ErrCode=SUCCESS,
        Data=schema_user.UserInfo(username=user.username)
    )
