import pandas as pd 
import numpy as np 
from ta import *
import talib
#import matplotlib.pyplot as plt 
#import matplotlib.dates as mdates
from config import config

# import seaborn as sns
# sns.set()
# sns.axes_style('darkgrid')
modo =  config['modo']
window = config['ventana']
windowAroon = config['ventanaAroon']

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
        datos['shiftedTR'] = datos['TR'].shift(1)

        datos['smoothedTR'] = datos['shiftedTR'] - (datos['shiftedTR']/window) + datos['TR']

        

        datos['ATR'] = self.promedioMovilExponcial(dfHelper['TR'],window)
        datos['ATR2'] = datos['smoothedTR'].rolling(14).mean()
        #datos['ATR3'] = dfHelper['TR'].ewm(span=window,adjust = False).mean()
       
        
        return datos

    def ADX(self,data):
        """Indicador ADX
        """
        
        data['ADX'] = adx(data['H'],data['L'],data['C'], n = window, fillna = False )  
        data['NS_PDI'] = adx_pos(data['H'],data['L'],data['C'], n = window, fillna = False)
        
        data['PDI'] = data['NS_PDI'].shift() - (data['NS_PDI'].shift()/window) + data['NS_PDI']
        
        
        data['NS_NDI'] = adx_neg(data['H'],data['L'],data['C'], n = window, fillna = False) 
        
        data['NDI'] = data['NS_NDI'].shift() - (data['NS_NDI'].shift()/window) + data['NS_NDI']
        if modo == 1 :
            data['PDI'] = data['PDI'].shift(-1)
            data['NDI'] = data['NDI'].shift(-1)
            
        data['shift_PDI'] = data['PDI'].shift()
        data['shift_NDI'] = data['NDI'].shift()
        return data

    def talib_ADX(self,data):
        """Version de Talib del ADX, esperando perfeccion
        """
        df = data.copy()

        df['ADX'] = talib.ADX(df['H'],df['L'],df['C'], timeperiod=window)

        df['PDI'] = talib.PLUS_DI(df['H'],df['L'],df['C'], timeperiod=window)
        df['shift_PDI'] = df['PDI'].shift(1)
        
        df['NDI'] =  talib.MINUS_DI(df['H'],df['L'],df['C'], timeperiod=window)
        df['shift_NDI'] = df['NDI'].shift(1)
        
        return df

    def talib_ADX_atrasado(self,data):
        """Version de Talib del ADX, con un periodo atrasado
        :param data: dataFrame que contiene las velas
        :type data: pd.DataFrame

        :param retraso: Numero de velas para retrasar
        :type retraso: Int
        
        """
        df = data.copy()

        df['ADX'] = talib.ADX(df['H'],df['L'],df['C'], timeperiod=window)

        df['PDI'] = talib.PLUS_DI(df['H'],df['L'],df['C'], timeperiod=window)
        df['PDI'] = df['PDI'].shift(-1)
        df['shift_PDI'] = df['PDI'].shift(1)
        
        df['NDI'] =  talib.MINUS_DI(df['H'],df['L'],df['C'], timeperiod=window)
        df['NDI'] = df['NDI'].shift(-1)
        df['shift_NDI'] = df['NDI'].shift(1)
        
        return df

    def VWMA(self,df,kline,ventana):
        """ Media movil ponderada por volumen
        """
        data = df.copy()
        price = data[kline]
        volume = data['V']
        volumexprice = price * volume
        #print(type(price))
        #print(type(volume))
        #print(type(volumexprice))
        data['VMA'] = volumexprice.rolling(ventana).mean() / volume.rolling(ventana).mean()
 

        return data['VMA']

    def aroon(self,df):
        """ Indicador Aroon

        """
        data = df.copy()

        data['aroonDown'],data['aroonUp'] = talib.AROON(data['H'],data['L'],windowAroon)
        data['shift_aroonDown'] = data['aroonDown'].shift()
        data['shift_aroonUp'] = data['aroonUp'].shift()

        return data