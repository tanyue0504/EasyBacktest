import sys, os
# 添加父文件夹到 sys.path, 策略回测文件夹可以不放在框架下, 但需要按此方法添加框架路径
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from datetime import datetime

import pandas as pd

from src import *

class DemoStrategy(Strategy):
    def __init__(self, id: str):
        super().__init__(id)
        self.flag = True

    def on_data(self, dt: datetime, data: pd.DataFrame):
        if self.flag:
            self.execute('haha', 1)
            self.flag = False
        print(f"Strategy {self.id} received data at {dt}:\n{data}")

if __name__ == '__main__':
    # 创建一个简单的数据集
    data = pd.DataFrame({
        'time': [0, 1, 2, 3],
        'price': [10, 11, 12, 13],
        'volume': [100, 110, 120, 130]
    })

    # 创建数据集实例
    data_set = DataSet(data)

    # 创建回测引擎实例
    bacttest_engine = BacktestEngine(data_set)

    # 创建策略实例
    demo_strategy = DemoStrategy('demo_strategy')

    # 将策略添加到回测引擎
    bacttest_engine.add_strategy(demo_strategy)

    # 运行回测
    result = BacktestEngine.backtest(bacttest_engine)

    # 打印回测结果
    print(result)