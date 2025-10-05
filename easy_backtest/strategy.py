from abc import ABC, abstractmethod
from datetime import datetime

import pandas as pd

class Strategy(ABC):
    def __init__(self, id:str):
        super().__init__()
        self.id = id

    @abstractmethod
    def on_data(self, dt:datetime, data:pd.DataFrame):
        pass