import pandas as pd 
import numpy as np 
import datetime 

from binanceFeeder import BinanceFeeder
from binance.client import Client


myBinance = BinanceFeeder()


def main():
    
    candles = myBinance.get_candle("BNBBTC")
    print(candles)





if __name__ == '__main__':
    main()
    