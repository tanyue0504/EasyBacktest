from pathlib import Path
from datetime import datetime
from typing import Union

class Recorder:
    def __init__(self, path: Union[str, Path]):
        """
        缓冲记录器
        
        Args:
            path: 文件保存路径
        """
        self.path = Path(path) if isinstance(path, str) else path
        self.file = None
        
    def __enter__(self):
        """打开文件并返回记录器实例"""
        self.file = open(self.path, mode='w', encoding='utf-8-sig')
        self.file.write("dt,symbol,trade,position\n")  # 写入表头
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        """确保关闭文件前刷新缓冲区"""
        if self.file and not self.file.closed:
            self.file.flush()
            self.file.close()
            
        if exc_type is not None:
            print(f"记录器异常: {exc_val}")
        # 无论如何返回False，否则调试很麻烦
        return False

    def record(self, dt: str, symbol: str, quantity: float, position: float):
        """
        记录一条数据
        
        Args:
            dt: 时间戳, 精确到秒
            symbol: 符号/标识
            quantity: 交易量，正负号表示方向
            position: 交易后的持仓量
        """
        self.file.write(f"{dt},{symbol},{str(quantity)},{str(position)}\n")