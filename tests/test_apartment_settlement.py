from src.manager import Manager
from src.models import Parameters, Bill, Transfer


def test_get_apartment_settlement():
    manager = Manager(Parameters())

    manager.bills.append(Bill(
        apartment='apart-polanka',
        date_due='2025-02-15',
        settlement_year=2025,
        settlement_month=2,
        amount_pln=150.0,
        type='electricity'
    ))

    manager.bills.append(Bill(
        apartment='apart-polanka',
        date_due='2025-02-15',
        settlement_year=2025,
        settlement_month=2,
        amount_pln=200.0,
        type='water'
    ))

    manager.transfers.append(Transfer(
        amount_pln=2500.0,
        date='2025-02-04',
        settlement_year=2025,
        settlement_month=2,
        tenant='tenant-1'
    ))

    manager.transfers.append(Transfer(
        amount_pln=2500.0,
        date='2025-02-05',
        settlement_year=2025,
        settlement_month=2,
        tenant='tenant-2'
    ))

    settlement = manager.get_apartment_settlement('apart-polanka', 2025, 2)

    assert settlement is not None
    assert settlement.apartment == 'apart-polanka'
    assert settlement.year == 2025
    assert settlement.month == 2
    assert settlement.total_bills_pln == 350.0
    assert settlement.total_rent_pln == 5000.0
    assert settlement.total_due_pln == 4650.0


def test_get_apartment_settlement_no_bills():
    manager = Manager(Parameters())

    manager.transfers.append(Transfer(
        amount_pln=2500.0,
        date='2025-03-04',
        settlement_year=2025,
        settlement_month=3,
        tenant='tenant-1'
    ))

    manager.transfers.append(Transfer(
        amount_pln=2500.0,
        date='2025-03-05',
        settlement_year=2025,
        settlement_month=3,
        tenant='tenant-2'
    ))

    settlement = manager.get_apartment_settlement('apart-polanka', 2025, 3)

    assert settlement is not None
    assert settlement.apartment == 'apart-polanka'
    assert settlement.year == 2025
    assert settlement.month == 3
    assert settlement.total_bills_pln == 0.0
    assert settlement.total_rent_pln == 5000.0
    assert settlement.total_due_pln == 5000.0
