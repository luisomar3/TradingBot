import pandas as pd 
import numpy as np 

import time

from config import config
from estrategias.basestrategy import BaseStrategy
from indicadores import *


monedaBase = config['MonedaBase']
capital = config['capitalSimulacion']
indicadores = Indicadores()

class EstrategiaAdx(BaseStrategy):
    def __init__(self):
        self.name = 'Estrategia : ADX'

    
    def PDI_NDI_Cossover(self,dataFrame):
        """ Estrategia Crossover del ADX, en realidad, usaremos los NDI y PDI para generar las señales de compra/venta

        """
        datos = dataFrame.copy()
        datos = indicadores.ADX(datos)
        datos['signal'] = datos.apply(self.crossover,args = ('PDI','NDI'),axis = 1)
        
        return datos

    def plot_and_stats(self,data1,moneda,plot=True,historico=True):
        """Grafica la estrategia
        """
        mercado = moneda+monedaBase
        data = data1.copy()
        compra= data[data['signal']==1][3:]
        venta = data[data['signal']==-1][3:]
        df_compras = pd.DataFrame()

        df_compras['compras']= compra['C']
        df_compras['comprasMoneda'] = capital/df_compras['compras']
        df_compras = df_compras.reset_index()
        df_compras = df_compras.rename({'datetime':'datetimecompras'},axis='columns')

        df_ventas = pd.DataFrame()

        df_ventas['ventas']  = venta['C']
        #df_ventas['ventasMoneda'] = capital/df_ventas['ventas']
        df_ventas = df_ventas.reset_index()

        dfProfit = pd.DataFrame()
        dfProfit = pd.concat([df_compras,df_ventas],ignore_index = False, axis = 1)
        dfProfit['total'] = (dfProfit['ventas']-dfProfit['compras'])
        nombre = 'cantidad'+moneda
        dfProfit[nombre] = capital/dfProfit['compras']
        dfProfit['cantidadBTC'] = dfProfit[nombre] * dfProfit['ventas']
        dfProfit['porcentajeBTC'] = ((dfProfit['cantidadBTC']*100) / capital)- 100
        dfProfit['cumsumPorcentaje'] = dfProfit['porcentajeBTC'].cumsum()
        dfProfit['gananciasBTC'] = dfProfit['cantidadBTC'] - capital 
        dfProfit['acumuladoGanancias'] = dfProfit['gananciasBTC'].cumsum()
        #dfProfit['monedaTotal'] = (dfProfit['ventasMoneda']-dfProfit['comprasMoneda'])
        dfProfit['cumsum'] = dfProfit['total'].cumsum()
        
        #dfProfit['cumsumCapital'] = dfProfit['monedaTotal'].cumsum()
        
        if historico == True:
            print(dfProfit[['compras',nombre,'ventas','cantidadBTC'
            ,'porcentajeBTC','datetime','cumsumPorcentaje','gananciasBTC','acumuladoGanancias']].to_string())
            
        numeroOperaciones = len(compra) + len(venta)
        
        averageGanancias = dfProfit['gananciasBTC'].mean()
        averagePorcentaje = dfProfit['porcentajeBTC'].mean()
        maximaGanancia = dfProfit['gananciasBTC'].max()
        maximaPerdida = dfProfit['gananciasBTC'].min()
        
        averages = {
            'averageGanancias':averageGanancias,
            'averagePorcentaje':averagePorcentaje,
            'maximaGanancia':maximaGanancia,
            'maximaPerdida':maximaPerdida,
            'numeroDeOperaciones':numeroOperaciones
            
            }
         
        
        if plot == True:
            f2, ax2 = plt.subplots(nrows =2,ncols=1,figsize = (8,4),sharex=True)
            f2.suptitle(mercado)
            ax2[0].plot(data.index, data['C'], color = 'black', lw=2, label='Close')
            #ax2[0].plot(data.index, data['emaC'], color = 'red', lw =3, label = "Ema window ")

            ax2[1].plot(data.index, data['PDI'], color='green', lw=1,label='PDI')
            ax2[1].plot(data.index, data['NDI'], color='red', lw=1, label='NDI')
            ax2[1].plot(data.index, data['ADX'], color = 'gray', alpha=0.5, label='ADX')          
            

            #print(venta)
            ax2[0].plot(compra.index, compra['C'], 'go--', linewidth=0.01, markersize=5,label = 'COMPRA')
            ax2[0].plot(venta.index, venta['C'], 'ro--', linewidth=0.01, markersize=5,label = 'VENTA')
            

            ax2[0].legend(loc = 'upper left')
            ax2[1].legend(loc = 'upper left')

            plt.gcf().autofmt_xdate()
            
            
            plt.show()

            plt.plot(dfProfit['datetime'], dfProfit['acumuladoGanancias'],label = ' Ganancias Acumuladas')
            plt.gcf().autofmt_xdate()
            plt.show()
        
        return averages