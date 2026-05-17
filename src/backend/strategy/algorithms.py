import pandas as pd
from .indicators import Indicators


class Algorithms:
    """Startegy Implementation"""

    def __init__(self):
        self.indicators = Indicators()

    def ma_crossover(self, df: pd.DataFrame, short_period: int, long_period: int) -> pd.DataFrame:
        # creates a copy of passed DataFrame data structure and creates 3 columns
        # 2 columns hold the returned series from the ma indicators and the last one hold the
        # buy or sell signals that will be used by engine.py
        result = df.copy()
        result["ema_short"] = self.indicators.ema(result["closes"], short_period)
        result["sma_long"] = self.indicators.sma(result["closes"], long_period)
        result["signal"] = 0  # init pandas series with default values of 0
        ema_short, sma_long = result["ema_short"], result["sma_long"]

        # Provides boolean values that are used for buy or sell signals
        is_bullish, is_bearish = ema_short > sma_long, ema_short < sma_long
        buy_crossing = (is_bullish) & (ema_short.shift(1) <= sma_long.shift(1))
        sell_crossing = (is_bearish) & (ema_short.shift(1) >= sma_long.shift(1))

        # Result signal column population
        result.loc[buy_crossing, "signal"] = 1
        result.loc[sell_crossing, "signal"] = -1

        return result
