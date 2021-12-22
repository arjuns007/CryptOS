# Import the libraries we need
from pymongo import MongoClient
import requests

# Connect to the database with the connection string we got from Atlas, replacing user and password.
client = MongoClient("mongodb+srv://dru444:aman123@cluster0.vszgj.mongodb.net/Cryptos?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE")
db = client.test

# Next we define the database we are using.
# It does not have to exist first, like with relational databases.
db = client.get_database('Cryptos')

# Now, we make the API call and prices the results to the terminal.
prices = requests.get('https://api.coingecko.com/api/v3//coins/markets?vs_currency=usd&order=market_cap_desc&per_page=100&page=1&sparkline=false')
prices = prices.json()

# We define the collection we will store this data in,
# which is created dynamically like the database,
# and insert the data into the collection.

db_prices = db.get_collection('prices')
x = db_prices.delete_many({})
inserted = db_prices.insert_many(prices)
# Print a count of documents inserted.
print(str(len(inserted.inserted_ids)) + " documents inserted")

# Historical of last 1000 days---------------------------
coins = []
for item in prices:
    coins.append(item['id'])
    if item['market_cap_rank'] == 10:
        break

coins_hist = []
rank = 0
for id in coins:
    hist_data= requests.get('https://api.coingecko.com/api/v3/coins/'+id+'/market_chart?vs_currency=usd&days=1000&interval=daily')
    hist_data = hist_data.json()
    
    data ={'_id':id, 'rank':rank}
    data['prices'] = hist_data['prices']
    coins_hist.append(data)
    rank = rank + 1

db_hist = db.get_collection('historical')
x = db_hist.delete_many({})
insert = db_hist.insert_many(coins_hist)
print(str(len(insert.inserted_ids)) + " historical documents inserted")
