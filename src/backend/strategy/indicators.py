import pandas as pd

class Indicators:
    """Houses all available indicators"""
    
    # Takes price_data['close'] value and creating a rolling array of window period and calculates the mean
    def sma(self, price_data: pd.Series, period: int) -> pd.Series:
        return price_data.rolling(window=period).mean()
    
    # Takes price_data['close] value, creates a exponentially weighted window view of this data with the smoothing
    # factor of a N-period EMA followed by using the recursive forumla a * P(t) + (1-a) * EMA(P(-t))
    def ema(self, price_data: pd.Series, period: int) -> pd.Series:
        return price_data.ewm(span=period, adjust=False).mean()