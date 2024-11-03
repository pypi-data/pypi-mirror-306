import typing as _typing
# from typing_extensions import NotRequired

class MessageProtocol(_typing.TypedDict):
    """### 消息协议接口类型"""
    

class InitDataTypedDict(_typing.TypedDict):
    """
    ### 初始化数据接口类型
    - **imp_ations**: list[str]     # 导入的模块列表
    - **server_uri**: str           # [可选] 服务器地址，如果为空则表示该主机只作为客户端
    """
    imp_ations:list[str]
    server_uri: _typing.Optional[str]
    

class BaseMessageTypedDict(MessageProtocol):
    """
    ### 定义消息的基础件
    - **msg_id**: str         # 消息的唯一标识，用于确认消息是否被回复，以及回复消息的来源
    - **from_host**: list[str]      # 消息来源列表，其中第一个元素为发起的源主机，后续元素为转发或处理了该消息的主机
    - to_host: str        # 如果收到非本主机的消息，则查看本地是否有该host的连接，如果有则转发到该连接，没有则广播出去。(使用方法:收到消息优先判断to_host是否为本机或者空，如果不是则转发。是则根据from_host[0]进行回复)
    """
    msg_id: str
    from_host: list[str]
    to_host: str


class BaseFirstMessageTypedDict(MessageProtocol):
    """
    ### 首次消息接口类型
    - **init_data**: InitDataTypedDict   # 初始化数据
    """
    init_data:InitDataTypedDict
    
    
    

class GeneralMessageTypedDict(_typing.TypedDict,total=False):
    """
    ### 常规消息的接口类型
    - future_id: str      # [可选] 消息中就存在`future_id`，表示本地发起请求并作为`futrue`等待回复，直到接收到回复完成该`future`。
    - data: dict          # [可选] 具体的消息内容
    - confirm: bool       # [可选] 是否需要确认收到，如果是则用本次`msg_id`回复消息
    - action: str         # [可选] 执行action列表中的动作函数
    - error: str          # [可选] 错误信息
    """
    
    future_id: _typing.Optional[str]
    data: dict[str, _typing.Any]
    confirm: bool
    action: str
    error: str
    



class FirstMessageTypedDict(BaseMessageTypedDict,BaseFirstMessageTypedDict):
    """### 完整的首次消息接口类型"""
 

class MessageTypedDict(BaseMessageTypedDict,GeneralMessageTypedDict):
    """### 完整的常规消息接口类型"""
    
class FullMessageTypedDict(BaseMessageTypedDict,BaseFirstMessageTypedDict,GeneralMessageTypedDict):
    """### 完整的消息接口类型, 包含首次消息和常规消息"""





BaseMessage = _typing.TypeVar('BaseMessage', bound=BaseMessageTypedDict)

FirstMessage = _typing.TypeVar('FirstMessage', bound=FirstMessageTypedDict)

Message = _typing.TypeVar('Message', bound=MessageTypedDict)

