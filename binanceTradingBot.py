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
        posicion = capitalINT / len(monedas)
        print('\n\n Su posicion optima es : {optima} BTC por trade'.format(optima = posicion))
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
        capitalSTR = cuenta.capital()
        capitalINT = float(capitalSTR)
        cliente = cuenta.client
        posicion = capitalINT / len(monedas)
        montoMoneda = cuenta.inTheMarket(posicion,moneda)
        print(montoMoneda)
        priunt(type(montoMoneda))
        analizados =  estrategia.PDI_NDI_Cossover(datos)
        #print(analizados)
        señal = estrategia.message(analizados)
        price = analizados['C'].iloc[-1]
        
        valorMoneda = trader.equivalent(posicion,price)

        if señal == 1 & (posicion >= montoMoneda)  :
            
            print('compré {coin}'.format(coin = moneda))
            
            try:
                print(valorMoneda)
                compra = trader.market_buy(moneda,valorMoneda)
            except Exception as e:
                print(e.message)

        elif señal == -1  :

            print('vendí {coin}'.format(coin = moneda))
            try:
                print(valorMoneda)
                venta = trader.market_sell(moneda,valorMoneda)
            except Exception as e:
                print(e.message)
            

        else:
            print('Esperando Señal para {coin}'.format(coin = moneda))
            row = {'MONEDA': moneda,'CANTIDADC' : valorMoneda ,'PRECIOC' : price}
            df = df.append(row,ignore_index = True)
            print(df)


        


def main(acceso):
    """Funcion para ejecutar una orden cada intervalo
    """

    scheduler.add_job(liveTrader, trigger='cron',
                          minute='*/5', args=[acceso])
    scheduler.start()

if __name__ == '__main__':
    
    acceso = acces()

    if acceso is not None:
        main(acceso)

