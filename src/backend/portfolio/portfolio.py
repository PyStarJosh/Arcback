import pandas as pd

class Portfolio:
    '''Emulates & executes the properties and operations of a investment portfolio account'''
    
    def __init__(self, equity: float, dt_index: pd.DatetimeIndex) -> None:
        if equity <= 0:
            raise ValueError('The balance must be greater than $0')
        self.equity = equity
        self.portfolio = pd.DataFrame(
            {
                'price': self.equity,
            }, index= dt_index
        )
    
    def adjust_equity(self, amount: float) -> float:
        '''adjusts the portfolio's balance based on passed float amount'''
        self.equity += amount
        return self.equity