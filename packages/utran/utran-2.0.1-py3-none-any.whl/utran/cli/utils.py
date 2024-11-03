import os
import sys
import traceback
import types
from typing import cast
import click
import importlib
import utran
from utran.log import logger

class ModuleImporter:
    """上下文管理器，用于动态导入用户模块并在退出时清理 sys.path"""

    def __init__(self, entry):
        self.entry = entry
        self.original_sys_path = sys.path.copy()  # 备份原始 sys.path

    def __enter__(self):
        # 确保文件存在并是 .py 文件
        if not os.path.isfile(self.entry) or not self.entry.endswith(".py"):
            raise FileNotFoundError(f"Entry file not found: {self.entry}")

        # 添加文件目录到 sys.path
        directory = os.path.dirname(self.entry)
        sys.path.insert(0, directory)

        # 得到模块名称并动态导入
        module_name = os.path.basename(self.entry)[:-3]  # 去掉 .py 后缀
        try:
            self.imported_module = importlib.import_module(module_name)
            return self.imported_module
        except Exception as e:
            # 输出详细的错误信息，包括调用栈
            click.secho("An error occurred during module import:", err=True, fg="red")
            traceback.print_exc()  # 打印调用栈到标准错误流
            raise ImportError(f"Error importing module: {e}") from e

    def __exit__(self, exc_type, exc_value, tb):
        # 捕获异常并打印错误信息
        if exc_type is not None:
            traceback.print_exception(exc_type, exc_value, tb)
            click.secho(f"Error executing command: {exc_value}", err=True, fg="red")

        # 还原 sys.path
        sys.path = self.original_sys_path


def get_local_utran(entry: str):
    """### 从用户模块中获取utran模块"""
    with ModuleImporter(entry) as imported_user_module:
        for _, v in imported_user_module.__dict__.items():
            # 检查用户导入的模块中是否包含 utran模块
            if isinstance(v, types.ModuleType) and v.__name__ == "utran":
                return cast(utran,v)

    click.secho("The user module does not import utran module.", err=True, fg="red")
