from unittest.mock import patch

import pandas as pd
import pytest

from src.backend import Engine

# ---------------------------------------------------------------------------
# Shared constants
#
# With these values the position-sizing maths is fully deterministic:
#   dollar_risk   = equity * risk_pct      = 100_000 * 0.01 = 1_000
#   stop_distance = atr_multiplier * atr   = 2 * 14          = 28
#   shares        = int(1_000 / 28)                          = 35
#   tp/sl offset  = atr * atr_multiplier                     = 28
# ---------------------------------------------------------------------------
INITIAL_EQUITY = 100_000
RISK_PCT = 0.01
ATR = 14
ATR_MULTIPLIER = 2
EXPECTED_SHARES = 35
OFFSET = ATR * ATR_MULTIPLIER  # 28

INDEX = pd.DatetimeIndex(['2020-01-01', '2020-01-02', '2020-01-03'])


# ---------------------------------------------------------------------------
# Fixtures / helpers
# ---------------------------------------------------------------------------
def _tseries_df(highs, lows, closes, symbol='SPCX'):
    """Build a time-series price frame on the shared DatetimeIndex."""
    return pd.DataFrame(
        {
            'symbol': [symbol] * len(INDEX),
            'open': closes,
            'high': highs,
            'low': lows,
            'close': closes,
        },
        index=INDEX,
    )


def _commodity_df(prices, commodity_type='COPPER'):
    """Build a commodity price frame on the shared DatetimeIndex."""
    return pd.DataFrame(
        {
            'commodity_type': [commodity_type] * len(INDEX),
            'price': prices,
        },
        index=INDEX,
    )


def _signals(values):
    """Signal frame sharing the price index, as Entry.check_entry expects."""
    return pd.DataFrame({'signal': values}, index=INDEX)


@pytest.fixture
def make_engine():
    """
    Factory that builds an Engine with DataManager patched out.

    The patch stays active for the whole test (yield), so the live data
    layer (network + SQLite) is never touched and the constructor call args
    remain inspectable via ``make_engine.mock``.
    """
    with patch('src.backend.engine.engine.DataManager') as MockDM:
        instance = MockDM.return_value

        def _factory(price_df, asset_type='tseries', initial_equity=INITIAL_EQUITY):
            if asset_type == 'tseries':
                instance.get_formatted_time_series_data.return_value = price_df
                return Engine(
                    initial_equity=initial_equity,
                    asset_type='tseries',
                    interval='1day',
                    symbol='SPCX',
                )
            instance.get_formatted_commodities_data.return_value = price_df
            return Engine(
                initial_equity=initial_equity,
                asset_type='commodity',
                interval='daily',
                commodity_type='COPPER',
            )

        _factory.mock = MockDM
        yield _factory


# ---------------------------------------------------------------------------
# __init__
# ---------------------------------------------------------------------------
class TestEngineInit:

    def test_init_sets_core_attributes(self, make_engine):
        price_df = _tseries_df(highs=[105, 110, 130], lows=[98, 95, 99], closes=[100, 100, 100])
        engine = make_engine(price_df)

        assert engine.asset_type == 'tseries'
        assert engine._pos_records == []
        pd.testing.assert_frame_equal(engine.price_data_df, price_df)
        assert engine.portfolio.equity == INITIAL_EQUITY
        # equity curve is seeded across every bar of the price index
        assert list(engine.portfolio.equity_df.index) == list(INDEX)

    def test_init_tseries_fetches_time_series_data(self, make_engine):
        price_df = _tseries_df(highs=[105, 110, 130], lows=[98, 95, 99], closes=[100, 100, 100])
        make_engine(price_df)

        make_engine.mock.return_value.get_formatted_time_series_data.assert_called_once_with(
            'SPCX', '1day', None, None
        )

    def test_init_commodity_fetches_commodities_data(self, make_engine):
        price_df = _commodity_df(prices=[100, 100, 130])
        make_engine(price_df, asset_type='commodity')

        # regression guard: commodity assets must hit the commodities loader,
        # never the time-series one.
        make_engine.mock.return_value.get_formatted_commodities_data.assert_called_once_with(
            'COPPER', 'daily'
        )
        make_engine.mock.return_value.get_formatted_time_series_data.assert_not_called()


# ---------------------------------------------------------------------------
# trade_entry_execution
# ---------------------------------------------------------------------------
class TestTradeEntryExecution:

    def test_returns_pos_df_and_equity_df(self, make_engine):
        price_df = _tseries_df(highs=[105, 110, 130], lows=[98, 95, 99], closes=[100, 100, 100])
        engine = make_engine(price_df)

        result = engine.trade_entry_execution(_signals([0, 1, 0]), RISK_PCT, ATR_MULTIPLIER, ATR)

        assert isinstance(result, tuple) and len(result) == 2
        pos_df, equity_df = result
        assert isinstance(pos_df, pd.DataFrame)
        assert isinstance(equity_df, pd.DataFrame)

    def test_no_signals_opens_no_positions(self, make_engine):
        price_df = _tseries_df(highs=[105, 110, 130], lows=[98, 95, 99], closes=[100, 100, 100])
        engine = make_engine(price_df)

        pos_df, equity_df = engine.trade_entry_execution(_signals([0, 0, 0]), RISK_PCT, ATR_MULTIPLIER, ATR)

        assert pos_df.empty
        assert engine.portfolio.equity == INITIAL_EQUITY
        assert (equity_df['price'] == INITIAL_EQUITY).all()

    def test_long_take_profit(self, make_engine):
        # entry @100 on bar 1 -> tp=128, sl=72; bar 2 high 130 hits tp
        price_df = _tseries_df(highs=[105, 110, 130], lows=[98, 95, 99], closes=[100, 100, 100])
        engine = make_engine(price_df)

        pos_df, equity_df = engine.trade_entry_execution(_signals([0, 1, 0]), RISK_PCT, ATR_MULTIPLIER, ATR)

        assert len(pos_df) == 1
        trade = pos_df.iloc[0]
        assert trade['side'] == 1
        assert trade['entry_time'] == pd.Timestamp('2020-01-02')
        assert trade['entry_price'] == 100
        assert trade['symbol'] == 'SPCX'
        assert trade['quantity'] == EXPECTED_SHARES
        assert trade['tp'] == 100 + OFFSET   # 128
        assert trade['sl'] == 100 - OFFSET   # 72
        assert trade['status'] == 'closed'
        assert trade['exit_reason'] == 'take_profit'
        assert trade['exit_time'] == pd.Timestamp('2020-01-03')
        assert trade['exit_price'] == 128
        assert trade['pnl'] == (128 - 100) * EXPECTED_SHARES  # 980

        # equity only steps up on the exit bar
        assert equity_df.loc['2020-01-01', 'price'] == INITIAL_EQUITY
        assert equity_df.loc['2020-01-02', 'price'] == INITIAL_EQUITY
        assert equity_df.loc['2020-01-03', 'price'] == INITIAL_EQUITY + 980
        assert engine.portfolio.equity == INITIAL_EQUITY + 980

    def test_long_stop_loss(self, make_engine):
        # entry @100 -> sl=72; bar 2 low 70 hits stop before tp
        price_df = _tseries_df(highs=[105, 110, 80], lows=[98, 95, 70], closes=[100, 100, 100])
        engine = make_engine(price_df)

        pos_df, equity_df = engine.trade_entry_execution(_signals([0, 1, 0]), RISK_PCT, ATR_MULTIPLIER, ATR)

        trade = pos_df.iloc[0]
        assert trade['exit_reason'] == 'stop_loss'
        assert trade['exit_price'] == 72
        assert trade['pnl'] == (72 - 100) * EXPECTED_SHARES  # -980
        assert equity_df.loc['2020-01-03', 'price'] == INITIAL_EQUITY - 980
        assert engine.portfolio.equity == INITIAL_EQUITY - 980

    def test_short_take_profit(self, make_engine):
        # short @100 -> tp=72, sl=128; bar 2 low 70 hits tp
        price_df = _tseries_df(highs=[105, 105, 110], lows=[98, 98, 70], closes=[100, 100, 100])
        engine = make_engine(price_df)

        pos_df, equity_df = engine.trade_entry_execution(_signals([0, -1, 0]), RISK_PCT, ATR_MULTIPLIER, ATR)

        trade = pos_df.iloc[0]
        assert trade['side'] == -1
        assert trade['tp'] == 100 - OFFSET   # 72
        assert trade['sl'] == 100 + OFFSET   # 128
        assert trade['exit_reason'] == 'take_profit'
        assert trade['exit_price'] == 72
        # short pnl = (entry - exit) * qty
        assert trade['pnl'] == (100 - 72) * EXPECTED_SHARES  # 980
        assert engine.portfolio.equity == INITIAL_EQUITY + 980

    def test_position_left_open_when_no_exit_hit(self, make_engine):
        # tp=128 / sl=72 never touched across the remaining bars
        price_df = _tseries_df(highs=[105, 110, 115], lows=[98, 95, 90], closes=[100, 100, 100])
        engine = make_engine(price_df)

        pos_df, equity_df = engine.trade_entry_execution(_signals([0, 1, 0]), RISK_PCT, ATR_MULTIPLIER, ATR)

        trade = pos_df.iloc[0]
        assert trade['status'] == 'open'
        assert pd.isna(trade['exit_price'])
        assert pd.isna(trade['pnl'])
        assert (equity_df['price'] == INITIAL_EQUITY).all() # Equity shouldnt update until trade is closed
        assert engine.portfolio.equity == INITIAL_EQUITY

    def test_commodity_long_take_profit(self, make_engine):
        price_df = _commodity_df(prices=[100, 100, 130])
        engine = make_engine(price_df, asset_type='commodity')

        pos_df, equity_df = engine.trade_entry_execution(_signals([0, 1, 0]), RISK_PCT, ATR_MULTIPLIER, ATR)

        trade = pos_df.iloc[0]
        assert trade['symbol'] == 'COPPER'
        assert trade['entry_price'] == 100
        assert trade['exit_reason'] == 'take_profit'
        assert trade['exit_price'] == 128
        assert trade['pnl'] == (128 - 100) * EXPECTED_SHARES  # 980
        assert engine.portfolio.equity == INITIAL_EQUITY + 980