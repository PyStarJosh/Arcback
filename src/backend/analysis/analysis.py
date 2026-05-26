import pandas as pd
from dataclasses import dataclass

@dataclass
class Analysis:
    '''Computes results from backtest and returns insights'''
    final_pos_df: pd.DataFrame
    final_equity_df: pd.DataFrame
    
    def final_equity(self) -> float:
        return self.final_equity_df.iat[-1, 0]
    
    def gross_revenue(self) -> float:
        return self.final_pos_df[self.final_pos_df['pnl'] > 0]['pnl'].sum()
    
    def net_revenue(self) -> float:
        return self.final_pos_df['pnl'].sum() 
        
    def num_of_winners(self) -> int:
        return self.final_pos_df[self.final_pos_df['pnl'] > 0]['pnl'].count()
    
    def most_profitable_trade(self) -> pd.Series:
        return self.final_pos_df.loc[self.final_pos_df['pnl'].idxmax()]