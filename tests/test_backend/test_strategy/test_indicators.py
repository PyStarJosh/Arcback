import pytest
import pandas as pd
from src.backend import Indicators

class TestIndicators:
    
    def test_sma(self, price_data):
        expected_result = pd.Series([
            float('nan'),
            float('nan'),
            float('nan'),
            float('nan'),
            103.32,
            104.56,
            106.06,
            107.56,
            108.96,
            110.4,
            107.806,
            96.452,
            181.638,
            167.802,
            155.448
        ])
        result = Indicators.sma(price_data, period=5)
        pd.testing.assert_series_equal(
            result, expected_result,
            check_names=False, 
            check_dtype=True,
            rtol=1e-3)
        
    def test_ema(self, price_data):
        expected_result = pd.Series([
            100.0000,
            101.2500,
            101.1250,
            103.2125,
            105.5063,
            105.8531,
            107.9266,
            108.2133,
            110.2566,
            112.6283,
            102.9292,
            78.0796,
            306.2548,
            174.6874,
            113.9587,
        ])

        result = Indicators.ema(price_data, period=3)
        pd.testing.assert_series_equal(
            result, expected_result,
            check_names=False, 
            check_dtype=True, 
            rtol=1e-3
        )                     