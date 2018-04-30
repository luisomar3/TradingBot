import pandas as pd 
import numpy as np 
import datetime 

from apscheduler.schedulers.blocking import BlockingScheduler


from indicadores import *
from feeders.binanceFeeder import BinanceFeeder
from binance.client import Client

from estrategias.basestrategy import BaseStrategy
from estrategias.estrategiaadx import EstrategiaAdx

from config import config
coin = config['coin']

intervalo = config['interval']
#cronInterval = config['cron_intervals']
#cronTrigger = cronInterval[intervalo]
#configuracion de los intervalos de CRON para la ejecucion de trader

myStrategy = BaseStrategy()
adxStrategy = EstrategiaAdx()
myBinance = BinanceFeeder()
miIndicador = Indicadores()

scheduler = BlockingScheduler()

contador = 0

def run():
    print("Actualizando...")
    candles = myBinance.get_candle(coin)
    global contador
    contador +=1
    
    
        
    print(contador)
    a = adxStrategy.PDI_NDI_Cossover(candles)
    print(a.to_string())
    if contador == 15:
        #adxStrategy.plot(a)
        print(a.to_string())
        contador = 0

    b = adxStrategy.message(a)
    print(b.to_string(header = False,dtype=False))

def main():
    
    scheduler.add_job(run, trigger='cron',
                          minute=cronTrigger)#, args=[markets])
    scheduler.start()

if __name__ == '__main__':
    
    run()

        
    