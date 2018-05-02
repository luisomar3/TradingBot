import pandas as pd 
import numpy as np 
import datetime 

from feeders.dataFeeder import DataFeeder
from binance.client import Client
from config import config

base = config['MonedaBase']
intervalo = config['interval']
client = Client('','')

class BinanceFeeder(DataFeeder):
    def __init__(self):
        pass
        

    def get_candle(self,coin):

        mercado = coin + base
        klines = pd.DataFrame(client.get_klines(symbol = mercado, interval = intervalo),
        columns = ("datetime","O","H","L","C","V","x","x","x","x","x","x") ) 
        #Arreglo especifico de exchange
        # mercado = coin + base
        # klines = pd.DataFrame(client.get_historical_klines(mercado,intervalo,"1 Ago, 2016"),
        # columns = ("datetime","O","H","L","C","V","x","x","x","x","x","x") ) 
        
        columnsName = klines.columns.values.tolist()
        candles = self.normalizeKlines(klines,columnsName)
        return candles

    def get_orders(self,coin):
        """ Get active orders
        """
        data = pd.DataFrame(client.get_orderbook_ticker() )
        return data
        








if __name__ == '__main__':
    main()
    