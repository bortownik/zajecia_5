from src.manager import Manager
from src.models import Parameters, Bill, ApartmentSettlement, Transfer


def test_get_tenant_settlements_multiple_tenants():
    manager = Manager(Parameters())

    manager.bills.append(Bill(
        apartment='apart-polanka',
        date_due='2025-02-15',
        settlement_year=2025,
        settlement_month=2,
        amount_pln=300.0,
        type='electricity'
    ))

    apartment_settlement = ApartmentSettlement(
        apartment='apart-polanka',
        month=2,
        year=2025,
        total_rent_pln=4500.0,
        total_bills_pln=300.0,
        total_due_pln=4200.0
    )

    tenant_settlements = manager.get_tenant_settlements(apartment_settlement)

    assert len(tenant_settlements) == 3
    
    settlement_tenant_1 = next(s for s in tenant_settlements if s.tenant == 'tenant-1')
    assert settlement_tenant_1.apartment_settlement == 'apart-polanka'
    assert settlement_tenant_1.month == 2
    assert settlement_tenant_1.year == 2025
    assert settlement_tenant_1.rent_pln == 1500.0
    assert settlement_tenant_1.bills_pln == 100.0
    assert settlement_tenant_1.total_due_pln == 1600.0
    assert settlement_tenant_1.balance_pln == -1600.0

    settlement_tenant_2 = next(s for s in tenant_settlements if s.tenant == 'tenant-2')
    assert settlement_tenant_2.rent_pln == 1400.0
    assert settlement_tenant_2.bills_pln == 100.0
    assert settlement_tenant_2.total_due_pln == 1500.0

    settlement_tenant_3 = next(s for s in tenant_settlements if s.tenant == 'tenant-3')
    assert settlement_tenant_3.rent_pln == 1300.0
    assert settlement_tenant_3.bills_pln == 100.0
    assert settlement_tenant_3.total_due_pln == 1400.0


def test_get_tenant_settlements_single_tenant():
    manager = Manager(Parameters())

    manager.bills.append(Bill(
        apartment='apart-polanka',
        date_due='2025-03-15',
        settlement_year=2025,
        settlement_month=3,
        amount_pln=450.0,
        type='water'
    ))

    apartment_settlement = ApartmentSettlement(
        apartment='apart-polanka',
        month=3,
        year=2025,
        total_rent_pln=1500.0,
        total_bills_pln=450.0,
        total_due_pln=1050.0
    )

    manager.tenants = {
        'tenant-1': manager.tenants['tenant-1']
    }

    tenant_settlements = manager.get_tenant_settlements(apartment_settlement)

    assert len(tenant_settlements) == 1
    
    settlement = tenant_settlements[0]
    assert settlement.tenant == 'tenant-1'
    assert settlement.apartment_settlement == 'apart-polanka'
    assert settlement.month == 3
    assert settlement.year == 2025
    assert settlement.rent_pln == 1500.0
    assert settlement.bills_pln == 450.0
    assert settlement.total_due_pln == 1950.0
    assert settlement.balance_pln == -1950.0


def test_get_tenant_settlements_no_tenants():
    manager = Manager(Parameters())

    manager.bills.append(Bill(
        apartment='apart-polanka',
        date_due='2025-04-15',
        settlement_year=2025,
        settlement_month=4,
        amount_pln=200.0,
        type='internet'
    ))

    apartment_settlement = ApartmentSettlement(
        apartment='apart-polanka',
        month=4,
        year=2025,
        total_rent_pln=0.0,
        total_bills_pln=200.0,
        total_due_pln=200.0
    )

    manager.tenants = {}

    tenant_settlements = manager.get_tenant_settlements(apartment_settlement)

    assert len(tenant_settlements) == 0
    assert isinstance(tenant_settlements, list)
