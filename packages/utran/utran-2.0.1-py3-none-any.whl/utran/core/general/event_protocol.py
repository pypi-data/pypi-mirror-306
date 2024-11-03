from enum import Enum as _Enum
import typing as _typing

from utran.core.backend.base import AbstractConnection as _AbstractConnection
from utran.core.local.action import LocalAction as _LocalAction
import asyncio as _asyncio


class EventProtocolTypes(_Enum):
    new_connection = "new_connection"
    close_connection = "close_connection"
    execute_wokeblock = "execute_wokeblock"
    execute_local_action = "execute_local_action"
    
    

class NewConnectionEvent(_typing.TypedDict):
    type: _typing.Literal[EventProtocolTypes.new_connection]
    conn: _AbstractConnection


class CloseConnectionEvent(_typing.TypedDict):
    type: _typing.Literal[EventProtocolTypes.close_connection]
    surplus_connections: tuple[_AbstractConnection, ...]
    cur_imp_action_keys: tuple[str, ...]


class ExecuteWokeBlockEvent(_typing.TypedDict):
    type: _typing.Literal[EventProtocolTypes.execute_wokeblock]


class ExecuteLocalActionEvent(_typing.TypedDict):
    """执行本地Action"""
    type: _typing.Literal[EventProtocolTypes.execute_local_action]
    action: _LocalAction
    params: dict
    future:_asyncio.Future


