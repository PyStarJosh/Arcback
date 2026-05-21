import pandas as pd
from dataclasses import dataclass
from typing import Optional

@dataclass()
class Position:
    entry_price: float
    side: int # +1 long, -1 short
    sl: float # stop-loss price
    tp: float # take-profit price

@dataclass()
class ExitSignal():
    price: float # trade exit price
    reason: str # "stop_loss" or "take_profit"
    
class Exits:
    '''Runs configured exit rules each bar; first match wins.'''
    
    def check(self, bars: pd.DataFrame, pos: Position) -> Optional[ExitSignal]:
        '''Checks if position's take profit or stop loss was crossed/met'''
        high = bars['high']
        low = bars['low']
        
        if pos.side == 1:
            if high >= pos.tp:
                return ExitSignal(pos.tp, 'take_profit')
            elif low <= pos.sl:
                return ExitSignal(pos.sl, 'stop_loss')
        else: 
            if high >= pos.sl:
                return ExitSignal(pos.sl, 'stop_loss')
            elif low <= pos.tp:
                return ExitSignal(pos.tp, 'take_profit')
        
        return None
    
    