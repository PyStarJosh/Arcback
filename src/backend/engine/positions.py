import pandas as pd
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Positons:
    '''Handles all open positions and their operations during backtest'''
    entry_time: datetime
    exit_time: datetime | None = None
    entry_price: float
    exit_price: float | None = None
    pnl: float | None = None
    symbol: str
    reason: str | None = None
    status: str = 'open'
    side: str # 'long' or 'short'
    quantity: float
    
    def __post_init__(self) -> None:
        if self.side not in ('long', 'short'):
            raise ValueError(f'position side must be "long" or "short", got', {self.side})