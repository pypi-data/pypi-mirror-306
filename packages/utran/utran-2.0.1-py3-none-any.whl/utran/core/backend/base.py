# interface.py
from abc import ABC, abstractmethod
import asyncio
import threading
from typing import (
    Any,
    AsyncGenerator,
    Callable,
    Coroutine,
    Generic,
    Literal,
    Optional,
    TypeVar,
    cast,
)
import uuid
from utran.core.general.message_protocol import MessageTypedDict, FirstMessageTypedDict,BaseMessageTypedDict
from utran.core import context

SocketResponse = TypeVar("SocketResponse")

App = TypeVar("App")
Request = TypeVar("Request")
Response = TypeVar("Response")
Connection = TypeVar("Connection", bound="AbstractConnection")


# class Handler(Protocol, Generic[Request, Response]):
#     async def __call__(self, request: Request) -> Response: ...
class ConectionClosedError(Exception):
    """连接已关闭"""

    pass


class AbstractConnection(ABC, Generic[SocketResponse]):
    """
    ### Ut连接抽象类
    """

    imp_ations: list[str]
    peername: str
    uri: str  # uri: 用于标识连接的来源,和发起连接。

    __slots__ = (
        "imp_ations",
        "_host_id",
        "__connection_id",
        "_socket",
        "__msgNum",
        "_all_future_ids",
        "__connect_type",
        "__close_event",
        "_server_uri",
    )

    def __init__(
        self,
        ws: SocketResponse,
        *,
        host_id: Optional[str] = None,
        connect_type: Literal["act", "psv"] = "psv",
    ):
        """###
        - connect_type: 连接分类，用于区分是主动连接`act`，还是被动连接`psv`。即：`psv`被动等待客户端的连接，`act`主动连接到指定的服务端。
        """
        self._host_id = host_id
        self.__connect_type = connect_type

        self.__connection_id = uuid.uuid4().hex
        self._socket = ws
        self.__msgNum = 0
        self.imp_ations = []
        self._server_uri = ""
        self._all_future_ids: list[str] = []
        self.pre_init()
        self.__close_event = asyncio.Event()
        self.loop.create_task(
            self.__waiting_close_event(),
            name=f"conn_waiting_close::{self.__connection_id}",
        )

    @property
    def loop(self):
        """backend loop"""
        return context.__UTRAN_CONTEXT__["backend_loop"]

    @property
    def close_event(self):
        return self.__close_event

    async def __waiting_close_event(self):
        await self.__close_event.wait()
        await self.close()

    def pre_init(self) -> None:
        pass

    def set_init_data(
        self, host_id: str, server_uri: str, imp_ations: list[str]
    ) -> None:
        if not host_id:
            raise RuntimeError("cannot set empty of host_id.")
        if self._host_id is not None:
            raise RuntimeWarning("host_id can't be set repeatedly.")
        self._host_id = host_id
        self._server_uri = server_uri
        self.imp_ations = imp_ations

    @property
    def connect_type(self):
        return cast(Literal["act", "psv"], self.__connect_type)

    @property
    def LOCAL_HOST_ID(self):
        return context.__UTRAN_CONTEXT__["host_id"]

    @property
    def HOST_INSTANCE(self):
        return context.__UTRAN_CONTEXT__["host_instance"]

    @property
    def host_id(self):
        if self._host_id is None:
            raise RuntimeError("host_id is not set")
        return self._host_id

    @property
    def connection_id(self):
        return self.__connection_id

    def new_msg_id(self):
        self.__msgNum += 1
        return "msg_" + str(self.__msgNum)

    async def send(
        self,
        msg: BaseMessageTypedDict,
    ):
        # return asyncio.run_coroutine_threadsafe(self._send_json(msg), self.loop)
        await self._send_json(msg)

    def __aiter__(
        self,
    ) -> AsyncGenerator[
        FirstMessageTypedDict | MessageTypedDict,
        Any,
    ]:
        return self.iter_msg()

    @abstractmethod
    def iter_msg(
        self,
    ) -> AsyncGenerator[
        FirstMessageTypedDict | MessageTypedDict,
        Any,
    ]:
        pass

    @abstractmethod
    async def _send_json(self, data: Any) -> None:
        pass

    @abstractmethod
    def is_closed(self) -> bool:
        pass

    @abstractmethod
    async def close(self):
        pass


MethodType = Literal["GET", "POST"]


class AbstractBackend(ABC, Generic[App, Connection]):
    """_summary_
    ### 后端抽象类
    Args:
        ABC (_type_): _description_
        Generic (_type_): _description_

    Returns:
        _type_: _description_
    """

    __slots__ = (
        "_app",
        "__context__",
        "_ping_interval",
        "_ping_timeout",
        "_safe_stop_signal",
    )

    def __init__(
        self,
        app_instance: App,
        acept_connection: Callable[[AbstractConnection], Coroutine],
        run_startup: Callable,
        ping_interval: Optional[float] = None,
        ping_timeout: Optional[float] = None,
    ):
        self._app = app_instance
        entry_url = context.__UTRAN_CONTEXT__["entry_url"]
        self._safe_stop_signal = False
        self.pre_init(
            run_startup=run_startup,
            entry_url=entry_url,
            acept_connection=acept_connection,
        )
        self._ping_interval = ping_interval
        self._ping_timeout = ping_timeout


    @abstractmethod
    def name(self)->str:
        """后端名称"""
        pass


    @property
    def LOCAL_HOST_ID(self):
        return context.__UTRAN_CONTEXT__["host_id"]

    @property
    def host_instance(self):
        """Host实例"""
        if context.__UTRAN_CONTEXT__["host_instance"]:
            return context.__UTRAN_CONTEXT__["host_instance"]
        raise RuntimeError("host instance is None")

    @property
    def loop(self):
        """backend loop"""
        return context.__UTRAN_CONTEXT__["backend_loop"]

    @abstractmethod
    def pre_init(
        self,
        *,
        run_startup: Callable,
        entry_url: str,
        acept_connection: Callable[[AbstractConnection], Coroutine],
    ):
        # handle = partial(self._handle_request, self._request_processor)
        # self.get(self.entry_url, cast(Handler, handle))  # 注册websocket入口
        pass

    def run(self, host: str, port: int):
        context.__UTRAN_CONTEXT__["backend_thread_id"] = threading.current_thread().native_id
        self._run(host, port)

    def stop(self):
        self._safe_stop_signal = True
        self._stop()

    @abstractmethod
    def _run(self, host: str, port: int):
        pass

    @abstractmethod
    def _stop(self):
        pass
