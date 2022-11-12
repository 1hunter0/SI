from typing import Union

from pydantic import BaseModel


class MyResponse(BaseModel):
    Data: Union[object, None] = None
    ErrCode: int  # 必填
    ErrMessage: Union[str, None] = None


