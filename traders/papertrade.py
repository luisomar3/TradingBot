import pandas as pd
import numpy as np 

import pandas as pd 
import numpy as numpy

import time 
from config import config

coin = config['coin']
intervalo = config['interval']

from binance.client import Client
from binance.enums import *

from traders.basetrader import BaseTrader

client = Client('AIc1YLwGtRDJzy4wpMRe7CcAUBxTMIIfT1ddhQOhTJbHRP2xqhMkIyt5EABHLPZt',"I3S3KFNBanZStUpXHhPKTgWAxHrUUtGgBjuU7XIL2Eb1bct83nKqEMucjfR6q7qe")


class BinanceTrader(BaseTrader):

    def __init__(self):
        pass

    def exchange_place_order(self,*args,**kwargs):
            
        client.create_order()