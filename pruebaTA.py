import pandas as pd 
import numpy as np 

from feeders.binanceFeeder import BinanceFeeder
from estrategias.estrategiaadx import EstrategiaAdx
from indicadores import Indicadores
from config import config
from traders.binancetrader import BinanceTrader
import matplotlib.pyplot as plt 
import talib

indi = Indicadores()
moneda = config['monedaSimulacion']
feeder = BinanceFeeder()
adx = EstrategiaAdx()
trader = BinanceTrader()

def Backtest():
    
    velas = feeder.get_candle('ETH')
    
    #ordenes = trader.open_orders('SNM')
    #trader.cancel_open_order('SNM')
    #print(velas['H'].head(5) )

   # velas['H'].iloc[0] = 22

    #print(velas['H'].head(5))
    analizados = adx.AROON_DI_Cossover(velas)

    #print(b.to_string())
    #c = a & b
   # print(analizados.tail(10))
    print(analizados[['signalDM','signalAroon','signal']].to_string())
    #print(velas.index)
    #print(aroonUp,aroonDown)
    # plt.plot(velas.index, aroonUp, color = 'green')
    # plt.plot(velas.index,aroonDown, color = 'red')

    # plt.show()
    




    #VMA = indi.VWMA(velas,'C',20)
    #print(velas['C'].tail(10))
    #print(VMA.tail(10))

    #ultimo = VMA.iloc[-1]
    #print(ultimo)
    #analizados = adx.PDI_NDI_Cossover(velas)
    #print(analizados.tail(10))
    #archivo = analizados[['O','H','L','C','stopLoss','signal','salidasStopLoss']]
    #archivo.to_csv('OperacionesConStopLoss.csv')
    #print(velas)
    #a = indi.talib_ADX(velas)
    #print(a)
    #a.plot(x=a.index, y=["ADX", "PDI", "NDI"])
    
    #plt.show()
    #
    
    #analizados
    
    #print(analizados)
    #analizados.plot(x = analizados.index , y = ['PDI','NDI'])
    #plt.show()
    #promedio = adx.plot_and_stats(analizados,moneda,plot = True,historico = False)

    #print(promedio)



def stopLoss():


    inTheMarket = trader.in_the_market('BNB',pos)

    
    

if __name__ == '__main__':
    Backtest()
