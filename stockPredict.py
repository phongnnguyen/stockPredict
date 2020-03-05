# -*- coding: utf-8 -*-
"""Stock predict with neural network & ARIMA

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1zTDeD3_UmzIreGfmUa3hTob0owZN73EY
"""

# reference: https://towardsdatascience.com/aifortrading-2edd6fac689d
#https://towardsdatascience.com/stock-market-analysis-using-arima-8731ded2447a
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# !pip install ta
import ta
import seaborn as sns
import io
from sklearn import metrics

data = pd.read_csv('vnindex.csv',names=['Ticker','Date','Open','High','Low','Close','Volume'],skiprows=1)
data=data.loc[data['Ticker']=='VNINDEX']
vnindex_data = data.iloc[::-1]
vnindex_data.reset_index(inplace=True)
final_data=vnindex_data.reset_index(inplace=False)
final_data.drop(['index'],axis=1)
# Add all ta features filling nans values



# final_data=utils.dropna(final_data)
df=[]
df=pd.DataFrame()
close=final_data['Close']
df=final_data.drop(['Ticker','index','Date'],axis=1)
# df['Month']=[int(str(d)[-4:-2]) for d in final_data.loc[:,'Date']]
# # df['EMA10']=ema_indicator(close,n=10,fillna=True)
# fEMA20=ta.trend.EMAIndicator(close,n=20,fillna=True)
# fEMA50=ta.trend.EMAIndicator(close,n=50,fillna=True)
# fEMA100=ta.trend.EMAIndicator(close,n=100,fillna=True)
# fMACD = ta.trend.MACD(final_data["Close"], n_fast=12, n_slow=26,fillna=True)
# fRSI=ta.momentum.RSIIndicator(close,n=14,fillna=True)

# df['EMA20']=fEMA20.ema_indicator()
# df['EMA50']=fEMA50.ema_indicator()
# df['EMA100']=fEMA100.ema_indicator()
# df['MACD'] = fMACD.macd()
# df['RSI']=fRSI.rsi()
# df['Max'] = df['Close'].rolling(window = 10).max()
# df['Max'][:10] = df['Max'][10]
df = df.drop(['level_0'],axis=1)

df = df.iloc[:-1] # get previous features

close = close.iloc[1:]

x_train=df.loc[:3237,:]
x_test=df.loc[3237:,:]
y_train=close.loc[:3238]
y_test=close.loc[3238:]

len(x_train),len(x_test),len(y_train),len(y_test)

df

# build neural network to forecast
#Dependencies
import keras
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam
# Neural network
model = Sequential()
model.add(Dense(5, input_dim=5, activation='linear'))
model.add(Dense(1, activation='linear'))
# model.add(Dense(1, activation='linear'))

model.compile(loss='mean_squared_error', optimizer=Adam(lr=0.01))

history = model.fit(x_train, y_train,validation_data = (x_test,y_test), epochs=500, batch_size=256)

plt.plot(history.history['loss'])
plt.plot(history.history['val_loss']) 
plt.title('Model loss') 
plt.ylabel('Loss') 
plt.xlabel('Epoch') 
plt.legend(['Train', 'Test'], loc='upper left') 
plt.show()

y_pred= model.predict(x_test)

priceClose = y_train

# Forecast
n_periods = 1386
index_of_fc = np.arange(len(priceClose), len(priceClose)+n_periods)

# make series for plotting purpose
fc_series = pd.Series(y_pred.reshape((len(y_pred),)), index=index_of_fc)

# Plot
plt.figure(figsize=(20,6))
plt.plot(priceClose,label='History Price')
plt.plot(fc_series, color='red',label='Forecast')
plt.plot(df['Close'][3237:],color = 'green',label='True')
plt.legend(loc='upper left')
plt.title("Forecast VN Index")
plt.show()
# plt.savefig('forecast_vnindex.png')

## STOCK PREDICT WITH ARIMA
fd=final_data

fd

from pandas.plotting import lag_plot
from pandas import datetime
from statsmodels.tsa.arima_model import ARIMA
from sklearn.metrics import mean_squared_error

plt.figure(figsize=(10,10))
lag_plot(fd['Close'], lag=5)
plt.title('VN-Index Autocorrelation plot')

# Format date time 
fd['DOTR']=pd.to_datetime(fd.Date, format='%Y%m%d')
fd

train_data, test_data = fd[0:int(len(fd)*0.8)], fd[int(len(fd)*0.8):]
plt.figure(figsize=(12,7))
plt.title('Vnindex')
plt.xlabel('DOTR')
plt.ylabel('Close Prices')
plt.plot(fd['Close'], 'blue', label='Training Data')
plt.plot(test_data['Close'], 'green', label='Testing Data')
plt.xticks(np.arange(0,6000, 1300), fd['DOTR'][0:6000:1300])
plt.legend()

def smape_kun(y_true, y_pred):
    return np.mean((np.abs(y_pred - y_true) * 200/ (np.abs(y_pred) + np.abs(y_true))))

train_ar = train_data['Close'].values
test_ar = test_data['Close'].values
history = [x for x in train_ar]
print(type(history))
predictions = list()
for t in range(len(test_ar)):
    if (t % 100)==0:
      print(t)
    model = ARIMA(history, order=(5,1,0))
    model_fit = model.fit(disp=0)
    output = model_fit.forecast()
    yhat = output[0]
    predictions.append(yhat)
    obs = test_ar[t]
    history.append(obs)
error = mean_squared_error(test_ar, predictions)
print('Testing Mean Squared Error: %.3f' % error)
error2 = smape_kun(test_ar, predictions)
print('Symmetric mean absolute percentage error: %.3f' % error2)

plt.figure(figsize=(12,7))
plt.plot(fd['Close'], 'green', color='blue', label='Training Data')
plt.plot(test_data.index, predictions, color='green', 
         label='Predicted Price')
plt.plot(test_data.index, test_data['Close'], color='red', label='Actual Price')
plt.title('VN index Prediction')
plt.xlabel('DOTR')
plt.ylabel('Close Prices')
plt.xticks(np.arange(0,6000, 1300), fd['DOTR'][0:6000:1300])
plt.legend()

plt.figure(figsize=(12,7))
plt.plot(test_data.index, predictions, color='green',label='Predicted Price')
plt.plot(test_data.index, test_data['Close'], color='red', label='Actual Price')
plt.legend()
plt.title('VN index Prediction')
plt.xlabel('Dates')
plt.ylabel('Prices')
plt.xticks(np.arange(3699,4623, 300), fd['DOTR'][3699:4623:300])
plt.legend()

plt.plot(np.array(predictions[-100:]),color ='r')
plt.plot(np.array(test_data['Close'].iloc[-100:]))

test_data
