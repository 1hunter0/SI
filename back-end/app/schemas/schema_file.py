from typing import Union
from pydantic import BaseModel


class FileBase(BaseModel):
    sha1: Union[str, None] = None
    file_name: Union[str, None] = None
    file_type: Union[str, None] = None
    submit_time: Union[str, None] = None
    threat_level: Union[str, None] = None
    multi_engines: Union[str, None] = None
    sandbox_type_list: Union[str, None] = None
    threat_score: Union[str, None] = None
    sandbox_behaviors: Union[str, None] = None
    multiengines_results: Union[str, None] = None
