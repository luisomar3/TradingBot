import pandas as pd
import numpy as np 
import smtplib

import pandas as pd 
import numpy as numpy

import time 
from config import config


intervalo = config['interval']
monedaBase = config['MonedaBase']
mail= config['email']
mail_password = config['email_password']
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

    def equivalent(self,moneda,posicion,price):
        """Metodo para calcular el equivalente en MONEDA de X cantidad de BTC
        """
        mercado = moneda+monedaBase
        decimales  = self.decimales(moneda)
        equivlalente = round(posicion/price,decimales)
        if decimales == 0 :
            equivlalente = int(equivlalente)
        
        #print(equivlalente)
        return  equivlalente

    def decimales(self,moneda):
        mercado = moneda + monedaBase
        info = client.get_symbol_info(mercado)
       
        filters = info['filters']
        stepSize = filters[1]['stepSize']
        noComa = stepSize.replace('.','')
        #print(noComa)
        #print(noComa.find('1'))
        return noComa.find('1')
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

    def in_the_market(self,moneda,posicion,price):
        """Metodo para saber si estoy o no en el mercado
        """
        infoActivo = client.get_asset_balance(moneda)
        comprado = float(infoActivo['free'])
        porComprar = self.equivalent(moneda,posicion,price) 
        porComprarPor = porComprar - (porComprar*0.2)
        if comprado >= porComprarPor:
            inTheMarket = 1  # Verifico que la posicion sea mayor al monto q poseo en esa moneda.
        else:
            inTheMarket = 0

        return inTheMarket 
    
    def limit_buy(self,moneda,cantidad,price):
        
        mercado = moneda + monedaBase
        order = client.order_limit_buy(
            
            symbol=mercado,
            quantity=cantidad,
            price=price)

        return order

    def limit_sell(self,moneda,cantidad,price):
        
        mercado = moneda + monedaBase
        order = client.order_limit_sell(
            symbol=mercado,
            quantity=cantidad,
            price=precio)
        return order

    def verify_order(order):

        if order['status'] == 'Filled':
            return 1
        else :
            return 0


    def get_best_price(self,moneda,side,cantidad):
        """Funcion para encontrar los mejores precios en el libro de ordenes
        :param moneda: Moneda a evaluar
        :type moneda: Str

        :param side: Bid o Ask para la orden.
        :type side: Str.

        """
        mercado = moneda + monedaBase
        order_book =client.get_order_book(symbol=mercado)

        side_list  = pd.DataFrame(order_book[side])
        orders = pd.DataFrame.from_items(zip(side_list.index, side_list.values)).T
        orders = orders.rename(index=str, columns={0: "prices", 1: "quantity"})
        orders = orders.drop(columns = 2 ,  axis =1 )
        orders = orders.apply(pd.to_numeric)
        orders['sumatoria'] = orders['quantity'].cumsum()

        def mejor_precio(orders,cantidad):
            porcentaje = cantidad * 1.5
            for row in orders.itertuples():
                if row[3]> porcentaje:
                    return row[1]
                    break
 
        precio = mejor_precio(orders,cantidad)

        return precio
        


    def send_email(self,msg):
        """
        Takes all the params to build the email and send it
        """
        fromaddr = 'luisomar242@gmail.com' #from
        toaddrs  = 'luisomar242@gmail.com' #to

        msg = "\r\n".join([
        "From: {}".format(fromaddr),
        "To: {}".format(toaddrs),
        "Subject: Investment Opportunity!",
        "",
        msg
        ])
        username = mail         #username
        password = mail_password       #password
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        server.login(username,password)
        server.sendmail(fromaddr, toaddrs, msg)
        server.quit()
        
        
        
        

        






