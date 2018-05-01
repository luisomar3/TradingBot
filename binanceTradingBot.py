import pandas as pd 
import numpy as np 

from estrategias.estrategiaadx import   EstrategiaAdx
from feeders.binanceFeeder import BinanceFeeder
from accounts.binanceaccount import BinanceAccount
from traders.binancetrader import BinanceTrader 


#Iniciar modulos
estrategia = EstrategiaAdx()
datos = BinanceFeeder()
cuenta = BinanceAccount()
trader = BinanceTrader()


def LiveTrader():
    

if __name__ == '__main__':
    main()
