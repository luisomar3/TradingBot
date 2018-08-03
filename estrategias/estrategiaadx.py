import pandas as pd 
import numpy as np 

import time
from time import gmtime, strftime
from config import config
from estrategias.basestrategy import BaseStrategy
from indicadores import *


monedaBase = config['MonedaBase']
capital = config['capitalSimulacion']
indicadores = Indicadores()

class EstrategiaAdx(BaseStrategy):
    def __init__(self):
        self.name = 'Estrategia : ADX'

    
    def PDI_NDI_Cossover(self,dataFrame,ventana):
        """ Estrategia Crossover del ADX, en realidad, usaremos los NDI y PDI para generar las señales de compra/venta

        """
        datos = dataFrame.copy()
        #datos['stopLoss'] =  indicadores.VWMA(datos,'L',12) incluir para hacer simulacion con stopLoss

        datos = indicadores.talib_ADX(datos,ventana)
        datos['signal'] = datos.apply(self.crossover,args = ('PDI','NDI'),axis = 1)
        #datos['salidasStopLoss']  = np.where(datos['stopLoss'] > datos['L'],-1,0)  
        
        for index,row in datos['signal'].iteritems():
            if (row!=0) & (row==-1):
                #print(row,'primer valor venta')
                datos.drop(index, inplace=True)
                break
            
            if (row!=0) & (row== 1):
                #print(row,'primer valor c')
                break
        #print(len(datos))
        return datos

    def AROON_DI_Cossover(self,dataFrame,ventana):
        """ Estrategia Crossover del ADX, en realidad, usaremos los NDI y PDI para generar las señales de compra/venta

        """
        datos = dataFrame.copy()
        #datos['stopLoss'] =  indicadores.VWMA(datos,'L',12) incluir para hacer simulacion con stopLoss

        datos = indicadores.talib_ADX(datos,ventana)
        datos = indicadores.aroon(datos)
        datos['signalDM'] = datos.apply(self.crossover,args = ('PDI','NDI'),axis = 1)
        datos['signalAroon'] = datos.apply(self.crossover,args = ('aroonUp','aroonDown'),axis = 1)
        #datos['salidasStopLoss']  = np.where(datos['stopLoss'] > datos['L'],-1,0)  
        datos = self.del_primera_venta(datos,'signalDM')
        datos = self.del_primera_venta(datos,'signalAroon')
        datos['signal'] = datos.apply(self.two_entry_signals_and,args = ('DM','Aroon'),axis = 1 )
        
        
        datos = self.extraer_salidas(datos)
        #print(len(datos))
        return datos

    
    def adxCrossover_AroonPositive(self,dataFrame,ventana):

        datos = dataFrame.copy()

        datos = indicadores.talib_ADX(datos,ventana)
        datos = indicadores.aroon(datos)
        datos['signalDM'] = datos.apply(self.crossover,args = ('PDI','NDI'),axis = 1)
        datos['signalAroon'] = datos.apply(self.posMayorQueNeg,args = ('aroonUp','aroonDown'), axis = 1)
        
        datos = self.del_primera_venta(datos,'signalDM')
        datos = self.del_primera_venta(datos,'signalAroon')
        
        datos['signal'] = datos.apply(self.two_entry_signals_and,args = ('DM','Aroon'),axis = 1 )
        
        
        datos = self.extraer_salidas(datos)

        return datos 


    def adxCrossover_Aroon100(self,dataFrame,ventana):

        datos = dataFrame.copy()

        datos = indicadores.talib_ADX(datos,ventana)
        datos = indicadores.aroon(datos)
        datos['signalDM'] = datos.apply(self.crossover,args = ('PDI','NDI'),axis = 1)
        datos['signalAroon'] = datos.apply(self.aroon100,args = ('aroonUp','aroonDown'), axis = 1)
        
        datos = self.del_primera_venta(datos,'signalDM')
        datos = self.del_primera_venta(datos,'signalAroon')
        
        datos['signal'] = datos.apply(self.two_entry_signals_and,args = ('DM','Aroon'),axis = 1 )
        
        
        datos = self.extraer_salidas(datos)

        return datos 


    def adxCrossover_AroonPositive_daily(self,dataframeInterval,dataFrameDaily,ventana):
        
        datos = dataframeInterval.copy()
        datos2 = dataFrameDaily.copy()

        porIntervalos = self.adxCrossover_AroonPositive(datos,ventana)
        
        porDia = self.PDI_NDI_Cossover(datos2,12)
        
        

        #diarios = 
        analizados = estrategia(velas,ventana)
        datos['signalDM'] = datos.apply(self.crossover,args = ('PDI','NDI'),axis = 1)
        datos['signalAroon'] = datos.apply(self.aroon100,args = ('aroonUp','aroonDown'), axis = 1)








    def plot_and_stats(self,data1,moneda,plot=True,historico=True):
        """Grafica la estrategia
        """
        mercado = moneda+monedaBase
        data = data1.copy()
        compra= data[data['signal']==1]
        venta = data[data['signal']==-1]    

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
        dfProfit['porcentajeBTC']
        dfProfit['cumsumPorcentaje'] = dfProfit['porcentajeBTC'].cumsum()
        dfProfit['gananciasBTC'] = dfProfit['cantidadBTC'] - capital 
        dfProfit['acumuladoGanancias'] = dfProfit['gananciasBTC'].cumsum()
        #dfProfit['monedaTotal'] = (dfProfit['ventasMoneda']-dfProfit['comprasMoneda'])
        dfProfit['cumsum'] = dfProfit['total'].cumsum()
        fecha = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        path = 'Backtest/' +moneda + '-' + fecha +  '.csv'
        dfProfit.dropna(inplace = True) 
        dfProfit.to_csv(path, sep = ',')
        #dfProfit['cumsumCapital'] = dfProfit['monedaTotal'].cumsum()
        
        if historico == True:
            print(dfProfit[['compras',nombre,'ventas','porcentajeBTC','datetime','cumsumPorcentaje','gananciasBTC','acumuladoGanancias']])
            pass
        numeroOperaciones = int((len(compra) + len(venta))/2)
        
        averageGanancias = dfProfit['gananciasBTC'].mean()
        averagePorcentaje = dfProfit['porcentajeBTC'].mean()
        maximaGanancia = dfProfit['gananciasBTC'].max()
        maximaPerdida = dfProfit['gananciasBTC'].min()
        if np.isnan(dfProfit['cumsumPorcentaje'].iloc[-1]) == True:

            porcentajeAcumulado = dfProfit['cumsumPorcentaje'].iloc[-2]
        else:
            porcentajeAcumulado = dfProfit['cumsumPorcentaje'].iloc[-1]
        
        averages = {

            'averageGanancias':averageGanancias,
            'averagePorcentaje':averagePorcentaje,
            'maximaGanancia':maximaGanancia,
            'maximaPerdida':maximaPerdida,
            'numeroDeOperaciones':numeroOperaciones,
            'porcentajeAcumulado' : porcentajeAcumulado
            
            }
         
        
        if plot == True:
            f2, ax2 = plt.subplots(nrows =1,ncols=1,figsize = (8,4),sharex=True)
            f2.suptitle(mercado)
            ax2.plot(data.index, data['C'], color = 'black', label='Close')
            #ax2[0].plot(data.index, data['emaC'], color = 'red', lw =3, label = "Ema window ")

            # ax2[1].plot(data.index, data['PDI'], color='green', lw=1,label='PDI')
            # ax2[1].plot(data.index, data['NDI'], color='red', lw=1, label='NDI')
            # ax2[1].plot(data.index, data['ADX'], color = 'gray', alpha=0.5, label='ADX')          
            

            #print(venta)
            ax2.plot(compra.index, compra['C'], 'go--', linewidth=0.01, markersize=5,label = 'COMPRA')
            ax2.plot(venta.index, venta['C'], 'ro--', linewidth=0.01, markersize=5,label = 'VENTA')
            

            ax2.legend(loc = 'upper left')
           

            plt.gcf().autofmt_xdate()
            
            
            plt.show()

            plt.plot(dfProfit['datetime'], dfProfit['acumuladoGanancias'],label = ' Ganancias Acumuladas')
            plt.gcf().autofmt_xdate()
            plt.show()
        
        return averages


    def del_primera_venta(self,datos,senal):


        for index,row in datos[senal].iteritems():
            if (row!=0) & (row==-1):
                #print(row,'primer valor venta')
                datos.drop(index, inplace=True)
                break
            
            if (row!=0) & (row== 1):
                #print(row,'primer valor c')
                break
        
        return  datos



    