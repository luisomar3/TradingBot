import pandas as pd 
import numpy as np 

from config import config
from basestrategy import BaseStrategy
from indicadores import *

indicadores = Indicadores()

class EstrategiaAdx(BaseStrategy):
    
    def PDI_NDI_Cossover(self,dataFrame):
        """ Estrategia Crossover del ADX, en realidad, usaremos los NDI y PDI para generar las señales de compra/venta

        """
        datos = indicadores.ADX(dataFrame)
        datos = datos.apply(self.crossover,args = ('PDI','NDI'),axis = 1)
        
        return datos