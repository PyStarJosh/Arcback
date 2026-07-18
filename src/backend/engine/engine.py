import pandas as pd
from ..risk import Exits, Entry, Sizing
from ..portfolio import Portfolio
from ..data import DataManager
from .positions import Positions
from ..strategy import Indicators

class Engine:
    '''Executes all backtester operations'''
    
    def __init__(self, initial_equity: float, asset_type: str, interval: str, symbol: str | None = None, commodity_type: str | None = None, start_date: str | None = None, end_date: str | None = None, atr_period: int = 14):
        self._pos_records = []
        self.data_manager = DataManager()
        self.asset_type = asset_type
        
        if self.asset_type == 'tseries':
            self.price_data_df = self.data_manager.get_formatted_time_series_data(symbol, interval, start_date, end_date)
            self.atr_series = Indicators.atr(
            self.price_data_df['high'], self.price_data_df['low'],
            self.price_data_df['close'], atr_period)
        else:
            self.price_data_df = self.data_manager.get_formatted_commodities_data(commodity_type, interval)
            self.atr_series = self.price_data_df['price'].diff().abs().rolling(window=atr_period).mean()

        self.portfolio = Portfolio(initial_equity, self.price_data_df.index)
    
    def trade_entry_execution(self, signal_df: pd.DataFrame, risk_pct: float, atr_multiplier: int):
        
        for timestamp in self.price_data_df.index:
            price_row = self.price_data_df.loc[timestamp]
            
            signal = Entry.check_entry(timestamp, signal_df)
            
            if signal != 0:
                atr = self.atr_series[timestamp]
                if pd.notna(atr) and atr > 0:
                    if self.asset_type == 'tseries':
                        self._open_position(risk_pct, price_row, signal, atr=atr, atr_multiplier=atr_multiplier, symbol_column_name='symbol', price_column_name='close')
                    else:
                        self._open_position(risk_pct, price_row, signal, atr=atr, atr_multiplier=atr_multiplier, symbol_column_name='commodity_type', price_column_name='price')


            for record in self._pos_records:
                # skip the bar the position opened on — its high/low already printed before we entered at the close
                if record['status'] == 'open' and record['entry_time'] < timestamp:
                    if self.asset_type == 'tseries':
                        exit_signal = Exits.check_tseries_trade(price_row, record)
                    else: 
                        exit_signal = Exits.check_commodity_trade(price_row, record)
                        
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

        self.portfolio.equity_df['price'] = self.portfolio.equity_df['price'].ffill()
        self.pos_df = pd.DataFrame(self._pos_records)
        return self.pos_df, self.portfolio.equity_df
        
    def _open_position(self, risk_pct: float, data: pd.Series, signal: int, price_column_name: str, symbol_column_name: str, atr: float, atr_multiplier: int) -> None:
        shares = Sizing.volatility_targeted_sizing(risk_pct, self.portfolio.equity, atr_multiplier, atr)
        pos = Positions(
                    entry_time=data.name,
                    entry_price=data[price_column_name],
                    symbol=data[symbol_column_name],
                    side=signal,
                    quantity=shares,
                    tp=Entry.set_tp(signal, data[price_column_name], atr, atr_multiplier),
                    sl=Entry.set_sl(signal, data[price_column_name], atr, atr_multiplier),
                    exit_time=None,
                    exit_price=None,
                    pnl=None,
                    exit_reason=None,
                    status='open',
                )
        self._pos_records.append(vars(pos))