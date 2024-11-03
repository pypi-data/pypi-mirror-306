import asyncio
import base64
import hashlib
from typing import Optional

from .base import WebSocketProtocol, WS_KEY, WSMsgType
from utran.log import logger

class WebSocketClient(WebSocketProtocol):

    _use_mask = True
    def __init__(self):
        super().__init__(headers={})    
        
    async def connect(self, uri: str):
        # 解析 URI
        if not uri.startswith("ws://"):
            raise ValueError("Invalid WebSocket URI")

        (host, port) = uri[5:].split("/")[0].split(":")
        path = "/" + "/".join(uri[5:].split("/")[1:])

        # 创建 TCP 连接
        (self._reader, self._writer) = await asyncio.open_connection(host, port)

        # 生成 WebSocket Key
        ws_key = base64.b64encode(b"1234567890123456").decode("utf-8")

        # 创建并发送握手请求
        handshake_request = (
            f"GET {path} HTTP/1.1\r\n"
            f"Host: {host}:{port}\r\n"
            f"Upgrade: websocket\r\n"
            f"Connection: Upgrade\r\n"
            f"Sec-WebSocket-Key: {ws_key}\r\n"
            f"Sec-WebSocket-Version: 13\r\n"
            "\r\n"
        )
        self._writer.write(handshake_request.encode())
        await self._writer.drain()

        # 读取握手响应
        response = await self._reader.readuntil(b"\r\n\r\n")

        # 验证握手
        lines = response.decode().splitlines()
        
        is_valid_handshake = False
        for line in lines:
            if "Sec-WebSocket-Accept:" in line:
                accept_key = line.split(": ")[1].strip()
                expected_key = base64.b64encode(
                    hashlib.sha1((ws_key + WS_KEY.decode()).encode()).digest()
                ).decode()
                if accept_key == expected_key:
                    is_valid_handshake = True
                    self._headers['Sec-WebSocket-Accept'] = accept_key
                    break


        if not is_valid_handshake:
            raise ValueError("Invalid WebSocket handshake")
        




            



if __name__ == "__main__":

    async def main():
        uri = "ws://localhost:2525/utran"  # 修改为你的服务器地址和端口
        client = WebSocketClient()

        await client.connect(uri)

        await client.send_msg("Hello, WebSocket!")
        async for msg in client:  # 循环读取消息
            if msg.type == WSMsgType.text:
                print(f"Received: {msg}")

    asyncio.run(main())
