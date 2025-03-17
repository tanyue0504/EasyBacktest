import pandas as pd

class Dataset:
    """
    在传入数据时, 按时间排序并分组保存
    通过__iter__方法结合yield将数据逐个时间点返回
    这样能降低内存占用
    注意这样的设计要求所有数据都合并到一个df中
    """
    def __init__(self, time_col:str, data:pd.DataFrame):
        self.time_col = time_col
        self.grouped_data = data.sort_values(time_col).groupby(time_col)

    def __iter__(self):
        for dt, data in self.grouped_data:
            yield dt, data.copy()