from src.manager import Manager
from src.models import Parameters, ApartmentSettlement, Bill


def test_get_apartment_settlement_with_bills():
    manager = Manager(Parameters())
    
    settlement = manager.get_apartment_settlement('apart-polanka', 2025, 1)
    
    assert settlement is not None
    assert isinstance(settlement, ApartmentSettlement)
    assert settlement.apartment == 'apart-polanka'
    assert settlement.month == 1
    assert settlement.year == 2025
    assert settlement.total_rent_pln == 4200.0
    assert settlement.total_bills_pln == 910.0
    assert settlement.total_due_pln == 5110.0


def test_get_apartment_settlement_without_bills_in_month():
    manager = Manager(Parameters())
    
    settlement = manager.get_apartment_settlement('apart-polanka', 2025, 12)
    
    assert settlement is not None
    assert settlement.apartment == 'apart-polanka'
    assert settlement.month == 12
    assert settlement.year == 2025
    assert settlement.total_rent_pln == 4200.0
    assert settlement.total_bills_pln == 0.0
    assert settlement.total_due_pln == 4200.0


def test_get_apartment_settlement_nonexistent_apartment():
    manager = Manager(Parameters())
    
    settlement = manager.get_apartment_settlement('nonexistent', 2025, 1)
    
    assert settlement is None
