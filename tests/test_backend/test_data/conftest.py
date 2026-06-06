from unittest.mock import patch
import pytest
from src.backend import Loader, Processor, DataManager

@pytest.fixture
def loader():
    av_api_key = 'src.backend.data.loader.Constants.get_alphavantage_api_key'
    td_api_key = 'src.backend.data.loader.Constants.get_twelvedata_api_key'
    with patch(av_api_key, return_value='fake'), \
        patch(td_api_key, return_value='fake'):
        yield Loader() # returns Loader obj with patches being applied

@pytest.fixture
def processor():
    with patch('src.backend.data.processor.sqlite3.connect'):
        yield Processor()
        
@pytest.fixture
def data_manager():
    with patch('src.backend.data.data_manager.Loader'), \
        patch('src.backend.data.data_manager.Processor'):
        yield DataManager()