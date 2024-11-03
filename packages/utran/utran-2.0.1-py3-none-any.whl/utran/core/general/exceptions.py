
# Remote相关错误
class RemoteRunActionError(Exception):
    """远程调用错误,基类"""


class RemoteResultError(RemoteRunActionError):
    """远程调用结果错误，即: 远程调用成功, 但是远程调用返回的结果中包含error字段"""


class RemoteRuntimeError(RemoteRunActionError):
    """远程调用运行时,发生内部错误"""


class RemoteTimeoutError(RemoteRunActionError):
    """远程调用超时错误"""


class RemoteNotImplementedError(RemoteRunActionError):
    """远程无可调用实现"""



# WokeBlock相关错误

class WokeBlockError(Exception):
    """WokeBlock错误,基类"""


class WokeBlockRuntimeError(WokeBlockError):
    """WokeBlock运行时错误"""


class WokeBlockHandlerRegisterError(WokeBlockError):
    """WokeBlockHandler注册错误"""

class WokeBlockScopeError(WokeBlockError):
    """WokeBlock作用域错误"""