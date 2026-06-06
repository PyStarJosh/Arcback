import pytest
import pandas as pd
import sqlite3
from unittest.mock import patch, MagicMock
from .conftest import processor

class TestProcessor:
    """A class to test Processor class."""
    
    def test_get_time_series_data(self, processor):
        processor.cur.fetchall.return_value = [
            (
            'AAPL',
            '1day',
            '2022-01-02',
            20.46,
            30.23,
            15.78,
            17.52,
            93
            )
        ]
        result = processor.get_time_series_data('AAPL', '1day')
        assert isinstance(result, pd.DataFrame)
        assert list(result.columns) == [
            'symbol',
            'interval',
            'open',
            'high',
            'low',
            'close',
            'volume'
        ]
        
        assert result.index.name == 'datetime'
        
    def test_get_commodity_data(self, processor):
       processor.cur.fetchall.return_value = (('daily', 'COPPER', '01-11-2022', '23.4534'),)
       result = processor.get_commodity_data('COPPER', 'daily')
       assert isinstance(result, pd.DataFrame)
       assert list(result.columns) == ['interval', 'commodity_type', 'price']
       assert result.index.name == 'date'
        
    def test_get_last_updated(self, processor):
        processor.cur.fetchone.return_value = ('01-22-2024', '01-01-2026')
        result = processor.get_last_updated('AAPL', '1day')
        assert isinstance(result, dict)
        assert {'start_date','last_date'} <= result.keys() # checks if set is subset of dict_keys()
            
    def test_populate_time_series_data_table_raises_on_operational_error(self, processor):
        with patch.object(processor.cur, 'execute', side_effect=sqlite3.OperationalError):
            with pytest.raises(sqlite3.OperationalError):
                processor.populate_time_series_data_table(
                    'interval',
                    {'values': [{
                    'datetime': '2022-01-02',
                    'open': '20.00',
                    'high': '30.00',
                    'low': '15.00',
                    'close': '17.00',
                    'volume': '93'
                    }]},
                    'symbol')
                
    def test_populate_commodities_prices_table_raises_on_operation_error(self, processor):
        with patch.object(processor.cur, 'execute', side_effect=sqlite3.OperationalError):
            with pytest.raises(sqlite3.OperationalError):
                processor.populate_commodities_prices_table(
                    { 'data': [
                        {
                          'date': '01-01-2026',
                          'value': '5423.324'
                        }]
                    }, 'monthly', 'COPPER'
                )
    
    def test_populate_time_series_data_table(self, processor):
        data_dict = {
            'values': [
                {'datetime': '2022-01-02', 'open': '20.46', 'high': '30.23', 'low': '15.78', 'close': '17.52', 'volume': '93'},
                {'datetime': '2022-01-03', 'open': '21.00', 'high': '31.00', 'low': '16.00', 'close': '18.00', 'volume': '100'}
            ]
        }
        processor.cur.reset_mock()
        processor.conn.reset_mock()
        processor.cur.fetchone.return_value = None
        processor.populate_time_series_data_table('1day', data_dict, 'AAPL')

        assert processor.cur.execute.call_count == 4 # once per row x 2
        processor.conn.commit.call_count == 2
        
    def test_populate_commodities_prices_table(self, processor):
        data_dict = {"data": [
        {
            "date": "2026-05-01",
            "value": "13483.75153846154"
        },
        {
            "date": "2026-04-01",
            "value": "12890.68772727273"
        },
        {
            "date": "2026-03-01",
            "value": "12528.70954545455"
        }
        ]
        }
        processor.cur.execute.reset_mock()
        processor.conn.commit.reset_mock()
        processor.cur.fetchone.return_value = None
        processor.populate_commodities_prices_table(data_dict, 'monthly', 'COPPER')
        
        assert processor.cur.execute.call_count == 5
        processor.conn.commit.call_count == 2