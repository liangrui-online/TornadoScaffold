"""
websocket 接口
用于实时向前端推送消息
"""
from typing import Optional, Awaitable

import tornado.websocket

from src.utils.log_tools import logger


class WsHandler(tornado.websocket.WebSocketHandler):
    connections = set()  # 用来存放连接

    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        pass

    async def open(self):
        logger.info(f"{id(self)}接入websocket连接")
        self.connections.add(self)  # 建立连接后添加用户到容器中
        await self.write_message("hello")

    async def on_message(self, message):
        logger.info(f"接收到{id(self)}发来的消息{message}")

    def on_close(self):
        self.connections.remove(self)  # 用户关闭连接后从容器中移除用户
        logger.info(f"{id(self)}断开websocket连接")

    @classmethod
    async def public_message(cls, message):
        for conn in cls.connections:
            await conn.write_message(message)

    def check_origin(self, origin):
        # 允许WebSocket的跨域请求
        return True
