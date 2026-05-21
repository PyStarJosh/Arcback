import pandas as pd

class Limits:
    '''Measure Trade Risk Exposure'''
    
    def check_exposure(portfolio: float, proposed_trade: float) -> pd.Series:
        
        return