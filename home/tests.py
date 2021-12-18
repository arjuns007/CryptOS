import unittest
import requests
from . import models

class DataTest(unittest.TestCase):
                 
    def test_1(self):
        
        url = 'https://api.coingecko.com/api/v3/coins/markets?vs_currency=USD&order=market_cap_desc&per_page=10&page=1&sparkline=false'
        data = requests.get(url).json()
        self.assertEqual(data[0]["name"],"Bitcoin")

    def test_2(self):
        url = 'https://api.coingecko.com/api/v3/coins/markets?vs_currency=USD&order=market_cap_desc&per_page=10&page=1&sparkline=false'
        data = requests.get(url).json()
        self.assertEqual(data[0]["symbol"],"btc")

    def test_3(self):
        url = 'https://api.coingecko.com/api/v3/coins/markets?vs_currency=USD&order=market_cap_desc&per_page=10&page=1&sparkline=false'
        data = requests.get(url).json()
        self.assertEqual(data[1]["symbol"],"eth")
        

