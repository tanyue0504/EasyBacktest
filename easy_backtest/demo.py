"""
数据预处理(不含在本框架内)
1. 读取历史行情和因子数据, 计算衍生变量, 方便dataset构建
2. 该步骤请用jupyter或其他方法自行完成, 本框架仅提供极简回测功能

回测演示
1. 创建数据集，继承自 Dataset, 重写 __iter__ 方法, 建议流式读取, 并推送dt和data
2. 创建策略，继承自 Strategy, 重写on_data 方法, self.execute和self.get_position用于下单和获取仓位
3. 创建Recorder实例, 指定回测结果保存位置
4. 创建BacktestEngine实例, 传入dataset, strategy, recorder
5. 调用engine.run()运行回测

tips:
1. 本回测框架仅支持单策略单进程回测, 如需并行回测请自行多进程启动engine实例
2. 本框架不检测是否能够撮合, 请在策略中自行保证
3. 本框架不提供交易成本计算, 请在后续分析阶段自行处理

回测结果分析(不含在本框架内)
1. 读取Recorder保存的交易记录文件
2. 计算盘口滑点, 手续费等交易成本
3. 计算pnl曲线
4. 计算保证金占用曲线
5. 计算净值曲线
6. 计算各类绩效指标
"""

from .dataset import Dataset
from .strategy import Strategy
from .recorder import Recorder
from .engine import BacktestEngine
from datetime import datetime

class MyDataset(Dataset):
    def __iter__(self):
        # 示例数据流式读取
        for i in range(10):
            dt = f'2024-01-{i+1:02d}'
            data = ...  # 读取或生成当天的DataFrame数据
            yield dt, data

class MyStrategy(Strategy):
    def on_data(self, dt, data):
        # 示例策略逻辑
        if self.get_position():
            return
        else:
            self.execute('AAPL', 10)  # 买入10股AAPL一直持有
if __name__ == "__main__":
    recorder = Recorder(f'result_{int(datetime.now().timestamp())}.csv')
    dataset = MyDataset()
    strategy = MyStrategy()
    engine = BacktestEngine(dataset, strategy, recorder)
    # 模拟多进程启动，如果单进程可以直接调用 engine.run()
    from multiprocessing import Pool
    with Pool(1) as pool:
        async_result = pool.apply_async(engine.run)
    