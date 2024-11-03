import asyncio
import base64
import binascii
from enum import Enum
from functools import partial
from urllib.parse import parse_qs
import xml.etree.ElementTree as ET

import hashlib
import json
from multidict import CIMultiDict
from typing import (
    Any,
    Callable,
    Coroutine,
    Dict,
    Iterable,
    List,
    Literal,
    Optional,
    Tuple,
    Protocol,
    Union,
    overload,
)

from .base import (
    CONNECTION,
    SEC_WEBSOCKET_ACCEPT,
    SEC_WEBSOCKET_KEY,
    SEC_WEBSOCKET_VERSION,
    UPGRADE,
    WebSocketProtocol,
    WS_KEY,
    WSMsgType,
)
from .utils import URLHandler
from utran.log import logger


class WSHandshakeError(Exception):
    """WebSocket protocol handshake error."""


class Middleware(Protocol):
    async def __call__(self, request: "Request") -> Optional["Response"]: ...


class Handler(Protocol):
    async def __call__(self, request: "Request") -> Union["Response", dict, str]: ...


class Request:
    __slots__ = (
        "_method",
        "_URL",
        "_headers",
        "_body",
        "_reader",
        "_writer",
        "_ws_creator",
    )

    def __init__(
        self,
        method: str,
        path: str,
        headers: Dict[str, str],
        reader: asyncio.StreamReader,
        writer: asyncio.StreamWriter,
        body: Any = None,
        ws_creator: Optional[Callable[["Request"], "WebSocketResponse"]] = None,
    ):
        """请求类，封装 HTTP 请求信息"""
        self._method = method
        self._URL = URLHandler(path)
        self._headers = headers
        self._body = body
        self._reader = reader
        self._writer = writer
        self._ws_creator = ws_creator

    def upgrade(self) -> "WebSocketResponse":
        """升级 WebSocket 请求"""
        if self.is_upgrade():
            # await websocket.prepare()
            if self._ws_creator is None:  # pragma: no cover
                raise RuntimeError("WebSocket handler is not defined")
            return self._ws_creator(self)

        raise NotImplementedError("Not a WebSocket request")

    def is_upgrade(self) -> bool:
        """判断请求是否为 WebSocket 请求"""
        return (
            "Upgrade" in self._headers
            and self._headers["Upgrade"].lower() == "websocket"
            and "Connection" in self._headers
            and "Upgrade" in self._headers["Connection"]
        )

    async def __read_body(self):
        if self.method == "POST":
            content_length = int(self.headers.get("Content-Length", 0))
            try:
                if content_length > 0:
                    body_bytes = await asyncio.wait_for(
                        self._reader.read(content_length), timeout=10
                    )

                    # 获取 Content-Type
                    content_type = self.content_type

                    if content_type == "application/json":
                        return json.loads(body_bytes)  # 解码为 JSON 对象

                    elif content_type == "application/x-www-form-urlencoded":
                        return parse_qs(body_bytes.decode("utf-8"))  # 解析为字典

                    elif content_type == "application/xml":
                        return ET.fromstring(body_bytes)  # 解析为 XML 对象

                    elif content_type == "text/plain":
                        return body_bytes.decode("utf-8")  # 作为字符串返回

                    else:
                        return body_bytes  # 其他类型返回原始字节
            except Exception as e:
                logger.debug(f"Error reading body: {e}")

        return ""

    @property
    def accept(self) -> str:
        """获取请求的 Accept 头信息"""
        return self._headers.get("Accept", "*/*")

    async def get_body(self) -> Any:
        """获取请求体"""
        if self._body is None:
            self._body = await self.__read_body()
        return self._body

    @property
    def content_type(self) -> str:
        """获取请求内容的类型"""
        return self._headers.get("Content-Type", "text/plain").lower()

    @property
    def query(self):
        return self._URL.get_query_params()

    @property
    def method(self) -> str:
        """获取请求方法"""
        return self._method

    @property
    def path(self) -> str:
        """获取请求路径"""
        return self._URL.get_path()

    @property
    def headers(self) -> Dict[str, str]:
        """获取请求头"""
        return self._headers


class HTTPStatus(Enum):
    OK = 200
    NOT_FOUND = 404
    INTERNAL_SERVER_ERROR = 500
    BAD_REQUEST = 400
    LENGTH_REQUIRED = 411


ContentType = Literal["text/plain", "text/html", "application/json"]


class Response:
    __slots__ = ("status", "body", "content_type", "charset", "headers")

    def __init__(
        self,
        status: HTTPStatus = HTTPStatus.OK,
        body: Union[str, dict] = "",
        content_type: str = "text/plain",
        charset: str = "utf-8",
        headers: Optional[Dict[str, str]] = None,
    ):
        """响应类，封装 HTTP 响应信息

        Args:
            status (HTTPStatus): HTTP响应状态码，默认200 OK
            body (Union[str, dict]): 响应体，可以是字符串或字典
            content_type (str): 内容类型，默认"text/plain"
            charset (str): 字符集，默认"utf-8"
            headers (Optional[Dict[str, str]]): 自定义HTTP响应头部
        """
        self.status = status
        self.body = body
        self.content_type = content_type
        self.charset = charset
        self.headers = headers or {}

    def to_http_response(self) -> str:
        """转换为 HTTP 响应格式"""
        header_lines = [
            f"HTTP/1.1 {self.status}",
            f"Content-Type: {self.content_type}; charset={self.charset}",
        ]

        # 添加自定义响应头
        for key, value in self.headers.items():
            header_lines.append(f"{key}: {value}")

        # 组合所有头部信息
        headers_str = "\r\n".join(header_lines) + "\r\n\r\n"

        # 如果返回的是字典，则将其转换为 JSON 格式
        if isinstance(self.body, dict):
            self.body = json.dumps(self.body)
            self.content_type = "application/json"

        return f"{headers_str}{self.body}"

    def set_header(self, key: str, value: str):
        """设置自定义的 HTTP 响应头

        Args:
            key (str): 响应头的名称
            value (str): 响应头的值
        """
        self.headers[key] = value

    def json(self, data: dict):
        """设置响应体为 JSON 格式

        Args:
            data (dict): 要设置的 JSON 数据
        """
        self.body = data
        self.content_type = "application/json"


class AppServer:
    def __init__(
        self,
        *,
        ping_interval: Optional[float] = None,
        ping_timeout: Optional[float] = None,
    ):
        """构造函数，初始化应用程序"""
        self.router = Router()
        self.server = WebServer(
            self.router, ping_interval=ping_interval, ping_timeout=ping_timeout
        )
        self._startup_callbacks: list[Callable] = []
        self._shutdown_callbacks: list[Callable] = []

    @overload
    def get(self, path: str) -> Callable: ...
    @overload
    def get(self, path: str, handler: Handler) -> None: ...
    def get(self, path: str, handler: Optional[Handler] = None) -> Optional[Callable]:
        if handler is None:
            return self.__decorator("GET", path)
        self.add_route("GET", path, handler)
        return None

    @overload
    def post(self, path: str) -> Callable: ...
    @overload
    def post(self, path: str, handler: Handler) -> None: ...
    def post(self, path: str, handler: Optional[Handler] = None):
        if handler is None:
            return self.__decorator("POST", path)
        self.add_route("POST", path, handler)

    def __decorator(self, method: Literal["GET", "POST"], path: str) -> Callable:
        return lambda handler: self.add_route(method, path, handler)

    def add_route(self, method: Literal["GET", "POST"], path: str, handler: Handler):
        """添加路由规则"""
        self.server.router.add_route(method, path, handler)

    def add_middleware(self, middleware: Middleware) -> None:
        """添加中间件"""
        self.router.add_middleware(middleware)

    def add_startup_callback(self, callback: Callable) -> None:
        """添加启动回调函数"""
        self._startup_callbacks.append(callback)

    def add_shutdown_callback(self, callback: Callable) -> None:
        """添加关闭回调函数"""
        self._shutdown_callbacks.append(callback)

    async def _startup(self) -> None:
        for fn in self._startup_callbacks:
            await fn() if asyncio.iscoroutinefunction(fn) else fn()

    async def _shutdown(self) -> None:
        for fn in self._shutdown_callbacks:
            await fn() if asyncio.iscoroutinefunction(fn) else fn()

    def run(
        self,
        host: str,
        port: int,
        *,
        loop: asyncio.AbstractEventLoop = asyncio.get_event_loop(),
    ) -> None:
        """运行服务器"""
        loop.run_until_complete(
            self.server.run(
                host=host,
                port=port,
                on_startup=self._startup,
                on_shutdown=self._shutdown,
            )
        )

    def stop(self) -> None:
        """停止服务器"""
        self.server.stop()


class Router:
    __slots__ = ("__routes", "__middlewares")

    def __init__(self) -> None:
        self.__routes: Dict[Tuple[str, str], Handler] = {}
        self.__middlewares: List[Middleware] = []

    def add_route(self, method: str, path: str, handler: Handler) -> None:
        """添加路由规则"""
        path = URLHandler(path).get_path()
        self.__routes[(method, path)] = handler

    def remove_route(self, method: str, path: str) -> None:
        """删除指定的路由规则"""
        path = URLHandler(path).get_path()
        self.__routes.pop((method, path), None)

    def list_routes(self) -> List[Tuple[str, str]]:
        """列出所有路由规则"""
        return list(self.__routes.keys())

    def add_middleware(self, middleware: Middleware) -> None:
        """添加中间件"""
        self.__middlewares.append(middleware)

    async def _handle_middleware(self, request: Request) -> Optional[Response]:
        """处理请求并调用中间件和路由处理函数"""
        try:
            for middleware in self.__middlewares:
                response = await middleware(request)
                if response is not None:
                    return response

        except Exception as e:
            logger.debug(f"处理中间件时发生错误: {e}")
            return Response(HTTPStatus.INTERNAL_SERVER_ERROR, str(e))
        
        return None

    async def _handle_request(self, request: Request) -> Any:
        """处理请求并调用对应的处理函数"""
        handler = self.__routes.get((request.method, request.path))

        if handler is not None:
            if asyncio.iscoroutinefunction(handler):
                return await handler(request)
            else:
                return handler(request)

        return Response(HTTPStatus.NOT_FOUND, "未找到请求的资源")


class WebSocketResponse(WebSocketProtocol):

    def __init__(
        self,
        request: Request,
        *,
        protocols: Iterable[str] = (),
        ping_interval: Optional[float] = None,
        ping_timeout: Optional[float] = None,
    ):
        """构造函数，初始化 WebSocket 连接"""
        super().__init__(
            request.headers,
            protocols=protocols,
            ping_interval=ping_interval,
            ping_timeout=ping_timeout,
        )
        self._reader = request._reader
        self._writer = request._writer

    async def prepare(self):
        """### 准备 WebSocket 连接"""
        try:
            response_headers = await self.__handshake()
            self._headers.update(response_headers)
            await self.__send_handshake_response(response_headers)

        except WSHandshakeError as e:
            logger.debug(e)
            await self._writer.drain()
            self._writer.close()
            return

    async def __send_handshake_response(self, headers: CIMultiDict) -> None:
        """发送 WebSocket 握手响应"""
        response_lines = [
            "HTTP/1.1 101 Switching Protocols",
        ]
        for key, value in headers.items():
            response_lines.append(f"{key}: {value}")
        response_message = "\r\n".join(response_lines) + "\r\n\r\n"
        self._writer.write(response_message.encode("utf-8"))
        await self._writer.drain()

    async def auto_send_ping(self, ping_interval: float) -> None:
        await asyncio.sleep(ping_interval)  # 空转，让其他等任务可以执行
        while not self.closed:
            await self._send_ping()
            self._pong_wait_event.clear()
            try:
                # 计算耗时
                start_time = asyncio.get_running_loop().time()
                await asyncio.wait_for(
                    self._pong_wait_event.wait(), timeout=self._ping_timeout
                )
                dt = asyncio.get_running_loop().time() - start_time
                sleep_time = ping_interval - dt
                if sleep_time > 0:
                    await asyncio.sleep(sleep_time)
            except asyncio.TimeoutError:
                if self.closed:
                    break                    
                else:
                    logger.debug("pong timeout.")
                    # self._writer.close() 
                
        logger.debug("auto ping task is stoped.")

    async def __handshake(self) -> CIMultiDict:
        """处理 WebSocket 握手请求"""
        headers = self._headers
        upgrade_hdr = headers.get(UPGRADE, "").lower().strip()
        conn_hdr = headers.get(CONNECTION, "").lower()
        ws_key = headers.get(SEC_WEBSOCKET_KEY)

        if not (upgrade_hdr == "websocket" and "upgrade" in conn_hdr):
            raise WSHandshakeError(f"No WebSocket UPGRADE hdr: {upgrade_hdr}")

        protocol = self._negotiate_protocol(headers)
        version = headers.get(SEC_WEBSOCKET_VERSION, "")
        if version not in ("13", "8", "7"):
            raise WSHandshakeError(f"Unsupported version: {version}")

        try:
            if not ws_key or len(base64.b64decode(ws_key)) != 16:
                raise WSHandshakeError(f"Handshake error: {ws_key!r}")
        except binascii.Error:
            raise WSHandshakeError(f"Handshake error: {ws_key!r}") from None

        accept_val = base64.b64encode(
            hashlib.sha1(ws_key.encode() + WS_KEY).digest()
        ).decode()
        response_headers = CIMultiDict(
            {
                UPGRADE: "websocket",
                CONNECTION: "upgrade",
                SEC_WEBSOCKET_ACCEPT: accept_val,
            }
        )
        return response_headers


class WebServer:
    __slots__ = ("router", "ws_creator")

    def __init__(
        self,
        router: Router,
        *,
        ping_interval: Optional[float] = None,
        ping_timeout: Optional[float] = None,
    ):
        """构造函数，初始化服务器的主机和端口"""
        self.router = router
        self.ws_creator = partial(
            WebSocketResponse, ping_interval=ping_interval, ping_timeout=ping_timeout
        )

    async def run(
        self,
        *,
        host: str = "localhost",
        port: int = 8090,
        on_startup: Optional[Callable[[], Coroutine]] = None,
        on_shutdown: Optional[Callable[[], Coroutine]] = None,
    ) -> None:
        """启动 HTTP 和 WebSocket 服务器"""
        server = await asyncio.start_server(self.handle_client, host, port)
        logger.success(f"server on http://{host}:{port}")
        await on_startup() if on_startup else None
        async with server:
            await server.serve_forever()

        await on_shutdown() if on_shutdown else None

    def stop(self) -> None:
        """终止事件循环，停止服务器"""
        loop = asyncio.get_running_loop()
        loop.stop()
        # loop.close()

    async def handle_client(
        self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter
    ) -> None:
        """处理每个客户端连接的协程"""

        # 初始化
        request_line = await reader.readline()
        logger.debug(f"接收到请求: {request_line.decode().strip()}")

        try:
            method, path = request_line.decode().strip().split(" ")[:2]
            headers = await self.parse_headers(reader)

            request = Request(
                method,
                path,
                headers,
                reader=reader,
                writer=writer,
                ws_creator=self.ws_creator,
            )
        except ValueError:
            await self.send_http_response(
                writer, Response(HTTPStatus.BAD_REQUEST, "请求格式不正确")
            )
            return

        #  处理逻辑
        try:
            if (
                response := await self.router._handle_middleware(request)  # 处理中间件
            ) and isinstance(response, Response):
                return await self.send_http_response(writer, response)

            response = await self.router._handle_request(request)  # 处理请求

            if response is not None:
                if isinstance(response, Response):
                    return await self.send_http_response(writer, response)
                else:
                    if isinstance(response, str):
                        return await self.send_http_response(
                            writer, Response(status=HTTPStatus.OK, body=response)
                        )
                    elif isinstance(response, bytes):
                        return await self.send_http_response(
                            writer,
                            Response(status=HTTPStatus.OK, body=response.decode()),
                        )
                    elif isinstance(response, dict):
                        return await self.send_http_response(
                            writer,
                            Response(
                                status=HTTPStatus.OK,
                                body=json.dumps(response),
                                content_type="application/json",
                            ),
                        )
                    else:
                        return await self.send_http_response(
                            writer,
                            Response(
                                status=HTTPStatus.OK,
                                body=str(response),
                            ),
                        )

            await self.send_http_response(writer, Response(HTTPStatus.BAD_REQUEST))

        except ConnectionResetError:  # 客户端断开连接
            logger.debug(f"客户端断开连接")

        except Exception as e:
            logger.debug(f"处理请求时发生错误: {e}")
            logger.exception(e)
            await self.send_http_response(
                writer, Response(HTTPStatus.INTERNAL_SERVER_ERROR, str(e))
            )

    async def parse_headers(self, reader: asyncio.StreamReader) -> dict:
        """解析 HTTP 请求头并返回字典"""
        chunk = bytearray()
        while True:
            header = await reader.readline()
            if header == b"\r\n":  # 空行表示请求头结束
                break
            chunk.extend(header)

        return self._parse_header_lines(chunk.decode("utf-8").split("\r\n"))

    def _parse_header_lines(self, header_lines):
        """解析 HTTP 请求头部线"""
        headers = {}
        for line in header_lines:
            if ": " in line:
                key, value = line.split(": ", 1)
                headers[key] = value.strip()
        return headers

    async def send_http_response(
        self, writer: asyncio.StreamWriter, response: Response
    ) -> None:
        """发送 HTTP 响应"""
        res = response.to_http_response()
        writer.write(res.encode("utf-8"))
        await writer.drain()
        writer.close()


if __name__ == "__main__":
    app = AppServer()

    @app.get("/")
    async def index(request: Request):
        """首页处理函数"""
        # a = await request.params()
        logger.debug(request.query)
        return {"message": "Hello, World!"}

    @app.post("/echo")
    async def echo(request: Request):
        """Echo 处理函数"""
        return await request.get_body()

    @app.get("/ws")
    async def websocket_handler(request: Request):
        """WebSocket 处理函数"""
        ws = request.upgrade()
        await ws.prepare()

        async for msg in ws:
            if msg.type == WSMsgType.TEXT:
                await ws.send_json({"message": msg.data})

    async def example_middleware(request: Request) -> Optional[Response]:
        """示例中间件"""
        logger.debug(f"处理中间件: {request.method} {request.path}")
        return None

    app.add_middleware(example_middleware)
    app.run("localhost", 2525)
