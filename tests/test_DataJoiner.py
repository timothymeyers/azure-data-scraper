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


def test_getProductDetails_NotExist(dataj):
    test = dataj.getProductDetails("")
    assert type(test) is dict
    assert test == {}

    test = dataj.getServiceDetails("")
    assert type(test) is dict
    assert test == {}

    test = dataj.getCapabilityDetails("")
    assert type(test) is dict
    assert test == {}


def test_getServiceDetailsDeep(dataj):
    cog = dataj.getServiceDetailsDeep("Azure Cognitive Services")

    assert cog['prod-id'] == "Azure Cognitive Services"
    assert type(cog['capabilities']) is dict
    assert 'Personalizer' in cog['capabilities']
    assert type(cog['capabilities']['Personalizer']) is dict


def test_getCategoryServiceList(dataj):
    assert len(dataj.getCategoryServiceList('Compute')) > 0
    assert len(dataj.getCategoryServiceList('SUPER LASERS')) == 0
    assert len(dataj.getCategoryServiceList('')) == 0
    # assert len(dataj.getCategoryServiceList(None)) == 0
