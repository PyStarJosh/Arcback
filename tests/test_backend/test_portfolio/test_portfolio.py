import pandas as pd
import pytest
from src.backend import Portfolio

@pytest.fixture
def dt_index():
    return pd.DatetimeIndex(['2020-01-01', '2020-01-02', '2020-01-03'])
    
@pytest.fixture
def portfolio(dt_index):
    return Portfolio(equity=100, dt_index=dt_index)

class TestPortfolio:
    def test_init_sets_equity(self, portfolio, dt_index):
        expected = pd.DataFrame({'price': [100, 100, 100]}, index=dt_index)
        assert portfolio.equity == 100.00
        pd.testing.assert_frame_equal(portfolio.equity_df, expected)
        
    def test_init_raises_value_error(self, dt_index):
        with pytest.raises(expected_exception=ValueError, match='The balance must be greater than'):
            Portfolio(equity=0, dt_index=dt_index)
            
    def test_adjust_equity_pos_value(self, portfolio):
        portfolio.adjust_equity(20)
        assert portfolio.equity == 120
        
    def test_adjust_equity_neg_value(self, portfolio):
        portfolio.adjust_equity(amount=-50)
        assert portfolio.equity == 50
    
    def test_adjust_equity_zero(self, portfolio):
        portfolio.adjust_equity(amount=0)
        assert portfolio.equity == 100