# -*- coding: utf-8 -*-
"""Forecast VNINDEX.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1KTvs9hpI1uD88xG9OK5DDDfu5XKpxSrE
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# !pip install ta
import ta
import seaborn as sns
import io
from sklearn import metrics
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.arima_model import ARIMA
import pmdarima as pm

data = pd.read_csv('vnindex.csv',names=['Ticker','Date','Open','High','Low','Close','Volume'],skiprows=1)

data=data.loc[data['Ticker']=='VNINDEX']
vnindex_data = data.iloc[::-1]

vnindex_data.reset_index(inplace=True)

final_data=vnindex_data.reset_index(inplace=False)
final_data.drop(['index'],axis=1)

plt.plot(final_data['Close'])

close = np.array(final_data['Close'])
x_train = close[:3237]
x_test = close[3237:]

# Add all ta features filling nans values
# final_data=utils.dropna(final_data)
df=[]
df=pd.DataFrame()
close=final_data['Close']
df=final_data.drop(['Ticker','index','Date'],axis=1)
df['Month']=[int(str(d)[-4:-2]) for d in final_data.loc[:,'Date']]
# df['EMA10']=ema_indicator(close,n=10,fillna=True)
fEMA20=ta.trend.EMAIndicator(close,n=20,fillna=True)
fEMA50=ta.trend.EMAIndicator(close,n=50,fillna=True)
fEMA100=ta.trend.EMAIndicator(close,n=100,fillna=True)
fMACD = ta.trend.MACD(final_data["Close"], n_fast=12, n_slow=26,fillna=True)
fRSI=ta.momentum.RSIIndicator(close,n=14,fillna=True)

df['EMA20']=fEMA20.ema_indicator()
df['EMA50']=fEMA50.ema_indicator()
df['EMA100']=fEMA100.ema_indicator()
df['MACD'] = fMACD.macd()
df['RSI']=fRSI.rsi()
df['Max'] = df['Close'].rolling(window = 10).max()
df['Max'][:10] = df['Max'][10]
df = df.drop(['level_0'],axis=1)

df

def take_price(price,period):
  priceValue = np.array(price.iloc[period:])
  pricePre = np.array(price.iloc[:-period])
  difPrice = (priceValue/pricePre)-1
  difPrice[difPrice >= 0.01]=1
  difPrice[difPrice<0.01]=0
  difPrice=difPrice.tolist()
  difPrice=[0]*period+difPrice
  return priceValue, pricePre,difPrice

# take price value
priceValue,pricePre,difPrice = take_price(close,5)

# take diff between n days to get labels

label=pd.DataFrame(difPrice)

df['Label']=label

corrMatrix = df.corr()
sns.heatmap(corrMatrix, annot=True)

x_train=df.loc[:3237,:].drop(['Label'],axxis=1)
x_test=df.loc[3237:,:].drop(['Label'],axis=1)
y_train=df.loc[:3237,'Label']
y_test=df.loc[3237:,'Label']

y_test = pd.DataFrame(y_test)
y_train = pd.DataFrame(y_train)

from sklearn import svm
from sklearn import metrics

#Create a svm Classifier
clf = svm.SVC(kernel='linear') # Linear Kernel

#Train the model using the training sets
clf.fit(x_train, y_train)

#Predict the response for test dataset
y_pred = clf.predict(x_test)

print("Accuracy:",metrics.accuracy_score(y_test,y_pred))
print("Precision:",metrics.precision_score(y_test, y_pred))
print("Recall:",metrics.recall_score(y_test, y_pred))
print("F-score:",metrics.f1_score(y_test, y_pred))

from sklearn.linear_model import LogisticRegression
# all parameters not specified are set to their defaults
logisticRegr = LogisticRegression()
logisticRegr.fit(x_train, y_train)
y_pred=logisticRegr.predict(x_test)

from sklearn import metrics
print("Accuracy:",metrics.accuracy_score(y_test,y_pred))
print("Precision:",metrics.precision_score(y_test, y_pred))
print("Recall:",metrics.recall_score(y_test, y_pred))
print("F-score:",metrics.f1_score(y_test, y_pred))

from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import confusion_matrix
from sklearn.tree import export_graphviz
from sklearn.externals.six import StringIO 
from sklearn import metrics

dt = DecisionTreeClassifier()
dt.fit(x_train, y_train)

# dot_data = StringIO()
# export_graphviz(dt, out_file=dot_data, feature_names=iris.feature_names)
# (graph, ) = graph_from_dot_data(dot_data.getvalue())
# Image(graph.create_png())
y_pred = dt.predict(x_test)
print("Accuracy:",metrics.accuracy_score(y_test,y_pred))
print("Precision:",metrics.precision_score(y_test, y_pred))
print("Recall:",metrics.recall_score(y_test, y_pred))
print("F-score:",metrics.f1_score(y_test, y_pred))

# dot_data = StringIO()
# nameCol =['Close','Volumn','Month','EMA20','EMA50','EMA100','MACD','RSI']
# export_graphviz(dt, out_file=dot_data, feature_names=nameCol)
# (graph, ) = graph_from_dot_data(dot_data.getvalue())
# Image(graph.create_png())

# Import the model we are using
from sklearn.ensemble import RandomForestRegressor
# Instantiate model with 1000 decision trees
rf = RandomForestRegressor(n_estimators = 1000, random_state = 42)
# Train the model on training data
rf.fit(x_train, y_train)

# Use the forest's predict method on the test data
from sklearn import metrics
y_pred = rf.predict(x_test)
y_prednew=[1 if yp > 0.5 else 0 for yp in y_pred]
print("Accuracy:",metrics.accuracy_score(y_test,y_prednew))
print("Precision:",metrics.precision_score(y_test, y_prednew))
print("Recall:",metrics.recall_score(y_test, y_prednew))
print("F-score:",metrics.f1_score(y_test, y_prednew))

from sklearn.metrics import confusion_matrix
confusion_matrix(y_test, y_prednew)

plt.plot( np.array(y_test)[:200],marker='o', linewidth=2)
plt.plot( y_prednew[:200], marker='', linewidth=2)

# forecasting with time series approach
# check stationary
result = adfuller(df['Close'])

print('ADF Statistic: {}'.format(result[0]))
print('p-value: {}'.format(result[1]))
print('Critical Values:')
for key, value in result[4].items():
    print('\t{}: {}'.format(key, value))

difClose = df['Close']-df['Close'].shift()
difClose=difClose.dropna()

print('ADF Statistic: {}'.format(result[0]))
print('p-value: {}'.format(result[1]))
print('Critical Values:')
for key, value in result[4].items():
    print('\t{}: {}'.format(key, value))

# Look at the ADF test above, we can see the p-value is greater than threshold (0.5%) and Statistic value is greater than Critical value . Thus we conclude the time series is not stationary. We need take the log for the serie
Close = df['Close']
logReturn = np.log(Close) - np.log(Close.shift())
y_train=logReturn[:3237]
y_test=logReturn[3237:]
y_train = y_train.dropna()
y_test = y_test.dropna()

plt.plot(difClose) # log return

result = adfuller(y_train)
print('ADF Statistic: {}'.format(result[0]))
print('p-value: {}'.format(result[1]))
print('Critical Values:')
for key, value in result[4].items():
    print('\t{}: {}'.format(key, value))

from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.arima_model import ARIMA
from statsmodels.graphics.tsaplots import plot_acf
from statsmodels.graphics.tsaplots import plot_pacf

plt.figure()
plt.subplot(211)
plot_acf(logReturn, ax=plt.gca())
plt.subplot(212)
plot_pacf(logReturn, ax=plt.gca())
plt.show()

model = ARIMA(logReturn, order=(7,1,7))
results = model.fit()

plt.plot(logReturn[-60:])
plt.plot(results.fittedvalues[-60:], color='red')

# check RSS. Less the RSS value, the more effective the model is
RSS = np.nansum((results.fittedvalues-logReturn))**2
RSS

y_pred, se, conf = results.forecast(1387, alpha=0.05)  # 95% conf

# plt.plot(np.array(y_test))
plt.plot(y_pred, color='red')

# actual vs fitted plot
results.plot_predict(dynamic=False)
plt.show()

# Plot residual errors
residuals = pd.DataFrame(results.resid)
fig, ax = plt.subplots(1,2)
residuals.plot(title="Residuals", ax=ax[0])
residuals.plot(kind='kde', title='Density', ax=ax[1])
plt.show()

# Accuracy metrics
def forecast_accuracy(forecast, actual):
    mape = np.mean(np.abs(forecast - actual)/np.abs(actual))  # MAPE
    me = np.mean(forecast - actual)             # ME
    mae = np.mean(np.abs(forecast - actual))    # MAE
    mpe = np.mean((forecast - actual)/actual)   # MPE
    rmse = np.mean((forecast - actual)**2)**.5  # RMSE
    corr = np.corrcoef(forecast, actual)[0,1]   # corr
    mins = np.amin(np.hstack([forecast[:,None], 
                              actual[:,None]]), axis=1)
    maxs = np.amax(np.hstack([forecast[:,None], 
                              actual[:,None]]), axis=1)
    minmax = 1 - np.mean(mins/maxs)             # minmax
    # acf1 = acf(fc-test)[1]                      # ACF1
    return({'mape':mape, 'me':me, 'mae': mae, 
            'mpe': mpe, 'rmse':rmse, 
            'corr':corr, 'minmax':minmax})

forecast_accuracy(y_pred, np.array(y_test))

df



priceClose = df['Close'][:3237]

model = pm.auto_arima(priceClose, start_p=1, start_q=1,
                      test='adf',       # use adftest to find optimal 'd'
                      max_p=3, max_q=3, # maximum p and q
                      m=1,              # frequency of series
                      d=None,           # let model determine 'd'
                      seasonal=False,   # No Seasonality
                      start_P=0, 
                      D=0, 
                      trace=True,
                      error_action='ignore',  
                      suppress_warnings=True, 
                      stepwise=True)

print(model.summary())

# Forecast
n_periods = 1387
fc, confint = model.predict(n_periods=n_periods, return_conf_int=True)
index_of_fc = np.arange(len(priceClose), len(priceClose)+n_periods)

# make series for plotting purpose
fc_series = pd.Series(fc, index=index_of_fc)
lower_series = pd.Series(confint[:, 0], index=index_of_fc)
upper_series = pd.Series(confint[:, 1], index=index_of_fc)

# Plot
plt.figure(figsize=(8,6))
plt.plot(priceClose,label='History Price')
plt.plot(fc_series, color='orange',label='Forecast')
plt.fill_between(lower_series.index, 
                 lower_series, 
                 upper_series, 
                 color='k', alpha=.15,label='Interval')
plt.plot(df['Close'][3237:],color = 'darkgreen',label='True')
plt.legend(loc='upper left')
plt.title("Forecast VN Index")
plt.show()

fc_series

# build neural network to forecast
#Dependencies
import keras
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam
# Neural network
model = Sequential()
model.add(Dense(8, input_dim=11, activation='relu'))
model.add(Dense(4, activation='relu'))
model.add(Dense(1, activation='linear'))

model.compile(loss='mean_squared_error', optimizer=Adam(lr=0.008))

x_train=df.loc[:3236,:].drop(['Label','Close'],axis=1)
x_test=df.loc[3237:4622,:].drop(['Label','Close'],axis=1)
y_train=df.loc[1:3237,'Close']
y_test=df.loc[3238:,'Close']

history = model.fit(x_train, y_train,validation_data = (x_test,y_test), epochs=100, batch_size=30)

# import matplotlib.pyplot as plt
# plt.plot(history.history['acc'])
# plt.plot(history.history['val_acc'])
# plt.title('Model accuracy')
# plt.ylabel('Accuracy')
# plt.xlabel('Epoch')
# plt.legend(['Train', 'Test'], loc='upper left')
# plt.show()

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

fc_series
