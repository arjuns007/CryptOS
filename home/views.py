from django.shortcuts import render
import requests

# Create your views here.

def top_bar():

    url = 'https://api.coingecko.com/api/v3/coins/markets?vs_currency=USD&order=market_cap_desc&per_page=100&page=1&sparkline=false'
    data = requests.get(url).json()

    for item in data:

            if item['symbol'] == 'btc':
                btc = float(item['current_price'])
                c_btc = item['price_change_24h']
                if c_btc < 0:
                    c_btc = "tf-ion-arrow-down-b down-status"
                else:
                    c_btc = str("tf-arrow-dropup up-status")


            if item['symbol'] == 'eth':
                eth = float(item['current_price'])
                c_eth = item['price_change_24h']
                if c_eth < 0:
                    c_eth = "tf-ion-arrow-down-b down-status"
                else:
                    c_eth = "tf-arrow-dropup up-status"

            
            if item['symbol'] == 'bnb':
                bnb = float(item['current_price'])
                c_bnb = item['price_change_24h']
                if c_bnb < 0:
                    c_bnb = "tf-ion-arrow-down-b down-status"
                else:
                    c_bnb = "tf-arrow-dropup up-status"

            
            if item['symbol'] == 'usdt':
                usdt = float(item['current_price'])
                c_usdt = item['price_change_24h']
                if c_usdt < 0:
                    c_usdt = "tf-ion-arrow-down-b down-status"
                else:
                    c_usdt = "tf-arrow-dropup up-status"


            if item['symbol'] == 'ada':
                ada = float(item['current_price'])
                c_ada = item['price_change_24h']
                if c_ada < 0:
                    c_ada = "tf-ion-arrow-down-b down-status"
                else:
                    c_ada = "tf-arrow-dropup up-status"

    return {'btc':btc,'eth':eth,'bnb':bnb,'usdt':usdt,'ada':ada,'c_ada': c_ada,'c_bnb': c_bnb,'c_btc': c_btc,'c_eth' : c_eth,'c_usdt' : c_usdt}


def home(request):
   dict = top_bar()           
   return render(request, 'home.html', d)

def cal_con(request):
    url = 'https://api.coingecko.com/api/v3/coins/markets?vs_currency=USD&order=market_cap_desc&per_page=100&page=1&sparkline=false'
    data = requests.get(url).json()



    url2 ='https://api.exchangeratesapi.io/latest?base=USD'
    data2= requests.get(url2).json()
    rates = data2['rates']

    d = top_bar()           
   

    if request.method == 'POST':
        value1 = float(request.POST['value']) 
        curr1 = request.POST['curr1']
        curr2 = request.POST['curr2']
        

        for item in data:
            if item['symbol'] == curr1.lower():
                price = float(item['current_price'])
                if curr2 == 'USD':
                    Result = round(value1*price,2)
                else:
                    Result = round(value1*price*rates[curr2],2)                  
        
        k= {'Result': str('= ' + str(Result)),'value':value1,'curr1':curr1,'curr2': curr2}
        
        
        k.update(d)
        return render(request, 'cal_con.html', k)

    
    else:
        return render(request, 'cal_con.html', d)

def about(request):
    d = top_bar()  
    return render(request, 'about.html', d)


def faq(request):
    d = top_bar()  
    return render(request, 'faq.html', d)

def blog(request):
    d = top_bar()  
    return render(request, 'blog.html',d)

def guide(request):
    d = top_bar()  
    return render(request, 'guide.html',d)
