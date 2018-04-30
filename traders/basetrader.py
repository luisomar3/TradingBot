import pandas as pd 
import numpy as numpy

import time 
from config import config

coin = config['coin']
intervalo = config['interval']

from binance.client import Client
from binance.enums import *

client = Client('AIc1YLwGtRDJzy4wpMRe7CcAUBxTMIIfT1ddhQOhTJbHRP2xqhMkIyt5EABHLPZt',"I3S3KFNBanZStUpXHhPKTgWAxHrUUtGgBjuU7XIL2Eb1bct83nKqEMucjfR6q7qe")


class BaseTrader():

    def __init__(self):
        pass

    def place_order(self,*args,**kwargs):
        pass
        #self.exchange_order()

    def exchange_order(self,*args,**kwargs):
        """Funcion especifica de cara exchange, debe ser sobreescrita para cada exchange
        """
        print("Debes sobreescribir este metodo para el exchange que desees")
        
    def verify_order(self):

        self.exchange_verify()

    def exchange_verify_order(self):
        """Funcion especifica de cara exchange, debe ser sobreescrita para cada exchange
        """

        print("Debes sobreescribir este metodo para el exchange que desees")
        

    def place_test_order(self):
        pass

