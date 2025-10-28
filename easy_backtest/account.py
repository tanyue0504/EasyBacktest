class Account:
    def __init__(self):
        self.position_dict = {}
    
    def execute(self, symbol: str, quantity: float) -> float:
        self.position_dict[symbol] = self.position_dict.get(symbol, 0.0) + quantity
        return self.position_dict[symbol]

    def get_position(self, drop_empty:float = None) -> dict[str, float]:
        if drop_empty:
            return {k:v for k,v in self.position_dict.items() if abs(v) > drop_empty}
        return self.position_dict.copy()