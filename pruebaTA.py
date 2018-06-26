import pandas as pd 
import numpy as np 

from feeders.binanceFeeder import BinanceFeeder
from estrategias.estrategiaadx import EstrategiaAdx
from indicadores import Indicadores
from config import config
import matplotlib.pyplot as plt 

indi = Indicadores()
moneda = config['monedaSimulacion']
feeder = BinanceFeeder()
adx = EstrategiaAdx()

def Backtest():
    
    velas = feeder.get_candle(moneda)
    #print(velas)
    #a = indi.talib_ADX(velas)
    #print(a)
    #a.plot(x=a.index, y=["ADX", "PDI", "NDI"])
    
    #plt.show()
    analizados = adx.PDI_NDI_Cossover(velas)
    
    analizados.to_csv('NANO-12PERIODOS-30m-CONOPERACIONES.csv')
    
    print(analizados)

    #promedio = adx.plot_and_stats(analizados,moneda,plot = True,historico = False)

    #print(promedio)

if __name__ == '__main__':
    Backtest()
