import pandas as pd 
import numpy as np 
import os 

class DataFeeder():

    def __init__():
        self.attributes 
        self.keys 
        self.name = name 
    
    def normalizeKlines(self,dataFrame):
        """ Recibe un Pandas DataFrame y normaliza sus columnas para que todas tengan un mismo formato
        DTOHLC (Date, Time, Open, High, Low, Close)
        param dataFrame: Pandas DF contenedor, contiene los datos como los trae por defecto el provider.
        type dataFrame: pd.DataFrame

        return: DataFrame ordenado.
        """
        pass
    
    def normalizeCoins(self,coins):
        """The idea of this method is that every exchanga has his owns coin-pair name
        i.e.: Binance ETH BTC Pair is ETHBTC
              Bittrex is ETH-BTC
        param coins: List of coins we gonna trade.
        type coins: python list.

        return List of coins normalize.
              
        """ 
        pass

    def authentication(self,*args, **kwargs):
        """Metodo par autentificar la identidad del usuario con cualquier exchange

        """
        pass
    

class exchangeFeeder(DataFeeder):
    
    def __init__(coins):
        """List of coins
        """
        self.coins = coins

    def especificExchangeMethods():



class encrypter():
    """Class to encrypt secrets keys, we wanna create a script that ask for our credentials,
    encrypt those credentials and save it to a file. So we can Dencrypted later.
    """

    def key_entry(exchanges):
        print('Select Exchange: {exchanges}',exchanges: exchanges)
        selected_exc = input().lower.trim()
        if selected_exc == binance :
            api_key = input("enter api key:")
            secret_Key = input("Enter secret key")
            # I think to create an json file or something
        cypher(api_key,secret_key,exchange_name, wb_encrypted_name)

   def decrypter(exchange_name):
       exchanges_credentials = os.listdir()
       exchange_to_look = exchange_name + "extension"
       if exchange_to_look is in exchanges_credentials
           decypher('thisfile')



class indicators():
    """ Class with available indicators, the idea is to create a class with indicators that can be 
    used later for the strategy class, something like:
                    ema = indicators.ema("dataFrame")

                    adx+ema_strategy = strategies(indicators):

    """
    def ema(self,short_window,long_window):
        pass
    
    def adx(self,volume,power):
        pass
    

class strategy_name(indicators):
    """This class inherit indicators because will use indicators available in order to 
    create an specific strategy
    """

    def adx():
        if adx() is 1 buy 0 do nothing -1 sell.
    
class trader():
    pass #creo que lo más optimo es una lista con las ordenes y posiciones a tomar en cada moneda.

class portfolio():
    pass
    positionSizing #En espera de decision si binance o python-binance. Recibirá un dataFrame
                   #con las ordenes de compra, y determinará cuanto debe comprar o vender y agregarlo
                   # a una columna en el df.

class accounting():
    pass    #Esta clase vigilará el p&l y si es solicitado una curva grafica de las ganancias con 
            #cada trade que será guardada en la carpeta root.
            #estrechamente relacionada con portfolio. 

class robot():
    """This class is the main class, it runs everything from feeders to auth
    It should be initialize with the cypher pass
    It should be run indefinitly 

    """
    
    #Buscar librerias para el manejo de estas, probablemente terminemos con crontabs y scheduler.
    #Si crontab no se puede usar mejor. Esta será la clase más modular. 


    
class liveTrade():
    

