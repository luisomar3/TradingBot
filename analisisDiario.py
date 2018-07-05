import pandas as pd 
import numpy as np 
import json
import time
import os

from feeders.binanceFeeder import BinanceFeeder
from estrategias.estrategiaadx import EstrategiaAdx
from tqdm import tqdm
from traders.binancetrader import BinanceTrader

trader = BinanceTrader()
feeder = BinanceFeeder()
adx = EstrategiaAdx()

estrategia = adx.PDI_NDI_Cossover
path = os.getcwd() + '/config.json'

def Analisis():
    
    
    with open(path, 'r') as f:
        config = json.load(f)
    
    viejas = config['monedas']
    monedasBTC = feeder.get_btc_markets()
    
    try:
        portfolio = []

        for moneda in tqdm(monedasBTC):

            time.sleep(0.3)

            velas = feeder.get_daily_candle(moneda)

            analizados = estrategia(velas)

            prueba = adx.message(analizados)
            
            if prueba == 1 :
                portfolio.append(moneda)

            #analizados = adx.AROON_DI_Cossover(velas)

        
        config['monedas'] = portfolio
        
        actuales = set(config['monedas'])
        extraidas = [x for x in viejas if x not in actuales]
        



        with open(path, 'w') as f:
            json.dump(config, f)    

        msg = "El analisis diario arrojo las siguientes monedas: {lista_monedas} Y se extrajeron {extract}".format(

            lista_monedas = portfolio,
            extract = extraidas)

        trader.send_email(msg,"Analis diario")
    except Exception as e :
        print('Error analizando',e)    
        
    

if __name__ == '__main__':
    Analisis()