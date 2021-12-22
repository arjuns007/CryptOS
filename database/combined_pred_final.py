#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import adfuller
get_ipython().run_line_magic('matplotlib', 'inline')
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.arima_model import ARIMA
from pandas.tseries.offsets import DateOffset

# from pymongo import MongoClient

import datetime
import requests
import json

def get_data(position):
    url = "https://data.mongodb-api.com/app/data-ujlqt/endpoint/data/beta/action/find"

    payload = json.dumps({
        "collection": "historical",
        "database": "Cryptos",
        "dataSource": "Cluster0",

    })
    headers = {
        'Content-Type': 'application/json',
        'Access-Control-Request-Headers': '*',
        'api-key': 'Zp1y5ZyMVbyiPc8e1FHyVm2JF5tTT0h39uiJC0HrNdJiRmQzb37UWZIeaHxdYMBA'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    data = response.json()
    doc = data['documents'][position]
    return doc

def get_pred(doc, orders, seasonal_orders):
    date_list = []
    price_list = []
    for i in doc['prices']:
      date_list.append(datetime.datetime.fromtimestamp(i[0]/1000).date())
      price_list.append(i[1])

    data = {'Date': date_list,'Close':price_list}
    date_list

    df = pd.DataFrame.from_dict(data)

    df['Date'] = pd.to_datetime(df['Date'])
    df = df[:len(df)-1]
    df.set_index('Date',inplace=True)
    df.sort_index(inplace=True)

    fuller_test = adfuller(df['Close'])

    df['First_diff'] = df['Close'] - df['Close'].shift(1)

    df['Second_diff'] = df['First_diff'] - df['First_diff'].shift(1)

    df['Seasonal_diff'] = df['Close'] - df['Close'].shift(7)
    model = sm.tsa.statespace.SARIMAX(df['Close'],order=orders,seasonal_order=seasonal_orders)
    results = model.fit(disp=-1)

    df['prediction'] = results.predict()
    extra_dates = [df.index[-1] + DateOffset(days=d) for d in range (1,31)]
    forecast_df = pd.DataFrame(index=extra_dates,columns=df.columns)

    final_df = pd.concat([df,forecast_df])
    final_df['prediction'] = results.predict(start=len(df)-1, end = len(df)+31)

    preds = final_df.tail(120)
    
    last120_dates = [df.index[-91] + DateOffset(days=d) for d in range (1,121)]
    for i in range(len(last120_dates)):
        last120_dates[i] =  last120_dates[i].date()

    final = preds.tail(30)
    final1 = preds.head(90)
    last90price = list(final1["Close"])
    last30price = list(final["prediction"])

    last120prices = last90price + last30price
    
    return [last120_dates,last120prices]


# data = [last120_dates,last120prices]
# client = MongoClient("mongodb+srv://dru444:aman123@cluster0.vszgj.mongodb.net/Cryptos?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE")
# db = client.test
# db = client.get_database('Cryptos')
# db_pred = db.get_collection('predictions')
# inserted = db_pred.insert_one({'Bitcoin': data})


# In[2]:


crypto_list = {'Bitcoin':{'orders':(0,1,0),'seasonal_orders':(6,1,1,7),'position':0},
'Ethereum':{'orders':(0,1,0),'seasonal_orders':(6,1,1,7),'position':1},
'Binance Coin':{'orders':(0,1,0),'seasonal_orders':(6,1,2,7),'position':2},
'Tether':{'orders':(0,1,0),'seasonal_orders':(0,1,0,7),'position':3},
'Solana':{'orders':(0,1,0),'seasonal_orders':(6,1,2,7),'position':4},
'XRP':{'orders':(0,1,0),'seasonal_orders':(0,1,0,7),'position':5},
'USD Coin':{'orders':(0,1,0),'seasonal_orders':(5,1,1,7),'position':6},
'Cardano':{'orders':(0,1,0),'seasonal_orders':(11,1,1,7),'position':7},
'Terra':{'orders':(0,1,0),'seasonal_orders':(5,1,1,7),'position':8},
'Avalanche':{'orders':(0,1,0),'seasonal_orders':(5,1,1,7),'position':9},
}


# In[ ]:


total_output = []
for i in crypto_list:
    d = get_pred(get_data(crypto_list[i]['position']),crypto_list[i]['orders'],crypto_list[i]['seasonal_orders'])
    total_output.append(d[1])
total_output.append(d[0])


# In[ ]:

dates = total_output[10]
dates = [str(i) for i in dates]

total_output[10] = dates
total_output[10]


# In[ ]:

from pymongo import MongoClient
client = MongoClient("mongodb+srv://dru444:aman123@cluster0.vszgj.mongodb.net/Cryptos?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE")
db = client.test
db = client.get_database('Cryptos')
db_pred = db.get_collection('predictions')
x = db_pred.delete_many({})
inserted = db_pred.insert_one({'_id':'all','data': total_output})


