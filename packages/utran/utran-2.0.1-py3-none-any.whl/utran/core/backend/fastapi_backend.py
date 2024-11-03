# fastapi_backend.py
import threading
from typing import Any, AsyncGenerator, Callable, Coroutine
import fastapi
from fastapi import FastAPI
import uvicorn.config

from utran.core import context
from utran.log import logger
from utran.core.general import message_protocol
from .base import AbstractBackend,AbstractConnection
import uvicorn



SocketResponse = fastapi.WebSocket
ImplementBackend = AbstractBackend[FastAPI, "Connection"]
ImplementConnection = AbstractConnection[SocketResponse]



class Connection(ImplementConnection):
    
    def is_closed(self) -> bool:
        return self._socket.state == "DISCONNECTED"

    async def close(self):
        try:
            await self._socket.close()
        except: pass
        
    def pre_init(self) -> None:
        if self._socket.client is not None:
            client_host = self._socket.client.host
            client_port = self._socket.client.port
            self.peername = f"{client_host}:{client_port}"
        else:
            self.peername = "unknown"
            raise ValueError("pre_init中self._socket.client 为空，无法获取主机信息。")

    async def receive(self) -> message_protocol.FullMessageTypedDict:
        msg = await self._socket.receive_json()
        return msg

    def iter_msg(self) -> AsyncGenerator[message_protocol.FullMessageTypedDict, Any]:
        return self._socket.iter_json() # type: ignore

    async def _send_json(self, data:Any) -> None:
        try:
            return await self._socket.send_json(data)
        except Exception as e:
            logger.error(e)
            raise e



class Backend(ImplementBackend):
    
    def name(self) -> str:
        return "fastapi"
      
    def pre_init(self, *, run_startup: Callable[..., Any], entry_url: str, acept_connection: Callable[[AbstractConnection], Coroutine]):
        
        async def shutdown_event():
            logger.info("shutdown event")
        self._app.add_event_handler("shutdown",shutdown_event)
        
        self._app.add_event_handler("startup",run_startup)
        # self.auto_ping_interval
        @self._app.websocket(entry_url)
        async def websocket_endpoint(websocket: fastapi.WebSocket):
            await websocket.accept()
            await acept_connection(Connection(websocket))

    
    def _run(self, host: str, port: int):
        context.__UTRAN_CONTEXT__["backend_thread_id"] = threading.current_thread().native_id
        log_level = "debug" if context.__UTRAN_CONTEXT__["debug"] else None
        try:
            uvicorn.run(self._app, host=host, port=port, log_level=log_level,ws_ping_interval=self._ping_interval, ws_ping_timeout=self._ping_timeout)
        except Exception as e:
            if self._safe_stop_signal:
                logger.info("backend stopped")
            else:
                logger.exception(e)
                raise e
        
    def _stop(self):
        import os
        os._exit(0)