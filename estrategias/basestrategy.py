import pandas as pd 
import numpy as np

#import matplotlib.pyplot as plt
from config import config




class BaseStrategy():

    def __strategySignal(self, dataFrame):
        """Extrae la señal del dataFrame generado 
        por la estrategia, esta clase es para ser usada por el liveTrade para ver el tipo de orden que tiene que poner 
        1 para comprar. 0 para no hacer nada y -1 para vender.
        :param dataFrame: DataFrame con los datos de la estrategia.
        

        """
        
        order  =  dataFrame['signal'].iloc[-1]
        #order2 = dataFrame['signal'].iloc[-2]
        
        return order#,order2

    def message(self,dataFrame):
        """ Metodo para extraer estadisticas generales de la estrategia.

        """
        data = dataFrame.copy()

        senal1 =  self.__strategySignal(data)  #senal 2 al lado de senal1 si hay problemas
        #print(senal1)
        #print(type(senal1))
        # if (senal1 == 1) &  (senal2 == -1) : 
        #     item = senal1
        # elif (senal1 == -1) & (senal2 == 1) : 
        #     item = senal1 
        # else :
        #     item = senal1 or senal2
        
        return senal1

    def crossover(self,row,indicadorAlza,indicadorBaja,inTheMarket = False):
        """Realiza el crossover de 2 indicadores, si el indicador de alza supera al de baja,
            manda señal de compra, si el de baja supera al de alta, manda señal de venta.

        """
        inAlzaAnterior = 'shift_'+ indicadorAlza
        inBajaAnterior = 'shift_'+ indicadorBaja
        #se le agrega el prefijo shift porque así esta en el DataFrame armado.
           
        if (row[indicadorAlza] > row[indicadorBaja] ) & (row[inBajaAnterior] >= row[inAlzaAnterior])  :
            inTheMarket = True 
            #Si PDI es mayor que NDI y anteriormente NDI era mayor (PDI supera NDI) doy señal de compra 
            return  1
        elif (row[indicadorBaja] > row[indicadorAlza] ) & (row[inAlzaAnterior] >= row[inBajaAnterior]) :
            inTheMarket = False
            #Si NDI es mayor que PDI y anteriormente PDI era mayor (NDI supera PDI) doy señal de venta
            return -1    
        else:
            return  0

    def posMayorQueNeg(self,row,indicadorAlza,indicadorBaja):
        """Realiza el crossover de 2 indicadores, si el indicador de alza supera al de baja,
            manda señal de compra, si el de baja supera al de alta, manda señal de venta.

        """
           
        if (row[indicadorAlza] >= row[indicadorBaja] )  :
            
            return  int(1)
        elif (row[indicadorBaja] > row[indicadorAlza] ) :

            return  int(0)


    def aroon100(self,row,indicadorAlza,indicadorBaja):
        """Realiza el crossover de 2 indicadores, si el indicador de alza supera al de baja,
            manda señal de compra, si el de baja supera al de alta, manda señal de venta.

        """
           
        if (row[indicadorAlza] == 100 )  :
            
            return  int(1)
        else :

            return  int(0)


    def two_entry_signals_and(self,row,indicador1,indicador2):
        """En este caso, devolveremos la senal indicador 1 porque es la señal del ADX la que queremos como salida
        """

        senal = 'signal'+indicador1
        senal2 = 'signal'+indicador2

        if (row[senal] == 1 ) & (row[senal2] == 1) :

            return 1

        elif (row[senal] == -1) :

            return int(row[senal] )

        else :
            return 0


    def extraer_salidas(self,dataFrame):
        """Procedimiento para extraer salidas innecesarias
        """
        datos = dataFrame.copy()
        compra = self.compra(datos,'signal')
        for idx,item in enumerate(dataFrame['signal']):
            
            if (item == -1) & (compra == False):
                datos['signal'].iloc[idx] = 0
            if (item == -1 ) & (compra == True):
                compra = False
            if item == 1 :
                compra = True
        return datos

    def compra(self,datos,senal):


        for index,row in datos[senal].iteritems():
            if (row==-1):
                #print(row,'primer valor venta')
                compra = False
                return compra
                break
            
            if (row== 1):
                #print(row,'primer valor c')
                compra = True
                return compra
                break
        
        

