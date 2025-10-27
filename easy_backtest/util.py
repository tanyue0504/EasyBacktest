import pandas as pd

class ReadOnlyWrapper:
    def __init__(self, df):
        self._df = df
    
    def _block(self, *args, **kwargs):
        raise PermissionError("Data modification not allowed in backtesting")
    
    def __getitem__(self, key):
        result = self._df[key]
        return ReadOnlyWrapper(result) if isinstance(result, pd.DataFrame) else result
    
    # 拦截所有修改方法
    __setitem__ = _block
    __delitem__ = _block
    __setattr__ = _block
    
    # 显式拦截常见方法
    def assign(self, *args, **kwargs): self._block()
    def drop(self, *args, **kwargs): self._block()
    def fillna(self, *args, **kwargs): self._block()
    def replace(self, *args, **kwargs): self._block()
    
    # 允许访问属性和方法
    def __getattr__(self, name):
        attr = getattr(self._df, name)
        if callable(attr):
            def wrapper(*args, **kwargs):
                result = attr(*args, **kwargs)
                if isinstance(result, pd.DataFrame):
                    return ReadOnlyWrapper(result)
                return result
            return wrapper
        return attr
