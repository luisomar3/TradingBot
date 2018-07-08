import pandas as pd 
import numpy as np 

from feeders.binanceFeeder import BinanceFeeder
from estrategias.estrategiaadx import EstrategiaAdx
from config import config
umbral = config['umbralOptimizador']
ventana = config['ventana']
#moneda = config['monedaSimulacion']
feeder = BinanceFeeder()
adx = EstrategiaAdx()
if config['estrategia'] == 1:
    estrategia = adx.PDI_NDI_Cossover
elif config['estrategia'] == 2:
    estrategia = adx.AROON_DI_Cossover
elif config['estrategia'] == 3 :
    estrategia = adx.adxCrossover_AroonPositive
elif config['estrategia'] == 4 :
    estrategia = adx.adxCrossover_Aroon100
def Backtest():
    
    

    monedasBTC = feeder.get_btc_markets()
    try:
        portafolio = []
        porcentajeTotal = []
        for moneda in monedasBTC:

            velas = feeder.get_candle(moneda)

            analizados = estrategia(velas,ventana)
            #analizados = adx.AROON_DI_Cossover(velas)

            promedio = adx.plot_and_stats(analizados,moneda,plot = False,historico = False)
            print(moneda,promedio)
            
            porcentajeTotal.append(promedio['porcentajeAcumulado'])
            if promedio['porcentajeAcumulado'] > umbral :
                portafolio.append(moneda)
        
    except Exception as e :
        print('Error analizando {coin}'.format(coin=moneda))    
        
    print('Las siguientes monedas presentan ganancia promedio > a {u}% '.format(u = umbral),portafolio)
    suma = sum(porcentajeTotal)
    print(suma,'porcentajeTotal')
if __name__ == '__main__':
    Backtest()