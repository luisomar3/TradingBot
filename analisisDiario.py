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
path_miconfig = os.getcwd() + '/config_diario.json'
path = os.getcwd() + '/config.json'

with open(path_miconfig, 'r') as f:
        config_general = json.load(f)

ventana = config_general['ventana']

def Analisis():
    
    
    with open(path, 'r') as f:
        config = json.load(f)
    
    actuales = config['monedas']
    viejas = list(actuales)
    monedasBTC = feeder.get_btc_markets()
    
    try:
        portfolio = []

        for moneda in tqdm(monedasBTC):

            time.sleep(0.3)

            velas = feeder.get_daily_candle(moneda)

            analizados = estrategia(velas,ventana)
           
            prueba = adx.message(analizados)

            if (prueba == 1) & (moneda not in actuales):
                actuales.append(moneda)
            if (prueba == -1) & (moneda in actuales) :
                actuales.remove(moneda)

            #analizados = adx.AROON_DI_Cossover(velas)

        
        config['monedas'] = actuales
        
        actuales = set(config['monedas'])
        extraidas = [x for x in viejas if x not in actuales]
        
        


        with open(path, 'w') as f:
            json.dump(config, f)    
        

        msg = "El analisis diario arrojo las siguientes monedas: {lista_monedas} Y se extrajeron {extract}".format(

            lista_monedas = actuales,
            extract = extraidas)

        trader.send_email(msg,"Analis diario")
    except Exception as e :
        print('Error analizando',e)    
        
    

if __name__ == '__main__':
    Analisis()