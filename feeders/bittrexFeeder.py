import pandas as pd 
import numpy as np 

from dataFeeder import DataFeeder
from bittrex import Bittrex, API_V2_0, TICKINTERVAL_FIVEMIN


my_Bittrex_v2 = Bittrex(None, None, api_version=API_V2_0)
my_Bittrex_v1 = Bittrex(None, None)


class BittrexFeeder(DataFeeder):
    def __init__():
        pass


    def get