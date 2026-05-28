"""Takes the passed positions and equity dataframes to compute results and return
meaningful data to the frontend
"""
import pandas as pd
from dataclasses import dataclass

@dataclass
class Analysis:
    '''Computes results from backtest and returns insights'''
    final_pos_df: pd.DataFrame
    final_equity_df: pd.DataFrame
    
    def final_equity(self) -> float:
        return round(self.final_equity_df.iat[-1, 0], 2)
    
    def lowest_equity(self) -> float:
        return round(self.final_equity_df['price'].min(), 2)
    
    def highest_equity(self) -> float:
        return round(self.final_equity_df['price'].max(), 2) 
    
    def gross_revenue(self) -> float:
        return round(self.final_pos_df[self.final_pos_df['pnl'] > 0]['pnl'].sum(), 2)
    
    def total_losses(self) -> float:
        return round(self.final_pos_df[self.final_pos_df['pnl'] < 0]['pnl'].sum(), 2)
    
    def net_revenue(self) -> float:
        return round(self.final_pos_df['pnl'].sum(), 2)
        
    def equity_pct_change(self) -> float:
        initial_equity = round(self.final_equity_df.iat[0, 0], 2)
        return (self.final_equity() - initial_equity) / initial_equity * 100
    
    def num_of_winners(self) -> int:
        return len(self.final_pos_df[self.final_pos_df['pnl'] > 0])
    
    def num_of_losers(self) -> int:
        return len(self.final_pos_df[self.final_pos_df['pnl'] < 0])
    
    def most_profitable_trade(self) -> pd.Series:
        return self.final_pos_df.loc[self.final_pos_df['pnl'].idxmax()]
    
    def biggest_losing_trade(self) -> pd.Series:
        return self.final_pos_df.loc[self.final_pos_df['pnl'].idxmin()] 
       
    def num_of_positions(self) -> int:
        return len(self.final_pos_df)
    
    def num_of_buys(self) -> int:
        return len(self.final_pos_df[self.final_pos_df['side'] == 1])
    
    def num_of_sells(self) -> int:
        return len(self.final_pos_df[self.final_pos_df['side'] == -1])
    
    def win_percentage(self) -> float:
        return round(self.num_of_winners() / self.num_of_positions(), 2)
    
    def avg_win(self) -> float:
        return round(self.final_pos_df[self.final_pos_df['pnl'] > 0]['pnl'].mean(), 2)

    def avg_loss(self) -> float:
        return round(self.final_pos_df[self.final_pos_df['pnl'] < 0]['pnl'].mean(), 2)

    def risk_reward_ratio(self) -> float:
        return round(self.avg_win() / self.avg_loss(), 2)
    
    def profit_factor(self) -> float:
        return self.gross_revenue() / abs(self.total_losses())
    
    def drawdown(self) -> float:
        price = self.final_equity_df['price']
        rolling_peak = price.cummax()
        drawdown = (price - rolling_peak) / rolling_peak * 100
        return round(drawdown.min(), 2)
    
    def sharpe_ratio(self, risk_free_rate: float = 0.0) -> float:
        daily_returns = self.final_equity_df['price'].pct_change().dropna()
        excess_returns = daily_returns - risk_free_rate / 252
        return (excess_returns.mean() / excess_returns.std()) * (252 ** 0.5)
    
    def avg_trade_duration(self) -> int:
        closed = self.final_pos_df[self.final_pos_df['status'] == 'closed']
        return (closed['exit_price'] - closed['entry_price']).mean()