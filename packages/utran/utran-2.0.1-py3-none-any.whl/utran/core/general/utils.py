def list_methods_from_classes(instance, base_class):
    """## 列举出实例方法来自哪些类，按类名分组返回
    - instance: 实例对象
    - base_class: 基类,用于限定查找的范围
    ### return: 字典，键为类名，值为该类的方法名列表,`eg: {'A': ['method1','method2'], 'B': ['method3']}`
    """
    method_dict: dict[str, list[str]] = {}
    # 查找方法来源，使用集合加速查找
    instance_methods = {
        method_name
        for method_name in dir(instance)
        if callable(getattr(instance, method_name))
    }
    for cls in instance.__class__.__mro__:
        if issubclass(cls, base_class):
            cls_methods = instance_methods.intersection(cls.__dict__)
            if cls_methods:
                method_dict[cls.__name__] = list(cls_methods)
            instance_methods.difference_update(cls_methods)
    return method_dict


from typing import Dict, List, Any


class TablePrinter:
    def __init__(
        self,
        data_dict: Dict[str, Any],
        item_col: int,
        front_space: int = 1,
        back_space: int = 2,
        key_warp: str = "",
        value_warp: str = "",
        ignore_startwith_symbol: str = "_",
    ):
        self.ignore_startwith_symbol = ignore_startwith_symbol
        self.key_warp = key_warp
        self.value_warp = value_warp
        self.data_dict = data_dict
        self.item_col = item_col
        self.front_space = front_space
        self.back_space = back_space
        self.groups: List[Any] = []

    def _prepare_data(self) -> None:
        items = list(self.data_dict.items())
        col_num = self.item_col
        temp: List[Any] = []

        for item in items:
            # 将键和值合并为一个字符串
            if item[0].startswith(self.ignore_startwith_symbol):
                combined_item = f"{str(item[1])}"
            else:
                key = (
                    str(item[0])
                    if self.key_warp.__len__() <= 1
                    else self.key_warp[0] + str(item[0]) + self.key_warp[1]
                )
                value = (
                    str(item[1])
                    if self.value_warp.__len__() <= 1
                    else self.value_warp[0] + str(item[1]) + self.value_warp[1]
                )
                combined_item = f"{key}: {value}"
            temp.append(combined_item)
            # 当达到列数时，保存并重置temp
            if len(temp) == col_num:
                self.groups.append(temp)
                temp = []

        # 添加最后一组数据，并补齐空单元格
        if temp:
            temp.extend([""] * (col_num - len(temp)))  # 补齐空单元格
            self.groups.append(temp)

    def _calculate_column_sizes(self) -> List[int]:
        max_col_sizes = []
        for i in range(self.item_col):
            max_size = max(len(str(g[i])) if i < len(g) else 0 for g in self.groups)
            max_col_sizes.append(max_size)
        return max_col_sizes

    def _format_groups(self, max_col_sizes: List[int]) -> List[str]:
        formatted_rows = []

        for g in self.groups:
            row = "|".join(
                f"{' ' * self.front_space}{str(x).ljust(max_col_sizes[i])}{' ' * self.back_space}"
                for i, x in enumerate(g)
            )
            # 无论是否是空行，添加一行
            formatted_rows.append(f"|{row}|")

        return formatted_rows

    def print_table(self) -> None:
        self._prepare_data()
        max_col_sizes = self._calculate_column_sizes()
        formatted_rows = self._format_groups(max_col_sizes)
        print("\n".join(formatted_rows))

    def get_table_str(self) -> str:
        self._prepare_data()
        max_col_sizes = self._calculate_column_sizes()
        formatted_rows = self._format_groups(max_col_sizes)
        return "\n".join(formatted_rows)


def __print_header(
    version: str,
    backend: str,
    remote_actions_num: int = 0,
    local_actions_num: int = 0,
    wokeblock_num: int = 0,
    is_debug: bool = False,
    is_dev: bool = False,
):
    """## 绘制头部logo"""

    dict_data = {
            "backend server": backend,      
            "wokeblock num": wokeblock_num if wokeblock_num else "-",      
            "remote actions": remote_actions_num if remote_actions_num else "-",
            "local actions": local_actions_num if local_actions_num else "-",            
        }

    top_str = ""
    if is_debug or is_dev:
        dict_data = {"_": "", "__": "",**dict_data}
        
        if is_dev:
            top_str += " [DEV MODE] "
        if is_debug:
            top_str += " / DEBUG / "
        
        
        
    info = TablePrinter(
        dict_data,
        item_col=2,
        front_space=2,
        back_space=2,
        value_warp="()",
    ).get_table_str()
    
    str_ = f"""
    _____  __________________ _______ _____   __
    __  / / /___  __/___  __ \___    |___  | / /
    _  / / / __  /   __  /_/ /__  /| |__   |/ / 
    / /_/ /  _  /    _  _, _/ _  ___ |_  /|  /  
    \____/   /_/     /_/ |_|  /_/  |_|/_/ |_/  v{version}
    
 ==={top_str+'='*(49-len(top_str))}
{info}
 {'='*52}
    """
    return str_


# from typing import TypedDict
# from Crypto.Cipher import AES
# from Crypto.Util.Padding import pad, unpad
# import os
# import hashlib
# class _SecretKeys(TypedDict):
#     publicKey: str
#     privateKey: bytes


# def generate_key_pair()->_SecretKeys:
#     """生成密钥对"""
#     private_key = os.urandom(16)  # 128位随机私钥
#     sha256_hash = hashlib.sha256(private_key).hexdigest()
#     return {'privateKey': private_key, 'publicKey': sha256_hash}  # 返回私钥和公钥


# def encrypt(plain_text: str, key: bytes) -> bytes:
#     """使用AES加密"""
#     cipher = AES.new(key, AES.MODE_CBC)  # CBC模式
#     ct_bytes = cipher.encrypt(pad(plain_text.encode(), AES.block_size))  # 填充数据并加密
#     return bytes(cipher.iv) + ct_bytes  # 返回IV和密文


# def decrypt(ciphertext: bytes, key: bytes) -> str:
#     """使用AES解密"""
#     iv = ciphertext[:16]  # 提取IV
#     ct = ciphertext[16:]  # 提取密文
#     cipher = AES.new(key, AES.MODE_CBC, iv)  # 使用相同的IV解密
#     plain_text = unpad(cipher.decrypt(ct), AES.block_size).decode()  # 解密并去掉填充
#     return plain_text
