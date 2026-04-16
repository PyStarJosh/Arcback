import requests
import logging
from ..constants import Constants 

# Logger initialization
logger = logging.getLogger(__name__) # Allows for proper error logging of functions utilizing logging config from main py

class Loader():
    """Loads EOD Data from Financial Data API dating back 10yrs"""
        
        
    def __init__(self):
        self.__API_KEY = Constants.get_api_key()


    # Returns a JSON file of raw EOD stock data
    def get_raw_stock_data(self, symbol):
        url = f'''https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol.upper()}&apikey={self.__API_KEY}'''
        try:
            r = requests.get(url, timeout=5) # Makes HTTP request to Alpha Vantage APi with a timeout of 5 seconds
            r.raise_for_status() # Raises an HTTPError if the HTTP request returned an unsuccessful status code
            data = r.json()
            return data
        except(requests.exceptions.ConnectionError) as errc: # Most common error, catches HTTP connection errors
            logger.critical(f"HTTP Connection Error: {errc}")
        except(requests.exceptions.Timeout) as errh: # Catches  HTTP Timeout errors
            logger.critical(f"HTTP Timeout Error: {errh}")
        except(requests.exceptions.HTTPError) as erra: # Catches HTTP unsuccessful status code errors
            logger.critical(f"HTTP Error: {erra.args[0]}")
        except(requests.exceptions.RequestException) as err: # Catches any other HTTP request errors 
            logger.critical(f"HTTP Request Error: {err}") 
            
            
     # Returns a JSON file of raw EOD forex data
    def get_raw_forex_data(self, from_currency, to_currency):
        url = f'''https://www.alphavantage.co/query?function=FX_DAILY&from_symbol={from_currency.upper()}&to_symbol={to_currency.upper()}&apikey={self.__API_KEY}'''
        try:
            r = requests.get(url, timeout=5)
            r.raise_for_status()
            data = r.json()
            return data
        except(requests.exceptions.ConnectionError) as errc: # Most common error, catches HTTP connection errors
                logger.critical(f"HTTP Connection Error: {errc}")
        except(requests.exceptions.Timeout) as errh: # Catches  HTTP Timeout errors
                logger.critical(f"HTTP Timeout Error: {errh}")
        except(requests.exceptions.HTTPError) as erra: # Catches HTTP unsuccessful status code errors
                logger.critical(f"HTTP Error: {erra.args[0]}")
        except(requests.exceptions.RequestException) as err: # Catches any other HTTP request errors 
                logger.critical(f"HTTP Request Error: {err}")
    
    
     # Returns a JSON file of raw EOD cryptocurrency data
    def get_raw_crypto_data(self, symbol, market='USD'):
        url = f'''https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_DAILY&symbol={symbol.upper()}&market={market.upper()}&apikey={self.__API_KEY}'''
        try:
            r = requests.get(url, timeout=5)
            r.raise_for_status()
            data = r.json()
            return data
        except(requests.exceptions.ConnectionError) as errc: # Most common error, catches HTTP connection errors
            logger.critical(f"HTTP Connection Error: {errc}")
        except(requests.exceptions.Timeout) as errh: # Catches  HTTP Timeout errors
            logger.critical(f"HTTP Timeout Error: {errh}")
        except(requests.exceptions.HTTPError) as erra: # Catches HTTP unsuccessful status code errors
            logger.critical(f"HTTP Error: {erra.args[0]}")
        except(requests.exceptions.RequestException) as err: # Catches any other HTTP request errors 
            logger.critical(f"HTTP Request Error: {err}")
    
    
    # Returns a JSON file of raw EOD Gold data
    def get_raw_gold_data(self, interval="daily"):
        url = f'''https://www.alphavantage.co/query?function=GOLD_SILVER_HISTORY&symbol=XAU&interval={interval.lower()}&apikey={self.__API_KEY}'''
        try:
            r = requests.get(url, timeout=5)
            r.raise_for_status()
            data = r.json()
            return data
        except(requests.exceptions.ConnectionError) as errc: # Most common error, catches HTTP connection errors
            logger.critical(f"HTTP Connection Error: {errc}")
        except(requests.exceptions.Timeout) as errh: # Catches  HTTP Timeout errors
            logger.critical(f"HTTP Timeout Error: {errh}")
        except(requests.exceptions.HTTPError) as erra: # Catches HTTP unsuccessful status code errors
            logger.critical(f"HTTP Error: {erra.args[0]}")
        except(requests.exceptions.RequestException) as err: # Catches any other HTTP request errors 
            logger.critical(f"HTTP Request Error: {err}")
    
    
    # Returns a JSON file of raw EOD Silver data
    def get_raw_silver_data(self, interval='daily'):
        url = f'''https://www.alphavantage.co/query?function=GOLD_SILVER_HISTORY&symbol=XAG&interval={interval.lower()}&apikey={self.__API_KEY}'''
        try:
            r = requests.get(url, timeout=5)
            r.raise_for_status()
            data = r.json()
            return data
        except(requests.exceptions.ConnectionError) as errc: # Most common error, catches HTTP connection errors
            logger.critical(f"HTTP Connection Error: {errc}")
        except(requests.exceptions.Timeout) as errh: # Catches  HTTP Timeout errors
            logger.critical(f"HTTP Timeout Error: {errh}")
        except(requests.exceptions.HTTPError) as erra: # Catches HTTP unsuccessful status code errors
            logger.critical(f"HTTP Error: {erra.args[0]}")
        except(requests.exceptions.RequestException) as err: # Catches any other HTTP request errors 
            logger.critical(f"HTTP Request Error: {err}")
    
    
    # Returns a JSON file of raw EOD commodities data (excluding silver and gold)
    def get_raw_commodities_data(self, commodity_type, interval='daily'):
        url = f'''https://www.alphavantage.co/query?function={commodity_type.upper()}&interval={interval.lower()}&apikey={self.__API_KEY}'''
        try:
            r = requests.get(url, timeout=5)
            r.raise_for_status()
            data = r.json()
            return data
        except(requests.exceptions.ConnectionError) as errc: # Most common error, catches HTTP connection errors
            logger.critical(f"HTTP Connection Error: {errc}")
        except(requests.exceptions.Timeout) as errh: # Catches  HTTP Timeout errors
            logger.critical(f"HTTP Timeout Error: {errh}")
        except(requests.exceptions.HTTPError) as erra: # Catches HTTP unsuccessful status code errors
            logger.critical(f"HTTP Error: {erra.args[0]}")
        except(requests.exceptions.RequestException) as err: # Catches any other HTTP request errors 
            logger.critical(f"HTTP Request Error: {err}")
    