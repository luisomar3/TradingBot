import pandas as pd 
import numpy as np 

from feeders.binanceFeeder import BinanceFeeder
from estrategias.estrategiaadx import EstrategiaAdx
from config import config
umbral = config['umbralOptimizador']

#moneda = config['monedaSimulacion']
feeder = BinanceFeeder()
adx = EstrategiaAdx()

def Backtest():
    
    

    monedasBTC = feeder.get_btc_markets()
    try:
        portafolio = []

        for moneda in monedasBTC:

            velas = feeder.get_candle(moneda)

            analizados = adx.PDI_NDI_Cossover(velas)

            promedio = adx.plot_and_stats(analizados,moneda,plot = False,historico = False)
            print(moneda,promedio)
            
            if promedio['porcentajeAcumulado'] > umbral :
                portafolio.append(moneda)
        
    except Exception as e :
        print('Error analizando {coin}'.format(coin=moneda))    
        
    print('Las siguientes monedas presentan ganancia promedio > a {u}% '.format(u = umbral),portafolio)

if __name__ == '__main__':
    Backtest()