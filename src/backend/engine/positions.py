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
    side: int # 'long' = 1 or 'short' = -1
    quantity: float
    tp: float
    sl: float