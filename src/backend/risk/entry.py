import pandas as pd
from dataclasses import dataclass
    
class Entry:
    '''Executes trade entry based on configured entry criteria'''
    
    def check_entry(self, timestamp: pd.DatetimeIndex, entry_indicator: pd.DataFrame) -> bool:
        return entry_indicator.at[timestamp, 'signal'] == 1