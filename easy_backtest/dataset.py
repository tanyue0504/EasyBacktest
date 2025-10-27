from abc import ABC, abstractmethod

class Dataset(ABC):
    """
    数据集抽象基类
    __iter__ 方法应返回 (datetime.datetime, pd.DataFrame) 元组
    表示在某个时刻的全部数据，包括行情、因子和衍生变量等
    """
    
    @abstractmethod
    def __iter__(self):
        pass