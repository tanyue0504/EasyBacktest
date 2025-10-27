import functools
from loguru import logger
from datetime import datetime

from .strategy import Strategy
from .dataset import Dataset
from .account import Account
from .util import ReadOnlyWrapper
    
class BacktestEngine:
    def __init__(
        self,
        dataset:Dataset,
        result_path:str,
        buffer_size:int=10**5,
        data_protect_mode:str='copy'
    ):
        self.account_dict:dict[str, Account] = {} # 账户字典
        self.strategy_dict:dict[str, Strategy] = {} # 策略字典
        self.dataset = dataset # 数据集
        self.dt:datetime = None # 回测进行到的时点
        self.result_path = result_path
        self.buffer_size = buffer_size
        self.data_protect_mode = data_protect_mode

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
        version_tracker = {}
        buffer = []
        buffer_count = 0

        with open(self.result_path, 'w', encoding='utf-8-sig') as f:
            f.write("dt,strategy_id,symbol,quantity\n")

            for dt, data in self.dataset:
                self.dt = dt
                for strategy in self.strategy_dict.values():
                    # 数据推送
                    try:
                        if self.data_protect_mode == 'copy':
                            strategy.on_data(dt, data.copy())
                        elif self.data_protect_mode == 'wrapper':
                            strategy.on_data(dt, ReadOnlyWrapper(data))
                        else:
                            strategy.on_data(dt, data)
                    except Exception as e:
                        logger.error(f"error occured in strategy {strategy.id} at {dt}: {e}")
                    
                    # 记录持仓
                    account = self.account_dict[strategy.id]
                    if version_tracker.get(strategy.id, 0) == account.position_version:
                        continue
                    version_tracker[strategy.id] = account.position_version
                    for symbol, quantity in account.get_position().items():
                        buffer.append(",".join([
                            int(dt.timestamp()),
                            strategy.id,
                            symbol,
                            f"{quantity:.{account.epsilon}f}"
                        ]) + '\n')
                    buffer_count += len(account.position_dict)
                    if buffer_count >= self.buffer_size:
                        f.writelines(buffer)
                        buffer.clear()
                        buffer_count = 0
            if buffer:
                f.writelines(buffer)