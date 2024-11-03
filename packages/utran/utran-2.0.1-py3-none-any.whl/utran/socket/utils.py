import asyncio
import base64
import binascii
from enum import Enum, IntEnum
from functools import partial
from urllib.parse import urlparse, urlunparse, parse_qs, urlencode
import xml.etree.ElementTree as ET

# 使用 HTML 转义或其他安全措施来防止 XSS 攻击
import html
import hashlib
import json
from multidict import CIMultiDict, istr
from typing import (
    Any,
    Callable,
    Dict,
    Final,
    Iterable,
    List,
    Literal,
    NamedTuple,
    Optional,
    Tuple,
    Protocol,
    Union,
    cast,
    overload,
)


class URLHandler:
    """### URL 处理器"""

    def __init__(self, url: str):
        self.url = url
        self.parsed_url = urlparse(url)

    def get_scheme(self) -> str:
        """获取 URL 的协议 (scheme)"""
        return self.parsed_url.scheme

    def get_netloc(self) -> str:
        """获取 URL 的网络位置 (netloc)"""
        return self.parsed_url.netloc

    def get_path(self) -> str:
        """获取 URL 的路径 (path)"""
        return self.parsed_url.path

    def get_query_params(self) -> dict:
        """获取 URL 的查询参数 (query parameters)"""
        return parse_qs(self.parsed_url.query)

    def set_query_param(self, key: str, value: str) -> None:
        """设置 URL 的查询参数"""
        query_params = self.get_query_params()
        query_params[key] = value
        self._update_query_params(query_params)

    def _update_query_params(self, query_params: dict) -> None:
        """更新 URL 的查询参数"""
        new_query = urlencode(query_params, doseq=True)
        self.url = urlunparse(
            (
                self.parsed_url.scheme,
                self.parsed_url.netloc,
                self.parsed_url.path,
                self.parsed_url.params,
                new_query,
                self.parsed_url.fragment,
            )
        )
        self.parsed_url = urlparse(self.url)

    def get_full_url(self) -> str:
        """获取完整的 URL"""
        return self.url

