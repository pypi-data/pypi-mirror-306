import asyncio
from functools import partial
import inspect
from typing import (
    Any,
    Callable,
    Literal,
    Optional,
    ParamSpec,
    TypeVar,
    cast,
    overload,
)


from utran.core.backend.base import AbstractConnection
from utran.core.general.baseclass import BaseWokeBlockTemplate
from ..general.exceptions import (
    RemoteNotImplementedError,
    RemoteRuntimeError,
    WokeBlockScopeError,
)
from ..general.base_action import Action, ActionRuntimeError, CacheType, keys
from utran.core import context


actionKeyStr = str
REMOTE_IMP_ACTIONS: dict[actionKeyStr, "RemoteImpAction"] = {}


def _get_all_imp_actions() -> list["RemoteImpAction"]:
    """获取所有远程action, 给tots command使用"""
    return list(REMOTE_IMP_ACTIONS.values())


def get_remote_imp_action(action_key: str) -> Optional["RemoteImpAction"]:
    """获取远程实现action"""
    return REMOTE_IMP_ACTIONS.get(action_key)


R = TypeVar("R")
P = ParamSpec("P")


class RemoteImpAction(Action[P, R]):
    """远程实现action"""

    def _pre_init(self, *, action_key: str, source_fn: Callable[..., R]):
        """前置检查 action_key是否合法"""
        for k, v in REMOTE_IMP_ACTIONS.items():
            if k == action_key:
                raise ValueError(f"action_key '{action_key}' already be used by {v}")

    def __call__(self, *args: P.args, **kwargs: P.kwargs) -> R:
        # 提示不应该在backend线程中调用同步action
        if (
            context.__UTRAN_CONTEXT__["host_instance"]._is_in_backend_thread()
            and not self._is_async
        ):
            raise ActionRuntimeError(
                f"action '{self._action_key}' is sync function, can not be called in backend thread."
            )

        if isinstance(args[0], BaseWokeBlockTemplate):
            args = args[1:]  # type: ignore   # 去掉第1个参数, cls 后 self

        return self._action(*args, **kwargs)  # type: ignore


_D = TypeVar("_D")


@overload
def register_remote_imp_action(
    fn: Callable[P, R],
    action_key: Optional[str],
    *,
    default_fn: Literal[None] = None,
    timeout: Optional[float] = None,
    **kwargs,
) -> RemoteImpAction[P, R]: ...
@overload
def register_remote_imp_action(
    fn: Callable[P, R],
    action_key: Optional[str],
    *,
    default_fn: Callable[..., _D],
    timeout: Optional[float] = None,
    **kwargs,
) -> RemoteImpAction[P, R | _D]: ...
def register_remote_imp_action(
    fn: Callable[P, R],
    action_key: Optional[str],
    *,
    default_fn: Callable[..., _D] | None = None,
    timeout: Optional[float] = None,
    **kwargs,
) -> RemoteImpAction[P, R] | RemoteImpAction[P, R | _D]:
    """
    添加远程实现action函数
    - fn: 远程实现函数
    - action_key: 远端实现的action名称,默认为函数名称
    - default_fn: 默认函数,当远端无可调用实现时调用,默认为None
    - timeout: 远端调用超时时间,默认为None,不超时
    - **kwargs: 其他参数
    """

    action_key = fn.__name__ if action_key is None else action_key

    if ac := get_remote_imp_action(action_key):
        ac.check_signatures(fn)
        return ac

    from utran.core.host import __CONNECTIONS__
    from utran.core.ipc import async_remote_call, sync_remote_call
    from .wokeblock import _WokeBlockHandler

    backend_loop = context.__UTRAN_CONTEXT__["backend_loop"]

    if asyncio.iscoroutinefunction(fn):

        def async_wrapper(*args, **kw):
            """异步函数远程调用目标Action"""

            wokeblock_handler: Optional[_WokeBlockHandler] = context.__UTRAN_CONTEXT__[
                "thread_local_data"
            ].wokeblock_handler
            target_conns: AbstractConnection | None = None
            allow_hosts = None

            try:
                allow_hosts = (
                    wokeblock_handler.scope_remote_actions[action_key]
                    if wokeblock_handler
                    else None
                )
            except KeyError as e:
                name = (
                    wokeblock_handler.wokeblock_name if wokeblock_handler else "unknown"
                )

                raise WokeBlockScopeError(
                    f"action '{action_key}' not declared, but it is used in '{name}'."
                ) from e

            for conn in __CONNECTIONS__.values():
                if allow_hosts is None or conn.host_id in allow_hosts:
                    if action_key in conn.imp_ations:
                        target_conns = conn
                        break

            if target_conns is None:
                if default_fn is None:
                    raise RemoteNotImplementedError(f"'{action_key}',远端无可调用实现")
                else:
                    return default_fn(*args, **kw)

            if not context.__UTRAN_CONTEXT__["host_instance"]._is_in_backend_thread():
                fu = asyncio.Future[Any]()

                def callback(f):
                    try:
                        res = f.result()
                        fu.get_loop().call_soon_threadsafe(fu.set_result, res)
                    except Exception as e:
                        fu.get_loop().call_soon_threadsafe(fu.set_exception, e)

                asyncio.run_coroutine_threadsafe(
                    async_remote_call(
                        target_conns,
                        action_key,
                        params=dict(args=args, kwargs=kw),
                        timeout=timeout,
                    ),
                    loop=backend_loop,
                ).add_done_callback(callback)
                return fu
            else:
                return async_remote_call(
                    target_conns,
                    action_key,
                    params=dict(args=args, kwargs=kw),
                    timeout=timeout,
                )

        impAction = RemoteImpAction(async_wrapper, action_key, source_fn=fn, **kwargs)

    else:

        def wrapper(*args, **kw):
            """同步函数远程调用目标Action"""
            wokeblock_handler: Optional[_WokeBlockHandler] = context.__UTRAN_CONTEXT__[
                "thread_local_data"
            ].wokeblock_handler
            target_conns: AbstractConnection | None = None
            allow_hosts = None

            try:
                allow_hosts = (
                    wokeblock_handler.scope_remote_actions[action_key]
                    if wokeblock_handler
                    else None
                )
            except KeyError as e:
                raise RemoteRuntimeError(
                    f"action_key '{action_key}' not in scope_remote_actions"
                ) from e

            for conn in __CONNECTIONS__.values():
                if allow_hosts is None or conn.host_id in allow_hosts:
                    if action_key in conn.imp_ations:
                        target_conns = conn
                        break

            if target_conns is None:
                if default_fn is None:
                    raise RemoteNotImplementedError(f"'{action_key}',远端无可调用实现")
                else:
                    return default_fn(*args, **kw)

            return sync_remote_call(
                target_conns,
                action_key,
                params=dict(args=args, kwargs=kw),
                timeout=timeout,
            )

        impAction = RemoteImpAction(wrapper, action_key, source_fn=fn, **kwargs)  # type: ignore

    REMOTE_IMP_ACTIONS[action_key] = impAction
    return cast(RemoteImpAction[P, R], impAction)


@overload
def remote_imp(
    _: Callable[P, R],
    *,
    action_key: Optional[str] = None,
    default_fn: Literal[None] = None,
    cache: CacheType = None,
    cache_key_func: Callable = keys.hashkey,
    lock=False,
    timeout: Optional[float] = None,
) -> RemoteImpAction[P, R]: ...
@overload
def remote_imp(
    *args,
    action_key: Optional[str] = None,
    default_fn: Literal[None] = None,
    cache: CacheType = None,
    cache_key_func: Callable = keys.hashkey,
    lock=False,
    timeout: Optional[float] = None,
) -> Callable[[Callable[P, R]], RemoteImpAction[P, R]]: ...
@overload
def remote_imp(
    *args,
    action_key: Optional[str] = None,
    default_fn: Callable[..., _D],
    cache: CacheType = None,
    cache_key_func: Callable = keys.hashkey,
    lock=False,
    timeout: Optional[float] = None,
) -> Callable[[Callable[P, R]], RemoteImpAction[P, R | _D]]: ...
def remote_imp(
    *args,
    _: Callable[P, R] | None = None,
    action_key: Optional[str] = None,
    default_fn: Callable[..., _D] | None = None,
    cache: CacheType = None,
    cache_key_func: Callable = keys.hashkey,
    lock=False,
    timeout: Optional[float] = None,
) -> (
    Callable[[Callable[P, R]], RemoteImpAction[P, R] | RemoteImpAction[P, R | _D]]
    | RemoteImpAction[P, R]
):
    """### 装饰器,将函数注册远程实现action
    - action_key: 远端实现的action名称,默认为函数名称
    - default_fn: 默认值函数,当远端无可调用实现时调用
    - cache: 缓存类型,默认为None,不缓存
    - cache_key_func: 缓存key生成函数,默认为hashkey
    - lock: 是否加锁,默认为False
    - timeout: 远端调用超时时间,默认为None,不超时
    """
    fn = args[0] if args.__len__() > 0 and inspect.isfunction(args[0]) else None
    if fn is None:
        return partial(
            remote_imp,
            action_key=action_key,
            default_fn=default_fn,
            cache=cache,
            lock=lock,
            cache_key_func=cache_key_func,
            timeout=timeout,
        )  # type: ignore

    return cast(
        RemoteImpAction[P, R],
        register_remote_imp_action(
            fn,
            action_key=action_key,
            default_fn=default_fn,
            cache=cache,
            lock=lock,
            cache_key_func=cache_key_func,
            timeout=timeout,
        ),
    )

