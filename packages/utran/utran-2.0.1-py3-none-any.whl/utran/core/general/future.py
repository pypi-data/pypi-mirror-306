"""
全局Future管理器
"""

import asyncio as _asyncio
from concurrent import futures as _futures
from typing import overload as _overload
from . import message_protocol as _message_protocol


# Future计数器
__FUTURE_NUM_ = 0

AsyncUtFuture = _asyncio.Future[_message_protocol.MessageTypedDict]
SyncUtFuture = _futures.Future[_message_protocol.MessageTypedDict]

__FutureType = AsyncUtFuture | SyncUtFuture

# 所有缓存的未完成的futrue，按照分组存放
# 字典的键为分组的`名称`，值为`字典`{future_id:Future对象}
# {group:{future_id:Future对象}
__ALL_WAITING_FUTURES_: dict[str, dict[str, __FutureType]] = {}


@_overload
def __add_future(
    futrue: AsyncUtFuture, group="defualt"
) -> tuple[str, AsyncUtFuture]: 
    """### asyncio.Future"""
    ...
@_overload
def __add_future(
    futrue: SyncUtFuture, group="defualt"
) -> tuple[str, SyncUtFuture]: 
    """### futures.Future"""
    ...
def __add_future(futrue: __FutureType, group="defualt"):
    """
    ### 缓存一个Future
    """
    global __FUTURE_NUM_
    __FUTURE_NUM_ += 1
    future_id = "fid_" + str(__FUTURE_NUM_)
    groupWaitingFutrues = __ALL_WAITING_FUTURES_.get(group)
    if groupWaitingFutrues is None:
        groupWaitingFutrues = {}
        __ALL_WAITING_FUTURES_[group] = groupWaitingFutrues

    groupWaitingFutrues[future_id] = futrue
    return (future_id, futrue)


def create_future(group="defualt"):
    """
    ### futures.Future
    - group:(可选)， 默认值为'defualt'。用于对Future进行分组管理，方便后期清理和获取。
    - 返回值：一个元组，包含future_id和Future对象。
    """
    return __add_future(_futures.Future(), group)


def create_async_future(group="defualt"):
    """
    ### asyncio.Future
    - group:(可选)， 默认值为'defualt'。用于对Future进行分组管理，方便后期清理和获取。
    - 返回值：一个元组，包含future_id和Future对象。
    """
    loop = _asyncio.get_running_loop()    
    return __add_future(loop.create_future(), group)


def set_result_by_group(group: str, result:_message_protocol.MessageTypedDict):
    """
    ### 设置指定分组的所有Future的结果
    - group:分组名称
    - result:结果数据
    - 返回值：True/False
    """
    groupWaitingFutrues = __ALL_WAITING_FUTURES_.get(group)
    if groupWaitingFutrues is None:
        return False
    items = groupWaitingFutrues.items()
    if len(items) == 0:
        return False

    for future_id, futrue in items:
        futrue.set_result(result)
        del groupWaitingFutrues[future_id]
    return True


def set_result(future_id: str, result:_message_protocol.MessageTypedDict):
    """
    ### 设置指定Future的结果
    - future_id:Future的ID
    - result:结果数据
    - 返回值：True/False
    """
    if future_id is None:
        return False
    for group in __ALL_WAITING_FUTURES_:
        if future_id in __ALL_WAITING_FUTURES_[group]:
            __ALL_WAITING_FUTURES_[group][future_id].set_result(result)
            del __ALL_WAITING_FUTURES_[group][future_id]
            return True
    return False


def get_future(future_id: str):
    """
    ### 获取指定Future
    - future_id:Future的ID
    - 返回值：Future对象
    """
    if future_id is None:
        return None
    for group in __ALL_WAITING_FUTURES_:
        if future_id in __ALL_WAITING_FUTURES_[group]:
            return __ALL_WAITING_FUTURES_[group][future_id]
    return None


def get_futures_by_group(group: str):
    """
    ### 获取指定分组的所有Future
    - group:分组名称
    - 返回值：是一个生成器序列，每个元素为一个字典，包含future_id和Future对象。如： `(...,{'future_id': Future的ID, 'future': Future对象})`
    """
    groupWaitingFutrues = __ALL_WAITING_FUTURES_.get(group)
    if groupWaitingFutrues is None:
        return None
    items = groupWaitingFutrues.items()
    if len(items) == 0:
        return None

    return ({"future_id": future_id, "future": futrue} for (future_id, futrue) in items)


def wait_future(
    future_or_id: str | __FutureType, timeout: float | None = None
):
    """
    ### 等待指定Future,该等待会阻塞当前线程。
    - future_or_id:Future对象或Future的ID
    - timeout:超时时间，单位秒
    - 返回值：Future的结果
    """
    if type(future_or_id) is str:
        futrue = get_future(future_or_id)
        if futrue is None:
            return None
    else:
        futrue = future_or_id

    if _asyncio.isfuture(futrue):
        return _asyncio.run_coroutine_threadsafe(
            futrue, _asyncio.get_event_loop()
        ).result(timeout)

    if isinstance(futrue, _futures.Future):
        return futrue.result(timeout)


async def async_wait_future(
    future_or_id: str | __FutureType, timeout: float | None = None
):
    """
    ### 异步等待指定Future
    - future_or_id:Future对象或Future的ID
    - timeout:超时时间，单位秒
    - 返回值：Future的结果
    """
    if type(future_or_id) is str:
        futrue = get_future(future_or_id)
        if futrue is None:
            return None
    else:
        futrue = future_or_id

    if _asyncio.isfuture(futrue):
        return await _asyncio.wait_for(futrue, timeout)

    if isinstance(futrue, _futures.Future):
        _futrue = _asyncio.Future()
        futrue.add_done_callback(lambda f: _futrue.set_result(f.result(timeout)))
        return await _asyncio.wait_for(_futrue, timeout)


def wait_future_by_group(group: str, timeout=None):
    """
    ### 等待指定分组的所有Future
    - group:分组名称
    - timeout:超时时间，单位秒。注：该值不是总的超时时间，而是该分组中每个Future的超时时间。
    - 返回值：是一个生成器序列，每个元素为一个字典，包含future_id和Future的结果。如： `(...,{'result': Future的结果, 'future_id': Future的ID})`
    """
    groupWaitingFutrues = __ALL_WAITING_FUTURES_.get(group)
    if groupWaitingFutrues is None:
        return None
    items = groupWaitingFutrues.items()
    if len(items) == 0:
        return None

    return (
        {"result": wait_future(futrue, timeout), "future_id": future_id}
        for (future_id, futrue) in items
    )


def cancel_future_by_group(group: str):
    """
    ### 取消指定分组的所有Future
    - group:分组名称
    - 返回值：True/False
    """
    if group in __ALL_WAITING_FUTURES_:
        items = __ALL_WAITING_FUTURES_[group].items()
        if len(items) == 0:
            return False
        for _, futrue in items:
            futrue.cancel()
        del __ALL_WAITING_FUTURES_[group]
        return True
    return False


def cancel_future(future_id: str|None = None):
    """
    ### 取消指定Future
    - future_id:Future的ID
    - 返回值：True/False
    """
    if future_id is None: return False
    for group in __ALL_WAITING_FUTURES_:
        if future_id in __ALL_WAITING_FUTURES_[group]:
            __ALL_WAITING_FUTURES_[group][future_id].cancel()
            del __ALL_WAITING_FUTURES_[group][future_id]
            return True
    return False


def get_group_names():
    """
    ### 获取所有分组名称
    - 返回值：分组名称列表
    """
    return list(__ALL_WAITING_FUTURES_.keys())
