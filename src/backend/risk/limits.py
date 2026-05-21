class Limits:
    '''Measure Trade Risk Exposure'''
    
    
    @staticmethod
    def valid_exposure(max_exposure: float, equity: float, proposed_trade_size: float) -> bool:
        '''Returns a bool value stating if the proposed_trade_size is within per-trade max_exposure'''
        if equity == 0: # if account has no equity auto return false
            return False
        else:
            return max_exposure >= proposed_trade_size / equity