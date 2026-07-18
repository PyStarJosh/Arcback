import pandas as pd
import numpy as np

class Portfolio:
    '''Emulates & executes the properties and operations of a investment portfolio account'''
    
    def __init__(self, equity: float, dt_index: pd.DatetimeIndex) -> None:
        if equity <= 0:
            raise ValueError('The balance must be greater than $0')
        self.equity = equity
        self.equity_df = pd.DataFrame(
            {
                'price': np.nan,
            }, index= dt_index
        )
        self.equity_df.iat[0, 0] = self.equity
    
    def adjust_equity(self, amount: float) -> float:
        '''adjusts the portfolio's balance based on passed float amount'''
        self.equity += amount
        return self.equity