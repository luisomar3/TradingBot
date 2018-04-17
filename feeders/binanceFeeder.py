import pandas as pd 
import numpy as np 
import datetime 

from dataFeeder import DataFeeder
from binance.client import Client

client = Client('AIc1YLwGtRDJzy4wpMRe7CcAUBxTMIIfT1ddhQOhTJbHRP2xqhMkIyt5EABHLPZt',"")

class BinanceFeeder(DataFeeder):
    def __init__(self):
        pass
        

    def get_candle(self,coin):
        klines = pd.DataFrame(client.get_klines(symbol = coin, interval = client.KLINE_INTERVAL_30MINUTE),
        columns = ("datetime","O","H","L","C","V","x","x","x","x","x","x") ) # Arreglo especifico de exchange
        candles = self.normalizeKlines(klines)
        return candles









if __name__ == '__main__':
    main()
    