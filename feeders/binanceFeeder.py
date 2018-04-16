import pandas as pd 
import numpy as np 

from feeders.dataFeeder import DataFeeder
import binance 

class BinanceFeeder(DataFeeder):
    
    def __init__(self,coins):
    """This method initialize the feeder with the current coins to invest.
       It should be exchange information.

       :param coins: 
    """        
