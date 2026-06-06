from unittest.mock import patch, MagicMock
import pytest
import requests
    
class TestLoader():
    """A class used to test Loader class"""
    
    def test_call_api(self, loader):
        """Test normal operations of the _call_api() method."""
        mock_response = MagicMock() # creates mock obj
        response_dict = {'values': [{'close': '200.00'}]}
        mock_response.json.return_value = response_dict # returns response_dict if .json is called on mock_response
        
        with patch('requests.get', return_value=mock_response):
            result = loader._call_api('https://fake-url.com')
            
        assert result == response_dict
    
    def test_call_api_raises_on_empty_response(self, loader):
        """Test how _call_api handles API call responses."""
        mock_response = MagicMock()
        mock_response.json.return_value = {}
        
        with patch('requests.get', return_value=mock_response):
            with pytest.raises(ValueError, match='API returned empty response'):
                loader._call_api('htps://fake-url.com')
                
    def test_call_api_raises_on_api_error_key(self, loader):
        """Test how _call_api handles returned API error messages."""
        mock_response = MagicMock()
        mock_response.json.return_value = {'Error Message': 'Invalid API Call'}
        
        with patch('requests.get', return_value=mock_response):
            with pytest.raises(ValueError):
                loader._call_api('https://fake-url.com')
    
    def test_call_api_raises_on_http_error(self, loader):
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError('404')
        
        with patch('requests.get', return_value=mock_response):
            with pytest.raises(requests.exceptions.HTTPError):
                loader._call_api('https://fake-url.com')
                
    def test_call_api_raises_on_timeout_error(self, loader):
        with patch('requests.get', side_effect=requests.exceptions.Timeout):
            with pytest.raises(requests.exceptions.Timeout):
                loader._call_api('https://fake-url.com')
                
    def test_call_api_raises_on_json_decode_error(self, loader):
        mock_response = MagicMock()
        mock_response.json.side_effect = requests.exceptions.JSONDecodeError('msg', '', 0)
        
        with patch('requests.get', return_value=mock_response):
            with pytest.raises(requests.exceptions.JSONDecodeError):
                loader._call_api('https://fake-url.com')
                
    def test_call_api_raises_on_connection_error(self, loader):
        with patch('requests.get', side_effect=requests.exceptions.ConnectionError):
            with pytest.raises(requests.exceptions.ConnectionError):
                loader._call_api('https://fake-url.com')
                
    def test_call_api_raises_on_request_error(self, loader):
        with patch('requests.get', side_effect=requests.exceptions.RequestException):
            with pytest.raises(requests.exceptions.RequestException):
                loader._call_api('https://fake-url.com')
    
    def test_get_time_series_data(self, loader):
        response_dict = {"values": [{"close": "4788.09918"}]}
        with patch.object(loader, '_call_api', return_value=response_dict):
            result = loader.get_time_series_data('AAPL', '1day')
            assert result == response_dict
            
    def test_get_commodities_data(self, loader):
        response_dict = {"values": [{"price": "234.09918"}]}
        with patch.object(loader, '_call_api', return_value=response_dict):
            result = loader.get_commodities_data('wheat', 'daily')
            assert result == response_dict
            
    def test_get_supported_symbols(self, loader):
        response_dict = {'symbols': ['AAPL', 'Tesla', 'NVDA', 'META']}
        with patch.object(loader, '_call_api', return_value=response_dict):
            result = loader.get_supported_symbols('stocks')
            assert result == response_dict