from src.backend import Positions

class TestPositions:
    
    def test_init_assigns_default_values(self):
        position = Positions(
            entry_time= '2020-01-01',
            entry_price=100.00,
            symbol='SPCX',
            side=1,
            quantity=20,
            tp=184.32,
            sl=99.32,
        )
        
        assert position.exit_time is None
        assert position.exit_price is None
        assert position.pnl is None
        assert position.exit_reason is None
        assert position.status == 'open'