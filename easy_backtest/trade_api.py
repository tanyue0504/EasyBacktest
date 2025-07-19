import pandas as pd
from datetime import datetime
from loguru import logger

class PositionRecorder:
    def __init__(self):
        self.record_list:list[pd.DataFrame] = []

    def record(
        self,
        record_datetime:datetime,
        strategy_id:str,
        position_dict:dict[str, float]
    ):
        # logger.trace(f"Record {strategy_id} position at {record_datetime}: {position_dict}")
        df = pd.DataFrame(position_dict.items(), columns=["symbol", "quantity"])
        df["datetime"] = record_datetime
        df["strategy"] = strategy_id
        self.record_list.append(df)

    def get_record(self):
        if self.record_list:
            return pd.concat(self.record_list)
        return pd.DataFrame()

class TraderMatcher:
    def __init__(self, recorder:PositionRecorder = None):
        self.recorder = recorder if recorder else PositionRecorder()
        self.position_dict:dict[str, dict[str, float]] = {}
        self.dt = None
        self.data = None

    def on_data(
        self,
        dt:datetime,
        data:pd.DataFrame
    ):
        # 更新时间和数据, 以便撮合时使用
        logger.info(f"Receive data at {dt}")
        self.dt = dt
        self.data = data
        return self

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.record()
        return False

    def record(self):
        # 生成仓位记录
        for strategy_id, position_dict in self.position_dict.items():
            self.recorder.record(self.dt, strategy_id, position_dict)

    def execute(
        self,
        strategy_id:str,
        symbol:str,
        quantity:float
    ):
        # 如果需要撮合, 在这里实现
        if quantity == 0:
            return
        logger.trace(f"Execute trade: {strategy_id} {symbol} {quantity}")
        position = self.get_position(strategy_id)
        position[symbol] = position.get(symbol, 0) + quantity
        if abs(position[symbol]) < 1e-6: # 清理0仓位
            del position[symbol]
        self.position_dict[strategy_id] = position

    def get_position(self, strategy_id:str):
        return self.position_dict.get(strategy_id, {}).copy()