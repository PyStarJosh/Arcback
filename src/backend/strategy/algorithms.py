import pandas as pd
from .indicators import Indicators

class Algorithms:
    """Startegy Implementation"""
    
    @staticmethod    
    def ma_crossover(price_data: pd.Series, dt_series: pd.Series, short_period: int, long_period: int) -> pd.DataFrame:
        result = pd.DataFrame(
            {
                'ema_short': Indicators.ema(price_data, short_period).values,
                'sma_long': Indicators.sma(price_data, long_period).values,
                'signal': 0,
            }, index=dt_series
        )
        ema_short, sma_long = result["ema_short"], result["sma_long"]

        # Provides boolean values that are used for buy or sell signals
        is_bullish, is_bearish = ema_short > sma_long, ema_short < sma_long
        buy_crossing = (is_bullish) & (ema_short.shift(1) <= sma_long.shift(1))
        sell_crossing = (is_bearish) & (ema_short.shift(1) >= sma_long.shift(1))

        # Result signal column population
        result.loc[buy_crossing, "signal"] = 1
        result.loc[sell_crossing, "signal"] = -1
         
        return result