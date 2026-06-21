from src.backend import Sizing

class TestSizing:
    
    def test_volatility_targeted_sizing(self):
        result = Sizing.volatility_targeted_sizing(risk_pct=0.01, equity=100_000, atr_multiplier=2, atr=14)
        assert result == 35