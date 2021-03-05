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
    assert len(dataj.getJoinedData().keys()) > 0
    assert len(dataj.getProductDictionary().keys()) > 0

    assert len(dataj.getCategoryDictionary().keys()) > 0

    assert type(dataj.audit_scopes()) is AuditScopes
    assert type(dataj.product_availability()) is ProductsByRegion


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


@pytest.mark.parametrize("prod_id, expected_result", [
    ('API Management', True),  # service
    ('AI Builder', True),  # capability
    ('', False),  # empty
    (None, False)  # None
])
def test_getProductDetails(dataj, prod_id, expected_result):
    prod = dataj.getProductDetails(prod_id)
    assert type(prod) is dict
    print ('keys', prod.keys()) 
    assert (len(prod.keys()) > 0) == expected_result

@pytest.mark.parametrize("prod_id, expected_result", [
    ('API Management', True),  # service
    ('AI Builder', False),  # capability
    ('', False),  # empty
    (None, False)  # None
])
def test_getServiceDetails(dataj, prod_id, expected_result):
    prod = dataj.getServiceDetails(prod_id)
    assert type(prod) is dict
    print ('keys', prod.keys()) 
    assert (len(prod.keys()) > 0) == expected_result

@pytest.mark.parametrize("prod_id, expected_result", [
    ('API Management', False),  # service
    ('AI Builder', True),  # capability
    ('', False),  # empty
    (None, False)  # None
])
def test_getCapabilityDetails(dataj, prod_id, expected_result):
    prod = dataj.getCapabilityDetails(prod_id)
    assert type(prod) is dict
    print ('keys', prod.keys()) 
    assert (len(prod.keys()) > 0) == expected_result

def test_getServiceDetailsDeep(dataj):
    cog = dataj.getServiceDetailsDeep("Azure Cognitive Services")

    assert cog['prod-id'] == "Azure Cognitive Services"
    assert type(cog['capabilities']) is dict
    assert 'Personalizer' in cog['capabilities']
    assert type(cog['capabilities']['Personalizer']) is dict


@pytest.mark.parametrize("cat_id, expected_result", [
    ('Compute', True),  
    ('SUPER LASERS', False),  
    ('', False),  
    (None, False)
])
def test_getCategoryServiceList(dataj, cat_id, expected_result):
    assert (len(dataj.getCategoryServiceList(cat_id)) > 0) == expected_result

@pytest.mark.parametrize("cat_id, expected_result", [
    ('Compute', True),  
    ('SUPER LASERS', False),  
    ('', False),  
    (None, False)
])
def test_getCategoryServices(dataj, cat_id, expected_result):
    c = dataj.getCategoryServices(cat_id)
    assert (type(c) is dict) == True
    assert (len(c.keys()) > 0) == expected_result
