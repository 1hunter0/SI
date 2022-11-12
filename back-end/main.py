import uvicorn
from fastapi import FastAPI, Request
from app.database import Base, engine
from app.api import router_ip
from app.api import router_dns
from app.api import router_file
from app.api import router_url
from app.api import router_user
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from app.schemas import schema_response
from jose import jwt
import app.utils as utils
from app.global_variable import *

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(router_ip)
app.include_router(router_dns)
app.include_router(router_file)
app.include_router(router_url)
app.include_router(router_user)


@app.middleware("http")
async def check_token(request: Request, call_next):
    path: str = request.get('path')
    if path.startswith('/users/login') | path.startswith('/users/info') | path.startswith(
            '/users/register') | path.startswith(
            '/docs') | path.startswith('/openapi.json')|path.startswith('/ips/upload'):  # docs文档接口需要排除，登录接口需要排除,注册接口需要排除
        response = await call_next(request)
        return response
    else:
        try:
            x_token: str = request.headers.get('X-Token')
            if not x_token:
                return JSONResponse(
                    content=jsonable_encoder(schema_response.MyResponse(
                        ErrCode=TOKENFAIL,
                        ErrMessage="尚未登录，请先登录"
                    ))
                )
            _ = jwt.decode(x_token, utils.SECRET_KEY, algorithms=utils.ALGORITHM)
            response = await call_next(request)
            return response
        except jwt.ExpiredSignatureError:
            return JSONResponse(
                content=jsonable_encoder(schema_response.MyResponse(
                    ErrCode=TOKENEXPIRED,
                    ErrMessage="token已经过期，请重新登录"
                ))
            )
        except Exception:
            return JSONResponse(
                content=jsonable_encoder(schema_response.MyResponse(
                    ErrCode=TOKENFAIL,
                    ErrMessage="token验证失败"
                ))
            )


if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)
