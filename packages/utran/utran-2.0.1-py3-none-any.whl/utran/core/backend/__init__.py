# main.py

from typing import Literal
from .base import AbstractBackend, AbstractConnection
from .ut_backend import Backend as UtBackend
from .ut_backend import Connection as UtConnection
from .ut_backend import create_connection
from utran.socket.sever import AppServer
from utran.core import context

BackendType = Literal["aiohttp", "fastapi"]


def create_backend() -> AbstractBackend:
    from utran.core.host import run_startup, acept_connection

    server_instance = context.__UTRAN_CONTEXT__['_server_instance']
    ping_interval = context.__UTRAN_CONTEXT__["ping_interval"]
    ping_timeout = context.__UTRAN_CONTEXT__["ping_timeout"]

    if server_instance is None:
        return UtBackend(
            AppServer(ping_interval=ping_interval, ping_timeout=ping_timeout),
            acept_connection=acept_connection,
            run_startup=run_startup,
            ping_interval=ping_interval,
            ping_timeout=ping_timeout,
        )

    if isinstance(server_instance, AppServer):
        return UtBackend(
            server_instance,
            acept_connection=acept_connection,
            run_startup=run_startup,
            ping_interval=ping_interval,
            ping_timeout=ping_timeout,
        )

    try:
        from aiohttp import web

        if isinstance(server_instance, web.Application):
            from .aiohttp_backend import Backend as AiohttpBackend

            return AiohttpBackend(
                server_instance,
                acept_connection=acept_connection,
                run_startup=run_startup,
                ping_interval=ping_interval,
                ping_timeout=ping_timeout,
            )
    except Exception:
        pass

    try:
        from fastapi import FastAPI

        if isinstance(server_instance, FastAPI):
            from .fastapi_backend import Backend as FastAPIBackend

            return FastAPIBackend(
                server_instance,
                acept_connection=acept_connection,
                run_startup=run_startup,
                ping_interval=ping_interval,
                ping_timeout=ping_timeout,
            )
    except:
        pass

    raise ValueError(
        "Invalid app instance for backend,Options: aiohttp,fastapi,appServer"
    )


__all__ = [
    "create_backend",
    "AbstractBackend",
    "AbstractConnection",
    "UtConnection",
    "UtBackend",
    "create_connection",
]
