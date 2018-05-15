import pandas as pd 
import numpy as np 

from feeders.binanceFeeder import BinanceFeeder
from estrategias.estrategiaadx import EstrategiaAdx
from config import config

moneda = config['monedaSimulacion']
feeder = BinanceFeeder()
adx = EstrategiaAdx()

def Backtest():
    
    velas = feeder.get_candle(moneda)

    analizados = adx.PDI_NDI_Cossover(velas)


    promedio = adx.plot_and_stats(analizados,moneda,plot = True,historico = False)

    print(promedio)

if __name__ == '__main__':
    Backtest()
