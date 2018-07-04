import pandas as pd 
import numpy as np 

from feeders.binanceFeeder import BinanceFeeder
from estrategias.estrategiaadx import EstrategiaAdx
from config import config

moneda = config['monedaSimulacion']
feeder = BinanceFeeder()
adx = EstrategiaAdx()
if config['estrategia'] == 1:
    estrategia = adx.PDI_NDI_Cossover
elif config['estrategia'] == 2:
    estrategia = adx.AROON_DI_Cossover
def Backtest():
    
    velas = feeder.get_candle(moneda)
    #velas = velas.shift(-1)
    #analizados = adx.PDI_NDI_Cossover(velas)
    analizados = estrategia(velas)
    #print(analizados[['O','H','L','C','V','PDI','NDI']].to_string())
    #print(analizados['signal'])
    promedio = adx.plot_and_stats(analizados,moneda,plot = False,historico = True)

    print(promedio)

if __name__ == '__main__':
    Backtest()
