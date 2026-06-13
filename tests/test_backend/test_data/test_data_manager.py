import pytest
from unittest.mock import MagicMock, patch

class TestDataManager:
    """A class used to test DataManager."""
    
    def test_get_formatted_time_series_data_never_fetched(self, data_manager):
        data_manager.processor.get_last_updated.return_value = None
        response_dict = {'values': [{'close': '200.00'}]}
        data_manager.loader.get_time_series_data.return_value = response_dict
        data_manager.processor.populate_time_series_data_table.return_value = None
        data_manager.processor.get_time_series_data.return_value = response_dict
        result = data_manager.get_formatted_time_series_data('AAPL', '1day')
            
        assert result == response_dict
        
    def test_get_formatted_time_series_data_with_no_fetch_needed(self, data_manager):
        dates_dict = {
            'start_date': '01-01-2020',
            'last_date': '01-01-2026'
        }
        response_dict = {'values': [{'close': '200.00'}]}
        data_manager.processor.get_last_updated.return_value = dates_dict
        data_manager.processor.get_time_series_data.return_value = response_dict
        with patch.object(data_manager, '_get_missing_range', return_value=(False, None, None)):
            result = data_manager.get_formatted_time_series_data('AAPL', '1day')
            
        assert result == response_dict
        
    def test_get_formatted_time_series_data_with_start_date_fetch(self, data_manager):
        dates_dict = {
            'start_date': '01-01-2020',
            'last_date': '01-01-2026'
        }
        response_dict = {'values': [{'close': '200.00'}]}
        data_manager.processor.get_last_updated.return_value = dates_dict
        data_manager.loader.get_time_series_data.return_value = response_dict
        data_manager.processor.populate_time_series_data_table.return_value = None
        data_manager.processor.get_time_series_data.return_value = response_dict
        with patch.object(data_manager, '_get_missing_range', return_value=(True, '01-01-2019', dates_dict['last_date'])):
            result = data_manager.get_formatted_time_series_data('AAPL', '1day')
            
        assert result == response_dict
    
    def test_get_formatted_time_series_data_with_end_date_fetch(self, data_manager):
        dates_dict = {
            'start_date': '01-01-2020',
            'last_date': '01-01-2026'
        }
        response_dict = {'values': [{'close': '200.00'}]}
        data_manager.processor.get_last_updated.return_value = dates_dict
        data_manager.loader.get_time_series_data.return_value = response_dict
        data_manager.processor.populate_time_series_data_table.return_value = None
        data_manager.processor.get_time_series_data.return_value = response_dict
        with patch.object(data_manager, '_get_missing_range', return_value=(True, dates_dict['start_date'], '01-01-2027')):
            result = data_manager.get_formatted_time_series_data('AAPL', '1day')
            
        assert result == response_dict
        
    def test_get_formatted_time_series_data_with_start_and_end_date_fetch(self, data_manager):
        dates_dict = {
            'start_date': '2020-01-01',
            'last_date': '2020-01-02'
        }
        response_dict = {'values': [{'close': '283.3424'}]}
        data_manager.loader.get_time_series_data.return_value = response_dict
        data_manager.processor.populate_time_series_data_table.return_value = None
        data_manager.processor.get_time_series_data.return_value = response_dict
        with patch.object(data_manager, '_get_missing_range', return_value=(True, None, None)):
            result = data_manager.get_formatted_time_series_data('AAPL', '1day', None, None)
        
        assert result == response_dict
        
    def test_get_formatted_commodities_data(self, data_manager):
        response_dict = {'values': [{'price': '123.243'}]}
        data_manager.loader.get_commodities_data.return_value = response_dict
        data_manager.processor.populate_commodities_prices_table.return_value = None
        result = data_manager.processor.get_commodity_data.return_value = response_dict
        assert result == response_dict