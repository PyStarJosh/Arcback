import requests
import logging
from ..constants import Constants 

# Logger initialization
logger = logging.getLogger(__name__) # Allows for proper error logging of functions utilizing logging config from main py

class Loader:
    """Loads EOD Data from Financial Data API dating back 10yrs"""
    
    BASE_URL = 'https://www.alphavantage.co/query?'
    SUPPORTED_SYMBOLS = {'GOOGL': ''}
    VALID_COMMODITIES_INTERVALS = {
        'WTI': ['daily', 'weekly', 'monthly'],
        'BRENT': ['daily', 'weekly', 'monthly'],
        'COPPER': ['monthly', 'quarterly', 'annual'],
        'WHEAT': ['monthly', 'quarterly', 'annual'],
        'ALUMINUM': ['monthly', 'quarterly', 'annual'],
        'CORN': ['monthly', 'quarterly', 'annual'],
        'COTTON':['monthly', 'quarterly', 'annual'],
        'SUGAR':['monthly', 'quarterly', 'annual'],
        'COFFEE':['monthly', 'quarterly', 'annual'],
        'NATURAL_GAS':['daily', 'weekly', 'monthly'],
        }
    AV_API_ERROR_RESPONSES = {
        'Error Message': 'Invalid API Call',
        'Information': 'API Rate Limit Exceeded',
        'Note': 'API Rate Limit Exceeded',
        }
        
        
    def __init__(self):
        self.__API_KEY = Constants.get_api_key()


    def _call_api(self, url):
        try:
            r = requests.get(url, timeout=5) # Makes HTTP request to Alpha Vantage APi with a timeout of 5 seconds
            r.raise_for_status() # Raises an HTTPError if the HTTP request returned an unsuccessful status code
            data = r.json()
            for key in self.AV_API_ERROR_RESPONSES: 
                if key in data:
                    raise ValueError(data[key]) # Passes Alpha Vantage message to ValueError except block
            return data
        except(requests.exceptions.ConnectionError) as http_connection_error: # Most common error, catches HTTP connection errors
            logger.critical(f"HTTP Connection Error: {http_connection_error}")
            raise
        except(requests.exceptions.Timeout) as http_timeout: # Catches  HTTP Timeout errors
            logger.critical(f"HTTP Timeout Error: {http_timeout}")
            raise
        except(requests.exceptions.HTTPError) as http_error: # Catches HTTP unsuccessful status code errors
            logger.critical(f"HTTP Error: {http_error.args[0]}")
            raise
        except(requests.exceptions.JSONDecodeError):
            logger.critical('Response was not valid JSON')
            raise
        except(ValueError) as value_error:
            logger.critical(f'Unsuccessful API Call: {value_error}')
            raise
        except(requests.exceptions.RequestException) as request_error: # Catches any other HTTP request errors 
            logger.critical(f"HTTP Request Error: {request_error}")
            raise

    # Returns a JSON file of raw EOD stock data
    def get_raw_stock_data(self, symbol):
        url = f'''{self.BASE_URL}function=TIME_SERIES_DAILY&symbol={symbol.upper()}&apikey={self.__API_KEY}'''
        return self._call_api(url) 
            
            
     # Returns a JSON file of raw EOD forex data
    def get_raw_forex_data(self, from_currency, to_currency):
        url = f'''{self.BASE_URL}function=FX_DAILY&from_symbol={from_currency.upper()}&to_symbol={to_currency.upper()}&apikey={self.__API_KEY}'''
        return self._call_api(url)
    
    
     # Returns a JSON file of raw EOD cryptocurrency data
    def get_raw_crypto_data(self, symbol, market='USD'):
        url = f'''{self.BASE_URL}function=DIGITAL_CURRENCY_DAILY&symbol={symbol.upper()}&market={market.upper()}&apikey={self.__API_KEY}'''
        return self._call_api(url)
    
    
    # Returns a JSON file of raw EOD Gold data
    def get_raw_gold_data(self, interval="daily"):
        url = f'''{self.BASE_URL}function=GOLD_SILVER_HISTORY&symbol=XAU&interval={interval.lower()}&apikey={self.__API_KEY}'''
        return self._call_api(url)
    
    
    # Returns a JSON file of raw EOD Silver data
    def get_raw_silver_data(self, interval='daily'):
        url = f'''{self.BASE_URL}function=GOLD_SILVER_HISTORY&symbol=XAG&interval={interval.lower()}&apikey={self.__API_KEY}'''
        return self._call_api(url)
    
    
    # Returns a JSON file of raw EOD commodities data (excluding silver and gold)
    def get_raw_commodities_data(self, commodity_type, interval='daily'):        
        if commodity_type.upper() not in self.VALID_COMMODITIES_INTERVALS:
            raise ValueError(f'Unsupported Commodity Type: {commodity_type}')
        if interval.lower() not in self.VALID_COMMODITIES_INTERVALS[commodity_type.upper()]:
            raise ValueError(f'Unsupported Interval: {interval.lower()} for {commodity_type.upper()}')
        url = f'''{self.BASE_URL}function={commodity_type.upper()}&interval={interval.lower()}&apikey={self.__API_KEY}'''
        return self._call_api(url) 
    