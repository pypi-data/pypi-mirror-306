import inspect
from typing import Callable, Optional, overload
from utran.core.general.base_action import P, R, Action, ActionRuntimeError, CacheType, keys
from utran.core import context
from utran.log import logger

actionKeyStr = str
LOCAL_ACTIONS: dict[actionKeyStr, "LocalAction"] = {}


class LocalAction(Action[P, R]):
    """ "本地action"""
    
    def __call__(self, *args: P.args, **kwargs: P.kwargs) -> R:
        # 提示不应该在backend线程中调用同步action
        if (
            context.__UTRAN_CONTEXT__["host_instance"]._is_in_backend_thread()
            and not self._is_async
        ):
            raise ActionRuntimeError(
                f"action '{self._action_key}' is sync function, can not be called in backend thread."
            )

        return self._action(*args, **kwargs)  # type: ignore



def register_action(fn: Callable, **kwargs):
    """
    注册一个本地函数为action
    """
    action_key = kwargs.get("action_key") or fn.__name__
    if ac := get_action(action_key):
        ac.check_signatures(fn)
        return ac

    kwargs["action_key"] = action_key
    LOCAL_ACTIONS[action_key] = LocalAction(fn, **kwargs)
    return LOCAL_ACTIONS[action_key]


def remove_action(fn: Optional[Callable | str | LocalAction]):
    """删除一个action"""
    if fn is None:
        return

    action: Optional[LocalAction] = None

    if isinstance(fn, LocalAction):
        action = fn
    try:
        if inspect.isfunction(fn):
            action = LOCAL_ACTIONS[fn.__name__]

        if isinstance(fn, str):
            action = LOCAL_ACTIONS[fn]
    except:
        pass

    if action:
        action.destroy()
        del LOCAL_ACTIONS[action._action_key]


def get_action(action_key: str) -> Optional[LocalAction]:
    """获取本地action"""
    return LOCAL_ACTIONS.get(action_key)

def _get_all_actions() -> list[LocalAction]:
    """获取所有本地action, 给tots command使用"""
    return list(LOCAL_ACTIONS.values())


@overload
def action(
    *_: None,
    action_key: Optional[str] = None,
    cache: CacheType = None,
    cache_key_func: Callable = keys.hashkey,
    lock=False,
) -> Callable[[Callable[P, R]], Callable[P, R]]: ...
@overload
def action(
    *_: Callable[P, R],
    action_key: Optional[str] = None,
    cache: CacheType = None,
    cache_key_func: Callable = keys.hashkey,
    lock=False,
) -> Callable[P, R]: ...
def action(
    *_: Callable[P, R] | None,
    action_key: Optional[str] = None,
    cache: CacheType = None,
    cache_key_func: Callable = keys.hashkey,
    lock=False,
) -> Callable[[Callable[P, R]], Callable[P, R]] | Callable[P, R]:
    """装饰器,注册action函数, 不会更改原函数，进行注册后原样返回
    - action_key: str = None,  # action key
    - cache: CacheType = None,  # 缓存
    - cache_key_func: Callable[...] = keys.hashkey,  # 缓存key的生成函数
    - lock=False  # 是否加锁
    """
    fn = _[0] if _.__len__() > 0 and inspect.isfunction(_[0]) else None
    if fn is None:
        def wrapped_function(fn: Callable[P, R]) -> Callable[P, R]:
            return action(
                fn,
                action_key=action_key,
                cache=cache,
                cache_key_func=cache_key_func,
                lock=lock,
            )
        return wrapped_function

    register_action(
        fn, action_key=action_key, cache=cache, lock=lock, cache_key_func=cache_key_func
    )
    return fn
