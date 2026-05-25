import pandas as pd
from dataclasses import dataclass
from typing import Optional
from ..engine import Positions

@dataclass()
class ExitSignal:
    price: float # trade exit price
    reason: str # "stop_loss" or "take_profit"
    
class Exits:
    '''Runs configured exit rules each bar; first match wins.'''

    @staticmethod 
    def check_tseries_trade(price_df: pd.Series, pos: Positions) -> Optional[ExitSignal]:
        '''Checks if time series position's take profit or stop loss was crossed/met'''
        high = price_df['high']
        low = price_df['low']
        
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
    
    @staticmethod
    def check_commodity_trade(price_df: pd.Series, pos: Positions) -> Optional[ExitSignal]:
        '''Checks if commodity position's take profit or stop loss was crossed/met'''
        price = price_df['price']
    
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