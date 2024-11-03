import asyncio
from concurrent.futures import ThreadPoolExecutor, Future
from typing import Literal, Tuple
from weakref import WeakSet
from functools import partial
from itertools import chain

from utran.core.backend.base import AbstractConnection
from utran.core.remote.action import RemoteImpAction, get_remote_imp_action
from utran.core.remote import wokeblock as WokeBlockModule
from utran.log import logger
from utran.core.general import event_protocol
from utran.core.general.event_protocol import EventProtocolTypes
from utran.core.local import action as LocalActionModule
from utran.core import context

class ExecuteLocalActionError(Exception):
    """ 执行本地Action错误"""
    pass

class _WokeBlockDispatcher:
    """后端线程执行调度WokeBlockHandler"""

    already_imp_action: WeakSet[RemoteImpAction] = WeakSet()

    @classmethod
    def on_new_connection(cls, conn: AbstractConnection):
        imp_action_keys = conn.imp_ations
        actions = (get_remote_imp_action(k) for k in imp_action_keys)
        cls.already_imp_action.update(filter(None, actions))

    @classmethod
    def on_close_connection(
        cls,
        surplus_connections: Tuple[AbstractConnection, ...],
        cur_imp_action_keys: Tuple[str, ...],
    ):
        surplus_imp_action_keys = set(
            action for conn in surplus_connections for action in conn.imp_ations
        )
        imp_action_keys = [i for i in surplus_imp_action_keys if i not in cur_imp_action_keys]
        actions = (get_remote_imp_action(k) for k in imp_action_keys)
        cls.already_imp_action = WeakSet(filter(None, actions))
        
        
    @classmethod
    def __get_ready_wokeblock(cls,_type:Literal['new','close', 'imp']):
        """获取可用的WokeBlockHandler"""
        
        all_wh = list(chain(WokeBlockModule._Store._STORE_WOKEBLOCK_OF_CLASS.values(),
                                WokeBlockModule._Store._STORE_WOKEBLOCK_OF_FUNC.values()))
        
        # 获取所有有效的 WokeBlockHandler
        all_valid_wokeblock = [
            wokeblock_handler
            for wokeblock_handler in all_wh
            if wokeblock_handler.use_remote_actions.issubset(cls.already_imp_action)
            and not wokeblock_handler.is_runing
            and not wokeblock_handler.is_completed
            and not wokeblock_handler.is_abandoned
        ]
        
        if _type=='new':
            return [
                wokeblock_handler
                for wokeblock_handler in all_wh
                if wokeblock_handler.woke_mode == 'only_new_conn'
            ] + [
                wokeblock_handler
                for wokeblock_handler in all_valid_wokeblock
                if wokeblock_handler.woke_mode == 'new_conn' or wokeblock_handler.woke_mode == 'remote_imp'
            ]
        elif _type=='close':
            return [
                wokeblock_handler
                for wokeblock_handler in all_wh
                if wokeblock_handler.woke_mode == 'only_close_conn'
            ] + [
                wokeblock_handler
                for wokeblock_handler in all_valid_wokeblock
                if wokeblock_handler.woke_mode == 'close_conn' or wokeblock_handler.woke_mode == 'remote_imp'
            ]
        else:
            return all_valid_wokeblock


    @classmethod
    def dispatch_wokeblock(cls, pool: ThreadPoolExecutor,_type:Literal['new','close', 'imp']):
        all_run_wokeblock = cls.__get_ready_wokeblock(_type)
        
        if not all_run_wokeblock:
            return

        # 使用线程池执行
        for wokeblock_handler in all_run_wokeblock:
            pool.submit(wokeblock_handler).add_done_callback(
                partial(cls.__on_wokeblock_done, wokeblock_handler)
            )

        logger.log("WOKE",f"{len(all_run_wokeblock)} wokeblocks dispatched.")

    @classmethod
    def __on_wokeblock_done(cls, wokeblock_handler: WokeBlockModule._WokeBlockHandler, fut: Future):
        try:
            fut.result()
        except Exception as e:
            raise RuntimeError(f"wokeblock internal error: {e}") from e
        finally:
            wokeblock_handler.is_runing = False


class LocalActionDispatcher:
    """后端线程执行调度本地Action"""

    @classmethod
    def call_local(
        cls,
        pool: ThreadPoolExecutor,
        action: LocalActionModule.LocalAction,
        params: dict,
        future: asyncio.Future,
    ):
        """本地Action调用"""
        logger.debug(f"执行本地action调用: {action}")
        _args = params.get("args", [])
        _kwargs = params.get("kwargs", {})
        
        # 打印线程池剩余数量
        logger.info(f"thread pool size: {pool._max_workers - pool._work_queue.qsize()}")
        
        if action.is_async():
            # 使用主事件循环，执行异步本地调用 
            asyncio.run_coroutine_threadsafe(action(*_args, **_kwargs), future.get_loop()).add_done_callback(
                partial(cls.__on_local_action_done, future)
            )
        else:
            # 使用线程池，执行同步本地调用
            pool.submit(action, *_args, **_kwargs).add_done_callback(
                partial(cls.__on_local_action_done, future)
            )


    @classmethod
    def __on_local_action_done(cls, future: asyncio.Future, exe_fut: Future):
        """本地Action调用完成"""
        
        if future.done(): return   # 当futrue完成时，说明被撤销，直接返回
        try:
            result = exe_fut.result()
            future.get_loop().call_soon_threadsafe(future.set_result, result)
        except Exception as e:
            err = ExecuteLocalActionError(f"执行本地Action错误: {e}")
            future.get_loop().call_soon_threadsafe(future.set_exception, err)
            raise err from e


# class RemoteActionDispatcher:
#     """后端线程执行调度远程Action"""

#     @classmethod
#     def call_remote(
#         cls,
#         pool: ThreadPoolExecutor,
#         conn: AbstractConnection,
#         action: RemoteImpAction,
#         params: dict,
#         future: asyncio.Future,
#     ):
#         """远程同步Action调用"""
#         logger.debug(f"执行远程action调用: {action}")
#         _args = params.get("args", [])
#         _kwargs = params.get("kwargs", {})
        
#         # 打印线程池剩余数量
#         logger.info(f"thread pool size: {pool._max_workers - pool._work_queue.qsize()}")
        
#         if action.is_async():
#             # 使用主事件循环，执行异步远程调用 
#             asyncio.run_coroutine_threadsafe(action.remote_call(conn, *_args, **_kwargs), future.get_loop()).add_done_callback(
#                 partial(cls.__on_remote_action_done, future)
#             )
#         else:
#             # 使用线程池，执行同步远程调用
#             pool.submit(action.remote_call, conn, *_args, **_kwargs).add_done_callback(
#                 partial(cls.__on_remote_action_done, future)
#             )




class Dispatcher:
    """总调度器"""

    __slots__ = ()


    @property
    def queue(self):
        return context.__UTRAN_CONTEXT__["backend_dispatcher_queue"]

    @property
    def pool(self):
        return context.__UTRAN_CONTEXT__["worker_pool"]

    @property
    def loop(self):
        return context.__UTRAN_CONTEXT__["backend_loop"]

    def _do_event_new_connection(self, event: event_protocol.NewConnectionEvent):
        # 由后端线程队列触发
        _WokeBlockDispatcher.on_new_connection(event["conn"])
        
        _WokeBlockDispatcher.dispatch_wokeblock(self.pool,'new')

    def _do_event_close_connection(
        self,
        event: event_protocol.CloseConnectionEvent,
    ):
        # 由后端线程队列触发
        _WokeBlockDispatcher.on_close_connection(
            surplus_connections=event["surplus_connections"],
            cur_imp_action_keys=event["cur_imp_action_keys"],
        )

        _WokeBlockDispatcher.dispatch_wokeblock(self.pool,'close')
        

    def _do_event_executor_wokeblock(self,_type:Literal['new','close', 'imp']):
        # 由后端线程队列触发
        _WokeBlockDispatcher.dispatch_wokeblock(self.pool,_type)


    def _do_event_execute_local_action(
        self,
        event: event_protocol.ExecuteLocalActionEvent,
    ):
        # 由后端线程队列触发
        LocalActionDispatcher.call_local(
            pool=self.pool,
            action=event["action"],
            params=event["params"],
            future=event["future"],
        )


    def invoke_local_action(
        self,
        action: LocalActionModule.LocalAction,
        params: dict,
    ):
        """执行本地Action"""
        # if action.is_async():
        #     _args = params.get("args", [])
        #     _kwargs = params.get("kwargs", {})
        #     return action(*_args, **_kwargs)

        fu = asyncio.get_running_loop().create_future()
        event: event_protocol.ExecuteLocalActionEvent = {
            "type": EventProtocolTypes.execute_local_action,
            "action": action,
            "params": params,
            "future": fu,
        }
        self.loop.call_soon_threadsafe(self.queue.put_nowait, event)
        return fu


    def invoke_executor_wokeblock(self):
        """执行调度WokeBlockHandler"""
        # 使用线程安全加入队列
        event: event_protocol.ExecuteWokeBlockEvent = {
            "type": EventProtocolTypes.execute_wokeblock,
        }
        self.loop.call_soon_threadsafe(self.queue.put_nowait, event)

    def invoke_new_connection(self, conn: AbstractConnection):
        # 使用线程安全加入队列
        event: event_protocol.NewConnectionEvent = {
            "type": EventProtocolTypes.new_connection,
            "conn": conn,
        }
        self.loop.call_soon_threadsafe(self.queue.put_nowait, event)

    def invoke_close_connection(
        self,
        surplus_connections: tuple[AbstractConnection, ...],
        /,
        *cur_imp_action_keys: str,
    ):
        # 使用线程安全加入队列
        event: event_protocol.CloseConnectionEvent = {
            "type": EventProtocolTypes.close_connection,
            "surplus_connections": surplus_connections,
            "cur_imp_action_keys": cur_imp_action_keys,
        }
        self.loop.call_soon_threadsafe(self.queue.put_nowait, event)




async def run_backend_dispatcher_queue_forever():

    dispatcher = context.__UTRAN_CONTEXT__["host_instance"].dispatcher
    event_handlers = {
        EventProtocolTypes.new_connection: dispatcher._do_event_new_connection,
        EventProtocolTypes.close_connection: dispatcher._do_event_close_connection,
        EventProtocolTypes.execute_wokeblock: dispatcher._do_event_executor_wokeblock,
        EventProtocolTypes.execute_local_action: dispatcher._do_event_execute_local_action
    }
    
    while True:
        queue = context.__UTRAN_CONTEXT__["backend_dispatcher_queue"]
        try:
            event = await queue.get()
            logger.log("Q_EVENT",event)

            if event_type := event["type"]:
                handler = event_handlers.get(event_type)
                if handler:
                    handler(event)
                else:
                    logger.error(f"unknown event: {event}")
        except Exception as e:
            logger.error(f"backend queue error: {e}")
        finally:
            queue.task_done()
