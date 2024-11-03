import asyncio
from functools import wraps
import inspect
import threading
from typing import Any, Callable, Optional, TypeVar, Generic, ParamSpec
from cachetools import keys
from .caches import CacheType
from utran.log import logger

class ActionRegistrationError(Exception):
    pass


class ActionRuntimeError(Exception):
    pass


R = TypeVar("R")
P = ParamSpec("P")


class Action(Generic[P, R]):
    __slots__ = (
        "_action",
        "_lock",
        "_cache",
        "_is_async",
        "_action_key",
        "_source_fn",
    )

    def __init__(
        self,
        fn: Callable[P, R],
        action_key: Optional[str] = None,
        *,
        source_fn: Optional[Callable[..., R]] = None,
        cache: CacheType = None,
        cache_key_func: Callable[..., Any] = keys.hashkey,  # 缓存key的生成函数
        lock=False,
    ):

        self._source_fn: Callable[P, R] = fn if source_fn is None else source_fn
        self._action_key = fn.__name__ if action_key is None else action_key
        use_cache = True if cache else False
        self._cache = cache if cache else {}

        self._pre_init(
            action_key=self._action_key,
            source_fn=self._source_fn,
        )

        if asyncio.iscoroutinefunction(fn):
            self._is_async = True

            @wraps(self._source_fn)
            async def async_wrapper(*args, **kwargs):
                key = cache_key_func(*args, **kwargs)
                if use_cache:
                    try:
                        return self._cache[key]
                    except KeyError:
                        pass  # key 不存在
                try:
                    val = await fn(*args, **kwargs)
                except Exception as e:
                    stack = inspect.stack()
                    code_context = "".join(stack[1].code_context or [])
                    filename = stack[1].filename
                    lineno = stack[1].lineno
                    function_name = stack[1].function
                    trace = f'File: "{filename}", line: {lineno}, in {function_name}\n >> {code_context}'
                    e.args = ("exception occurred in :\n",trace) + e.args
                    e.args = (''.join(e.args),)
                    raise e
  
                if not use_cache:
                    return val
                try:
                    self._cache[key] = val
                except ValueError:
                    pass  # val 太大

                return val

            if lock == False:
                self._action = async_wrapper
            else:
                _alock = asyncio.Lock()

                @wraps(self._source_fn)
                async def async_wrapper_lock(*args, **kwargs):
                    async with _alock:
                        return await async_wrapper(*args, **kwargs)

                self._action = async_wrapper_lock

        else:
            self._is_async = False

            @wraps(self._source_fn)
            def wrapper(*args, **kwargs):
                key = cache_key_func(*args, **kwargs)
                if use_cache:
                    try:
                        return self._cache[key]
                    except KeyError:
                        pass  # key 不存在
                try:
                    val = fn(*args, **kwargs)
                except Exception as e:
                    stack = inspect.stack()
                    code_context = "".join(stack[1].code_context or [])
                    filename = stack[1].filename
                    lineno = stack[1].lineno
                    function_name = stack[1].function
                    trace = f'File: "{filename}", line: {lineno}, in {function_name}\n >> {code_context}'
                    e.args = ("exception occurred in :\n",trace) + e.args
                    e.args = (''.join(e.args),)
                    raise e
                
                if not use_cache:
                    return val
                try:
                    self._cache[key] = val
                except ValueError:
                    pass  # val 太大

                return val

            if lock == False:
                self._action = wrapper
            else:
                _lock = threading.Lock()

                @wraps(self._source_fn)
                def wrapper_lock(*args, **kwargs):
                    with _lock:
                        return wrapper(*args, **kwargs)

                self._action = wrapper_lock

    def __repr__(self) -> str:
        return f"<Action {self._action_key}>"

    def __str__(self) -> str:
        return self._action_key

    def _pre_init(self, *, action_key: str, source_fn: Callable[..., R]):
        pass

    def check_signatures(self, fn: Callable, raise_error: bool = True):
        """检查参数签名是否匹配"""
        sig = inspect.signature(self._source_fn)
        sig_fn = inspect.signature(fn)
        if sig != sig_fn:
            if raise_error:
                raise ActionRegistrationError(
                    f"签名不匹配, {self._source_fn.__name__}期望{sig}, 实际{sig_fn}"
                )
            return False
        return True

    def is_async(self) -> bool:
        return self._is_async

    def clear_cache(self):
        """清空缓存"""
        self._cache.clear()

    def destroy(self):
        """销毁action"""
        self.clear_cache()

