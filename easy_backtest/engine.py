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
    ):
        self.dataset = dataset
        self.strategy = strategy
        self.recorder = recorder
        self.account = Account()
        # 注入接口
        strategy.execute = self.execute
        strategy.get_position = self.account.get_position

    def execute(self, symbol:str, quantity:float):
        position = self.account.execute(symbol, quantity)
        self.recorder.record(self.dt, symbol, quantity, position)

    def run(self):
        with self.recorder:
            for dt, data in self.dataset:
                self.dt = dt.isoformat()
                self.strategy.on_data(dt, data)