# import pandas as pd

# class Portfolio:
#     '''Emulates & executes the properties and operations of a investment portfolio account'''
    
    
#     def __init__(self, balance: float, dt_index: pd.DatetimeIndex) -> None:
#         if balance <= 0:
#             raise ValueError('The balance must be greater than $0')
#         self.balance = balance
#         self.portfolio = pd.DataFrame(
#             {
#                 'price': self.balance,
#             }, index= dt_index
#         )
    
#     def adjust_balance(self, amount: float, datetime: pd.DatetimeIndex) -> pd.DataFrame:
#         '''adjusts the portfolio's balance based on passed float amount'''
#         self.balance += amount
#         self.portfolio.loc[datetime, 'price'] = self.balance
#         self.portfolio.loc[datetime, 'frac_change'] = self.portfolio.loc[datetime, 'pct_change'] / self.portfolio.loc[datetime, 'price'].shift(1)
#         return self.portfolio