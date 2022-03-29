# -*- coding: utf-8 -*-
"""hw1_Prophet.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ex6nPtCxnWtiIcKYDRalkp7ivpF9hkws
"""

# pip freeze > '/content/drive/MyDrive/Colab Notebooks/data_mining/hw1/requirements.txt'

# Commented out IPython magic to ensure Python compatibility.
# basic
import numpy as np
import pandas as pd
# get data
import pandas_datareader as pdr
# visual
import matplotlib.pyplot as plt
# %matplotlib inline
#time
import datetime as datetime
#Prophet
from fbprophet import Prophet

from sklearn import metrics
from matplotlib import pyplot

# Load your cloud drive
# from google.colab import drive
# drive.mount('/content/drive')

#讀取近三年每日轉備容量(2019-2021)
data = pd.read_csv('/content/drive/MyDrive/Colab Notebooks/data_mining/hw1/近三年每日尖峰備轉容量率.csv')
data['日期'] = pd.to_datetime(data['日期'], format = "%Y/%m/%d")1
data.rename(columns = {'日期': 'ds', '備轉容量(MW)': 'y', '備轉容量率(%)': 'transferCapacity'}, inplace = True)
#data.set_index(['Adj Close'], inplace = True)
data.iloc[:,1] = data.iloc[:,1] * 10
data = data[['ds', 'y']]
data.head()

#讀取2022年轉備容量
data2 = pd.read_csv('/content/drive/MyDrive/Colab Notebooks/data_mining/hw1/本年度每日尖峰備轉容量率.csv')
data2['日期'] = pd.to_datetime(data2['日期'], format = "%Y/%m/%d")
data2.rename(columns = {'日期': 'ds', '備轉容量(萬瓩)': 'y', '備轉容量率(%)': 'transferCapacity'}, inplace = True)
#data2.set_index(['Adj Close'], inplace = True)
data2.iloc[:,1] = data2.iloc[:,1] * 10
data2 = data2[['ds', 'y']]
data2.tail()

#合併2019-2022轉備容量
data3 = data.copy()
for i in range(len(data2)):
   data3=data3.append({'ds' : data2.loc[i, "ds"], 'y' : data2.loc[i, "y"]}, ignore_index=True)

#2019-2022 只取1-4月
data4 = data[:120].copy()
for i in range(365, 486):
   data4 = data4.append({'ds' : data.loc[i, "ds"], 'y' : data.loc[i, "y"]}, ignore_index=True)
for i in range(731, 851):
   data4 = data4.append({'ds' : data.loc[i, "ds"], 'y' : data.loc[i, "y"]}, ignore_index=True)
for i in range(len(data2)):
   data4 = data4.append({'ds' : data2.loc[i, "ds"], 'y' : data2.loc[i, "y"]}, ignore_index=True)

#觀察轉備容量分布
# plt.style.use('ggplot')
# data['y'].plot(figsize=(12, 8))

# data['y'] = np.log(data['y'])
# 定義模型
model = Prophet()

# 訓練模型
model.fit(data4)

# 建構預測集
future = model.make_future_dataframe(periods=16) #forecasting for 1 year from now.

# 進行預測
forecast = model.predict(future)

figure=model.plot(forecast)

# summarize the forecast
print(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail())

#測試最後14天的RMSE
y_pred = forecast['yhat'][-30:-16]
y_true = data4['y'][-14:]
print(y_pred, y_true)
day_pred = forecast['ds'][-30:-16]
day_ture = data4['ds'][-14:]
print(day_pred, day_ture)

#RMSE計算
from math import sqrt
print ("MSE:",metrics.mean_squared_error(y_pred, y_true))
print ("RMSE:",sqrt(metrics.mean_squared_error(y_pred, y_true)))

day_pred = forecast['ds'][-91:-76]
#day_pred
y_pred = forecast['yhat'][-91:-76]
#y_pred

#輸出預測天數的轉備容量及日期
from datetime import datetime
answer = forecast[-15:]
answer = answer[['ds','yhat']]
answer.rename(columns = {'ds': 'date', 'yhat': 'operating_reserve(MW)'}, inplace = True)
answer.set_index('date')
for i in range(len(answer)):
  answer.iloc[i,0] = answer.iloc[i,0].strftime('%Y%m%d')
answer.to_csv('/content/drive/MyDrive/Colab Notebooks/data_mining/hw1/submission.csv',index=False)
#answer