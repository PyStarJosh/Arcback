import pandas as pd
from .indicators import Indicators

class Algorithms:
    '''Startegy Implementation'''
    
    def __init__(self, df):
        self.indicators = Indicators()
        
    def ma_crossover(self, df: pd.DataFrame, short_period: int, long_period: int) -> pd.DataFrame:  
        result = df.copy()
        result['ema_short'] = self.indicators(df['closes'], short_period)
        result['sma_long'] = self.indicators(df['closes', long_period])   
        result['signal'] = 0
        
        # buy_crossing = (df['ema_short'] > long_sma) & (short_ema.shift(1) <= long_sma.shift(1))
        # sell_crossing = (short_ema < long_sma) & (short_ema.shift(1) >= long_sma.shift(1))
        