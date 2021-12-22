from datetime import time
from django.shortcuts import render
from dns.resolver import Timeout
import requests
import time as t
import plotly.graph_objects as go
from plotly.offline import plot




# close_train = close_train.reshape((-1))
# close_test = close_test.reshape((-1))
# prediction = prediction.reshape((-1))

# Retrieving Data from MongoDB Cluster

from pymongo import MongoClient,ASCENDING, DESCENDING

# Connect to the MongoDB database using our connection string.
client = MongoClient("mongodb+srv://dru444:aman123@cluster0.vszgj.mongodb.net/Cryptos?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE")
db = client.test

# Connect to the coin_markets database and the prices collection.
db = client.get_database('Cryptos')
db_prices = db.get_collection('prices')
db_pred = db.get_collection('prediction')

data=[]

for doc in db_prices.find().sort('market_cap_rank', ASCENDING):
    data.append(doc)


names = ["Bitcoin","Ethereum","Binance Coin","Tether","Solana","USD Coin","XRP","Cardano","Terra","Avalanche"]
data = data[0:10]

plot_doc = []

db_pred = db.get_collection('predictions')
plot_doc = db_pred.find_one({'_id':'all'})

def plot_chart(rank):
    
        
    # get the candles
    
    candles = plot_doc['data']
    
    
    # create lists to hold our different data elements
    dates = candles[10]
    close_data = candles[int(rank)-1]
    close_hist = close_data[:90]
    close_pred = close_data[89:]
    date_hist = dates[:90]
    date_pred = dates[89:]

    trace1 = go.Scatter(
        x = date_hist,
        y = close_hist,
        mode = 'lines',
        name = 'Historical'
    )
    trace2 = go.Scatter(
        x = date_pred,
        y = close_pred,
        mode = 'lines',
        name = 'Prediction'
    )

    layout = go.Layout(
        title = names[int(rank)-1].upper() + " PREDICTED PRICE ",
        xaxis = {'title' : "Date"},
        yaxis = {'title' : "Price"}
    )
    fig = go.Figure(data=[trace1,trace2], layout=layout)
    
    
  

    # construct the figure
    
    fig.update_layout(height = 900,width = 1500)

    # display our graph
    # fig.show()
    # print(fig)
    plt_div = plot(fig, output_type='div')
    return plt_div

# Search for records where the price_change_24h value is greater than 1000, loop the results, and print them to the terminal.

def top_bar():
    barlist=[]
    for item in data:
        sym = item['symbol'].upper()
        curr_p = float(item['current_price'])
        c_chng = item['price_change_24h']
        if c_chng < 0 or c_chng == None:
            c_chng = "tf-ion-arrow-down-b down-status"
        else:
            c_chng = "tf-arrow-dropup up-status"

         
        barlist.append({'sym': sym,'class':c_chng,'curr_p':curr_p }) 

    context = {'top_bar': barlist}
    return context
d_top = top_bar()

def cal_con(request):

    cryptolist = {'data': data }  
    url2 ='http://api.exchangeratesapi.io/latest?access_key=eb70758538d0f60d66ccf9abe7f9054f'
    
    data2= requests.get(url2).json()
    rates = data2['rates']

    
    cryptolist.update(d_top)          
   
    if request.method == 'POST':
        value1 = float(request.POST['value']) 
        curr1 = request.POST['curr1']
        curr2 = request.POST['curr2']
        

        for item in data:
            if item['symbol'] == curr1.lower():
                if type(item['current_price']) == int:
                    price = float(item['current_price'])
                else:
                    price = str(item['current_price']).replace(',',"")
                    price = float(price)
                if curr2 == 'EUR':
                    Result = "{:,}".format(round(value1*price,2))
                else:
                    Result = "{:,}".format(round(value1*price*rates[curr2],2) )                 
        
        k= {'Result': str('= ' + str(Result)),'value':value1,'curr1':curr1,'curr2': curr2}
        
        cryptolist.update(k)
        
        return render(request, 'cal_con.html', cryptolist)

    
    else:
        return render(request, 'cal_con.html', cryptolist)


def about(request):
    d = d_top 
    return render(request, 'about.html', d)


def faq(request):
    d = d_top  
    return render(request, 'faq.html', d)

def blog(request):
    d = d_top  
    return render(request, 'blog.html',d)

def guide(request):
    d = d_top  
    return render(request, 'guide.html',d)

def pred(request):
    res = False
    dataP ={'data':data}
    
    if request.method == 'POST':
        res = True
        rank= request.POST['coin']
        t.sleep(10)
        dataP.update({'plot':plot_chart(rank)})
        
        
        
    dataP.update({'result': res})
    
    d = d_top
    dataP.update(d) 
    return render(request,'pred.html',dataP )

def home(request):
    d = d_top
    dataH = data
    for i in dataH:
        # i['plot'] = plot_chart(i['symbol'].upper())
        if type(i['current_price']) != str: 
            i['current_price'] = "{:,}".format(float(i['current_price']))
            i['market_cap'] = "{:,}".format(float(i['market_cap']))
        

    context = {'data': dataH}
    context.update(d)

    return render(request, 'home.html', context)