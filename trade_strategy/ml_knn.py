import pandas as pd
import tushare as ts
import matplotlib.pyplot as plt
from sklearn import neighbors
from sklearn.model_selection import GridSearchCV
from sklearn.preprocessing import MinMaxScaler

scaler = MinMaxScaler(feature_range=(0, 1))

from pylab import *  # 改变plot字体，适应中文

mpl.rcParams['font.sans-serif'] = ['Arial Unicode MS']  # 设置中文字体


class kNN_pridict:
    stock_code = ''
    tsData = pd.DataFrame()

    def __init__(self, stock_code):
        self.stock_code = stock_code

    def date_setting(self, start_date, end_date):
        pro = ts.pro_api('5bdefc21c648d69a4e7132a9b2551dd661b093a025d9ff627c86c53d')
        self.tsData = pro.daily(ts_code=self.stock_code, start_date=start_date, end_date=end_date)
        # self.tsData = self.tsData.reset_index()

    def makePrediction(self, node):
        if len(self.tsData) < node:
            print(f"Not enough data to create training set. Available data: {len(self.tsData)}, Required: {node}")
            return

        new_data = pd.DataFrame(index=range(0, len(self.tsData)), columns=['Date', 'Close'])
        for i in range(0, len(self.tsData)):
            new_data.loc[i, 'Date'] = self.tsData['trade_date'][i]
            new_data.loc[i, 'Close'] = self.tsData['close'][i]
        new_data['Date'] = pd.to_datetime(new_data.Date, format='%Y%m%d')
        new_data.index = new_data['Date']

        # Prepare data
        new_data = new_data.sort_index(ascending=True)
        train = new_data[:node]
        valid = new_data[node:]

        if train.empty or valid.empty:
            print("Training or validation data is empty.")
            return

        x_train = train.drop('Close', axis=1)
        y_train = train['Close']
        x_valid = valid.drop('Close', axis=1)
        y_valid = valid['Close']

        # Scale data
        x_train_scaled = scaler.fit_transform(x_train)
        x_train = pd.DataFrame(x_train_scaled)
        x_valid_scaled = scaler.transform(x_valid)  # Use transform instead of fit_transform
        x_valid = pd.DataFrame(x_valid_scaled)

        # Use grid search to find best parameters
        params = {'n_neighbors': [2, 3, 4, 5, 6, 7, 8, 9]}
        knn = neighbors.KNeighborsRegressor()
        model = GridSearchCV(knn, params, cv=5)

        # Fit model and predict
        model.fit(x_train, y_train)
        preds = model.predict(x_valid)

        # Plot results
        valid['Predictions'] = preds
        plt.plot(valid[['Close', 'Predictions']])
        plt.plot(train['Close'])
        plt.title(f'Predictions for {self.stock_code}')
        plt.xlabel('Date')
        plt.ylabel('Close Price')
        plt.grid()
        plt.legend(['真实值', '预测值'], loc='best')
        plt.show()


a = kNN_pridict('000001.SZ')
a.date_setting(start_date='20190512', end_date='20191219')
a.makePrediction(140)
