import pandas as pd 
import numpy as np 
import time 
import tqdm
import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
import threading
from timeit import default_timer as timer

from estrategias.estrategiaadx import   EstrategiaAdx
from feeders.binanceFeeder import BinanceFeeder
from accounts.binanceaccount import BinanceAccount
from traders.binancetrader import BinanceTrader 
from config import config

#Iniciar modulos
estrategia = EstrategiaAdx()
feeder = BinanceFeeder()
cuenta = BinanceAccount()
trader = BinanceTrader()
monedas = config['monedas']
scheduler = BlockingScheduler()
posicion = config['posicion'] 
intervalo =  config['interval']
intervals =config['cron_intervals']
frame = config['frame']
crontrigger = intervals[intervalo]



df = pd.DataFrame(columns = ['ID','MONEDA','CANTIDADC','PRECIOC','CANTIDADV','PRECIOV','GANANCIA','GANACIA%'])

def acces():
    """Funcion que habilita el uso de la cuenta
    """
    
    if cuenta.habilitado == True:
        print('Acceso a cuenta exitoso')
        time.sleep(0.5)
        monedaBase, portafolio = cuenta.portafolio(monedas)
        capitalSTR = cuenta.capital()
        capitalINT = float(capitalSTR)
        cliente = cuenta.client
        
        print('\n\n Su posicion es : {optima} BTC por trade'.format(optima = posicion ))
        print('Esperando para iniciar ')
        time.sleep(0.5)
        return cliente
    else:
        return None

def liveTrader(cliente,moneda):

    #print('Actualizando mercado')
    contador = 1
    capital = cuenta.capital()
    
    
    datos = feeder.get_candle(moneda)
    

    capital = cuenta.capital()
    #print(capital)
    pos =  posicion
    cliente = cuenta.client
        
        
    analizados =  estrategia.PDI_NDI_Cossover(datos)
    #|print(analizados[['O','H','L','C','PDI','NDI','signal']])
    senal = estrategia.message(analizados)

    price = analizados['C'].iloc[-1]
        
    valorMoneda = trader.equivalent(moneda,pos,price)
    inTheMarket= trader.in_the_market(moneda,pos,price)
    
    senal = 1
    

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
            trader.send_email(msg)
            print(msg,moneda,'inTheMarket: ',inTheMarket,'signal:',senal,analizados.index[-1])#analizados['signal'].tail(5))#analizados.index[-1])#,analizados['signal'].tail(5).to_string())
        except Exception as e:
            print(e)

    elif (senal == -1) & (inTheMarket == 1 ):

           
        try:
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
        
            
            trader.send_email(msg)

            print(msg,moneda,'inTheMarket: ',inTheMarket,'signal:',analizados.index[-1])#senal,analizados['signal'].tail(5))#,

        except Exception as e:
            print(e)
            

    else:
        
        print('Esperando senal para {coin}'.format(coin = moneda),
                'inTheMarket: ',inTheMarket,'signal:',senal,analizados.index[-1])#analizados['signal'].tail(5))#)



        


def main(acceso):
    """Funcion para ejecutar una orden cada intervalo
    """
    #liveTrader(acceso)
    if frame == 'm':
        scheduler.add_job(run, trigger='cron',
                            minute=crontrigger,args = [acceso])
        print('Revisando senal cada {min} minuto'.format(min = intervalo))
        scheduler.start()
       
    elif frame == 'h': 
        scheduler.add_job(liveTrader, trigger='cron',
                            hour=crontrigger, args=[acceso])
        print('Revisando senal cada {min} hora'.format(min = intervalo))
        scheduler.start()
        
def run(acceso):
    time.sleep(15)
    indice = 1
    print("Actualizando mercado")
    for moneda in monedas:
        indice = indice+1

        thread = threading.Thread(target=liveTrader, args=[acceso,moneda])
        thread.start()
        if indice == 30 : 
            time.sleep(15)
            indice = 1 

    
    

if __name__ == '__main__':
    
    acceso = acces()

    if acceso is not None:
        main(acceso)

