from src.models import Apartment, Bill, Parameters, Tenant, Transfer, ApartmentSettlement, TenantSettlement


class Manager:
    def __init__(self, parameters: Parameters):
        self.parameters = parameters 

        self.apartments = {}
        self.tenants = {}
        self.transfers = []
        self.bills = []
       
        self.load_data()

    def load_data(self):
        self.apartments = Apartment.from_json_file(self.parameters.apartments_json_path)
        self.tenants = Tenant.from_json_file(self.parameters.tenants_json_path)
        self.transfers = Transfer.from_json_file(self.parameters.transfers_json_path)
        self.bills = Bill.from_json_file(self.parameters.bills_json_path)

    def check_tenants_apartment_keys(self) -> bool:
        for tenant in self.tenants.values():
            if tenant.apartment not in self.apartments:
                return False
        return True
    
    def get_apartment_costs(self, apartment_key, year=None, month=None):
        if apartment_key not in self.apartments:
            return None
        
        total_costs = 0.0
        for bill in self.bills:
            if bill.apartment == apartment_key:
                if year is not None and bill.settlement_year != year:
                    continue
                if month is not None and bill.settlement_month != month:
                    continue
                total_costs += bill.amount_pln
        
        return total_costs
    
    def get_apartment_settlement(self, apartment_key, year, month):
        if apartment_key not in self.apartments:
            return None
        
        total_bills_pln = 0.0
        for bill in self.bills:
            if bill.apartment == apartment_key and bill.settlement_year == year and bill.settlement_month == month:
                total_bills_pln += bill.amount_pln
        
        total_rent_pln = 0.0
        for tenant_key, tenant in self.tenants.items():
            if tenant.apartment == apartment_key:
                for transfer in self.transfers:
                    if transfer.tenant == tenant_key and transfer.settlement_year == year and transfer.settlement_month == month:
                        total_rent_pln += transfer.amount_pln
        
        total_due_pln = total_rent_pln - total_bills_pln
        
        return ApartmentSettlement(
            apartment=apartment_key,
            month=month,
            year=year,
            total_rent_pln=total_rent_pln,
            total_bills_pln=total_bills_pln,
            total_due_pln=total_due_pln
        )
    
    def get_tenant_settlements(self, apartment_settlement):
        apartment_key = apartment_settlement.apartment
        
        apartment_tenants = [
            tenant for tenant in self.tenants.values()
            if tenant.apartment == apartment_key
        ]
        
        if not apartment_tenants:
            return []
        
        tenant_settlements = []
        number_of_tenants = len(apartment_tenants)
        bills_per_tenant = apartment_settlement.total_bills_pln / number_of_tenants
        
        for tenant_key, tenant in self.tenants.items():
            if tenant.apartment == apartment_key:
                total_due = tenant.rent_pln + bills_per_tenant
                balance = -total_due
                
                settlement = TenantSettlement(
                    tenant=tenant_key,
                    apartment_settlement=apartment_key,
                    month=apartment_settlement.month,
                    year=apartment_settlement.year,
                    rent_pln=tenant.rent_pln,
                    bills_pln=bills_per_tenant,
                    total_due_pln=total_due,
                    balance_pln=balance
                )
                tenant_settlements.append(settlement)
        
        return tenant_settlements