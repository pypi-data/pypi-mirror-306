"""
Host 交流模块
"""

import asyncio
import concurrent.futures
from concurrent.futures import CancelledError
from typing import Any, Literal, Optional, TypedDict, Union, overload, TypeVar

# from typing_extensions import NotRequired

from utran.core.general.exceptions import (
    RemoteResultError,
    RemoteRuntimeError,
    RemoteTimeoutError,
)

from .general import message_protocol as UtType
from .general import future as UtFuture
from utran.core.local import action as LocalActionModule

from utran.core.backend.base import AbstractConnection
from utran.log import logger
from utran.core import context


class MessageSendError(Exception):
    """消息发送失败"""

    pass


class ConnectionIdentifyAuthFailed(Exception):
    """连接身份认证失败"""

    pass


class SendQueueData(TypedDict):
    """发送消息队列的数据结构"""

    conn: AbstractConnection
    msg: UtType.BaseMessageTypedDict
    future: UtFuture.SyncUtFuture | UtFuture.AsyncUtFuture | None
    failed_to_broadcast:Optional[bool]


def gen_base_msg(
    conn: AbstractConnection,
    *,
    msg_id: Optional[str] = None,
    from_host: Optional[list[str]] = None,
    to_host: Optional[str] = None,
) -> UtType.BaseMessageTypedDict:
    """### 生成基础消息"""

    from_host = from_host or []
    from_host.append(conn.LOCAL_HOST_ID)

    return {
        "msg_id": msg_id or conn.new_msg_id(),
        "from_host": from_host,
        "to_host": to_host or conn.host_id,
    }


@overload
def gen_future_msg(
    msg: UtType.BaseMessageTypedDict,
    *,
    is_sync: Literal[False] = False,
    group: str = "defualt",
) -> UtFuture.AsyncUtFuture: ...
@overload
def gen_future_msg(
    msg: UtType.BaseMessageTypedDict,
    *,
    is_sync: Literal[True],
    group: str = "defualt",
) -> UtFuture.SyncUtFuture: ...
@overload
def gen_future_msg(
    msg: UtType.BaseMessageTypedDict,
    *,
    is_sync: bool,
    group: str = "defualt",
) -> UtFuture.AsyncUtFuture | UtFuture.SyncUtFuture: ...
def gen_future_msg(
    msg: UtType.BaseMessageTypedDict,
    *,
    is_sync: Literal[True, False] | bool = False,
    group: str = "defualt",
) -> UtFuture.AsyncUtFuture | UtFuture.SyncUtFuture:
    """### 生成 future_msg, 在原有消息上增加 future_id 字段，并返回 future 对象"""
    if msg.get("future_id", None) is not None:
        # ⚠️如果是消息是本地发起的不应该手动填写 future_id，只有回复和转发消息时才可以指定 future_id
        raise ValueError(
            "⚠️future_id and wait_response can't be true at the same time, because The local active message should not specify a future_id."
        )

    if is_sync:
        (future_id, futrue) = UtFuture.create_future(group)
        msg["future_id"] = future_id  # type: ignore
        return futrue
    else:
        (future_id, futrue) = UtFuture.create_async_future(group)
        msg["future_id"] = future_id  # type: ignore
        return futrue


def ready(conn: AbstractConnection, init_data: UtType.InitDataTypedDict):
    """准备完成，发送首次消息"""
    base_msg = gen_base_msg(conn, to_host="初始化连接")
    msg: UtType.FullMessageTypedDict = {**base_msg, "init_data": init_data}
    # conn.send(msg)
    
    qdata: SendQueueData = {"conn": conn, "msg": msg,"future": None,"failed_to_broadcast":False}
    q = context.__UTRAN_CONTEXT__["backend_send_queue"]
    context.__UTRAN_CONTEXT__["backend_loop"].call_soon_threadsafe(q.put_nowait, qdata)
    

def transpond(conn: AbstractConnection, payload: UtType.MessageTypedDict):
    """转发消息"""
    send(conn, payload)


def broadcast(payload: UtType.MessageTypedDict):
    """广播消息"""
    from utran.core.host import __CONNECTIONS__

    for conn in __CONNECTIONS__.values():
        transpond(conn, payload.copy())
        continue


_T = TypeVar("_T", bound=UtFuture.SyncUtFuture | UtFuture.AsyncUtFuture)


@overload
def send(
    conn: AbstractConnection,
    msg: UtType.BaseMessageTypedDict,
    *,
    failed_to_broadcast: bool = False,
) -> None: ...
@overload
def send(
    conn: AbstractConnection,
    msg: UtType.BaseMessageTypedDict,
    *,
    futrue: _T,
    failed_to_broadcast: bool = False,
) -> _T: ...
def send(
    conn: AbstractConnection,
    msg: UtType.BaseMessageTypedDict,
    *,
    futrue: Union[_T, None] = None,
    failed_to_broadcast: bool = False,
) -> Union[_T, None]:
    """发送消息"""

    qdata: SendQueueData = {"conn": conn, "msg": msg,"future": futrue,"failed_to_broadcast":failed_to_broadcast}
    q = context.__UTRAN_CONTEXT__["backend_send_queue"]
    context.__UTRAN_CONTEXT__["backend_loop"].call_soon_threadsafe(q.put_nowait, qdata)

    return futrue


def reply(
    conn: AbstractConnection,
    payload: Optional[UtType.FullMessageTypedDict] = None,
):
    """回复消息"""
    if not payload:
        base_msg = gen_base_msg(conn)
        _payload0: UtType.MessageTypedDict = {**base_msg, "to_host": conn.host_id}
        return send(conn, _payload0)
    else:
        payload["from_host"].append(conn.LOCAL_HOST_ID)
        _payload: UtType.FullMessageTypedDict = {**payload, "to_host": conn.host_id}
        return send(conn, _payload)


def sync_send_rpc_request(
    conn: AbstractConnection,
    action: str,
    params: dict,
):
    base_msg = gen_base_msg(conn)
    msg: UtType.MessageTypedDict = {**base_msg, "action": action, "data": params}
    fu = gen_future_msg(msg, group=conn.host_id, is_sync=True)
    return send(
        conn,
        msg,
        futrue=fu,
    )


def send_rpc_request(
    conn: AbstractConnection,
    action: str,
    params: dict,
):
    base_msg = gen_base_msg(conn)
    msg: UtType.MessageTypedDict = {**base_msg, "action": action, "data": params}
    fu = gen_future_msg(msg, group=conn.host_id, is_sync=False)
    return send(
        conn,
        msg,
        futrue=fu,
    )


def reply_rpc_result(
    conn: AbstractConnection,
    msg_id: str,
    future_id: Optional[str],
    from_host: list[str],
    result: Any = None,
):
    """发送rpc结果"""
    base_msg = gen_base_msg(conn, from_host=from_host, msg_id=msg_id)
    msg: UtType.MessageTypedDict = {**base_msg, "data": result, "future_id": future_id}
    send(
        conn,
        msg,
    )


def reply_rpc_error(
    conn: AbstractConnection,
    msg_id: str,
    future_id: Optional[str],
    from_host: list[str],
    error: str,
):
    """发送rpc结果"""
    base_msg = gen_base_msg(conn, from_host=from_host, msg_id=msg_id)
    msg: UtType.MessageTypedDict = {**base_msg, "error": error, "future_id": future_id}
    send(
        conn,
        msg,
    )


async def _call_local(
    target_conn: AbstractConnection,
    *,
    action: str,
    params: dict,
    reply: bool,
    msg_id: str,
    future_id: Optional[str],
    from_host: list[str],
):
    """本地Action调用"""
    logger.debug(f"请求调用本地action: {action} <- {target_conn.host_id}")
    try:
        targetAction = LocalActionModule.get_action(action)
        if not targetAction:
            if reply:
                reply_rpc_error(
                    target_conn,
                    msg_id=msg_id,
                    future_id=future_id,
                    error=f"'{action}' action not found.",
                    from_host=from_host,
                )
            logger.debug(f"无此本地action: {action}.")
            return

        result = None
        try:
            result = await target_conn.HOST_INSTANCE.dispatcher.invoke_local_action(
                targetAction, params
            )  # 等待本地调用结果
            logger.debug(f"本地action调用结果: {action} -> {result}")
        except Exception as e:
            logger.error(f"本地action调用错误: {action} -> {e}")
            if reply:
                reply_rpc_error(
                    target_conn,
                    msg_id=msg_id,
                    future_id=future_id,
                    error="remote error: " + str(e),
                    from_host=from_host,
                )

        if not reply:
            return
        # 发送结果
        reply_rpc_result(
            target_conn,
            result=result,
            msg_id=msg_id,
            future_id=future_id,
            from_host=from_host,
        )

    except Exception as e:
        logger.exception(e)
        logger.error(f"执行本地action调用发生内部错误。{e}")


def sync_remote_call(
    conn: AbstractConnection,
    action: str,
    params: dict,
    timeout: Optional[float] = None,
):
    """同步远程调用"""
    try:
        fu = sync_send_rpc_request(
            conn,
            action=action,
            params=params,
        )
        if fu is None:
            return None

        playload = fu.result(timeout=timeout)
        if playload:
            data = playload.get("data")
            error = playload.get("error")
            if error:
                raise RemoteResultError(error)
            return data
        return None
    except concurrent.futures.TimeoutError as e:
        raise RemoteTimeoutError("远程调用超时") from e
    except CancelledError as e:
        if conn.is_closed():
            raise RemoteTimeoutError("提供服务的连接已关闭，本次调用被取消 ") from e
        raise RemoteTimeoutError("远程调用被取消") from e
    except RemoteResultError as e:
        raise e
    except Exception as e:
        raise RemoteRuntimeError(e) from e


async def async_remote_call(
    conn: AbstractConnection,
    action: str,
    params: dict,
    timeout: Optional[float] = None,
):
    """异步远程调用"""
    try:
        fu = send_rpc_request(conn, action=action, params=params)

        if fu is None:
            return None

        if conn.HOST_INSTANCE._is_in_backend_thread():
            playload = await asyncio.wait_for(fu, timeout=timeout)
        else:

            async def _wait_fu():
                while not fu.done():
                    await asyncio.sleep(0)
                return fu.result()

            playload = await asyncio.wait_for(_wait_fu(), timeout=timeout)

        if playload:
            data = playload.get("data")
            error = playload.get("error")
            if error:
                raise RemoteResultError(error)
            return data
        return None
    except asyncio.exceptions.CancelledError as e:
        if conn.is_closed():
            raise RemoteTimeoutError("提供服务的连接已关闭，本次调用被取消") from e
        raise RemoteTimeoutError("远程调用被取消") from e

    except asyncio.exceptions.TimeoutError as e:
        raise RemoteTimeoutError("远程调用超时") from e
    except RemoteResultError as e:
        raise e
    except Exception as e:
        raise RemoteRuntimeError(e) from e


# 身份验证
async def auth_identity(
    target_conn: AbstractConnection,
    authenticated_conns: list[AbstractConnection],
    host_id: str,
):
    """身份验证"""
    # 1. 查看host_id是否被其他连接占用
    for conn in authenticated_conns:
        if conn.host_id == host_id:
            raise ConnectionIdentifyAuthFailed("身份验证失败, host_id已被占用")

    if True:
        return True
    else:
        raise ConnectionIdentifyAuthFailed("身份验证失败")


class IPC_Handler:
    """每个连接都会实例化一个IPC_Handler用于消息处理, 是connection的消息分发处理器"""

    __slots__ = (
        "CONNECTIONS",
        "is_first_msg",
        "conn",
    )

    def __init__(self, conn: AbstractConnection) -> None:

        from utran.core.host import __CONNECTIONS__

        self.CONNECTIONS = __CONNECTIONS__

        self.is_first_msg = True
        self.conn = conn
        imp_ations = list(LocalActionModule.LOCAL_ACTIONS.keys())
        server_uri = self.HOST_INSTANCE.server_uri
        init_data: UtType.InitDataTypedDict = {
            "server_uri": server_uri,
            "imp_ations": imp_ations,
        }
        ready(conn, init_data=init_data)  # 发送初始化消息

    @property
    def loop(self):
        return context.__UTRAN_CONTEXT__["backend_loop"]

    @property
    def dispatcher(self):
        return self.HOST_INSTANCE.dispatcher

    @property
    def LOCAL_HOST_ID(self):
        return context.__UTRAN_CONTEXT__["host_id"]

    @property
    def HOST_INSTANCE(self):
        return context.__UTRAN_CONTEXT__["host_instance"]

    async def on_first_message(self, payload: UtType.FirstMessageTypedDict):
        """仅处理首次消息"""
        if not self.is_first_msg:
            return False
        from_host = payload["from_host"]
        init_data = payload["init_data"]
        imp_ations = init_data["imp_ations"]
        server_uri: str = init_data.get("server_uri", None) or ""

        # 初步连接身份验证
        if from_host.__len__() != 1:
            raise ConnectionIdentifyAuthFailed(
                "身份验证失败, 首次消息中from_host长度大于1"
            )
        if from_host[0] == self.LOCAL_HOST_ID:
            raise ConnectionIdentifyAuthFailed("身份验证失败, 不合法host_id")

        if from_host[0] in self.CONNECTIONS:
            raise ConnectionIdentifyAuthFailed("身份验证失败, host_id已被占用")

        # 身份验证
        await auth_identity(
            target_conn=self.conn,
            authenticated_conns=list(self.CONNECTIONS.values()),
            host_id=from_host[0],
        )

        self.is_first_msg = False
        self.conn.set_init_data(
            host_id=from_host[0], server_uri=server_uri, imp_ations=imp_ations
        )
        self.CONNECTIONS[from_host[0]] = self.conn  # 保存连接

        server_info = "" if not server_uri else f"\nserver_uri: {server_uri}"
        logger.log("CONN",
            f"[{self.conn.connect_type}] ready: {self.conn.peername} {server_info}\nhost_id: {self.conn.host_id}\nimp_ations: {imp_ations}"
        )

        self.dispatcher.invoke_new_connection(self.conn)
        return True

    def on_local_message(self, payload: UtType.MessageTypedDict):
        """仅处理本地的消息"""
        to_host = payload["to_host"]
        if to_host != self.LOCAL_HOST_ID:
            return False

        from_host = payload["from_host"]
        msg_id = payload["msg_id"]

        action = payload.get("action")
        future_id = payload.get("future_id")
        confirm = payload.get("confirm")

        # 处理自发的消息
        if from_host[0] == self.LOCAL_HOST_ID:
            if future_id:  # 本地完成future
                logger.log("ROUND",f"future '{future_id}' done!")
                UtFuture.set_result(future_id, payload)
            return True

        is_reply = bool(confirm or future_id)  # 有confirm 或 future_id 都需要回复

        # 远程调用本地action
        if action:
            data: dict = payload.get("data", None) or {}
            self.loop.create_task(
                _call_local(
                    self.conn,
                    action=action,
                    params=data,
                    reply=is_reply,
                    msg_id=msg_id,
                    future_id=future_id,
                    from_host=from_host,
                ),
                name=f"conn_call_local_action::{self.conn.host_id}",
            )
            return True

        if is_reply:
            reply(self.conn, payload)  # type: ignore
            return True

    def on_transpond_message(self, payload: UtType.MessageTypedDict):
        """仅处理转发的消息，且确保只转发一次"""
        to_host = payload["to_host"]
        if to_host == self.LOCAL_HOST_ID or not to_host:
            return False

        from_host = payload["from_host"]

        if self.LOCAL_HOST_ID in from_host:  # 确保只转发一次
            return True

        target_host_id = to_host
        if target_host_id and (target_conn := self.CONNECTIONS[target_host_id]):
            transpond(target_conn, payload)
            logger.debug("🔁消息成功转发到指定host")
        else:
            broadcast(payload)
            logger.debug("📢广播转发消息")

        return True

    async def __call__(self):
        try:
            async for payload in self.conn:
                try:
                    logger.log("RECV",payload)
                    # 首次消息
                    if await self.on_first_message(payload):  # type: ignore
                        continue

                    # 防止冒用连接，终止本连接
                    if self.conn.host_id != payload["from_host"][-1]:
                        logger.warning(
                            "消息来源不合法, 连接的host_id与消息来源的host_id不一致"
                        )
                        break

                    # 本地消息
                    if self.on_local_message(payload):  # type: ignore
                        continue

                    # 转发消息
                    if self.on_transpond_message(payload):  # type: ignore
                        continue
                except Exception as e:
                    logger.warning(f"{e}")
                    break

        except Exception as e:
            # 打印具体错误traceback信息
            logger.exception(e)
        finally:
            UtFuture.cancel_future_by_group(self.conn.host_id)

            try:
                del self.CONNECTIONS[self.conn.host_id]
                logger.log("CONN",f"移除连接: {self.conn.host_id}")
            except:
                pass

            self.conn.close_event.set()
            self.dispatcher.invoke_close_connection(
                tuple(self.CONNECTIONS.values()), *self.conn.imp_ations
            )


async def run_backend_send_queue_forever():
    """后台线程，处理发送的消息队列"""
    qdata = None
    while True: 
        queue: asyncio.Queue[SendQueueData] = context.__UTRAN_CONTEXT__["backend_send_queue"]       
        try:
            qdata = await queue.get()
            logger.log("Q_SEND", f"qdata: {qdata}")  
            msg = qdata["msg"]
            await qdata["conn"].send(msg)
            logger.log("SEND",msg)
            await asyncio.sleep(0.1)  # 限制发送频率，防止过度占用CPU资源
        except Exception as e:
            logger.error(f"send message error: {e}")
            
            if qdata is not None:
                if (future := qdata.get('future')) and not future.done():
                    future.set_exception(e)
                    
                failed_to_broadcast = qdata.get("failed_to_broadcast", False)                
                if failed_to_broadcast and not qdata['msg'].get(
                    "init_data", None
                ):  # 不是初始化连接的消息，并且failed_to_broadcast为True，则重发
                    msg = qdata["msg"]
                    conn = qdata["conn"]
                
                    msg["to_host"] = conn.host_id
                    broadcast(msg)  # type: ignore
                    logger.warning("消息发送失败，消息已广播")
        
        finally:
            queue.task_done()
