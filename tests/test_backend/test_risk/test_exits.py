import pandas as pd
import pytest
from src.backend import Exits

@pytest.fixture
def price():
    return pd.Series(
        {
            'open': 101.11 ,
            'high': 123.02,
            'low': 113.32,
            'close': 116
        }
    )
    
@pytest.fixture
def date_price():
    return pd.Series(
        {
            'price': 125.43
        }
    )

class TestExits:
    
    def test_check_tseries_trade_buy_tp(self, price):
        pos = {'side': 1, 'tp': 122, 'sl': 112}
        exit_signal = Exits.check_tseries_trade(price, pos)
        assert exit_signal.price == pos['tp']
        assert exit_signal.reason == 'take_profit'
        
    def test_check_tseries_trade_buy_sl(self, price):
        pos = {'side': 1, 'tp': 150, 'sl': 114}
        exit_signal = Exits.check_tseries_trade(price, pos)
        assert exit_signal.price == pos['sl']
        assert exit_signal.reason == 'stop_loss'
        
    def test_check_tseries_trade_sell_tp(self, price):
        pos = {'side': -1, 'tp': 115, 'sl': 125}
        exit_signal = Exits.check_tseries_trade(price, pos)
        assert exit_signal.price == pos['tp']
        assert exit_signal.reason == 'take_profit'
        
    def test_check_tseries_trade_sell_sl(self, price):
        pos = {'side': -1, 'tp': 99, 'sl': 120}
        exit_signal = Exits.check_tseries_trade(price, pos)
        assert exit_signal.price == pos['sl']
        assert exit_signal.reason == 'stop_loss'
        
    def test_check_tseries_trade_no_exit_signal(self, price):
        pos = {'side': 1, 'tp': 200, 'sl': 50}
        exit_signal = Exits.check_tseries_trade(price, pos)
        assert exit_signal == None
        
    def test_check_commodity_trade_buy_tp(self, date_price):
        pos = {'side': 1, 'tp': 125, 'sl': 124}
        exit_signal = Exits.check_commodity_trade(date_price, pos)
        assert exit_signal.price == pos['tp']
        assert exit_signal.reason == 'take_profit'
        
    def test_check_commodity_trade_buy_sl(self, date_price):
        pos = {'side': 1, 'tp': 145, 'sl': 126}
        exit_signal = Exits.check_commodity_trade(date_price, pos)
        assert exit_signal.price == pos['sl']
        assert exit_signal.reason == 'stop_loss'
        
    def test_check_commodity_trade_sell_tp(self, date_price):
        pos = {'side': 1, 'tp': 125.43, 'sl': 126}
        exit_signal = Exits.check_commodity_trade(date_price, pos)
        assert exit_signal.price == pos['tp']
        assert exit_signal.reason == 'take_profit'
        
    def test_check_commodity_trade_sell_sl(self, date_price):
        pos = {'side': 1, 'tp': 150, 'sl': 126}
        exit_signal = Exits.check_commodity_trade(date_price, pos)
        assert exit_signal.price == pos['sl']
        assert exit_signal.reason == 'stop_loss'
        
    def test_check_commodity_trade_no_signal(self, date_price):
        pos = {'side': 1, 'tp': 175, 'sl': 10}
        exit_signal = Exits.check_commodity_trade(date_price, pos)
        assert exit_signal == None