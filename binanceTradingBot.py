import pandas as pd 
import numpy as np 
import time 
import tqdm

from apscheduler.schedulers.blocking import BlockingScheduler

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

def liveTrader(cliente):

    print('Actualizando mercado')
    contador = 1
    capital = cuenta.capital()
    
    for moneda in monedas:
        datos = feeder.get_candle(moneda)
        #datos = datos.shift(-1)

        capital = cuenta.capital()
        #print(capital)
        pos =  posicion
        cliente = cuenta.client
        
        
        analizados =  estrategia.PDI_NDI_Cossover(datos)
        #print(analizados[['O','H','L','C','PDI','NDI','signal']])
        señal = estrategia.message(analizados)

        price = analizados['C'].iloc[-2]
        
        valorMoneda = trader.equivalent(pos,price)
        inTheMarket= trader.in_the_market(moneda,pos,price)
        #print(inTheMarket,'inTheMarket')
        #print(señal,'signal')
        print(analizados.index[-1])
        if (señal == 1) & (inTheMarket==0) :
            
            
            
            try:

                msg = "Se compraron " + str(valorMoneda) + str(moneda) + " a " + str(price)
                print(msg)
                print(analizados.index[-1])
                compra = trader.market_buy(moneda,valorMoneda)
                trader.send_email(msg)
            except Exception as e:
                print(e)

        elif (señal == -1) & (inTheMarket == 1 ):

           
            try:
                info = cliente.get_asset_balance(asset=moneda)
                cantidad  =info['free']
                float_cantidad = int(float(cantidad) * 10**2) / 10.0**2
                #print(float_cantidad,"redondeado"," ",cantidad,'decimales')
                venta = trader.market_sell(moneda,float_cantidad)

                msg = "Se vendieron " + str(float_cantidad) + " " + str(moneda) + " a " + str(price)
                print(msg)
                print(analizados.index[-1])
                trader.send_email(msg)
                
                #print('Se vendieron {cantidad} {coin} a {precio}'.format(
                #  cantidad = float_cantidad, coin = moneda, precio = price))

            except Exception as e:
                print(e)
            

        else:
            print('Esperando Señal para {coin}'.format(coin = moneda))



        


def main(acceso):
    """Funcion para ejecutar una orden cada intervalo
    """
    liveTrader(acceso)
    scheduler.add_job(liveTrader, trigger='cron',
                          minute=crontrigger, args=[acceso])
    scheduler.start()

if __name__ == '__main__':
    
    acceso = acces()

    if acceso is not None:
        main(acceso)

