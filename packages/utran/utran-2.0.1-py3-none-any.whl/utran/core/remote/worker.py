import asyncio
import inspect
from typing import Any, Callable, Literal, Optional, cast, overload
from abc import ABCMeta, abstractmethod
from functools import partial, wraps
from utran.log import logger
from weakref import WeakKeyDictionary, WeakSet, WeakValueDictionary

from .action import (
    _D,
    P,
    R,
    RemoteImpAction,
    CacheType,
    keys,
    register_remote_imp_action,
    get_remote_imp_action,
)
from ..general.exceptions import (
    RemoteNotImplementedError,
    RemoteResultError,
    RemoteTimeoutError,
    RemoteRuntimeError,
)


class WorkerRuntimeError(Exception):
    """Worker运行时错误"""
    pass


class WorkerHandlerRegisterError(Exception):
    """WorkerHandler注册错误"""

    pass


class _Store:
    """### 全局存储类"""

    # 存储Worker中使用的RemoteImpAction, key是类名/函数名，value是使用的RemoteImpAction集合
    _STORE_WORER_USE_REOMET_ACTIONS: dict[str, WeakSet[RemoteImpAction]] = dict()

    # 存储wokerhandler, key是WorkerTemplate的子类，value是workerhandler实例
    _STORE_WORKER_OF_CLASS: WeakKeyDictionary[type["WorkerTemplate"], "_WorkerHandler"] = (
        WeakKeyDictionary()
    )

    # 存储wokerhandler, key是worker函数，value是workerhandler实例
    _STORE_WORKER_OF_FUNC: WeakValueDictionary[Callable, "_WorkerHandler"] = (
        WeakValueDictionary()
    )

    @classmethod
    def add_use_remote_actions(
        cls,
        name: str,
        *remote_imp_actions: RemoteImpAction,
    ):
        """标记所使用的RemoteImpAction"""
        cls._STORE_WORER_USE_REOMET_ACTIONS.setdefault(name, WeakSet()).update(
            remote_imp_actions
        )

    @classmethod
    def get_all_worker(cls):
        """获取所有得workerhandler"""
        return list(cls._STORE_WORKER_OF_CLASS.values()) + list(cls._STORE_WORKER_OF_FUNC.values())


    @classmethod
    def register_workerhandler_by_func(
        cls,
        target: Callable,
        use_remote_actions: WeakSet[RemoteImpAction],
        on_stop: Callable | None = None,
        on_before_start: Callable | None = None,
        on_error: Callable | None = None,
        on_complate: Callable | None = None,
    ):
        """注册workerhandler"""
        if inspect.isclass(target):
            raise TypeError("cannot register a class.")

        if not callable(target):
            raise TypeError("target must be a callable object")

        workerhandler = _WorkerHandler(
            target=target,
            worker_name=target.__name__,
            use_remote_actions=use_remote_actions,
            on_stop=on_stop,
            on_before_start=on_before_start,
            on_error=on_error,
            on_complate=on_complate,
        )

        cls._STORE_WORKER_OF_FUNC[target] = workerhandler
        return workerhandler


class _WorkerHandler:
    __slots__ = (
        "funcs",
        "use_remote_actions",
        "is_runing",
        "is_completed",
        "worker_name",
        "loop",
        "is_abandoned",
    )

    def __init__(
        self,
        target: Callable,
        worker_name: str,
        use_remote_actions: WeakSet[RemoteImpAction] = WeakSet(),
        on_stop: Callable | None = None,
        on_before_start: Callable | None = None,
        on_error: Callable | None = None,
        on_complate: Callable | None = None,
    ) -> None:
        self.is_runing = False
        self.is_completed = False
        self.worker_name = worker_name
        self.use_remote_actions = use_remote_actions
        self.loop: asyncio.AbstractEventLoop
        self.funcs = dict(
            target_fn=target,
            on_stop=on_stop,
            on_before_start=on_before_start,
            on_error=on_error,
            on_complate=on_complate,
        )
        self.is_abandoned = False

    def executer(
        self,
        key: Literal[
            "on_before_start", "on_stop", "on_error", "on_complate", "target_fn"
        ],
        *args: Any,
        **kwds: Any,
    ):
        """#### 触发on_stop函数:
        - RemoteNotImplementedError: 没有可调用的远程实现, 该错误用于触发on_stop函数

        #### 以下3种错误会触发on_error函数:
        - RemoteResultError: 远程调用结果错误
        - RemoteTimeoutError: 远程调用超时
        - WorkerRuntimeError: 运行时错误，执行用户注册的函数时发生错误

        #### 内部错误:
        - RemoteRuntimeError: 远程调用运行时发生内部错误
        """
        fn = self.funcs.get(key, None)
        if not fn:
            return
        try:
            if asyncio.iscoroutinefunction(fn):
                return self.loop.run_until_complete(fn(*args, **kwds))
            return fn(*args, **kwds)
        except RemoteNotImplementedError as e:
            raise e
        except (RemoteResultError, RemoteTimeoutError, RemoteRuntimeError) as e:
            raise e
        except Exception as e:
            raise WorkerRuntimeError(
                f'worker::{self.worker_name} -> error in "{key}": {e}'
            ) from e

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        """
        #### 会处理所有`executer`函数的异常,最终只会向外抛出两种运行时错误:
        - `RemoteRuntimeError`  远程调用运行时发生内部的错误
        - `WorkerRuntimeError`  本函数执行时的错误
        > 注: 当用户注册的`on_error`函数有错误时,该WorkerHandler会被遗弃
        """
        self.is_runing = True
        self.loop = asyncio.new_event_loop()
        try:
            try:
                logger.debug(
                    f"worker::{self.worker_name} -> executor 'on_before_start'"
                )
                self.executer(
                    "on_before_start", *args, **kwds
                )  # 执行on_before_start函数

                logger.debug(f"worker::{self.worker_name} -> executor 'target_fn'")
                self.executer("target_fn", *args, **kwds)  # 执行target_fn目标函数

                logger.debug(f"worker::{self.worker_name} -> executor 'on_complate'")
                self.executer("on_complate")  # 执行on_complate函数

                self.is_completed = True
                logger.debug(f"worker::{self.worker_name} -> 运行完毕")

            except RemoteNotImplementedError as e:
                logger.debug(f"worker::{self.worker_name} -> 暂停运行，{e}")
                logger.debug(f"worker::{self.worker_name} -> executor 'on_stop'")
                self.executer("on_stop")  # 执行on_stop函数

            except Exception as exec_error:
                raise exec_error

        except (RemoteResultError, RemoteTimeoutError, WorkerRuntimeError) as exec_error:
            try:
                if not self.funcs.get("on_error"):
                    logger.warning(exec_error)

                self.executer("on_error", exec_error)  # 执行on_error函数
            except RemoteRuntimeError as e:
                raise e
            except WorkerRuntimeError as e:
                # 用户注册的on_error函数发生错误，该错误会抛出到外层
                logger.error(f'原始错误：{exec_error}')  # 输出原始错误
                logger.error(
                    f"worker::{self.worker_name}.on_error 存在错误: {e}"
                )
                self.is_abandoned = True   # 标记该workerhandler已被遗弃

            except Exception as err:
                logger.error(f'原始错误：{exec_error}')  # 输出原始错误
                logger.error(f"worker::{self.worker_name} -> error in on_error: {err}")

        except RemoteRuntimeError as runtime_error:
            logger.exception(runtime_error)
            logger.error(runtime_error)
            raise runtime_error

        except Exception as e:
            # 其他运行时错误
            logger.error(f"_WorkerHandler 内部发生错误： {e}")
            raise WorkerRuntimeError(
                f"worker::{self.worker_name} -> runtime error: {e}"
            ) from e
        finally:
            self.is_runing = False








@overload
def mark_remote_imp(
    _: Callable[P, R],
    *,
    action_key: Optional[str] = None,
    default_fn: Literal[None] = None,
    cache: CacheType = None,
    cache_key_func: Callable = keys.hashkey,
    lock=False,
    timeout: Optional[float] = None,
) -> Callable[P, R]: ...
@overload
def mark_remote_imp(
    *args,
    action_key: Optional[str] = None,
    default_fn: Literal[None] = None,
    cache: CacheType = None,
    cache_key_func: Callable = keys.hashkey,
    lock=False,
    timeout: Optional[float] = None,
) -> Callable[[Callable[P, R]], Callable[P, R]]: ...
@overload
def mark_remote_imp(
    *args,
    action_key: Optional[str] = None,
    default_fn: Callable[..., _D],
    cache: CacheType = None,
    cache_key_func: Callable = keys.hashkey,
    lock=False,
    timeout: Optional[float] = None,
) -> Callable[[Callable[P, R]], Callable[P, R|_D]]: ...
def mark_remote_imp(
    *args,
    _: Callable[P, R]|None = None,
    action_key: Optional[str] = None,
    default_fn: Callable[..., _D] | None=None,
    cache: CacheType = None,
    cache_key_func: Callable = keys.hashkey,
    lock=False,
    timeout: Optional[float] = None,
)-> Callable[[Callable[P, R]], Callable[P, R]|Callable[P, R|_D]]| Callable[P, R]:
    """### 装饰器,将函数注册到REMOTE_IMP_ACTIONS中
    - action_key: 远端实现的action名称,默认为函数名称
    - default_fn: 默认值函数,当远端没有实现时调用的函数
    - cache: 缓存类型,默认为None,不缓存
    - cache_key_func: 缓存key生成函数,默认为hashkey
    - lock: 是否加锁,默认为False
    - timeout: 远端调用超时时间,默认为None,不超时
    """
    fn = args[0] if args.__len__() == 1 and callable(args[0]) else None
    if fn is None:
        return partial(
            mark_remote_imp,
            action_key=action_key,
            default_fn=default_fn,
            cache=cache,
            cache_key_func=cache_key_func,
            lock=lock,
            timeout=timeout,
        ) # type: ignore

    _config = fn.__dict__.get("__remote_action_config__")
    if _config is None:
        action_key = action_key if action_key else fn.__name__
        fn.__dict__["__remote_action_config__"] = dict(
            action_key=action_key,
            default_fn=default_fn,
            cache=cache,
            cache_key_func=cache_key_func,
            lock=lock,
            timeout=timeout,
        )
        return fn # type: ignore

    raise ValueError(f"Method '{fn.__name__}' is already been marked as remote action.")




class WorkerTemplateRegisterMeta(ABCMeta):
    """
    元类用于注册WorkerTemplate类到WorkerHandler注册表
    - 限制只能直接继承一个WorkerTemplate类,不能继承WorkerTemplate的子类
    """
    def __new__(cls, name, bases, attrs):
        
        new_class = super().__new__(cls, name, bases, attrs)
        if name == 'WorkerTemplate':
            return new_class
        
        all_mark_remote_imp: list[tuple[Callable, dict]] = []  # 类方法,配置

        use_remote_actions: WeakSet[RemoteImpAction] = WeakSet()
        for base in bases:
            # 检查继承关系
            if base != WorkerTemplate and issubclass(base, WorkerTemplate):
                # 不能继承WorkerTemplate的子类
                raise TypeError(
                    f"WorkerTemplate class '{name}' can only inherit from one WorkerTemplate class."
                )
            # 遍历父类的方法,获取远程调用方法
            if hasattr(base, "__dict__"):
                all_mark_remote_imp.extend(list(cls.get_imp_action_config(base)))

        all_mark_remote_imp.extend(list(cls.get_imp_action_config(new_class)))


        # # 将实例方法转换为类方法
        for attr_name, attr_value in attrs.items():
            if callable(attr_value) and not isinstance(attr_value, classmethod):
                attrs[attr_name] = classmethod(attr_value)
        
        # 
        for _method, _config in all_mark_remote_imp:
            wapper, impaction = cls.register_remote_imp(
                _method, **_config
            )  # 注册远程调用的函数
            
            attrs[_method.__name__] = wapper   # 绑定远程调用方法
            use_remote_actions.add(impaction)


        new_class = super().__new__(cls, name, bases, attrs)
        
        # 注册WorkerHandler
        cls.register_workerhandler(new_class, use_remote_actions)

        return new_class
    
    
    def __init__(cls, name, bases, attrs):
        super().__init__(name, bases, attrs)
        
        
    def __call__(cls, *args, **kwargs):
        """
        实例化WorkerTemplate类时,会调用该方法,用于创建实例并存储
        """
        print(args, kwargs)
        instance = super().__call__(*args, **kwargs)
        # _Store.create_worker_template_instance(cls)
        return instance
        

    @classmethod
    def get_imp_action_config(cls, _class: type):
        for _method_name, fn in _class.__dict__.items():
            if inspect.isfunction(fn):
                if config := fn.__dict__.get("__remote_action_config__", None):
                    if action_key := config.get("action_key"):
                        if type(action_key) is str:
                            yield fn, cast(dict, config)
                        else:
                            logger.warning(
                                f"'{_class.__name__}.{_method_name}' has invalid action_key,must be str. Ignore it."
                            )
                    else:
                        logger.warning(
                            f"'{_class.__name__}.{_method_name}' has no action_key. Ignore it."
                        )

    @classmethod
    def register_remote_imp(cls, fn: Callable, **config):
        """注册远程调用方法,并标记远程调用方法"""
        action_key = config.get("action_key")
        if not action_key:
            raise WorkerHandlerRegisterError("action_key is required")
        if type(action_key) is not str:
            raise WorkerHandlerRegisterError("action_key must be str")

        target_fn = partial(fn, None)  # 排除slef或cls参数

        # action_key是否已经存在，如果存在验证是否签名一致
        if remoteImpAction := get_remote_imp_action(config["action_key"]):
            remoteImpAction.check_signatures(
                target_fn
            )  # 验证签名，如果不一致会抛出异常
        else:
            remoteImpAction = register_remote_imp_action(target_fn, **config)

        # return remoteImpAction

        @wraps(fn)
        def wrapper(*args, **kwargs):
            return remoteImpAction(*args[1:], **kwargs)

        return classmethod(wrapper), remoteImpAction

    @classmethod
    def register_workerhandler(
        cls,
        wt_class: type["WorkerTemplate"],
        use_remote_actions: WeakSet[RemoteImpAction],
    ):
        """注册workerhandler"""

        workerhandler = _WorkerHandler(
            worker_name=wt_class.__name__,
            use_remote_actions=use_remote_actions,
            target=wt_class.run,
            on_stop=wt_class.on_stop,
            on_before_start=wt_class.on_before_start,
            on_error=wt_class.on_error,
            on_complate=wt_class.on_complate,
        )

        _Store._STORE_WORKER_OF_CLASS[wt_class] = workerhandler


class WorkerTemplate(metaclass=WorkerTemplateRegisterMeta):
    """Worker模板类的根类,抽象类"""

    @abstractmethod
    def run(self, *args, **kwargs) -> Any:
        pass

    def on_before_start(self) -> Any:
        pass

    def on_stop(self) -> Any:
        pass

    def on_error(
        self, error: RemoteResultError | RemoteTimeoutError | WorkerRuntimeError
    ) -> Any:
        pass

    def on_complate(self) -> Any:
        pass


def register_remote_imp_for_worker_template_method(fn: Callable, **kwargs):
    """注册远程调用方法,并标记远程调用方法"""
    _ = fn.__qualname__.split(".")
    className = _[-1] if len(_) == 1 else _[-2]
    action_key = kwargs.get("action_key")
    kwargs["action_key"] = action_key if action_key else fn.__name__

    target_fn = partial(fn, None)  # 排除slef或cls参数

    # action_key是否已经存在，如果存在验证是否签名一致
    if remoteImpAction := get_remote_imp_action(kwargs["action_key"]):
        remoteImpAction.check_signatures(target_fn)  # 验证签名，如果不一致会抛出异常
    else:
        remoteImpAction = register_remote_imp_action(target_fn, **kwargs)

    _Store.add_use_remote_actions(className, remoteImpAction)

    @wraps(fn)
    def wrapper(*args, **kwargs):
        return remoteImpAction(*args[1:], **kwargs)

    return wrapper


def remote_imp_for_method(
    *args,
    action_key: Optional[str] = None,
    cache: CacheType = None,
    cache_key_func: Callable = keys.hashkey,
    lock: bool = False,
    timeout: Optional[float] = None,
):
    """装饰器,在worker模板类方法中使用"""
    fn = args[0] if args.__len__() == 1 and callable(args[0]) else None
    if fn is None:
        return partial(
            remote_imp_for_method,
            action_key=action_key,
            cache=cache,
            cache_key_func=cache_key_func,
            lock=lock,
            timeout=timeout,
        )

    return register_remote_imp_for_worker_template_method(
        fn,
        action_key=action_key,
        cache=cache,
        cache_key_func=cache_key_func,
        lock=lock,
        timeout=timeout,
    )


def worker_func(
    *args,
    use_remote_actions: tuple[RemoteImpAction, ...] = tuple(),
    on_stop: Callable | None = None,
    on_before_start: Callable | None = None,
    on_error: Callable | None = None,
):
    """### 装饰器 注册worker函数"""
    target = args[0] if args.__len__() == 1 and callable(args[0]) else None

    if target is None:
        return partial(
            worker_func,
            use_remote_actions=use_remote_actions,
            on_stop=on_stop,
            on_before_start=on_before_start,
            on_error=on_error,
        )

    _Store.register_workerhandler_by_func(
        target,
        use_remote_actions=WeakSet(use_remote_actions),
        on_stop=on_stop,
        on_before_start=on_before_start,
        on_error=on_error,
    )
    return target


# @worker_class
# class MyWorker(WorkerTemplate):

#     @remote_imp_for_method
#     def test(self, a: int, b: str) -> str: ...

#     def run(self, *args, **kwargs):
#         self.test(1, "2")
