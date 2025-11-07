from abc import ABC, abstractmethod
from datetime import datetime
import pandas as pd

class Strategy(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def on_data(self, dt:datetime, data:pd.DataFrame):
        pass

    def execute(self, symbol:str, quantity:float, e:float = 1e-8):
        """
        建议在调用前判定quantity是否为0, 以免记录过多无效内容, 通常1e-8以内视为0
        默认值不要在这改动, 引擎会注入, 从引擎交易类改动
        """
        raise NotImplementedError('This method need be injected by BacktestEngine')

    def get_position(self, drop_empty:float = 1e-8) -> dict[str, float]:
        """
        建议读取仓位时都使用drop_empty参数, 以免返回过多无效仓位
        默认值不要在这改, 引擎会注入, 从引擎账户类改动
        """
        raise NotImplementedError('This method need be injected by BacktestEngine')
    
class NullStrategy(Strategy):
    """
    空策略, 不进行任何交易, 用于空推数据测试
    """
    def on_data(self, dt: datetime, data: pd.DataFrame):
        pass