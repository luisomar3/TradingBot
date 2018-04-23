import pandas as pd 
import numpy as np 

import matplotlib.pyplot as plt 
import matplotlib.dates as mdates
from config import config

import seaborn as sns
sns.set()
sns.axes_style('darkgrid')

window = config['adx_window']

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
        datos['ATR'] = self.promedioMovilExponcial(dfHelper['TR'],window)

       
        
        return datos

    def ADX(self,data):
        """Indicador ADX
        """
        dfHelper = data.copy()
        dfHelper = self.calcularDM(dfHelper)
        dfHelper = self.ATR(dfHelper)

        emaPDM = self.promedioMovilExponcial(dfHelper['PDM'],window)
        emaNDM = self.promedioMovilExponcial(dfHelper['NDM'],window)
        
        data['PDI'] = 100 * ( emaPDM / dfHelper['ATR'])
        #Calcular el indice positivo
        data['NDI'] = 100 * ( emaNDM / dfHelper['ATR'])
        #calcular el indice negativo

        data['shift_PDI'] = data['PDI'].shift(1)
        #creamos una columna con fecha pasada para evaluar el crossover
        data['shift_NDI'] = data['NDI'].shift(1)
        
        
        terminoDividendo= abs(data['PDI']-data['NDI'])
        terminoDivisor = data['PDI'] + data['NDI']

     
        
        dfHelper['dx_calculation'] = 100 * ( terminoDividendo / terminoDivisor)

      

        data['ADX'] = self.promedioMovilExponcial(dfHelper['dx_calculation'],window)
        data['emaC'] = self.promedioMovilExponcial(data['C'],window)

       

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
        
        
        plt.show()

        # plt.plot(resultados.index, resultados['cumsum'])
        # plt.gcf().autofmt_xdate()
        # plt.show()

        return data

