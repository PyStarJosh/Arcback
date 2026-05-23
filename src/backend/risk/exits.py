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
class ExitSignal:
    price: float # trade exit price
    reason: str # "stop_loss" or "take_profit"
    
class Exits:
    '''Runs configured exit rules each bar; first match wins.'''
    
    def check_tseries_trade(self, bar: pd.Series, pos: Position) -> Optional[ExitSignal]:
        '''Checks if time series position's take profit or stop loss was crossed/met'''
        high = bar['high']
        low = bar['low']
        
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
    
    def check_commodity_trade(self, bar: pd.Series, pos: Position) -> Optional[ExitSignal]:
        '''Checks if commodity position's take profit or stop loss was crossed/met'''
        price = bar['price']
        
        if pos.side == 1:
            if price >= pos.tp:
                return ExitSignal(pos.tp, 'take_profit')
            elif price <= pos.sl:
                return ExitSignal(pos.sl, 'stop_loss')
        else: 
            if price >= pos.sl:
                return ExitSignal(pos.sl, 'stop_loss')
            elif price <= pos.tp:
                return ExitSignal(pos.tp, 'take_profit')
        
        return None        