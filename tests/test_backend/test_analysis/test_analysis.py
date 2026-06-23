import pandas as pd
import pytest

from src.backend.analysis.analysis import Analysis

# ---------------------------------------------------------------------------
# Fixtures
#
# Four fully-closed trades with hand-computable aggregates:
#
#   pnl:   +1000   +600   -400   -200
#   side:    1      -1      1      -1
#   days:    2       4      1       6     (exit_time - entry_time)
#
#   gross_revenue = 1600   total_losses = -600   net_revenue = 1000
#   winners = 2  losers = 2  buys = 2  sells = 2  positions = 4
#   avg_win = 800  avg_loss = -300   duration mean = 13/4 = 3.25
# ---------------------------------------------------------------------------
@pytest.fixture
def pos_df():
    return pd.DataFrame([
        {'entry_time': pd.Timestamp('2020-01-01'), 'exit_time': pd.Timestamp('2020-01-03'),
         'symbol': 'SPCX', 'side': 1, 'quantity': 10, 'entry_price': 100, 'exit_price': 200,
         'tp': 0, 'sl': 0, 'pnl': 1000, 'exit_reason': 'take_profit', 'status': 'closed'},
        {'entry_time': pd.Timestamp('2020-01-02'), 'exit_time': pd.Timestamp('2020-01-06'),
         'symbol': 'AAPL', 'side': -1, 'quantity': 5, 'entry_price': 300, 'exit_price': 250,
         'tp': 0, 'sl': 0, 'pnl': 600, 'exit_reason': 'take_profit', 'status': 'closed'},
        {'entry_time': pd.Timestamp('2020-01-03'), 'exit_time': pd.Timestamp('2020-01-04'),
         'symbol': 'TSLA', 'side': 1, 'quantity': 8, 'entry_price': 150, 'exit_price': 100,
         'tp': 0, 'sl': 0, 'pnl': -400, 'exit_reason': 'stop_loss', 'status': 'closed'},
        {'entry_time': pd.Timestamp('2020-01-04'), 'exit_time': pd.Timestamp('2020-01-10'),
         'symbol': 'MSFT', 'side': -1, 'quantity': 4, 'entry_price': 400, 'exit_price': 450,
         'tp': 0, 'sl': 0, 'pnl': -200, 'exit_reason': 'stop_loss', 'status': 'closed'},
    ])


@pytest.fixture
def equity_df():
    # peak is 110_000; the curve dips to 99_000 then to 98_010 (the trough)
    idx = pd.date_range('2020-01-01', periods=5, freq='D')
    return pd.DataFrame(
        {'price': [100_000.0, 110_000.0, 99_000.0, 108_900.0, 98_010.0]},
        index=idx,
    )


@pytest.fixture
def analysis(pos_df, equity_df):
    return Analysis(final_pos_df=pos_df, final_equity_df=equity_df)


# ---------------------------------------------------------------------------
# Equity-curve metrics
# ---------------------------------------------------------------------------
class TestEquityMetrics:

    def test_final_equity(self, analysis):
        assert analysis.final_equity() == 98_010.0

    def test_lowest_equity(self, analysis):
        assert analysis.lowest_equity() == 98_010.0

    def test_highest_equity(self, analysis):
        assert analysis.highest_equity() == 110_000.0

    def test_equity_pct_change(self, analysis):
        # (98_010 - 100_000) / 100_000 * 100
        assert analysis.equity_pct_change() == pytest.approx(-1.99)

    def test_drawdown(self, analysis):
        # trough 98_010 vs peak 110_000 -> -10.9%
        assert analysis.drawdown() == pytest.approx(-10.9)

    def test_sharpe_ratio_symmetric_returns(self, analysis):
        # returns are +/-10% alternating -> mean ~0 -> sharpe ~0
        assert analysis.sharpe_ratio() == pytest.approx(0.0, abs=1e-6)

    def test_sharpe_ratio_accepts_risk_free_rate(self, analysis):
        # non-zero rate shifts the result; just assert it stays finite/float
        result = analysis.sharpe_ratio(risk_free_rate=0.02)
        assert isinstance(result, float)


# ---------------------------------------------------------------------------
# PnL aggregates
# ---------------------------------------------------------------------------
class TestPnlAggregates:

    def test_gross_revenue(self, analysis):
        assert analysis.gross_revenue() == 1600

    def test_total_losses(self, analysis):
        assert analysis.total_losses() == -600

    def test_net_revenue(self, analysis):
        assert analysis.net_revenue() == 1000

    def test_avg_win(self, analysis):
        assert analysis.avg_win() == 800

    def test_avg_loss(self, analysis):
        assert analysis.avg_loss() == -300

    def test_risk_reward_ratio_uses_loss_magnitude(self, analysis):
        # 800 / abs(-300) -> 2.67 (positive)
        assert analysis.risk_reward_ratio() == pytest.approx(2.67)

    def test_profit_factor(self, analysis):
        # 1600 / abs(-600)
        assert analysis.profit_factor() == pytest.approx(1600 / 600)


# ---------------------------------------------------------------------------
# Trade counts
# ---------------------------------------------------------------------------
class TestTradeCounts:

    def test_num_of_winners(self, analysis):
        assert analysis.num_of_winners() == 2

    def test_num_of_losers(self, analysis):
        assert analysis.num_of_losers() == 2

    def test_num_of_positions(self, analysis):
        assert analysis.num_of_positions() == 4

    def test_num_of_buys(self, analysis):
        assert analysis.num_of_buys() == 2

    def test_num_of_sells(self, analysis):
        assert analysis.num_of_sells() == 2

    def test_win_percentage(self, analysis):
        # NOTE: returns a fraction (winners / positions), not a 0-100 percentage
        assert analysis.win_percentage() == 0.5


# ---------------------------------------------------------------------------
# Trade selection / duration
# ---------------------------------------------------------------------------
class TestTradeSelection:

    def test_most_profitable_trade(self, analysis):
        trade = analysis.most_profitable_trade()
        assert trade['pnl'] == 1000
        assert trade['symbol'] == 'SPCX'

    def test_biggest_losing_trade(self, analysis):
        trade = analysis.biggest_losing_trade()
        assert trade['pnl'] == -400
        assert trade['symbol'] == 'TSLA'

    def test_avg_trade_duration(self, analysis):
        # (2 + 4 + 1 + 6) / 4 days
        assert analysis.avg_trade_duration() == pytest.approx(3.25)

    def test_avg_trade_duration_excludes_open_trades(self):
        pos_df = pd.DataFrame([
            {'entry_time': pd.Timestamp('2020-01-01'), 'exit_time': pd.Timestamp('2020-01-03'),
             'side': 1, 'pnl': 500, 'status': 'closed'},
            {'entry_time': pd.Timestamp('2020-01-02'), 'exit_time': pd.NaT,
             'side': 1, 'pnl': None, 'status': 'open'},
        ])
        equity_df = pd.DataFrame({'price': [100_000.0, 100_500.0]},
                                 index=pd.date_range('2020-01-01', periods=2, freq='D'))
        analysis = Analysis(final_pos_df=pos_df, final_equity_df=equity_df)

        # only the single closed 2-day trade is counted
        assert analysis.avg_trade_duration() == pytest.approx(2.0)