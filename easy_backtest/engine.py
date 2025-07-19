import functools
from loguru import logger

import pandas as pd

from .strategy import Strategy
from .dataset import Dataset
from .trade_api import TraderMatcher

class BacktestEngine:
    """
    回测引擎类
    1. 初始化时传入数据集
    2. 添加策略
    3. 调用backtest方法, 直接运行回测并返回结果
    """
    def __init__(self, dataset:Dataset):
        self.flag:bool = False # 是否开始回测标志
        self.trader_api:TraderMatcher = TraderMatcher() # 交易接口
        self.strategy_dict:dict[str, Strategy] = {} # 策略字典
        self.dataset = dataset # 数据集

    def add_strategy(self, strategy:Strategy):
        # 添加策略, 并注入交易接口
        logger.info(f"Add strategy {strategy.id}")
        if strategy.id in self.strategy_dict:
            raise ValueError(f"Strategy {strategy.id} already exists")
        self.strategy_dict[strategy.id] = strategy
        strategy.execute = functools.partial(self.trader_api.execute, strategy.id)
        strategy.get_position = functools.partial(self.trader_api.get_position, strategy.id)

    def run(self):
        self.flag = True
        for dt, data in self.dataset:
            with self.trader_api.on_data(dt, data):
                for strategy in self.strategy_dict.values():
                    strategy.on_data(dt, data)

    @staticmethod
    def backtest(engine:"BacktestEngine") -> pd.DataFrame:
        engine.run()
        return engine.trader_api.recorder.get_record()
        