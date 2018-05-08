import pandas as pd
import numpy as np 

import pandas as pd 
import numpy as numpy

import time 
from config import config


intervalo = config['interval']
monedaBase = config['MonedaBase']

#from binance.client import Client
from binance.enums import *

from traders.basetrader import BaseTrader

from accounts.binanceaccount import BinanceAccount

account = BinanceAccount()
client = account.client
class BinanceTrader(BaseTrader):

    def __init__(self):
        pass

    def exchange_place_order(self,*args,**kwargs):

        client.create_order()

    def place_test_order(self,*args,**kwargs):
        order = client.create_test_order(
        symbol='BNBBTC',
        side=SIDE_BUY,
        type=ORDER_TYPE_LIMIT,
        timeInForce=TIME_IN_FORCE_GTC,
        quantity=100,
        price='0.00001')

        return 'placed'

    def equivalent(self,posicion,price):
        """Metodo para calcular el equivalente en MONEDA de X cantidad de BTC
        """
        equivlalente = posicion/price

        return  equivlalente

    def market_buy(self,moneda,cantidad):
        """Metodo para  realizar un market buy
        """
        mercado = moneda+monedaBase
        order = client.order_market_buy(symbol=mercado,quantity=cantidad)

        return order

    def market_sell(self,moneda,cantidad):
        """Metodo para  realizar un market buy
        """
        mercado = moneda+monedaBase
        order = client.order_market_sell(symbol=mercado,quantity=cantidad)
        return order

    def get_open_orders(self,moneda):
        
        mercado = moneda+monedaBase
        open_orders = client.get_open_orders(symbol=mercado)
        df_orders = pd.DataFrame(open_orders)
        return df_orders

    def cancel_order(self,moneda):

        orders = self.get_open_orders(moneda)
        df_orders= pd.DataFrame(orders)
        ids = df_orders['orderId']
        mercado = moneda+monedaBase

        for item in ids:

            print(mercado)
            client.cancel_order(symbol=mercado,orderId=item)
        
        return 'hola'

        
        





