from loguru import logger
from .dataset import Dataset
from .strategy import Strategy
from .account import Account
from .recorder import Recorder

class BacktestEngine:
    def __init__(
        self,
        dataset:Dataset,
        strategy:Strategy,
        recorder:Recorder,
        is_log:bool=True,
    ):
        self.dataset = dataset
        self.strategy = strategy
        self.recorder = recorder
        self.account = Account()
        self.is_log = is_log
        # 注入接口
        strategy.execute = self.execute
        strategy.get_position = self.account.get_position

    def execute(self, symbol:str, quantity:float, e:float = 1e-8):
        if abs(quantity) <= e:
            return
        position = self.account.execute(symbol, quantity)
        self.recorder.record(self.dt, symbol, quantity, position)
        if self.is_log:
            logger.info(f"execute {quantity} on {symbol} to {position} at {self.dt}")

    def run(self):
        with self.recorder:
            for dt, data in self.dataset:
                # 跳过空数据
                if data.empty: continue
                self.dt = dt.isoformat()
                self.strategy.on_data(dt, data)