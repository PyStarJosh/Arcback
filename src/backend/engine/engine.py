import pandas as pd
from ..risk import Exits, Entry, Limits, Sizing
from ..portfolio import Portfolio
from ..strategy import Algorithms, Indicators
from .positions import Positions

class Engine:
    '''Executes all backtester operations'''
    
    def __init__(self):
        self.pos_df = 