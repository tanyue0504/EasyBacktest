from pathlib import Path
from datetime import datetime
from typing import Union

class Recorder:
    def __init__(self, path: Union[str, Path], buffer_size: int = 10**5):
        """
        缓冲记录器
        
        Args:
            path: 文件保存路径
            buffer_size: 缓冲区大小，达到此数量时自动写入文件
        """
        self.path = Path(path) if isinstance(path, str) else path
        self.buffer_size = buffer_size
        self.buffer = []
        self.file = None
        
    def __enter__(self):
        """打开文件并返回记录器实例"""
        self.file = open(self.path, mode='w', encoding='utf-8-sig')
        self.buffer.clear()
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        """确保关闭文件前刷新缓冲区"""
        try:
            if self.buffer:
                self._flush_buffer()
        finally:
            if self.file and not self.file.closed:
                self.file.close()
            
        if exc_type is not None:
            print(f"记录器异常: {exc_val}")
        return True

    def _flush_buffer(self):
        """将缓冲区内容写入文件"""
        if self.file and self.buffer:
            try:
                self.file.writelines(self.buffer)
                self.file.flush()  # 确保数据写入磁盘
            except Exception as e:
                # 写入失败时保留缓冲区数据
                print(f"写入文件失败: {e}")
                raise e
            else:
                self.buffer.clear()

    def record(self, dt: datetime, symbol: str, quantity: float, position: float):
        """
        记录一条数据
        
        Args:
            dt: 时间戳, 精确到秒
            symbol: 符号/标识
            quantity: 交易量，正负号表示方向
            position: 交易后的持仓量
        """
        self.buffer.append(",".join([
            str(int(dt.timestamp())),
            symbol,
            str(quantity),
            str(position),
        ]) + '\n')
        
        if len(self.buffer) >= self.buffer_size:
            self._flush_buffer()

    def flush(self):
        """手动刷新缓冲区"""
        self._flush_buffer()

    