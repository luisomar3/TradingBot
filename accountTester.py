import pandas as pd 
#import numpy as np 
import datetime 
import time 
from config import config

#coin = config['coin']
#intervalo = config['interval']

from binance.client import Client
from binance.enums import *
monedas = config['monedas']
from accounts.binanceaccount import BinanceAccount
from traders.binancetrader  import BinanceTrader

trader = BinanceTrader()
account = BinanceAccount()

def main():
    
    params = ['ETHBTC']

    habilitado = account.habilitado

    if habilitado == True:

        monedaPrincipal,portafolio = account.portafolio(monedas)

        print(portafolio)
        
        print(account.capital())
        print(trader.in_the_market('BNB',0.01))






if __name__ == '__main__':
    main()