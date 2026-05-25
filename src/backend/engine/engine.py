import pandas as pd
from ..risk import Exits, Entry, Sizing
from ..portfolio import Portfolio
from ..strategy import Algorithms, Indicators
from ..data import DataManager
from .positions import Positions

class Engine:
    '''Executes all backtester operations'''
    
    def __init__(self, initial_equity: float, asset_type: str, interval: str, symbol: str | None = None, commodity_type: str | None = None, start_date: str | None = None, end_date: str | None = None):
        self._pos_records = []
        self.data_manager = DataManager()
        self.asset_type = asset_type
        
        if self.asset_type == 'tseries':
            self.price_data_df = self.data_manager.get_formatted_time_series_data(symbol, interval, start_date, end_date)
        else:
            self.price_data_df = self.data_manager.get_formatted_time_series_data(commodity_type, interval)

        self.portfolio = Portfolio(initial_equity, self.price_data_df.index)
    
    def trade_entry_execution(self, signal_df: pd.DataFrame, risk_pct: float, atr_multiplier: int, atr: int):
        
        for timestamp in self.price_data_df.index:
            price_row = self.price_data_df.loc[timestamp]
            
            signal = Entry.check_entry(timestamp, signal_df)
            
            if signal != 0:
                shares = Sizing.volatility_targeted_sizing(risk_pct, self.portfolio.equity, atr_multiplier, atr)
                
                pos = Positions(
                    entry_time=price_row.name,
                    entry_price=price_row['close'],
                    symbol=price_row['symbol'],
                    side=signal,
                    quantity=shares,
                    tp=Entry.set_tp(signal, price_row['close'], atr, atr_multiplier),
                    sl=Entry.set_sl(signal, price_row['close'], atr, atr_multiplier),
                    exit_time=None,
                    exit_price=None,
                    pnl=None,
                    exit_reason=None,
                    status='open',
                )
                self._pos_records.append(vars(pos))

            for record in self._pos_records:
                if record['status'] == 'open':
                    exit_signal = Exits.check_tseries_trade(price_row, record)
                    if exit_signal:
                        record['exit_time'] = timestamp
                        record['exit_price'] = exit_signal.price
                        record['exit_reason'] = exit_signal.reason
                        record['status'] = 'closed'
                        if record['side'] == 1:
                            record['pnl'] = (record['exit_price'] - record['entry_price']) * record['quantity']
                        else:
                            record['pnl'] = (record['entry_price'] - record['exit_price']) * record['quantity']
                        new_equity = self.portfolio.adjust_equity(record['pnl'])
                        self.portfolio.equity_df.at[timestamp, 'price'] = new_equity

        self.pos_df = pd.DataFrame(self._pos_records)
                        