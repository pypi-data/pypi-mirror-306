import asyncio
from concurrent.futures import ThreadPoolExecutor

import threading
from typing import Literal, Optional, TypedDict, cast
import uuid
import hashlib

from utran.core.host import Host


class ContextTypeDict(TypedDict):
    """上下文信息
    - host: str 主机名或IP地址
    - port: int 端口号
    - host_id: str 主机唯一标识
    - host_instance: Host 主机实例
    - act_connect_uris: list[str] 主动连接的服务地址列表
    - entry_url: str 入口URL
    - ping_interval: Optional[float] 心跳间隔
    - ping_timeout: Optional[float] 心跳超时
    - exit_event: threading.Event 退出事件
    - backend_loop: asyncio.AbstractEventLoop 服务后端的loop
    - backend_thread_id: Optional[int] 服务后端的线程ID
    - backend_dispatcher_queue: asyncio.Queue 服务后端的消息队列
    - main_thread_id: Optional[int] 主线程ID
    - max_workers: int 最大线程数
    - worker_pool: ThreadPoolExecutor 线程池
    - main_loop: asyncio.AbstractEventLoop 主线程的loop
    - debug: bool 调试模式
    - log_folder:str 日志文件夹, 默认为None 不输出日志
    - thread_local_data:threading.local 线程本地数据
    - _server_instance: Optional[object]   服务实例， 支持以下服务实例 AppServer, aiohttp.web.Application , fastapi.FastAPI
    - __env__: Literal["dev", "prod" , "_dev_"] 环境类型， 注： 本库_dev_ 仅用于开发环境
    - __identify_signature__: str 身份标识签名
    - __start_by__:Literal["default", "backend", None]    用于标识是否是通过那种方式启动的服务, 当为None时, 表示是服务还未启动
    """

    host: str
    port: int
    host_id: str
    host_instance: "Host"
    act_connect_uris: list[str]
    entry_url: str
    ping_interval: Optional[float]
    ping_timeout: Optional[float]
    exit_event: threading.Event
    backend_loop: asyncio.AbstractEventLoop
    backend_thread_id: Optional[int]
    backend_dispatcher_queue: asyncio.Queue
    backend_send_queue: asyncio.Queue
    main_thread_id: Optional[int]
    max_workers: int
    worker_pool: ThreadPoolExecutor
    main_loop: asyncio.AbstractEventLoop
    debug: bool
    log_folder:Optional[str]
    thread_local_data:threading.local
    _server_instance: Optional[object]
    __env__: Literal["dev", "prod", "_dev_"]   
    __identify_signature__: str
    __start_by__:Literal["default", "backend", None]
    

# 全局唯一实例
__UTRAN_CONTEXT__: ContextTypeDict = {
    "host": "localhost",
    "port": 2525,
    "host_id": str(uuid.uuid4()),
    "host_instance": cast("Host", None),
    "main_loop": asyncio.get_event_loop(),  # 主线程的loop
    "act_connect_uris": [],
    "entry_url": "/utran",
    "ping_interval": 20,
    "ping_timeout": 30,
    "exit_event": threading.Event(),
    "backend_loop": asyncio.new_event_loop(),  # 服务后端的loop
    "backend_thread_id": None,
    "backend_dispatcher_queue": asyncio.Queue(),
    "backend_send_queue": asyncio.Queue(),
    "main_thread_id": None,
    "max_workers": 10,
    "worker_pool": cast(ThreadPoolExecutor, None),    
    "_server_instance": None,  # 服务实例 AppServer, aiohttp.web.Application , fastapi.FastAPI
    "debug": True,
    "log_folder": None,
    "thread_local_data": threading.local(),
    "__env__": "dev",   
    "__identify_signature__": str(uuid.uuid4()),  # 非外部使用，身份标识签名
    "__start_by__": None  # 用于标识是否是通过那种方式启动的服务, 当为None时，表示是服务还未启动
}


def set_config(
    host: Optional[str] = None,
    port: Optional[int] = None,
    server_instance: Optional[object] = None,
    connect_uris: Optional[list[str]] = None,  # 改为 None
    ping_interval: Optional[float] = None,  # 心跳间隔
    ping_timeout: Optional[float] = None,  # 心跳超时
    entry_url: Optional[str] = None,
    max_workers: Optional[int] = None,
):
    """设置配置"""

    context_defaults = {
        "_server_instance": server_instance,
        "entry_url": entry_url,
        "host": host,
        "port": port,
        "ping_interval": ping_interval,
        "ping_timeout": ping_timeout,
        "max_workers": max_workers,
    }

    for key, value in context_defaults.items():
        if value is not None:
            __UTRAN_CONTEXT__[key] = value  # type: ignore

    if connect_uris is None:
        active_connect_uris = []
    elif isinstance(connect_uris, str):
        active_connect_uris = [connect_uris]
    else:
        active_connect_uris = list(connect_uris)  # 确保转换为列表
    __UTRAN_CONTEXT__["act_connect_uris"].extend(active_connect_uris)



def set_server_instance(ins):
    """支持以下服务实例
    - AppServer
    - aiohttp.web.Application
    - fastapi.FastAPI
    """
    __UTRAN_CONTEXT__["_server_instance"] = ins


def set_identify(key: str):
    """设置身份标识,该标识具有唯一性,该key通过SHA-2算法生成host_id"""
    # 使用SHA-256算法生成哈希值
    sha256_hash = hashlib.sha256(key.encode()).hexdigest()
    __UTRAN_CONTEXT__["__identify_signature__"] = key
    __UTRAN_CONTEXT__["host_id"] = sha256_hash
    return sha256_hash





# // js中的实现 导入crypto-js库
# const CryptoJS = require('crypto-js'); // 如果在Node.js环境中使用

# function setIdentify(key) {
#     // 使用SHA-256算法生成哈希值
#     const hash = CryptoJS.SHA256(key).toString(CryptoJS.enc.Hex);

#     // 将生成的host_id存储到上下文中
#     __UTRAN_CONTEXT__["host_id"] = hash;

#     return hash;
# }

# // 使用示例
# const hostId = setIdentify('your_unique_key');
# console.log('Generated host_id:', hostId);
