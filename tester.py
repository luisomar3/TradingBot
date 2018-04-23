import pandas as pd 
import numpy as np 
import datetime 

from indicadores import *
from feeders.binanceFeeder import BinanceFeeder
from binance.client import Client

from basestrategy import BaseStrategy
from estrategiaadx import EstrategiaAdx

from config import config
coin = config['coin']

myStrategy = BaseStrategy()
adxStrategy = EstrategiaAdx()
myBinance = BinanceFeeder()
miIndicador = Indicadores()

def main():
    
    candles = myBinance.get_candle(coin)
    
    
   
    a = adxStrategy.PDI_NDI_Cossover(candles)
    print(a.to_string())
    #message = myStrategy.message(candles2)
    #print(message)

if __name__ == '__main__':
    main()
    