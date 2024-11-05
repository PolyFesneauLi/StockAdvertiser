import pandas as pd
import numpy as np
import tushare as ts
import matplotlib.pyplot as plt
import yfinance as yf

from pylab import *  # 改变plot字体，适应中文
mpl.rcParams['font.sans-serif'] = ['Arial Unicode MS']  # 设置中文字体

class Moving_Average_Predict:
    stock_code = ''
    tsData = pd.DataFrame()

    def __init__(self, stock_code):
        self.stock_code = stock_code

    def date_setting(self, start_date, end_date):
        pro = ts.pro_api('5bdefc21c648d69a4e7132a9b2551dd661b093a025d9ff627c86c53d')
        self.tsData = pro.daily(ts_code=self.stock_code, start_date=start_date, end_date=end_date)
        print(self.tsData)

    def make_predict(self, day):  # day为窗口大小
        new_data = pd.DataFrame(index=range(0, len(self.tsData)), columns=['date', 'close'])
        for i in range(0, len(self.tsData)):  # 使用收盘价进行处理
            new_data['date'][i] = self.tsData.index[i]
            new_data['close'][i] = self.tsData["close"][len(self.tsData) - i - 1]
        new_data = new_data.sort_index(ascending=True)
        # 划定
        train = new_data[:len(self.tsData) - day]
        valid = new_data[len(self.tsData) - day:].copy()
        # 做出预测
        preds = []
        for i in range(0, day):
            a = train['close'][len(train) - day + i:].sum() + sum(preds)
            b = a / day
            preds.append(b)
        # 画图
        valid.loc[:, 'Predictions'] = preds
        plt.plot(train['close'], label=u'训练集')
        plt.plot(valid['Predictions'], label=u'预测值')
        plt.plot(valid['close'], label=u'真实值')

        # 添加图例并显示
        plt.legend(loc='best')  # 'best' 自动选择最佳位置
        plt.grid()
        plt.show()


if __name__ == '__main__':
    a = Moving_Average_Predict('000001.SZ')
    a.date_setting(start_date='20190512', end_date='20191219')
    a.make_predict(30)
