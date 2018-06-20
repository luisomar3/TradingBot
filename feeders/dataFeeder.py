import pandas as pd 
import numpy as np 
import regex

pd.options.mode.chained_assignment = None
class DataFeeder():

    def __init__():
        self.attributes 
        self.keys 
        self.name = name 
    
    def normalizeKlines(self,dataFrame,columnsName):
        """ Recibe un Pandas DataFrame y normaliza sus columnas para que todas tengan un mismo formato
        DTOHLC (Date, Time, Open, High, Low, Close)
        :param dataFrame: Pandas DF contenedor, contiene los datos como los trae por defecto el provider.
        :type dataFrame: pd.DataFrame

        return: DataFrame ordenado.
        """
        data = dataFrame.copy()
        data = self.dropUseless(data)
        data.datetime = pd.to_datetime(data.datetime, unit='ms')
        data = data.set_index("datetime")
        
        data = data.apply(pd.to_numeric)
        
        return data



    def dropUseless(self,DataFrame):
        
        data = DataFrame
        importantValues = ["datetime","O","H","L","C","V"]
        df_important = data[importantValues]
        return df_important   
        
        
    def normalizeCoins(self,coins):
        """The idea of this method is that every exchanga has his owns coin-pair name
        i.e.: Binance ETH BTC Pair is ETHBTC
              Bittrex is ETH-BTC
        :param coins: List of coins we gonna trade.
        :type coins: python list.

        return List of coins normalize.
              
        """
     
        pass
    