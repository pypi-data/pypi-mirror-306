import asyncio
from enum import IntEnum
from abc import ABC
import os
import struct

import html  # 使用 HTML 转义或其他安全措施来防止 XSS 攻击
import json
from multidict import istr
from typing import (
    Any,
    Callable,
    Dict,
    Final,
    Iterable,
    NamedTuple,
    Optional,
    cast
)

from utran.log import logger


class WSHandshakeError(Exception):
    """WebSocket protocol handshake error."""


JSONDecoder = Callable[[str], Any]

SEC_WEBSOCKET_PROTOCOL: Final[istr] = istr("Sec-WebSocket-Protocol")
SEC_WEBSOCKET_ACCEPT: Final[istr] = istr("Sec-WebSocket-Accept")
SEC_WEBSOCKET_VERSION: Final[istr] = istr("Sec-WebSocket-Version")
SEC_WEBSOCKET_KEY: Final[istr] = istr("Sec-WebSocket-Key")
CONNECTION: Final[istr] = istr("Connection")
WS_KEY: Final[bytes] = b"258EAFA5-E914-47DA-95CA-C5AB0DC85B11"
UPGRADE: Final[istr] = istr("Upgrade")


class WSMsgType(IntEnum):
    # websocket spec types
    CONTINUATION = 0x0
    TEXT = 0x1
    BINARY = 0x2
    PING = 0x9
    PONG = 0xA
    CLOSE = 0x8

    # aiohttp specific types
    CLOSING = 0x100
    CLOSED = 0x101
    ERROR = 0x102

    text = TEXT
    binary = BINARY
    ping = PING
    pong = PONG
    close = CLOSE
    closing = CLOSING
    closed = CLOSED
    error = ERROR


class WSMessage(NamedTuple):
    type: WSMsgType
    # To type correctly, this would need some kind of tagged union for each type.
    data: Any
    extra: Optional[str]

    def json(self, *, loads: Callable[[Any], Any] = json.loads) -> Any:
        """Return parsed JSON data.

        .. versionadded:: 0.22
        """
        return loads(self.data)


class Frame(NamedTuple):
    fin: bool
    rsv1: bool
    rsv2: bool
    rsv3: bool
    opcode: int
    mask: bool
    payload_length: int
    masking_key: Optional[bytes]
    payload_data: bytes


def extract_websocket_frame(data: bytes) -> Frame:
    """
    解析WebSocket帧并提取其组成部分。

    :param data: WebSocket帧的字节串
    :return: Frame NamedTuple，包含帧的所有部分
    """
    # 验证数据长度以防止溢出或内存访问违规
    data_length = len(data)
    if data_length < 2:
        raise ValueError("Invalid data length for WebSocket frame")

    # 提取第一个字节，包含FIN, RSV1, RSV2, RSV3, 和 Opcode
    first_byte = data[0]
    fin = (first_byte >> 7) & 1
    rsv1 = (first_byte >> 6) & 1
    rsv2 = (first_byte >> 5) & 1
    rsv3 = (first_byte >> 4) & 1
    opcode = first_byte & 0x0F

    # 提取第二个字节，包含Mask和Payload length
    second_byte = data[1]
    mask = (second_byte >> 7) & 1
    payload_length = second_byte & 0x7F

    index = 2
    # 提取Payload length
    if payload_length == 126:
        if data_length < index + 2:
            raise ValueError("Invalid data length for WebSocket frame")
        payload_length = int.from_bytes(data[index:index+2], 'big')
        index += 2
    elif payload_length == 127:
        if data_length < index + 8:
            raise ValueError("Invalid data length for WebSocket frame")
        payload_length = int.from_bytes(data[index:index+8], 'big')
        index += 8

    # 检查数据长度以确保不会读取超出数据范围
    if data_length < index + 4 * mask + payload_length:
        raise ValueError("Invalid data length for WebSocket frame")

    # 提取Masking-key
    masking_key = None
    if mask:
        masking_key = data[index:index + 4]
        index += 4

    # 提取Payload data
    payload_data = data[index:index + payload_length]

    # 如果Mask为1，解码Payload data
    if mask:
        masking_key = memoryview(masking_key) # type: ignore
        payload_data = bytes(b ^ masking_key[i % 4] for i, b in enumerate(payload_data))

    # 创建Frame实例并返回
    return Frame(fin=bool(fin), rsv1=bool(rsv1), rsv2=bool(rsv2), rsv3=bool(rsv3),
                 opcode=opcode, mask=bool(mask), payload_length=payload_length,
                 masking_key=masking_key, payload_data=payload_data)


def generate_mask():
    # 生成一个随机的 4 字节掩码
    return os.urandom(4)

def apply_mask(data, mask):
    # 应用掩码到数据载荷
    masked_data = bytearray(data)
    for i in range(len(data)):
        masked_data[i] = masked_data[i] ^ mask[i % 4]
    return bytes(masked_data)

class WebSocketProtocol(ABC):
    __slots__ = ("_reader", "_writer", "_protocols", "_ping_interval","_ping_timeout", "_headers","_pong_wait_event")

    _reader: asyncio.StreamReader
    _writer: asyncio.StreamWriter
    _use_mask: bool = False

    def __init__(
        self,
        headers: dict,
        *,
        protocols: Iterable[str] = (),
        ping_interval: Optional[float] = None,
        ping_timeout: Optional[float] = None,
    ):
        """构造函数，初始化 WebSocket 连接"""
        self._protocols = protocols
        self._ping_interval=ping_interval
        self._ping_timeout:float = ping_timeout if ping_timeout is not None else ping_interval if ping_interval is not None else 30
        self._headers: Dict[str, str] = {}
        self._headers.update(headers)
        self._pong_wait_event = asyncio.Event()
        self._pong_wait_event.set()
    def close(self, code: int = 1000) -> None:
        """关闭 WebSocket 连接"""
        self._writer.close()

    @property
    def closed(self) -> bool:
        """检查 WebSocket 连接是否已关闭"""
        return self._writer.transport.is_closing()

    def _negotiate_protocol(self, headers) -> Optional[str]:
        """协商 WebSocket 协议
        > 此方法暂时没有使用，后续版本会实现协议协商功能
        """
        protocol = None
        if SEC_WEBSOCKET_PROTOCOL in headers:
            req_protocols = [
                proto.strip() for proto in headers[SEC_WEBSOCKET_PROTOCOL].split(",")
            ]
            for proto in req_protocols:
                if proto in self._protocols:
                    protocol = proto
                    break
            else:
                logger.debug(
                    f"Client protocols {req_protocols} don't overlap server-known ones {self._protocols}"
                )
        return protocol

    async def receive(self, *, timeout: Optional[float] = None) -> WSMessage:
        """接收并解码 WebSocket 消息"""
        try:
            data = await asyncio.wait_for(self._reader.read(1024), timeout)
            if not data:
                await self._send_close_frame()
                return WSMessage(WSMsgType.CLOSED, None, None)
            
            try:
                frame = extract_websocket_frame(data)
            except Exception as e:
                try:
                    await self._send_close_frame()
                except: pass
                return WSMessage(
                    WSMsgType.ERROR,
                    None,
                    extra=f"Invalid frame data: {e}",
                )
            
            # 如果是关闭帧
            if frame.opcode == 0x8:  # Close 的操作码
                logger.log("DEV","Received CLOSE")
                return WSMessage(WSMsgType.CLOSED, None, extra=str(frame.payload_data))
            
            # 如果是 ping 帧
            if frame.opcode == 0x9:  # Ping 的操作码
                logger.log("PING","Received")
                await self._send_pong(frame.payload_data)
                return WSMessage(WSMsgType.PING, None, None)

            # 如果是 pong 帧，不需要处理
            if frame.opcode == 0xA:  # Pong 的操作码
                logger.log("PONG","Received")
                self._pong_wait_event.set()
                return WSMessage(WSMsgType.PONG, None, None)
            
            # 如果不是文本消息
            if frame.opcode not in (0, 1, 2):  # 非文本消息
                await self._send_close_frame()
                return WSMessage(
                    WSMsgType.ERROR,
                    None,
                    extra=f"Invalid opcode {frame.opcode}",
                )

            return WSMessage(WSMsgType.TEXT, frame.payload_data.decode("utf-8"), None)


        except Exception as e:
            try:
                await self._send_close_frame()
            except:
                pass
            
            return WSMessage(
                WSMsgType.ERROR, None, extra=e.__class__.__name__ + ": " + str(e)
            )


    async def _send_pong(self,data: bytes = b'') -> None:
        """发送 pong 帧"""
        await self.send_msg(data,opcode=0xA)
        logger.log("PONG","Sent")
        
    async def _send_ping(self,data: bytes = b'') -> None:
        """发送 ping 帧"""
        await self.send_msg(data,opcode=0x9)
        logger.log("PING","Sent")

    async def _send_close_frame(self, code: int = 1000) -> None:
        """发送关闭帧"""

        if self.closed:  # 判断是否已经关闭
            return
        # 发送关闭帧
        await self.send_msg(struct.pack('!H', code),opcode=0x8)
        logger.log("DEV","Sent CLOSE")
        self._writer.close()  # 关闭连接


    async def send_json(self, data: dict) -> None:
        """编码并发送 JSON 数据给客户端"""
        json_data = json.dumps(data)
        await self.send_msg(json_data)


    async def send_msg(self, data: str | bytes, opcode: Optional[int] = None) -> None:
        """编码并发送消息给客户端
        - data: 要发送的消息，可以是字符串或二进制数据
        """        
        msg = self.encode_message(data,opcode=opcode)
        self._writer.write(msg)
        await self._writer.drain()


    def parse_headers_sync(self, request: str) -> dict:
        """同步解析 HTTP 请求头并返回字典"""
        return self._parse_header_lines(request.split("\r\n"))

    def _parse_header_lines(self, lines: list) -> dict:
        headers = {}
        for line in lines:
            if ": " in line:
                key, value = line.split(": ", 1)
                headers[key] = value.strip()
        return headers




    def encode_message(self, message: str | bytes,opcode: Optional[int]=None) -> bytearray:
        """编码要发送的消息"""
        _opcode = opcode if opcode is not None else 1 if isinstance(message, str) else 2
        byte_message = message.encode("utf-8") if isinstance(message, str) else cast(bytes, message)

        payload_length = len(byte_message)
        fin_opcode = 0x80 | _opcode  # 0x80 表示 FIN，opcode 是操作码
        frame_header = bytearray([fin_opcode])  # 使用 bytearray 以便直接拼接

        # 确定是否需要掩码以及 payload 长度
        mask_bit = 0x80 if self._use_mask else 0x00

        if payload_length <= 125:
            frame_header.append(mask_bit | payload_length)
        elif payload_length <= 65535:
            frame_header.extend(struct.pack('!BH', mask_bit | 126, payload_length))
        else:
            frame_header.extend(struct.pack('!BQ', mask_bit | 127, payload_length))

        # 如果有掩码，添加掩码和掩码后的数据
        if self._use_mask:
            masking_key = generate_mask()  # 生成掩码
            frame_header.extend(masking_key)
            frame_header.extend(apply_mask(byte_message, masking_key))
        else:
            frame_header.extend(byte_message)

        return frame_header

    

    def sanitize_message(self, message: str) -> str:
        """对消息进行 XSS 防护"""

        return html.escape(message)

    def __aiter__(self) -> "WebSocketProtocol":
        return self

    async def __anext__(self) -> WSMessage:
        msg = await self.receive()
        if msg.type in (WSMsgType.CLOSE, WSMsgType.CLOSING, WSMsgType.CLOSED):
            raise StopAsyncIteration
        return msg
