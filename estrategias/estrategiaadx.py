import pandas as pd 
import numpy as np 

import time

from config import config
from estrategias.basestrategy import BaseStrategy
from indicadores import *

indicadores = Indicadores()

class EstrategiaAdx(BaseStrategy):
    
    def PDI_NDI_Cossover(self,dataFrame):
        """ Estrategia Crossover del ADX, en realidad, usaremos los NDI y PDI para generar las señales de compra/venta

        """
        datos = dataFrame.copy()
        datos = indicadores.ADX(datos)
        datos['signal'] = datos.apply(self.crossover,args = ('PDI','NDI'),axis = 1)
        
        return datos

    def plot(self,data):
        """Grafica la estrategia
        """
        f2, ax2 = plt.subplots(nrows =2,ncols=1,figsize = (8,4),sharex=True)
        f2.suptitle("ETH-BTC Pair")
        ax2[0].plot(data.index, data['C'], color = 'black', lw=2, label='Close')
        ax2[0].plot(data.index, data['emaC'], color = 'red', lw =3, label = "Ema window ")

        ax2[1].plot(data.index, data['PDI'], color='green', lw=1,label='PDI')
        ax2[1].plot(data.index, data['NDI'], color='red', lw=1, label='NDI')
        ax2[1].plot(data.index, data['ADX'], color = 'gray', alpha=0.5, label='ADX')          
        
        
        ax2[0].legend(loc = 'upper left')
        ax2[1].legend(loc = 'upper left')
        plt.gcf().autofmt_xdate()
        
        
        plt.show(block=False)

        time.sleep(20)
        plt.close()
        

        # plt.plot(resultados.index, resultados['cumsum'])
        # plt.gcf().autofmt_xdate()
        # plt.show()