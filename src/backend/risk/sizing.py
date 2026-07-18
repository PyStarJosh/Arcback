class Sizing:
    '''Determines the position sizing'''
    
    @staticmethod
    def volatility_targeted_sizing(risk_pct: float, equity: float, atr_multiplier: int, atr: float) -> int:
        '''Returns position size based on current market volatility'''
        dollar_risk = equity * risk_pct
        stop_distance = atr_multiplier * atr
        shares = dollar_risk / stop_distance
        return int(shares)