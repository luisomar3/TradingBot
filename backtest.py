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
    #velas = velas.shift(-1)
    analizados = adx.PDI_NDI_Cossover(velas)
    #print(analizados[['O','H','L','C','V','PDI','NDI']].to_string())

    promedio = adx.plot_and_stats(analizados,moneda,plot = True,historico = False)

    print(promedio)

if __name__ == '__main__':
    Backtest()
