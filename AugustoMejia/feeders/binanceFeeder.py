import pandas as pd 
import numpy as np 
import datetime 
import re

from feeders.dataFeeder import DataFeeder
from binance.client import Client
from config import config

inicio = config['fechaInicio']
base = config['MonedaBase']
intervalo = config['interval']
client = Client('','')

class BinanceFeeder(DataFeeder):
    def __init__(self):
        pass
        

    def get_candle(self,coin):

        # mercado = coin + base
        # klines = pd.DataFrame(client.get_klines(symbol = mercado, interval = intervalo),
        # columns = ("datetime","O","H","L","C","V","x","x","x","x","x","x") ) 
        #Arreglo especifico de exchange

        mercado = coin + base
        klines = pd.DataFrame(client.get_historical_klines(mercado,intervalo,inicio),
                columns = ("datetime","O","H","L","C","V","x","x","x","x","x","x") ) 
        
        columnsName = klines.columns.values.tolist()
        candles = self.normalizeKlines(klines,columnsName)
        return candles

    def get_orders(self,coin):
        """ Get active orders
        """
        data = pd.DataFrame(client.get_orderbook_ticker() )
        return data
        
    def get_btc_markets(self):

        prices = pd.DataFrame(client.get_all_tickers())
        monedas = prices['symbol'].tolist()
        
        mercadosBTC=[]

        for moneda in monedas:
            
            d = re.findall('^[A-Z]{3,6}[BTC]{3,}$',moneda)
            
            if d : 
                mercadosBTC.append(d)

            
        df = pd.DataFrame(mercadosBTC)
        monedasBTC = df[0].tolist()

        soloBTC = []

        for moneda in monedasBTC:
            
            d = re.sub('[BTC]{3,3}$','',moneda)
            soloBTC.append(d)

        return soloBTC








if __name__ == '__main__':
    main()
    