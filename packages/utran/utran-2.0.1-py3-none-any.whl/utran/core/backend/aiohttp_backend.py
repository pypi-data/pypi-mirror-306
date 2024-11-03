# aiohttp_backend.py
import asyncio
import json
import threading
from typing import Any, AsyncGenerator, Callable, Coroutine

from utran.core.general import message_protocol

from .base import AbstractBackend, AbstractConnection
from aiohttp import web
from aiohttp.web import Application
from utran.log import logger
from utran.core import context

SocketResponse = web.WebSocketResponse
ImplementBackend = AbstractBackend[Application, "Connection"]
ImplementConnection = AbstractConnection[SocketResponse]


class Connection(ImplementConnection):
    
    _waiting_close_event = asyncio.Event()
    def is_closed(self) -> bool:
        return self._socket.closed

    async def close(self):
        await self._socket.close()
        
    def pre_init(self) -> None:
        sock = self._socket.get_extra_info("socket")
        peername = sock.getpeername()
        self.peername = f'{peername[0]}:{peername[1]}'
        
        ping_interval = context.__UTRAN_CONTEXT__["ping_interval"]
        ping_timeout = context.__UTRAN_CONTEXT__["ping_timeout"]
        self._waiting_close_event.set()
        if ping_interval and ping_timeout:
            self.loop.create_task(self._send_ping(ping_interval, ping_timeout))
        
    async def _send_ping(self, ping_interval: float,ping_timeout: float) -> None:
        await asyncio.sleep(ping_interval)  # 空转，让其他等任务可以执行
        while not self._socket.closed:
            await self._socket.ping()
            logger.debug("send Ping")
            self._waiting_close_event.clear()
            try:
                # 计算耗时
                start_time = asyncio.get_running_loop().time()
                await asyncio.wait_for(self._waiting_close_event.wait(), timeout=ping_timeout)
                dt = asyncio.get_running_loop().time() - start_time
                sleep_time = ping_interval - dt
                if sleep_time > 0:
                    await asyncio.sleep(sleep_time)
            except asyncio.TimeoutError:
                await self._socket.close()
                break
        logger.debug("auto ping task is stoped.")
        
        
    async def iter_msg(self) -> AsyncGenerator[message_protocol.FirstMessageTypedDict | message_protocol.MessageTypedDict, Any]:
        while not self.is_closed():
            try:
                msg = await self._socket.receive()
            except Exception:  # pragma: no cover
                break
 
            if msg.type == web.WSMsgType.TEXT:
                data = json.loads(msg.data)
                yield data
                
            elif msg.type == web.WSMsgType.PONG:
                logger.debug("receive Pong")
                self._waiting_close_event.set()
                
            elif msg.type == web.WSMsgType.ERROR:
                logger.error(f"got error msg: {msg.extra}")
                
            elif msg.type in (web.WSMsgType.CLOSE, web.WSMsgType.CLOSING, web.WSMsgType.CLOSED):  # pragma: no cover
                break
            
            else:
                logger.debug(f"Received non-text message:[type]:{msg.type} ,[data]:{str(msg.data)}")

        logger.debug("Connection closed")

    async def _send_json(self, data: Any) -> None:
        return await self._socket.send_json(data)


class Backend(ImplementBackend):
    
    def name(self) -> str:
        return "aiohttp"
    
    def _run(self, host: str, port: int):
        context.__UTRAN_CONTEXT__["backend_thread_id"] = threading.current_thread().native_id
        try:
            web.run_app(self._app, host=host, port=port,loop=self.loop)
        except Exception as e:
            if self._safe_stop_signal:
                logger.info("backend stopped")
            else:
                logger.exception(e)
                raise e from e

    def pre_init(
        self,
        *,
        run_startup: Callable[..., Any],
        entry_url: str,
        acept_connection: Callable[[AbstractConnection], Coroutine]
    ):
        
        self.add_startup_callback(run_startup)
        async def _request_processor(
            request: web.Request
        ) -> web.Response:
            ws = web.WebSocketResponse(autoping=False)  # 取消默认的ping功能
            await ws.prepare(request)
            await acept_connection(Connection(ws))
            return web.Response()
    
        self._app.router.add_route("GET", entry_url, _request_processor)
                

    def add_startup_callback(self, callback: Callable): 
        async def handler(app):
            await callback() if asyncio.iscoroutinefunction(callback) else callback()
                
        self._app.on_startup.append(handler)
        
        
    def _stop(self):
        asyncio.run_coroutine_threadsafe(self._app.shutdown(), self.loop)
        self.loop.stop()
