from dataclasses import dataclass
from datetime import datetime

@dataclass
class Positions:
    '''Handles all open positions and their operations during backtest'''
    entry_time: datetime
    entry_price: float
    symbol: str
    side: int # 'long' = 1 or 'short' = -1
    quantity: float
    tp: float
    sl: float
    exit_time: datetime | None = None
    exit_price: float | None = None
    pnl: float | None = None
    exit_reason: str | None = None
    status: str = 'open'