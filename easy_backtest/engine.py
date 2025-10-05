import functools
from loguru import logger
from datetime import datetime
import pandas as pd

from .strategy import Strategy
from .dataset import Dataset
from .account import Account

class BacktestEngine:
    def __init__(self, dataset:Dataset):
        self.account_dict:dict[str, Account] = {} # 账户字典
        self.strategy_dict:dict[str, Strategy] = {} # 策略字典
        self.dataset = dataset # 数据集
        self.dt:datetime = None # 回测时点
        self.position_list = []

    def execute(self, symbol:str, quantity:float, price:float=None, strategy_id:str=None):
        account = self.account_dict[strategy_id]
        account.execute(self.dt, symbol, quantity, price)

    def add_strategy(self, strategy:Strategy):
        # 添加策略, 并注入交易接口
        if strategy.id in self.strategy_dict:
            raise ValueError(f"Strategy {strategy.id} already exists")
        logger.info(f"Add strategy {strategy.id}")
        self.strategy_dict[strategy.id] = strategy
        account = self.account_dict[strategy.id] = Account()
        # 注入交易API
        strategy.execute = functools.partial(self.execute, strategy_id=strategy.id)
        strategy.get_position = account.get_position

    def run(self):
        for dt, data in self.dataset:
            self.dt = dt
            for strategy in self.strategy_dict.values():
                strategy.on_data(dt, data)
                position_dict = self.account_dict[strategy.id].get_position()
                df = pd.DataFrame({
                    'symbol': position_dict.keys(),
                    'quantity': position_dict.values()
                })
                df['strategy_id'] = strategy.id
                df['dt'] = self.dt
                self.position_list.append(df)

    def get_result(self):
        return pd.concat(self.position_list, ignore_index=True)