import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestRegressor

data=pd.read_csv('btcpricepredictor.csv')#make sure to have btc historical price csv file ready
data.head()
data.corr()
data['date']=pd.to_datetime(data['date'], infer_datetime_format=True)
data.set_index('date',inplace=True)
data.isnull().any()
data.isnull().sum()
data=data.dropna()
data.describe()
plt.figure(figsize=(10,6))
x=data.groupby('date')['close'].mean()
x.plot(linewidth=0.5, color='r')
plt.xlabel('Date')
plt.ylabel('Volume')
plt.title('BTC Price')

data["gap"]=data["high"]-data["low"]+data["volume"]
data["y"]= data["high"]/data["volume"]
data["x"]=data["low"]/data["volume"]
data["w"]=data["close"]/data["volume"]
data["v"]=data["open"]/data["volume"]
data["a"]=data["high"]/data["low"]
data["b"]=(data["high"]/data["low"])*data["volume"]
abs(data.corr()["close"]).sort_values(ascending=False)

data=data[["close","volume","gap","y","x","w","v","a","b"]]
data.head()
data.describe()

df2= data.tail(30)
train=df2[:11]
test= df2[-19:]

print(train.shape, test.shape)

#pip install statsmodels
from statsmodels.tsa.statespace.sarimax import SARIMAX
model = SARIMAX(endog=train["close"], exog=train.drop("close", axis=1), order=(2,1,1))
results= model.fit()
print(results.summary())

test["close"].plot(legend=True, figsize=(12,6))
predictions = results.get_prediction(start=test.index[0], end=test.index[-1])
predictions.predicted_mean.plot(label='TimeSeries',legend=True)
data["gap"].plot(label='gap', legend=True)
data["y"].plot(label='high/volume', legend=True)
data["x"].plot(label='low/volume', legend=True)
data["w"].plot(label='close/volume', legend=True)
data["v"].plot(label='open/volume', legend=True)
data["a"].plot(label='high/low', legend=True)
data["b"].plot(label='(high.low)*volume', legend=True)
plt.show()
