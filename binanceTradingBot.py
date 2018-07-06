import pandas as pd 
import numpy as np 
import time 
import tqdm
import json
import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
import threading
from timeit import default_timer as timer

from estrategias.estrategiaadx import   EstrategiaAdx
from feeders.binanceFeeder import BinanceFeeder
from accounts.binanceaccount import BinanceAccount
from traders.binancetrader import BinanceTrader
from indicadores import Indicadores
from config import config

#Iniciar modulos
adx = EstrategiaAdx()
feeder = BinanceFeeder()
cuenta = BinanceAccount()
trader = BinanceTrader()
indicadores = Indicadores()


if config['estrategia'] == 1:
    estrategia = adx.PDI_NDI_Cossover
elif config['estrategia'] == 2:
    estrategia = adx.AROON_DI_Cossover



#monedas = config['monedas']
scheduler1 = BlockingScheduler()
scheduler2 = BlockingScheduler()
posicion = config['posicion'] 
intervalo =  config['interval']
intervals =config['cron_intervals']
frame = config['frame']
crontrigger = intervals[intervalo]
retraso_m = config['retraso']
retraso = retraso_m * 60
ventana = config['ventana']
periodo = config['ventanaVWMA']
vela = config['velaVWMA']

df = pd.DataFrame(columns = ['ID','MONEDA','CANTIDADC','PRECIOC','CANTIDADV','PRECIOV','GANANCIA','GANACIA%'])

def acces():
    """Funcion que habilita el uso de la cuenta
    """
    
    if cuenta.habilitado == True:
        print('Acceso a cuenta exitoso')
        time.sleep(0.5)
        monedaBase = cuenta.portafolio()
        capitalSTR = cuenta.capital()
        capitalINT = float(capitalSTR)
        cliente = cuenta.client
        
        #print('\n\n Su posicion es : {optima} BTC por trade'.format(optima = posicion ))
        print('Esperando para iniciar ')
        time.sleep(0.5)
        return cliente
    else:
        return None

def liveTrader(cliente,moneda):

    #print('Actualizando mercado')

    capital = cuenta.capital()
    
    
    datos = feeder.get_candle(moneda)
    

    capital = cuenta.capital()
    #print(capital)
    pos =  updatePosicion()

    cliente = cuenta.client
            
    analizados =  estrategia(datos,ventana)
    #print(analizados['signal'].tail(5))
    #analizados['signal'] = analizados['signal'].shift(1)
    #|print(analizados[['O','H','L','C','PDI','NDI','signal']])
    senal = adx.message(analizados)

    price = analizados['C'].iloc[-1]
        
    valorMoneda = trader.equivalent(moneda,pos,price)
    inTheMarket= trader.in_the_market(moneda,pos,price)

    
    if (senal == 1) & (inTheMarket==0) :
            
            
            
        try:


            precio = trader.get_best_price(moneda,'asks',valorMoneda)
            valorMoneda = trader.equivalent(moneda,pos,float(precio))
            verificado = False 
            while verificado == False : 

                compra = trader.limit_buy(moneda,valorMoneda,precio)

                order_id = compra['orderId']
                verificado = trader.verify_order(moneda,order_id)
                if verificado == False :    
                    trader.cancelar_orden(moneda,order_id)
            
            msg = "Se compraron " + str(valorMoneda) + str(moneda) + " a " + str(precio)
            trader.send_email(msg,"COMPRA REALIZADA")
            print(msg,moneda,'inTheMarket: ',inTheMarket,'signal:',analizados.index[-1])#analizados[['PDI','NDI','signal']].tail(2))#analizados[['PDI','NDI','signal']].tail(2))#senal,analizados['signal'].tail(5))#
        except Exception as e:
            print(e)

    elif (senal == -1) & (inTheMarket == 1 ):

           
        try:
            trader.cancel_open_order(moneda)
            info = cliente.get_asset_balance(asset=moneda)
            cantidad  =info['free']
            decimal = trader.decimales(moneda)
            if decimal == 0:
                float_cantidad = int(float(cantidad))
            else:
                float_cantidad = int(float(cantidad) * 10**decimal) / 10.0**decimal
                #print(float_cantidad,"redondeado"," ",cantidad,'decimales')
            
            valorMoneda = float_cantidad
           
            precio = trader.get_best_price(moneda,'bids',valorMoneda)
            
            verificado = False

            while verificado == False : 

                venta = trader.limit_sell(moneda,valorMoneda,precio)
                order_id = venta['orderId']
                verificado = trader.verify_order(moneda,order_id)
                if verificado == False :    
                    trader.cancelar_orden(moneda,order_id)
            

            
            
            msg = "Se vendieron " + str(float_cantidad) + " " + str(moneda) + " a " + str(precio)
        
            
            trader.send_email(msg,"VENTA REALIZADA")

            print(msg,moneda,'inTheMarket: ',inTheMarket,'signal:',analizados.index[-1])##)#analizados[['PDI','NDI','signal']].tail(2))

        except Exception as e:
            print(e)
            

    else:
        
        print('Esperando senal para {coin}'.format(coin = moneda),
                'inTheMarket: ',inTheMarket,'signal:',senal,analizados.index[-1])#analizados[['PDI','NDI','signal']].tail(2))



        


def main(acceso):
    """Funcion para ejecutar una orden cada intervalo
    """
    #liveTrader(acceso)
    if frame == 'm':
        delay_s = int(intervalo) * 60 

        scheduler1.add_job(run, trigger='cron',
                            minute=crontrigger,args = [acceso,delay_s])
        print('Revisando senal cada {min} minuto'.format(min = intervalo))
        #scheduler1.start()
       
    elif frame == 'h': 
        delay_s = int(intervalo) * 60**2
        scheduler1.add_job(run, trigger='cron',
                            minute=crontrigger, args=[acceso,delay_s])
        print('Revisando senal cada {min} hora'.format(min = intervalo))
        #scheduler1.start()

    scheduler1.add_job(run2,trigger='cron',
                            minute=crontrigger, args=[acceso])

    scheduler1.start()

def run(acceso,delay):
    tiempo = delay - retraso
    time.sleep(tiempo)
    
    print("Actualizando mercado para: ")

   
    
    monedas = updateMonedas()
    print(monedas)
    if monedas:
        posiciones = updatePosicion()
        print("Posiciones de : {posicon}".format(posicon = posiciones))
        for moneda in monedas:
            
            thread = threading.Thread(target=liveTrader, args=[acceso,moneda])
            thread.start()
    else:
        print('No hay monedas para trabajar, posible mecardo bajista')
def run2(acceso):

    monedas = updateMonedas()
    if monedas :
        for moneda in monedas:

            thread2 = threading.Thread(target=stopLoss, args=[acceso,moneda])
            thread2.start()
    else:
        print('No hay monedas para trabajar, posible mecardo bajista')
    
def stopLoss(cliente,moneda):


    inTheMarket= trader.in_the_market(moneda,posicion)
    #print(inTheMarket)
    if inTheMarket == 1 :
    
        trader.cancel_open_order(moneda)
        
        velas = feeder.get_candle(moneda)

        vwma = indicadores.VWMA(velas,vela,periodo)

        stopPrice = vwma.iloc[-1]

        decimalPrecio = trader.decimales_precio(moneda)       
        stopPrice =int(float(price) * 10**decimalPrecio) / 10.0**decimalPrecio

        stopPrice = trader.float_to_str(stopPrice)
        
        info = cliente.get_asset_balance(asset=moneda)

        cantidad  =info['free']

        decimal = trader.decimales(moneda)

        if decimal == 0:
            float_cantidad = int(float(cantidad))
        else:
            float_cantidad = int(float(cantidad) * 10**decimal) / 10.0**decimal
            #print(float_cantidad,"redondeado"," ",cantidad,'decimales')
            
        valorMoneda = float_cantidad
        
        price = trader.get_best_price(moneda,'bids',valorMoneda)

        venta = trader.stop_limit_sell(moneda,valorMoneda,price,stopPrice)
        
        print('Stop Loss para {coin} colocado en : {price1} con un precio de venta {venta} '.format(
            price1 = stopPrice,
            coin = moneda,
            venta = price
            ))


def updateMonedas():
    """Funcion para actualizar las monedas desde el archivo de configuracion
    """
    
    with open('config.json', 'r') as f:
        config_monedas = json.load(f)
    return config_monedas["monedas"]


def updatePosicion():
    """Funcion para actualizar las monedas desde el archivo de configuracion
    """
    
    with open('config.json', 'r') as f:
        config_monedas = json.load(f)
    return config_monedas["posicion"]


if __name__ == '__main__':
    
    acceso = acces()

    if acceso is not None:
        main(acceso)

