import pytest
import pandas as pd

@pytest.fixture
def price_data():
    return pd.Series([
        100.0,
        102.5,
        101.0,
        105.3,
        107.8,
        106.2,
        110.0,
        108.5,
        112.3,
        115.0,
        93.23,
        53.23,
        534.43,
        43.12,
        53.23
        ]
    )
    
@pytest.fixture
def dt_series(price_data):
    return pd.date_range(
        start='2020-01-01',
        periods=len(price_data),
        freq='D'
    )