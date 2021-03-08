import pytest
from azure_data_scraper.data_joiner import DataJoiner
#from azure_data_scraper.audit_scope_scraper import AuditScopes
#from azure_data_scraper.product_by_region_scraper import ProductsByRegion

# "Constaints"

# "Fixtures"


@pytest.fixture(scope="session")
def dataj():
    return DataJoiner()

# Tests


def test_isInitialized(dataj):
    assert len(dataj.products_list()) > 0
    assert len(dataj.categorys_list()) > 0
    assert len(dataj.services_list()) > 0
    assert len(dataj.capabilities_list()) > 0
    assert len(dataj.getJoinedData().keys()) > 0
    assert len(dataj.getProductDictionary().keys()) > 0

    assert len(dataj.getCategoryDictionary().keys()) > 0

    #assert type(dataj.audit_scopes()) is AuditScopes
    #assert type(dataj.product_availability()) is ProductsByRegion


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





### New from PbR



@pytest.mark.parametrize("service, cloud, expected_result", [
    ("Azure Databricks", "azure-government", True),
    ("Microsoft Genomics", "azure-government", False),
    ('Azure Blueprints', "azure-government", False),
    ('Windows Virtual Desktop', "azure-government", False)
])
def test_isServiceAvailable(dataj, service, cloud, expected_result):
    assert dataj.isServiceAvailable(service, cloud) == expected_result


@pytest.mark.parametrize("capability, cloud, expected_result", [
    ("H-series", "azure-government", True),
    ("Hb-series", "azure-government", False),
    ("Hc-series", "azure-government", False)
])
def test_isCapabilityAvailable(dataj, capability, cloud, expected_result):
    assert dataj.isCapabilityAvailable(
        capability, cloud) == expected_result


@pytest.mark.parametrize("product, expected_result", [
    ("Azure Databricks", True),
    ("Azure Bot Services", True),
    ("Azure Cognitive Search", True),
    ("Microsoft Genomics", False),
    ("Azure Machine Learning", True),
    ("Machine Learning Studio", False),
    ("Azure Cognitive Services", True),
    ("Azure Open Datasets", False),
    ("Project Bonsai", False),
    ("H-series", True),
    ("Hb-series", False),
    ("Hc-series", False)

])
def test_isProductAvailableAzureGovernment(dataj, product, expected_result):
    assert dataj.isProductAvailable(product, "azure-government") == expected_result


@pytest.mark.parametrize("prod, region, expected_result", [
    ('Azure Bot Services', 'usgov-non-regional', True),
    ('Azure Cognitive Services', 'usgov-non-regional', False),
    ('Azure Cognitive Services', 'usgov-arizona', True),

    ('Azure Bot Services', 'usgov-non-regional', True),
    ('Azure Bot Services', 'us-dod-central', False),
    ('Azure Bot Services', 'us-dod-east', False),
    ('Azure Bot Services', 'usgov-arizona', False),
    ('Azure Bot Services', 'usgov-texas', False),
    ('Azure Bot Services', 'usgov-virginia', False),

    ('Data Factory', 'usgov-non-regional', False),
    ('Data Factory', 'us-dod-central', False),
    ('Data Factory', 'us-dod-east', False),
    ('Data Factory', 'usgov-arizona', True),
    ('Data Factory', 'usgov-texas', True),
    ('Data Factory', 'usgov-virginia', True),

    ('Azure Cognitive Services', 'usgov-non-regional', False),
    ('Azure Cognitive Services', 'us-dod-central', False),
    ('Azure Cognitive Services', 'us-dod-east', False),
    ('Azure Cognitive Services', 'usgov-arizona', True),
    ('Azure Cognitive Services', 'usgov-texas', False),
    ('Azure Cognitive Services', 'usgov-virginia', True),

    ('Virtual Machines', 'usgov-non-regional', False),
    ('Virtual Machines', 'us-dod-central', True),
    ('Virtual Machines', 'us-dod-east', True),
    ('Virtual Machines', 'usgov-arizona', True),
    ('Virtual Machines', 'usgov-texas', True),
    ('Virtual Machines', 'usgov-virginia', True),

    ('Cognitive Search', 'usgov-non-regional', False),
    ('Cognitive Search', 'us-dod-central', False),
    ('Cognitive Search', 'us-dod-east', False),
    ('Cognitive Search', 'usgov-arizona', True),
    ('Cognitive Search', 'usgov-texas', False),
    ('Cognitive Search', 'usgov-virginia', True),

    ('Video Indexer', 'usgov-arizona', True),
    ('Video Indexer', 'usgov-texas', False)
])
def test_isProductAvailableInRegion(dataj, prod, region, expected_result):
    assert dataj.isProductAvailableInRegion(prod, region) == expected_result

@pytest.mark.parametrize("product, cloud", [
    ('Windows Virtual Desktop', 'azure-government'),
    #    ('Anomoly Detector', 'usgov-arizona'),
    #    ('Anomoly Detector', 'usgov-virginia'),
    #    ('Microsoft Genomics', False),
])
def test_isProductInPreview(dataj, product, cloud):
    assert len(dataj.getProductPreviewRegions(product, cloud)) > 0

@pytest.mark.parametrize("product, expected_result", [
    ('Windows Virtual Desktop', 'usgov-non-regional'),
    #    ('Anomoly Detector', 'usgov-arizona'),
    #    ('Anomoly Detector', 'usgov-virginia'),
    #    ('Microsoft Genomics', False),
])
def test_isProductInPreviewInRegion(dataj, product, expected_result):
    assert expected_result in dataj.getProductPreviewRegions(product)
    #assert True
    # previewList = availList.isProductInPreview(product)

    # if expected_result != False:
    #     assert expected_result in previewList.keys()
    # else :
    #     assert previewList == False
