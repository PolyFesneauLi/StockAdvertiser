import pandas as pd
import numpy as np
import tushare as ts
import matplotlib.pyplot as plt
from pylab import mpl

# 改变plot字体，适应中文
mpl.rcParams['font.sans-serif'] = ['Arial Unicode MS']


class Moving_Average_Predict:
    stock_code = ''
    tsData = pd.DataFrame()

    def __init__(self, stock_code):
        self.stock_code = stock_code

    def date_setting(self, start_date, end_date):
        pro = ts.pro_api('5bdefc21c648d69a4e7132a9b2551dd661b093a025d9ff627c86c53d')
        self.tsData = pro.daily(ts_code=self.stock_code, start_date=start_date, end_date=end_date)
        self.tsData = self.tsData.iloc[::-1].reset_index()  # 反转顺序并重置索引
        print(self.tsData)

    def make_predict(self, day, initial_capital=100000, order_size=100):  # 设定初始资金和每次买入的仓位
        self.tsData['MA'] = self.tsData['close'].rolling(window=day).mean()
        self.tsData['STD'] = self.tsData['close'].rolling(window=day).std()
        self.tsData['Upper'] = self.tsData['MA'] + (2 * self.tsData['STD'])
        self.tsData['Lower'] = self.tsData['MA'] - (2 * self.tsData['STD'])

        # 布林带买卖信号
        self.tsData['Buy_Signal'] = np.where(self.tsData['close'] < self.tsData['Lower'], self.tsData['close'], np.nan)
        self.tsData['Sell_Signal'] = np.where(self.tsData['close'] > self.tsData['Upper'], self.tsData['close'], np.nan)

        # 初始化仓位和现金
        cash = initial_capital
        position = 0
        total_value = []

        # 遍历数据以执行买卖
        for i in range(len(self.tsData)):
            # 买入信号
            if not np.isnan(self.tsData['Buy_Signal'][i]) and cash > self.tsData['Buy_Signal'][i] * order_size:
                # 买入并更新现金和持仓
                cash -= self.tsData['Buy_Signal'][i] * order_size
                position += order_size
                print(f"买入: {order_size} 股, 当前现金: {cash:.2f}")

            # 卖出信号
            elif not np.isnan(self.tsData['Sell_Signal'][i]) and position >= order_size:
                # 卖出并更新现金和持仓
                cash += self.tsData['Sell_Signal'][i] * order_size
                position -= order_size
                print(f"卖出: {order_size} 股, 当前现金: {cash:.2f}")

            # 计算当前总资产
            total_value.append(cash + position * self.tsData['close'][i])


        # 最后计算收益率和收益金额
        final_value = total_value[-1]  # 最后的总资产
        total_return = (final_value - initial_capital) / initial_capital * 100  # 收益率
        print(f"初始资金: {initial_capital:.2f}, 最终资产: {final_value:.2f}, 收益率: {total_return:.2f}%")

        # 画图
        plt.figure(figsize=(14, 7))
        plt.plot(self.tsData['close'], label='收盘价', color='blue')
        plt.plot(self.tsData['MA'], label='MA', color='orange')
        plt.plot(self.tsData['Upper'], label='上轨', color='green', linestyle='--')
        plt.plot(self.tsData['Lower'], label='下轨', color='red', linestyle='--')

        # 标出买卖信号
        plt.scatter(self.tsData.index, self.tsData['Buy_Signal'], label='买入信号', marker='^', color='green')
        plt.scatter(self.tsData.index, self.tsData['Sell_Signal'], label='卖出信号', marker='v', color='red')

        # 添加图例并显示
        plt.title(f'{self.stock_code} 布林带策略')
        plt.xlabel('日期')
        plt.ylabel('价格')
        plt.legend(loc='best')
        plt.grid()
        plt.show()


if __name__ == '__main__':
    a = Moving_Average_Predict('000004.SZ')
    a.date_setting(start_date='20220501', end_date='20240501')
    a.make_predict(30)  # 使用20日布林带