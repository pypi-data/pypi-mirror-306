"""唤醒模块"""

import asyncio
import inspect
from typing import (
    Any,
    Callable,
    List,
    Literal,
    Optional,
    Tuple,
    cast,
    overload,
)
from abc import ABCMeta, abstractmethod
from functools import partial
from utran.log import logger
from weakref import WeakKeyDictionary, WeakSet

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
    WokeBlockHandlerRegisterError,
    WokeBlockRuntimeError,
    WokeBlockScopeError,
)

from ..general.baseclass import BaseWokeBlockTemplate
from .. import context



WokeMode =Literal["remote_imp", "new_conn", "close_conn", "only_new_conn" , "only_close_conn"]

actionKeyStr = str
hostIdStr = str


class _Store:
    """### 全局存储类"""

    # 存储WokeBlock中使用的RemoteImpAction, key是类名/函数名，value是使用的RemoteImpAction集合
    _STORE_WOKEBLOCK_USE_REOMET_ACTIONS: dict[str, WeakSet[RemoteImpAction]] = dict()

    # 存储wokeblockrhandler, key是WokeBlockTemplate的子类，value是wokeblockhandler实例
    _STORE_WOKEBLOCK_OF_CLASS: WeakKeyDictionary[
        type["WokeBlockTemplate"], "_WokeBlockHandler"
    ] = WeakKeyDictionary()

    # 存储wokeblockrhandler, key是wokeblock函数，value是wokeblockhandler实例
    _STORE_WOKEBLOCK_OF_FUNC: WeakKeyDictionary[Callable, "_WokeBlockHandler"] = (
        WeakKeyDictionary()
    )

    @classmethod
    def add_use_remote_actions(
        cls,
        name: str,
        *remote_imp_actions: RemoteImpAction,
    ):
        """标记所使用的RemoteImpAction"""
        cls._STORE_WOKEBLOCK_USE_REOMET_ACTIONS.setdefault(name, WeakSet()).update(
            remote_imp_actions
        )

    @classmethod
    def get_all_wokeblock(cls):
        """获取所有得wokeblockhandler"""
        return list(cls._STORE_WOKEBLOCK_OF_CLASS.values()) + list(
            cls._STORE_WOKEBLOCK_OF_FUNC.values()
        )

    @classmethod
    def get_wokeblockhandler(cls, target: Callable) -> Optional["_WokeBlockHandler"]:
        """获取wokeblockhandler"""
        if inspect.isclass(target):
            return cls._STORE_WOKEBLOCK_OF_CLASS.get(target, None)
        return cls._STORE_WOKEBLOCK_OF_FUNC.get(target, None)

    @classmethod
    def get_wokeblockhandler_by_func_name(
        cls, name: str
    ) -> Optional["_WokeBlockHandler"]:
        """通过函数名获取wokeblockhandler"""
        for fn, wokeblockhandler in cls._STORE_WOKEBLOCK_OF_FUNC.items():
            if fn.__name__ == name:
                return wokeblockhandler
        return None

    @classmethod
    def get_wokeblockhandler_by_class_name(
        cls, name: str
    ) -> Optional["_WokeBlockHandler"]:
        """通过类名获取wokeblockhandler"""
        for cls_type, wokeblockhandler in cls._STORE_WOKEBLOCK_OF_CLASS.items():
            if cls_type.__name__ == name:
                return wokeblockhandler
        return None

    @classmethod
    def register_wokeblockhandler_by_func(
        cls,
        target: Callable,
        use_remote_actions: WeakSet[RemoteImpAction],
        scope_remote_actions: (
            WeakKeyDictionary[RemoteImpAction, Tuple[hostIdStr, ...]]
            | Tuple[hostIdStr, ...]
            | None
        ) = None,
        rounds: Optional[int] = None,  # 执行回合数
        woke_mode: WokeMode = "remote_imp",  # 唤醒的模式
        on_stop: Callable | None = None,
        on_before_start: Callable | None = None,
        on_error: Callable | None = None,
        on_complate: Callable | None = None,
    ):
        """注册wokeblockhandler"""
        if inspect.isclass(target):
            raise TypeError("cannot register a class.")

        if not callable(target):
            raise TypeError("target must be a callable object")


        # 不能在 only模式下使用 RemoteAction
        if use_remote_actions and (woke_mode == "only_new_conn" or woke_mode == "only_close_conn"):
            raise ValueError(f"In '{target.__name__}', woke_mode can not be '{woke_mode}' when has remote imp action.")
        
        wokeblockhandler = _WokeBlockHandler(
            target=target,
            wokeblock_name=target.__name__,
            use_remote_actions=use_remote_actions,
            rounds=rounds,
            woke_mode=woke_mode,
            scope_remote_actions=scope_remote_actions,
            on_stop=on_stop,
            on_before_start=on_before_start,
            on_error=on_error,
            on_complate=on_complate,
        )

        cls._STORE_WOKEBLOCK_OF_FUNC[target] = wokeblockhandler
        return wokeblockhandler


def r_scope(
    *values: hostIdStr
    | Tuple[RemoteImpAction, hostIdStr]
    | Tuple[RemoteImpAction, List[hostIdStr]]
):
    """#### 限定RemoteImpAction来源的host, 默认可以使用所有host提供的远程实现。
    参数可以是以下几种类型:
    - hostIdStr
    - Tuple[RemoteImpAction, hostIdStr]
    - Tuple[RemoteImpAction, hostIdStr]
    """
    res: WeakKeyDictionary[RemoteImpAction, Tuple[hostIdStr, ...]] = WeakKeyDictionary()
    full: List[hostIdStr] = []
    for item in values:
        if isinstance(item, str):
            full.append(item)
        elif isinstance(item, tuple):
            if item.__len__() != 2:
                raise ValueError(f"scope item {item} length must be 2")
            r, h = item
            if not isinstance(r, RemoteImpAction):
                raise ValueError(f"scope item {r} must be RemoteImpAction")
            if isinstance(h, str):
                h = [h]
            if not isinstance(h, list):
                raise ValueError(f"scope item {h} must be list")
            res[r] = res.get(r, tuple()) + tuple(h)
    if full:
        return tuple(full)
    return res


class _WokeBlockHandler:
    __slots__ = (
        "funcs",
        "use_remote_actions",
        "is_runing",
        "is_completed",
        "wokeblock_name",
        "loop",
        "is_abandoned",
        "scope_remote_actions",
        "rounds",
        "rounds_count",
        "_temp_remote_action_scope",
        "woke_mode",
    )

    def __init__(
        self,
        target: Callable,
        wokeblock_name: str,
        use_remote_actions: WeakSet[RemoteImpAction] = WeakSet(),
        scope_remote_actions: (
            WeakKeyDictionary[RemoteImpAction, Tuple[hostIdStr, ...]]
            | Tuple[hostIdStr, ...]
        ) | None = None,
        rounds: Optional[int] = None,  # 执行回合数
        woke_mode: WokeMode = "remote_imp",  # 唤醒的模式
        on_stop: Callable | None = None,
        on_before_start: Callable | None = None,
        on_error: Callable | None = None,
        on_complate: Callable | None = None,
    ) -> None:
        self.rounds = max(float('inf') if rounds is None else rounds,1)  # 执行回合数
        self.rounds_count = 0  # 执行回合数计数器
        self.is_runing = False
        self.is_completed = False
        self.wokeblock_name = wokeblock_name
        self.woke_mode = woke_mode
        self.use_remote_actions = use_remote_actions

        self._temp_remote_action_scope = scope_remote_actions or tuple()
        self.scope_remote_actions: dict[actionKeyStr, Tuple[hostIdStr, ...] | None] = {}

        self.loop: asyncio.AbstractEventLoop
        self.funcs = dict(
            target_fn=target,
            on_stop=on_stop,
            on_before_start=on_before_start,
            on_error=on_error,
            on_complate=on_complate,
        )
        self.is_abandoned:Optional[str] = None  # 如果有值，则表示该wokeblockhandler已被遗弃

    def _pre_proccess(self):
        """预处理，需要再程序启动前执行"""
        from .action import REMOTE_IMP_ACTIONS

        # 处理use_remote_actions
        if not self.use_remote_actions:
            self.use_remote_actions = WeakSet(REMOTE_IMP_ACTIONS.values())

        use_action_keys = [a._action_key for a in self.use_remote_actions]

        # 处理remote_action_scope
        if type(self._temp_remote_action_scope) is tuple:
            allow_hosts = (
                self._temp_remote_action_scope
                if self._temp_remote_action_scope
                else None
            )
            self.scope_remote_actions = {k: allow_hosts for k in use_action_keys}

        elif isinstance(self._temp_remote_action_scope, WeakKeyDictionary):
            for k in use_action_keys:
                self.scope_remote_actions[k] = self._temp_remote_action_scope.get(
                    REMOTE_IMP_ACTIONS[k], None
                )
        else:
            raise ValueError(
                f"scope_remote_actions {self._temp_remote_action_scope} type error"
            )

        self._temp_remote_action_scope = None  # 处理完毕，释放内存

    def _executer(
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
        - WokeBlockRuntimeError: 运行时错误，执行用户注册的函数时发生错误

        #### 内部错误:
        - RemoteRuntimeError: 远程调用运行时发生内部错误
        
        #### 程序终止的错误:
        - WokeBlockScopeError: 作用域相关错误
        """
        context.__UTRAN_CONTEXT__["thread_local_data"].wokeblock_handler = self        
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
        except WokeBlockScopeError as e:            
            raise e
        except Exception as e:
            raise WokeBlockRuntimeError(
                f'wokeblock::{self.wokeblock_name} -> error in "{key}": {e}'
            ) from e

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        """
        #### 会处理所有`_executer`函数的异常,最终只会向外抛出两种运行时错误:
        - `RemoteRuntimeError`  远程调用运行时发生内部的错误
        - `WokeBlockRuntimeError`  本函数执行时的错误
        > 注: 当用户注册的`on_error`函数有错误时,该WokeBlockHandler会被遗弃
        """
        self.is_runing = True
        self.loop = asyncio.new_event_loop()
        logger.log("WOKE",f'executer "{self.wokeblock_name}".')
        try:
            try:
                logger.log("DEV",
                    f"wokeblock::{self.wokeblock_name} -> executor 'on_before_start'"
                )
                self._executer(
                    "on_before_start", *args, **kwds
                )  # 执行on_before_start函数

                logger.log("DEV",
                    f"wokeblock::{self.wokeblock_name} -> executor 'target_fn'"
                )
                self._executer("target_fn", *args, **kwds)  # 执行target_fn目标函数

                logger.log("DEV",
                    f"wokeblock::{self.wokeblock_name} -> executor 'on_complate'"
                )
                self._executer("on_complate")  # 执行on_complate函数

                
                # 执行回合数计数器
                self.rounds_count += 1
                if self.rounds and self.rounds_count >= self.rounds:
                    self.is_completed = True
                    
                logger.log("WOKE",f"'{self.wokeblock_name}' completed [{self.rounds_count}/{self.rounds}].")

            except RemoteNotImplementedError as e:
                logger.log("DEV",f"wokeblock::{self.wokeblock_name} -> 暂停运行，{e}")
                logger.log("DEV",f"wokeblock::{self.wokeblock_name} -> executor 'on_stop'")
                self._executer("on_stop")  # 执行on_stop函数

            except WokeBlockScopeError as e:
                logger.error(f"WokeBlockScopeError \n {e}")
                self.is_abandoned = str(e)  # 标记该wokeblockhandler已被遗弃
                
            except Exception as exec_error:
                raise exec_error

        except (
            RemoteResultError,
            RemoteTimeoutError,
            WokeBlockRuntimeError,
        ) as exec_error:
            try:
                if not self.funcs.get("on_error"):
                    logger.warning(exec_error)

                self._executer("on_error", exec_error)  # 执行on_error函数
            except RemoteRuntimeError as e:
                raise e
            except WokeBlockRuntimeError as e:
                # 用户注册的on_error函数发生错误，该错误会抛出到外层
                logger.error(f"原始错误：{exec_error}")  # 输出原始错误
                logger.error(f"wokeblock::{self.wokeblock_name}.on_error 存在错误: {e}")
                self.is_abandoned = str(e)  # 标记该wokeblockhandler已被遗弃

            except Exception as err:
                logger.error(f"原始错误：{exec_error}")  # 输出原始错误
                logger.error(
                    f"wokeblock::{self.wokeblock_name} -> error in on_error: {err}"
                )

        except RemoteRuntimeError as runtime_error:
            logger.exception(runtime_error)
            logger.error(runtime_error)
            raise runtime_error

        except Exception as e:
            # 其他运行时错误
            logger.error(f"_WokeBlockHandler 内部发生错误： {e}")
            raise WokeBlockRuntimeError(
                f"wokeblock::{self.wokeblock_name} -> runtime error: {e}"
            ) from e
        finally:
            self.is_runing = False
            self.loop.stop()
            logger.log("WOKE",f'"{self.wokeblock_name}" over.')


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
) -> Callable[[Callable[P, R]], Callable[P, R | _D]]: ...
def mark_remote_imp(
    *args,
    _: Callable[P, R] | None = None,
    action_key: Optional[str] = None,
    default_fn: Callable[..., _D] | None = None,
    cache: CacheType = None,
    cache_key_func: Callable = keys.hashkey,
    lock=False,
    timeout: Optional[float] = None,
) -> Callable[[Callable[P, R]], Callable[P, R] | Callable[P, R | _D]] | Callable[P, R]:
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
        )  # type: ignore

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
        return fn  # type: ignore

    raise ValueError(f"Method '{fn.__name__}' is already been marked as remote action.")


class WokeBlockTemplateRegisterMeta(BaseWokeBlockTemplate, ABCMeta):
    """
    元类用于注册WokeBlockTemplate类到WokeBlockHandler注册表
    - 限制只能直接继承一个WokeBlockTemplate类,不能继承WokeBlockTemplate的子类
    """

    def __new__(cls, name, bases, attrs):

        new_class = super().__new__(cls, name, bases, attrs)
        if name == "WokeBlockTemplate":
            return new_class

        all_mark_remote_imp: list[tuple[Callable, dict]] = []  # 类方法,配置

        use_remote_actions: WeakSet[RemoteImpAction] = WeakSet()
        for base in bases:
            # 检查继承关系
            if base != WokeBlockTemplate and issubclass(base, WokeBlockTemplate):
                # 不能继承WokeBlockTemplate的子类
                raise TypeError(
                    f"WokeBlockTemplate class '{name}' can only inherit from one WokeBlockTemplate class."
                )
            # 遍历父类的方法,获取远程调用方法
            if hasattr(base, "__dict__"):
                all_mark_remote_imp.extend(list(cls.get_imp_action_config(base)))

        all_mark_remote_imp.extend(list(cls.get_imp_action_config(new_class)))

        # # 将实例方法转换为类方法
        for attr_name, attr_value in attrs.items():
            if callable(attr_value) and not isinstance(attr_value, classmethod):
                attrs[attr_name] = classmethod(attr_value)

        woke_mode = attrs.get("woke_mode", "remote_imp")
        
        # 不能在 only模式下使用 RemoteAction
        if all_mark_remote_imp and (woke_mode == "only_new_conn" or woke_mode == "only_close_conn"):
            raise ValueError(f"WokeBlockTemplate class '{name}', woke_mode can not be '{woke_mode}' when has remote imp action.")
        
        for _method, _config in all_mark_remote_imp:
            wapper, impaction = cls.register_remote_imp(
                _method, **_config
            )  # 注册远程调用的函数

            attrs[_method.__name__] = wapper  # 绑定远程调用方法
            use_remote_actions.add(impaction)

        new_class = super().__new__(cls, name, bases, attrs)

        # 注册WokeBlockHandler
        cls.register_wokeblockhandler(new_class, use_remote_actions)

        return new_class

    def __init__(cls, name, bases, attrs):
        super().__init__(name, bases, attrs)

    def __call__(cls, *args, **kwargs):
        """
        实例化WokeBlockTemplate类时,会调用该方法,用于创建实例并存储
        """
        print(args, kwargs)
        instance = super().__call__(*args, **kwargs)
        # _Store.create_wokeblock_template_instance(cls)
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
            raise WokeBlockHandlerRegisterError("action_key is required")
        if type(action_key) is not str:
            raise WokeBlockHandlerRegisterError("action_key must be str")

        target_fn = partial(fn, None)  # 排除slef或cls参数

        # action_key是否已经存在，如果存在验证是否签名一致
        if remoteImpAction := get_remote_imp_action(config["action_key"]):
            remoteImpAction.check_signatures(
                target_fn
            )  # 验证签名，如果不一致会抛出异常
        else:
            remoteImpAction = register_remote_imp_action(target_fn, **config)

        return classmethod(remoteImpAction), remoteImpAction

    @classmethod
    def register_wokeblockhandler(
        cls,
        wt_class: type["WokeBlockTemplate"],
        use_remote_actions: WeakSet[RemoteImpAction],
    ):
        """注册wokeblockhandler"""

        wokeblockhandler = _WokeBlockHandler(
            wokeblock_name=wt_class.__name__,
            use_remote_actions=use_remote_actions,
            scope_remote_actions=wt_class.scope_remote_actions,
            rounds=wt_class.rounds,
            woke_mode=wt_class.woke_mode,
            target=wt_class.run,
            on_stop=wt_class.on_stop,
            on_before_start=wt_class.on_before_start,
            on_error=wt_class.on_error,
            on_complate=wt_class.on_complate,
        )

        _Store._STORE_WOKEBLOCK_OF_CLASS[wt_class] = wokeblockhandler


class WokeBlockTemplate(metaclass=WokeBlockTemplateRegisterMeta):
    """WokeBlock模板类的根类,抽象类
    - scope_remote_actions: 限定RemoteImpAction来源的host, 默认可以使用所有host提供的远程实现。 配合 utran.r_scope() 使用。
    - rounds: 执行回合数
    - woke_mode: 唤醒的模式 'remote_imp', 'new_conn', 'close_conn', `'only_new_conn'(不支持使用 RemoteAction)`, `'only_close_conn'(不支持使用 RemoteAction)`
    - run: 目标函数
    - on_before_start: 启动前函数
    - on_stop: 停止函数
    - on_error: 错误函数
    - on_complate: 完成函数
    """

    scope_remote_actions: (
        WeakKeyDictionary[RemoteImpAction, Tuple[hostIdStr, ...]]
        | Tuple[hostIdStr, ...]
        | None
    ) = None
    
    rounds: Optional[int] = None  # 执行回合数
    woke_mode: WokeMode = "remote_imp"  # 唤醒的模式

    @abstractmethod
    def run(self, *args, **kwargs) -> Any:
        pass

    def on_before_start(self) -> Any:
        pass

    def on_stop(self) -> Any:
        pass

    def on_error(
        self, error: RemoteResultError | RemoteTimeoutError | WokeBlockRuntimeError
    ) -> Any:
        pass

    def on_complate(self) -> Any:
        pass


def wokeblock_func(
    *args,
    use_remote_actions: tuple[RemoteImpAction, ...] = tuple(),
    scope_remote_actions: (
        WeakKeyDictionary[RemoteImpAction, Tuple[hostIdStr, ...]]
        | Tuple[hostIdStr, ...]
        | None
    ) = None,
    rounds: Optional[int] = None,
    woke_mode: WokeMode = "remote_imp",
    on_stop: Callable | None = None,
    on_before_start: Callable | None = None,
    on_error: Callable | None = None,
):
    """### 装饰器 注册wokeblock函数
    - use_remote_actions: 远程调用方法列表
    - scope_remote_actions: 限定RemoteImpAction来源的host, 默认可以使用所有host提供的远程实现。 配合 utran.r_scope() 使用。
    - rounds: 执行回合数
    - on_stop: 停止函数
    - on_before_start: 启动前函数
    - on_error: 错误函数
    """
    target = args[0] if args.__len__() == 1 and callable(args[0]) else None

    if target is None:
        return partial(
            wokeblock_func,
            use_remote_actions=use_remote_actions,
            scope_remote_actions=scope_remote_actions,
            rounds=rounds,
            woke_mode=woke_mode,
            on_stop=on_stop,
            on_before_start=on_before_start,
            on_error=on_error,
        )

    _Store.register_wokeblockhandler_by_func(
        target,
        use_remote_actions=WeakSet(use_remote_actions),
        scope_remote_actions=scope_remote_actions,
        rounds=rounds,
        woke_mode=woke_mode,
        on_stop=on_stop,
        on_before_start=on_before_start,
        on_error=on_error,
    )
    return target


def __pre_process__():
    """预处理"""
    for wb in _Store.get_all_wokeblock():
        wb._pre_proccess()
