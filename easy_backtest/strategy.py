from abc import ABC, abstractmethod
from datetime import datetime
import pandas as pd

class Strategy(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def on_data(self, dt:datetime, data:pd.DataFrame):
        pass

    def execute(self, symbol:str, quantity:float):
        raise NotImplementedError('This method need be injected by BacktestEngine')

    def get_position(self, drop_empty:float = None) -> dict[str, float]:
        raise NotImplementedError('This method need be injected by BacktestEngine')