import pandas as pd
import pytest
from src.backend import Entry

@pytest.fixture
def timestamp():
    return pd.DatetimeIndex(['2020-01-01', '2020-01-02', '2020-01-03'])

@pytest.fixture
def entry_indicator(timestamp):
    return pd.DataFrame(
        {
            'ema_short': [100, 130, 104],
            'sma_long': [101, 111, 112],
            'signal': [0, 1, -1]
        }, index=timestamp
    )

class TestEntry:
    
    def test_check_entry(self, entry_indicator):
        result = Entry.check_entry(timestamp='2020-01-02', entry_indicator=entry_indicator)
        assert result == 1
        
    def test_set_tp_long(self):
        result = Entry.set_tp(side=1, entry_price=101.23, atr=14, multiplier=2)
        assert round(result, 2) == 129.23
        
    def test_set_tp_short(self):
        result = Entry.set_tp(side=-1, entry_price=101.23, atr=14, multiplier=2)
        assert round(result, 2) == 73.23
        
    def test_set_sl_long(self):
        result = Entry.set_sl(side=1, entry_price=101.23, atr=14, multiplier=2)
        assert round(result, 2) == 73.23
        
    def test_sl_short(self):
        result = Entry.set_sl(side=-1, entry_price=101.23, atr=14, multiplier=2)
        assert round(result, 2) == 129.23