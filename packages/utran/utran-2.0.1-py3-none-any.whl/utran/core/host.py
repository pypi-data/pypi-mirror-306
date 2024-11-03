"""# utran.core.host"""

import threading
import asyncio
import typing
from concurrent.futures import ThreadPoolExecutor
from cachetools import TTLCache
from utran.core.backend import (
    AbstractConnection,
    AbstractBackend,
    create_backend,
)


from utran.log import logger
from utran.core.backend import create_connection
from utran.core import ipc as UtIPC
from utran.core.local.action import Action
from utran.core import schedule as UtSchedule


# 所有在线的连接
__CONNECTIONS__: dict[str, AbstractConnection] = {}


# 获取延迟
class ConnectionDelay(typing.TypedDict):
    """连接延迟"""

    host_id: str
    delay: float


class GetConnectionsDelay(Action):
    """获取所有连接延迟"""

    def __init__(self):
        async def get_connections_delay(timeout: float = 5):
            """## 获取所有连接延迟"""
            from utran.core import context

            loop = context.__UTRAN_CONTEXT__["backend_loop"]

            async def _task(conn: AbstractConnection) -> ConnectionDelay:
                start_time = loop.time()
                try:
                    msg = UtIPC.gen_base_msg(conn)
                    fu = UtIPC.send(conn, msg, futrue=UtIPC.gen_future_msg(msg))
                    await asyncio.wait_for(fu, timeout=timeout)
                except asyncio.TimeoutError:
                    return {"host_id": conn.host_id, "delay": -1}
                delay = loop.time() - start_time
                return {"host_id": conn.host_id, "delay": delay}

            res = await asyncio.gather(
                *[loop.create_task(_task(conn)) for conn in __CONNECTIONS__.values()]
            )
            return res

        # 缓存2秒，并且带锁
        super().__init__(get_connections_delay, lock=True, cache=TTLCache(1, ttl=2))


async def acept_connection(conn: AbstractConnection):
    """### 允许连接"""
    try:
        conn.loop.create_task(
            UtIPC.IPC_Handler(conn)(),
            name=f"conn_handle::{conn.connection_id}",
        )
        await conn.close_event.wait()
    except Exception as e:
        logger.debug(e)
    finally:
        await conn.close()


async def run_startup():
    """前置运行
    > `AppServer`  `aiohttp.web.Application`  `fastapi.FastAPI` 服务的前置运行
    """
    from utran.core import context

    if context.__UTRAN_CONTEXT__["__start_by__"] == None:
        # from utran import __init_start__
        # __init_start__()
        context.__UTRAN_CONTEXT__["__start_by__"] = "backend"
        

    if (
        asyncio.get_running_loop() != context.__UTRAN_CONTEXT__["backend_loop"]
    ):  # 说明是由server_instance启动的
        context.__UTRAN_CONTEXT__["backend_loop"] = asyncio.get_running_loop()

    loop = context.__UTRAN_CONTEXT__["backend_loop"]
    loop.create_task(UtIPC.run_backend_send_queue_forever())  # 启动发送队列
    loop.create_task(UtSchedule.run_backend_dispatcher_queue_forever())  # 启动处理队列
    
    for uri in context.__UTRAN_CONTEXT__["act_connect_uris"]:  # 开始act连接
        try:
            logger.info(f"[act] connecting to {uri}")
            conn = await create_connection(uri)
            conn.uri = uri
            loop.create_task(UtIPC.IPC_Handler(conn)(), name="conn_handle::act")
            logger.log("CONN",f"[act] connection success: {uri}")
        except Exception as e:
            logger.exception(e)
            logger.error(f"[act] connection error: {e}")

    # if main_handler:
    #     loop.create_task(main_handler(), name="main_handler")  # 启动主服务


class Host:

    __slots__ = (
        "IMP_ACTION_LIST",
        "_backend",
        "__dispatcher",
        "__context__",
        "_wokeblock_store"
    )

    def __init__(self) -> None:
        from utran.core import context
        from utran.core.remote.wokeblock import _Store 
        
        self._wokeblock_store = _Store
        
        context.__UTRAN_CONTEXT__["host_instance"] = self

        max_workers = context.__UTRAN_CONTEXT__["max_workers"]
        context.__UTRAN_CONTEXT__["worker_pool"] = ThreadPoolExecutor(
            max_workers=max_workers
        )

        context.__UTRAN_CONTEXT__["main_thread_id"] = (
            threading.current_thread().native_id
        )

        asyncio.set_event_loop(
            context.__UTRAN_CONTEXT__["main_loop"]
        )  # 设置主线程的loop

        self.__context__ = context.__UTRAN_CONTEXT__

        self.__dispatcher = UtSchedule.Dispatcher()

        self._backend: AbstractBackend = create_backend()

    def _is_in_backend_thread(self):
        """是否在服务后端线程"""
        return (
            self.__context__["backend_thread_id"]
            == threading.current_thread().native_id
        )

    def _is_in_main_thread(self):
        """是否在主线程"""
        return (
            self.__context__["main_thread_id"] == threading.current_thread().native_id
        )

    @classmethod
    def instance(cls) -> "Host":
        """当前host实例"""
        from utran.core import context

        return context.__UTRAN_CONTEXT__["host_instance"]

    @property
    def server_uri(self):
        """本地服务地址"""
        return (
            self.__context__["host"]
            + ":"
            + str(self.__context__["port"])
            + self.__context__["entry_url"]
        )

    @property
    def conneted_uris(self):
        """已连接的uri"""
        return [
            conn.uri
            for conn in __CONNECTIONS__.values()
            if conn.uri in self.__context__["act_connect_uris"]
        ]

    @property
    def connect_uris(self):
        """需要去连接的主机uri"""
        return self.__context__["act_connect_uris"]

    @property
    def host_id(self):
        """本地host_id"""
        return self.__context__["host_id"]

    @property
    def dispatcher(self):
        """调度器"""
        return self.__dispatcher

    def stop_backend(self):
        """停止服务后端"""
        self._backend.stop()

    def exit(self):
        """停止服务"""
        self._backend.stop()
        self.__context__["exit_event"].set()

    @classmethod
    def add_connect_uri(cls, *uris: str):
        """添加需要主动连接的uri"""
        from utran.core import context

        context.__UTRAN_CONTEXT__["act_connect_uris"].extend(uris)


def add_act_uri(*uris: str):
    """添加主动连接 act"""
    from utran.core import context

    for uri in uris:
        if uri in context.__UTRAN_CONTEXT__["act_connect_uris"]:
            continue
        context.__UTRAN_CONTEXT__["act_connect_uris"].append(uri)
