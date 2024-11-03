# aiohttp_backend.py
import asyncio
import json
from typing import Any, AsyncGenerator, Callable, Coroutine, cast

from utran.core.general import message_protocol
from utran.socket.base import WSMsgType, WebSocketProtocol
from utran.socket.sever import AppServer, Request, Response, WebSocketResponse
from utran.socket.client import WebSocketClient
from utran.log import logger
from .base import AbstractBackend, AbstractConnection


SocketResponse = WebSocketProtocol
ImplementBackend = AbstractBackend[AppServer, "Connection"]
ImplementConnection = AbstractConnection[SocketResponse]


class Connection(ImplementConnection):
    def is_closed(self) -> bool:
        return self._socket.closed

    async def close(self):
        self._socket.close()

    def pre_init(self) -> None:
        peername = self._socket._writer.get_extra_info("peername")
        self.peername = f"{peername[0]}:{peername[1]}"

        if (
            isinstance(self._socket, WebSocketResponse) and self._socket._ping_interval
        ):  # 只有服务端才有ping功能
            socket = cast(WebSocketResponse, self._socket)
            self.loop.create_task(
                socket.auto_send_ping(self._socket._ping_interval), name="ping task"
            )

    async def iter_msg(
        self,
    ) -> AsyncGenerator[message_protocol.FullMessageTypedDict, Any]:
        while not self.is_closed():
            try:
                msg = await self._socket.receive()
            except Exception:
                break
            if msg.type == WSMsgType.TEXT:
                data = json.loads(msg.data)
                yield data
            elif msg.type == WSMsgType.ERROR:
                logger.error(f"got error msg: {msg.extra}")
            elif msg.type in (WSMsgType.CLOSE, WSMsgType.CLOSING, WSMsgType.CLOSED):
                break
            elif msg.type == WSMsgType.PING or msg.type == WSMsgType.PONG:
                pass
            else:
                logger.warning(
                    f"Received non-text message:[type]:{msg.type} ,[data]:{str(msg.data)}"
                )

        logger.debug("Connection closed")

    async def _send_json(self, data: Any) -> None:
        return await self._socket.send_json(data)


class Backend(ImplementBackend):

    def _run(self, host: str, port: int):
        try:
            self._app.run(host=host, port=port, loop=self.loop)
        except Exception as e:  # pragma: no cover
            if self._safe_stop_signal:
                logger.info("backend stopped")
            else:
                logger.exception(e)
                raise e


    def name(self) -> str:
        return "default"
    
    def _stop(self):
        self._app.stop()

    def pre_init(
        self,
        *,
        run_startup: Callable[..., Any],
        entry_url: str,
        acept_connection: Callable[[AbstractConnection], Coroutine],
    ):
        self._app.add_startup_callback(run_startup)

        async def _request_processor(
            request: Request,
        ) -> Response:
            ws = request.upgrade()
            await ws.prepare()
            await acept_connection(Connection(ws))
            return Response()

        self._app.add_route("GET", entry_url, _request_processor)  # 注册websocket入口


async def create_connection(uri: str) -> Connection:
    """## 创建主动连接 act, 无论后端是什么, act连接都使用WebSocketClient"""
    ws = WebSocketClient()
    await ws.connect(uri)
    return Connection(ws, connect_type="act")
