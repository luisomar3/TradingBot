import pandas as pd 
import numpy as np 

import matplotlib.pyplot as plt 
import matplotlib.dates as mdates
from config import config

import seaborn as sns
sns.set()
sns.axes_style('darkgrid')

window = config['ventana']

class Indicadores():
    """Esta clase contiene todos los indicadores disponibles en el sistema. Seran pasados
    a la estrategia como parametros
    Ejemplo:
        adx = indicadores.adx()
        estrategia_adx = estrategia(adx)
    """


    def promedioMovilExponcial(self, valores, ventana):
        """Promedio movil exponencial
        :parametro valores: DataFrame que contiene los datos a los cuales se les aplicará el promedio movil.
        :tipo valores: pd.DataFrame

        :parametro ventana: Número de dias en los cuales el EMA mirará.
        :tipo ventana: int.

            Ejemplo:

                datos = datosETH-BTC.
                EMA12 = promedioMovilExponencial(datos,12)
            """
        weights = np.exp(np.linspace(-1., 0., ventana))
        weights /= weights.sum()
        a = np.convolve(valores, weights, mode='full')[:len(valores)]
        a[:ventana] = a[ventana]

        return a

    def macd(self,data):
        """ Indicador MACD, el cual necesita los datos en formato DOHLCV
        :parametro data: DataFrame con los datos requeridos.
        :tipo data: pd.DataFrame
            Ejemplo:
            dfMacd = macd(datos)

        """
        data_macd = data
        data_macd['ema_12_macd'] = self.promedioMovilExponcial(data['C'],12)
        data_macd['ema_26_macd'] = self.promedioMovilExponcial(data['C'],26)
        data_macd['macd'] = data['ema_12_macd'] - data['ema_26_macd']
        return data_macd
    
    def calcularDM(self,data):
        """Parte de la estretegia ADX
        """
        previusHigh = data['H'].shift(1)
        previusLow = data['L'].shift(1)

        moveUp = data['H'] - previusHigh
        moveDown = data['L'] - previusLow

        data['PDM'] = np.where( (moveUp > 0 ) & (moveUp > moveDown),moveUp,0)
        data['NDM'] = np.where( (moveDown > 0 ) & (moveDown > moveUp),moveDown,0)

        return data


    def ATR(self,datos):
        """ Promedio del rango verdadero, es un instrumento que nos mide la volatilidad del activo.

        """

        dfHelper = datos.copy()
        dfHelper['PC'] = dfHelper['C'].shift(1)

        dfHelper['CH-CL'] = dfHelper['H'] - dfHelper['L']
        dfHelper['CH-PC'] = abs(dfHelper['H'] - dfHelper['PC'])
        dfHelper['CL-PC'] = abs(dfHelper['L'] - dfHelper['PC'])

        dfHelper['TR'] = dfHelper[['CH-CL','CH-PC','CL-PC']].max(axis=1)
        datos['TR'] = dfHelper['TR']
        datos['ATR'] = self.promedioMovilExponcial(dfHelper['TR'],window)
        datos['ATR2'] = dfHelper['TR'].rolling(window).mean()
        datos['ATR3'] = dfHelper['TR'].ewm(span=window,adjust = False).mean()
       
        
        return datos

    def ADX(self,data):
        """Indicador ADX
        """
        dfHelper = data.copy()
        dfHelper = self.calcularDM(dfHelper)
        dfHelper = self.ATR(dfHelper)

        #dfHelper['emaPDM'] = dfHelper['PDM'].ewm(span=window,adjust = False).mean()
        dfHelper['emaPDM'] = dfHelper['PDM'].rolling(window).mean()
        dfHelper['shifted_ema_pdm'] = dfHelper['emaPDM'].shift(1)
        dfHelper['smoothedPDM'] = dfHelper['shifted_ema_pdm'] - (dfHelper['shifted_ema_pdm']/window) + dfHelper['emaPDM']
        
        
        #dfHelper['emaNDM'] = dfHelper['NDM'].ewm(span=window,adjust = False).mean()
        dfHelper['emaNDM'] =  dfHelper['NDM'].rolling(window).mean()
        dfHelper['shifted_ema_ndm'] = dfHelper['emaNDM'].shift(1)
        dfHelper['smoothedNDM'] = dfHelper['shifted_ema_ndm'] - (dfHelper['shifted_ema_ndm']/window) + dfHelper['emaNDM']


        dfHelper['shifted_TR'] = dfHelper['ATR2'].shift(1)
        smoothedTR = dfHelper['shifted_TR'] - (dfHelper['shifted_TR']/window) + dfHelper['ATR2']

       
        #print(dfHelper[['emaPDM','shifted_ema_pdm','smoothedPDM','emaNDM','shifted_ema_ndm','smoothedNDM']].to_string())
        # data['PDI'] = 100 * ( emaPDM / dfHelper['ATR2'])
        # #Calcular el indice positivo
        # data['NDI'] = 100 * ( emaNDM / dfHelper['ATR2'])
        # #calcular el indice negativo


        data['PDI'] = 100 * (dfHelper['smoothedPDM'] / smoothedTR)

        data['NDI'] = 100 * (dfHelper['smoothedNDM']/ smoothedTR)

        data['shift_PDI'] = data['PDI'].shift(1)
        #creamos una columna con fecha pasada para evaluar el crossover
        data['shift_NDI'] = data['NDI'].shift(1)
        
        
        terminoDividendo= abs(data['PDI']-data['NDI'])
        terminoDivisor = data['PDI'] + data['NDI']

     
        
        dfHelper['dx_calculation'] = 100 * ( terminoDividendo / terminoDivisor)

      

        #data['ADX'] = self.promedioMovilExponcial(dfHelper['dx_calculation'],window)
        data['ADX'] =   dfHelper['dx_calculation'].rolling(window).mean()
        data['emaC'] = self.promedioMovilExponcial(data['C'],window)

        
        return data

