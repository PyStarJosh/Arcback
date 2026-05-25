import pandas as pd
from dataclasses import dataclass
    
class Entry:
    '''Executes trade entry based on configured entry criteria'''
    
    @staticmethod
    def check_entry(timestamp: pd.DatetimeIndex, entry_indicator: pd.DataFrame) -> bool:
        return entry_indicator.at[timestamp, 'signal'] == 1