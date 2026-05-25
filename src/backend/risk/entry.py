import pandas as pd
from dataclasses import dataclass
    
class Entry:
    '''Executes trade entry based on configured entry criteria'''
    
    @staticmethod
    def check_entry(timestamp: pd.DatetimeIndex, entry_indicator: pd.DataFrame) -> bool:
        return entry_indicator.at[timestamp, 'signal']
    
    @staticmethod
    def set_tp(side: int, entry_price: float, atr: float, multiplier: float) -> float:
        if side == 1:
            return entry_price + (atr * multiplier)
        return entry_price - (atr * multiplier)

    @staticmethod
    def set_sl(side: int, entry_price: float, atr: float, multiplier: float) -> float:
        if side == 1:
            return entry_price - (atr * multiplier)
        return entry_price + (atr * multiplier)
