import pandas as pd
from datetime import datetime
class Account:
    def __init__(self):
        self.trade_records:list[dict] = []
        self.position_dict:dict[str, float] = {}

    def execute(self, dt:datetime, symbol:str, quantity:float, price:float=None):
        self.trade_records.append({
            "dt": dt,
            "symbol": symbol,
            "quantity": quantity,
            "price": price,
        })
        if symbol not in self.position_dict:
            self.position_dict[symbol] = 0.0
        self.position_dict[symbol] += quantity

    def get_position(self) -> dict[str, float]:
        return self.position_dict.copy()
    
    def get_trade_records(self) -> pd.DataFrame:
        return pd.DataFrame(self.trade_records)