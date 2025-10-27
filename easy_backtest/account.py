from datetime import datetime
    
class Account:
    def __init__(self, epsilon=8):
        self.position_dict = {}
        self.position_version = 0
        self.epsilon = epsilon
        self.e = 10**(-epsilon)
    
    def execute(self, dt: datetime, symbol: str, quantity: float):
        if abs(quantity) < self.e:
            return
        self.position_version += 1
        self.position_dict[symbol] = self.position_dict.get(symbol, 0.0) + quantity

    def get_position(self, drop_empty: bool = False) -> dict[str, float]:
        if drop_empty:
            return {k: v for k, v in self.position_dict.items() if abs(v) >= self.e}
        return self.position_dict.copy()