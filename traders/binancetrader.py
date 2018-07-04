import pandas as pd
import numpy as np 
import smtplib

import pandas as pd 
import numpy as numpy

import time 
from config import config
import decimal
ctx = decimal.Context()

intervalo = config['interval']
monedaBase = config['MonedaBase']
mail= config['email']
mail_password = config['email_password']
destinatarios = config['destinatarios']
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

    def decimales_precio(self,moneda):
        mercado = moneda + monedaBase
        info = client.get_symbol_info(mercado)

        filters = info['filters']
        tickSize = filters[0]['tickSize']

        noComa = tickSize.replace('.','')
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

    def in_the_market(self,moneda,posicion,price = None):
        """Metodo para saber si estoy o no en el mercado
        """
        mercado = moneda+monedaBase

        infoActivo = client.get_asset_balance(moneda)
        comprado = float(infoActivo['free']) + float(infoActivo['locked'])

        if price is not None: 

            porComprar = self.equivalent(moneda,posicion,price) 

        else:

            price = client.get_symbol_ticker(symbol = mercado)

            porComprar = float(price['price'])
            
        porComprarPor = porComprar - (porComprar*0.8)

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
            price=price)
        return order

    def stop_limit_sell(self,moneda,cantidad,price,stop):
        
        mercado = moneda + monedaBase
        order = client.create_order(
            type = 'STOP_LOSS_LIMIT',
            side = 'SELL',
            symbol=mercado,
            quantity=cantidad,
            price=price,
            stopPrice = stop,
            timeInForce = "GTC")

        return order

    def verify_order(self,moneda,order_id):

        time.sleep(3)

        mercado = moneda + monedaBase

        status = client.get_order(
            symbol=mercado,
            orderId=order_id )
        if status['status'] == 'FILLED':
            
            return True
        else :
            return False
        

    def cancelar_orden(self,moneda,order_id):


        mercado = moneda + monedaBase
        client.cancel_order(
            symbol=mercado,
            orderId=order_id)


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

        ctx.prec = 20

        
 
        precio = mejor_precio(orders,cantidad)
        #print(orders)
        precio_str = self.float_to_str(precio)
        return precio_str
        

    def float_to_str(self,f):
            """
            Convert the given float to a string,
            without resorting to scientific notation
            """
            d1 = ctx.create_decimal(repr(f))
            return format(d1, 'f')  


    def open_orders(self,moneda):
        mercado = moneda + monedaBase
        orders = client.get_open_orders(symbol=mercado)
        if not orders:
            vacio = {}
            return vacio
        else:
            dict_order =  orders[0]
            return dict_order['orderId']
        
    def cancel_open_order(self,moneda):
        
        order_id = self.open_orders(moneda)

        if not order_id :
            
            return False

        else : 

            self.cancelar_orden(moneda,order_id)
            print(order_id,'cancelada')

            return True





    def send_email(self,msg,subject):
        """
        Takes all the params to build the email and send it
        """
        fromaddr = mail #from
        toaddrs  = destinatarios #to

        msg = "\r\n".join([
        "From: {}".format(fromaddr),
        "To: {}".format(toaddrs),
        "Subject: {}".format(subject),
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
        
        
        
        

        






