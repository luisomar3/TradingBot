import pandas as pd 
from binance.client  import Client

from config import config

monedaBase = config['MonedaBase']



class BinanceAccount():
    """Clase que maneja todo lo que tiene que ver con datos del cliente, info del exchange y posisiones
    de monedas.
    """
    def __init__(self):

        apiKey = 'AIc1YLwGtRDJzy4wpMRe7CcAUBxTMIIfT1ddhQOhTJbHRP2xqhMkIyt5EABHLPZt'
        secretKey = "I3S3KFNBanZStUpXHhPKTgWAxHrUUtGgBjuU7XIL2Eb1bct83nKqEMucjfR6q7qe"
        
        


        if secretKey == '' :
            client = Client(apiKey,'')
            print("Se accedio a la cuenta sin llave secreta, no está habilitado para ejecutar trades ")
            habilitado = False
        else:
            try:
                client = Client(apiKey,secretKey)
                client.get_account_status()
                self.client = client
                habilitado = True
            except Exception as e:
                habilitado = False
                print(e)
        
        setattr(self,'habilitado',habilitado)
        setattr(self,'cliente',self.client)
         #Esto es para verificar que no podemos hacer trades sin meter la secret API

    def portafolio(self,monedas):
        

        coinBase  = self.client.get_asset_balance(asset=monedaBase)
        
        print('\n La moneda base es: \n\n', coinBase,'\n\n')

        print('Su portafolio de monedas es : \n\n')
        lista = []
        for moneda in monedas:

            balance = self.client.get_asset_balance(asset=moneda)
            lista.append(balance)
            
        df_balance = pd.DataFrame(lista)
        df_balance = df_balance.set_index('asset')
        return coinBase, df_balance

    def capital(self):

        infoActivo = self.client.get_asset_balance(monedaBase)
        capital = infoActivo['free']

        return capital

    