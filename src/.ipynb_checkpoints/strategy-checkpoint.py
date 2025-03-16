from abc import ABC, abstractmethod
from datetime import datetime

import pandas as pd

class Strategy(ABC):
    def __init__(self, id:str):
        super().__init__()
        self.id = id

    @abstractmethod
    def on_data(self, dt:datetime, data:pd.DataFrame):
        """
        Called when new data is available
        """

    def execute(self, symbol:str, quantity:float):
        """
        Execute a trade
        Engine will inject this method into the strategy instance
        """
        raise NotImplementedError
    
    def get_position(self):
        """
        Get the current position of this strategy
        Engine will inject this method into the strategy instance
        """
        raise NotImplementedError