import pandas as pd
from src.backend import Algorithms

class TestAlgorithms:

    def test_ma_crossover(self, price_data, dt_series):
        expected_result = pd.DataFrame(
                {
                   'ema_short': [
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
                        113.9587],
                   'sma_long': [
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
                        155.448],
                   'signal': [
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        -1,
                        0,
                        1,
                        0,
                        -1]
                }, index=dt_series
        )
        result = Algorithms.ma_crossover(price_data, dt_series, short_period=3, long_period=5)
        pd.testing.assert_frame_equal(result,
                                      expected_result,
                                      check_names=True,
                                      check_column_type=True,
                                      check_dtype=True,
                                      check_index_type=True,
                                      )
