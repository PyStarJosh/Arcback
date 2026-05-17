

class Sizing:
    '''Determines the position sizing'''
    
    def volatility_targeted_sizing(risk_pct: float, equity: float, atr_multiplier: int, atr: int) -> int:
        dollar_risk = equity * risk_pct
        stop_distance = atr_multiplier * atr
        shares = dollar_risk / stop_distance
        return int(shares)