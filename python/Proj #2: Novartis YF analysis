$NVS$ $YF$ $analysis$

import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

Novartis= yf.download("NVS", start= "2010-01-01", end="2024-01-01")
Novartis

ticker = ["NTLA","LEGN","NVO", "NVS"]
stocks= yf.download(ticker,start= "2010-01-01", end="2024-01-01")

close= stocks.loc[:,"Close"] #single out value (close)
plt.style.use("seaborn")
close.plot(figsize=(15,8), fontsize=12)
plt.legend(fontsize=15) #better shows the tickers
plt.show()#shows graph 

close.iloc[0,2] ##shows the value for close= stocks.loc[:,"Close"] using points
close.NVO.div(close.iloc[0,2]).mul(100) ##percentage change at closing of date for stock

normclose=close.div(close.iloc[0,2]).mul(100)#plot for norm closing
normclose.plot(figsize=(15,8), fontsize=12)
plt.legend(fontsize=15) ##better shows the tickers
plt.show()#shows graph 2

nvs= close.NVS.copy().to_frame()#creates nvs closing p table
nvs.shift(periods=1)##shifts everything down 1
nvs["lag1"]=nvs.shift(periods=1) ##to calculate change by subtracting lag1 to nvs
nvs["Diff"]=nvs.NVS.sub(nvs.lag1) ## or nvs["Diff"]=nvs.NVS.diff(periods=1)
nvs["%change"]=nvs.NVS.div(nvs.lag1).sub(1).mul(100) ##or nvs["%change"]=nvs.NVS.per_change(periods=1).mul(100)
#successfully created nvs table with addtional %change and Diff and lag1

# to delete column= del nvs["lag1"]
# to rename column= nvs.rename(columns= {'%change':'change'}, inplace= true)
nvs.NVS.resample("M").last() ## price at last month ("M"), business day is ("BS")


ret=nvs.pct_change().dropna() ##applies per change to table nvs and drops any NA value

daily_mean_ret= ret.mean()
annual_mean_ret= ret.mean()*252
#daily and annual mean return

daily_var_ret= ret.var() #variance is how far away value is from the mean
annual_var_ret= ret.var()*252
#daily and annual p variance

std_daily_ret= np.sqrt(daily_var_ret) #standard deviation measures how dispersed the data is in relation to the mean
annual_std_ret= np.sqrt(annual_var_ret) 
#daily and annual standard dev of p

close= stocks.loc[:,"Close"].copy() ##choose only close
normclose=close.div(close.iloc[0,2])
normclose.dropna().head()
summary= normclose.describe() ##.T to switch the column with the rows (ticker with count mean...)
summary= normclose.describe().T.loc[:,["mean","std"]]
summary["mean"]=summary["mean"]*252
summary["std"]=summary["std"]*np.sqrt(252)
summary
#prints out summary table with annual mean and std


