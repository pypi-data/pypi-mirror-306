from pg_resourceloader import LoaderManager
from pg_common import FuncDecoratorManager
from pg_environment import config
from typing import Dict, Union, Tuple, Optional
from pg_common import datetime_now, datetime_2_timestamp, DictValType
from pydantic import BaseModel


__all__ = [
    "ENV_HANDLER_DIR", "httpserver_init", "ENV_NEEDS_BODY_MIDDLEWARE", "ENV_CHECK_SESSION_HEADER_KEY",
    "ENV_NEEDS_GAME_CONFIG", "ENV_NEEDS_GAME_PROPERTY", "ENV_NEEDS_CHECK_SESSION", "ENV_CHECK_SESSION_IGNORE_URI",
    "GameException", "GameErrorCode", "FieldContainer", "ResponseMap", "ResponseHeader", "ResponseData", "RequestMap",
    "RequestHeader", "RequestData", "Container", "SESSION_EXPIRED_TIME", "ENV_CONTAINER_KEY"
]
__auth__ = "baozilaji@gmail.com"


ENV_HANDLER_DIR = "handler_dir"
ENV_NEEDS_BODY_MIDDLEWARE = "needs_body_middleware"
ENV_NEEDS_GAME_CONFIG = "needs_game_config"
ENV_NEEDS_GAME_PROPERTY = "needs_game_property"
ENV_NEEDS_CHECK_SESSION = "needs_check_session"
ENV_CHECK_SESSION_IGNORE_URI = "check_session_ignore_uri"
ENV_CHECK_SESSION_HEADER_KEY = "check_session_header_key"
ENV_CONTAINER_KEY = "container_key"
"""
http server configuration
{
  "handler_dir": "handler",
  "needs_body_middleware": true,
  "needs_game_config": false,
  "needs_game_property": false,
  "needs_check_session": false,
  "check_session_ignore_uri": ['/test_uri',],
  "check_session_header_key": "Authentication",
  "container_key": "_container_",
}
"""


def httpserver_init():
    FuncDecoratorManager.scan_decorators(config.get_conf(ENV_HANDLER_DIR, "handlers"))
    LoaderManager.scan_loaders()


SESSION_EXPIRED_TIME = 3600


class GameErrorCode(object):
    RECEIVE_INPUT_ERROR = -100000
    NO_MATCHED_METHOD_ERROR = -100001
    OTHER_EXCEPTION = -100002


class GameException(Exception):

    def __init__(self, state: int, msg: str):
        self.state = state
        self.msg = msg

    def __str__(self):
        return f"\"{self.state}, {self.msg}\""

    def __repr__(self):
        return self.__str__()



class FieldContainer(object):
    def __init__(self):
        self._content: dict[str, set[str]] = {}

    def add(self, obj:str, field: str):
        if obj not in self._content:
            self._content[obj] = set()
        self._content[obj].add(field)

    def add_many(self, obj: str, fields: Union[set[str], list[str], Tuple[str]]):
        if obj not in self._content:
            self._content[obj] = set()
        self._content[obj].update(fields)

    def __str__(self):
        return str(self._content)


class ResponseMap(BaseModel):
    method: str = ""
    retCode: int = 0


class ResponseHeader(BaseModel):
    datas: list[ResponseMap] = []
    retCode: int = 0 # 错误码
    st: int = 0 # 自增计数
    token: str = "" # 单点登陆的token
    ts: int = int(datetime_2_timestamp(datetime_now())) # 时间（秒）
    offSt: int = 0 # 离线请求自增计数
    msg: str = "" # 消息


class ResponseData(BaseModel):
    head: ResponseHeader
    body: dict


class RequestMap(BaseModel):
    method: str = ""
    data: str = ""
    param: dict = {}


class RequestHeader(BaseModel):
    datas: list[RequestMap] = []
    method: str = ""
    uid: int = 0
    v: int = 0 # 客户端版本号
    mv: int = 0 # meta版本号
    ct: int = 0 # 客户端类型, 1: ios, 2: android, 3: wp
    uuid: str = "" # session key
    st: int = 0 # 自增计数
    channel: str = "" # 区分不同包
    lang: str = "" # 语言
    token: str = "" # 单点登陆的token
    offSt: int = 0 # 离线请求自增计数
    rv: int = 0 # res版本号
    extra: str = "" # 额外数据，如network环境等
    pj: str = "" # 项目名称


class RequestData(BaseModel):
    head: RequestHeader
    body: dict


class Container(BaseModel):
    log: dict[str, DictValType] = {}
    req: Optional[dict] = {}
    resp: Optional[dict] = {}
    user: Optional[dict] = {}