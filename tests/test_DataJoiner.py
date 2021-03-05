import pytest
from azure_data_scraper.data_joiner import DataJoiner
from azure_data_scraper.audit_scope_scraper import AuditScopes
from azure_data_scraper.product_by_region_scraper import ProductsByRegion

# "Constaints"

# "Fixtures"


@pytest.fixture(scope="session")
def dataj():  
    return DataJoiner()

# Tests


def test_isInitialized(dataj):
    assert len(dataj.product_list()) > 0
    assert len(dataj.category_list()) > 0

@pytest.mark.parametrize("service", [
    ("API Management"),
    ("Application Gateway")
])
def test_verifyDataJoined(dataj, service):
    prod = dataj.getProductDetails(service)

    assert len(prod['azure-public']['ga']) > 0
    assert len(prod['azure-public']['scopes']) > 0
    assert len(prod['azure-government']['ga']) > 0
    assert len(prod['azure-government']['scopes']) > 0
    
