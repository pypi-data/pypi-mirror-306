import threading as _threading
from typing import Optional as _Optional

from . import log as _log
from .core import context as _context
from .core.remote.action import _get_all_imp_actions
from .core.local.action import _get_all_actions
from .core.host import GetConnectionsDelay as _GetConnectionsDelay
from .core.general.utils import __print_header


#  导出模块
from .core.context import set_config, set_server_instance, set_identify
from . import py_ts as PyTs
from . import cli as Cli
from .core.host import add_act_uri, Host
from .core.local.action import action
from .core.remote.action import remote_imp
from .core.remote.wokeblock import wokeblock_func,r_scope

from .core.remote import wokeblock as UtWokeBlock
from .core.general import caches as UtCaches
from .core.general import base_action as UtAction
from .core.general import exceptions as UtExceptions
from .socket.sever import AppServer


__version__ = "2.0.1"


def run(
    *,
    host="localhost",
    port=2525,
    debug: _Optional[bool] = None,
    log_folder: _Optional[str] = None,
    _is_dev_mode: bool = False,
):
    """启动服务"""
    _context.__UTRAN_CONTEXT__["__start_by__"] = "default"
    _context.__UTRAN_CONTEXT__["host"] = host
    _context.__UTRAN_CONTEXT__["port"] = port
    _context.__UTRAN_CONTEXT__["debug"] = (
        debug if debug is not None else _context.__UTRAN_CONTEXT__["debug"]
    )
    _context.__UTRAN_CONTEXT__["__env__"] = "dev" if _is_dev_mode else "prod"
    _context.__UTRAN_CONTEXT__["log_folder"] = log_folder

    __init_start__()
    __start_backend_in_thread__(host=host, port=port)
    
    # 接收ctrl+c退出信号
    import signal

    def signal_handler(sig, frame):
        _log.logger.log("NOTICE", "Received signal {}, exiting...".format(sig))
        _context.__UTRAN_CONTEXT__["exit_event"].set()

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    while not _context.__UTRAN_CONTEXT__["exit_event"].is_set():
        _context.__UTRAN_CONTEXT__["exit_event"].wait(1)


def start_host():
    """启动Host
    > 该方法用在非utran.run启动的情况下使用。
    """
    if _context.__UTRAN_CONTEXT__["__start_by__"] == None:
        __init_start__()


def __init_start__():
    """启动前的初始化"""

    # 检查Host是否实例化，没有实例化则创建Host实例
    if not _context.__UTRAN_CONTEXT__.get("host_instance"):
        Host()

    utHost = _context.__UTRAN_CONTEXT__["host_instance"]
    log_folder = _context.__UTRAN_CONTEXT__["log_folder"]
    is_debug = _context.__UTRAN_CONTEXT__["debug"]
    is_dev_mode = _context.__UTRAN_CONTEXT__["__env__"] == "dev"
    
    # 初始化日志
    if is_dev_mode:
        _log.init_dev_logger()
    else:
        _log.init_prod_logger(is_debug=is_debug, output_folder=log_folder)

    # 执行预处理
    from utran.core.remote.wokeblock import __pre_process__
    __pre_process__()


    # 打印启动信息
    _log.logger.log(
        "NOTICE",
        __print_header(
            version=__version__,
            backend=utHost._backend.name(),
            local_actions_num=len(_get_all_actions()),
            remote_actions_num=len(_get_all_imp_actions()),
            wokeblock_num=len(UtWokeBlock._Store.get_all_wokeblock()),
            is_debug=is_debug,
            is_dev=is_dev_mode,
        ),
    )


def __start_backend_in_thread__(*args, **kwargs):
    utHost = _context.__UTRAN_CONTEXT__.get("host_instance")
    if not utHost:
        raise RuntimeError("No host instance found.")
    thread = _threading.Thread(target=utHost._backend.run, args=args, kwargs=kwargs, daemon=True)
    thread.start()


def stop_backend():
    utHost = _context.__UTRAN_CONTEXT__.get("host_instance")
    if not utHost:
        raise RuntimeError("No host instance found.")
    utHost._backend.stop()


def restart_backend():
    """待实现.."""
    utHost = _context.__UTRAN_CONTEXT__.get("host_instance")
    if not utHost:
        raise RuntimeError("No host instance found.")


# 延迟
getConnectionsDelay = _GetConnectionsDelay()


__all__ = [
    # 导出的模块
    "PyTs",
    "Cli",
    "Host",
    "AppServer",
    "UtExceptions",
    "UtAction",
    "UtCaches",
    "UtWokeBlock",
    # 注册的函数
    "action",
    "remote_imp",
    "wokeblock_func",
    # 运行相关
    "run",
    "start_host",
    # 设置相关
    "add_act_uri",
    "set_config",
    "set_server_instance",
    "set_identify",
    # 其他
    "getConnectionsDelay",
]
