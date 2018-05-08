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
cliente = account.client

def main():
    
    params = ['ETHBTC']

    habilitado = account.habilitado

    if habilitado == True:

 
        order = cliente.order_limit_sell(
        symbol='BNBBTC',
        quantity=0.67,
        price='0.001600')
        

        print(order)





if __name__ == '__main__':
    main()