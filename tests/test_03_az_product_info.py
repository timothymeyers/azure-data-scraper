import pytest
from azure_data_scraper.az_product_info import AzProductInfo
#from azure_data_scraper.audit_scope_scraper import AuditScopes
#from azure_data_scraper.product_by_region_scraper import ProductsByRegion

# "Constaints"

# "Fixtures"


@pytest.fixture(scope="session")
def az():
    return AzProductInfo()

# Tests


def test_localLoad():
    az = AzProductInfo(None,None,'tests/merged.json')
    assert len(az.products_list()) > 0
    assert len(az.categories_list()) > 0
    assert len(az.services_list()) > 0
    assert len(az.capabilities_list()) > 0
    assert len(az.getJoinedData().keys()) > 0
    assert len(az.getProductDictionary().keys()) > 0

    assert len(az.getCategoryDictionary().keys()) > 0


def test_isInitialized(az):
    assert len(az.products_list()) > 0
    assert len(az.categories_list()) > 0
    assert len(az.services_list()) > 0
    assert len(az.capabilities_list()) > 0
    assert len(az.getJoinedData().keys()) > 0
    assert len(az.getProductDictionary().keys()) > 0

    assert len(az.getCategoryDictionary().keys()) > 0

    #assert type(az.audit_scopes()) is AuditScopes
    #assert type(az.product_availability()) is ProductsByRegion


@pytest.mark.parametrize("service", [
    ("API Management"),
    ("Application Gateway")
])
def test_verifyJoined(az, service):
    prod = az.getProductDetails(service)

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
def test_getProductDetails(az, prod_id, expected_result):
    prod = az.getProductDetails(prod_id)
    assert type(prod) is dict
    print('keys', prod.keys())
    assert (len(prod.keys()) > 0) == expected_result


@pytest.mark.parametrize("prod_id, expected_result", [
    ('API Management', True),  # service
    ('AI Builder', False),  # capability
    ('', False),  # empty
    (None, False)  # None
])
def test_getServiceDetails(az, prod_id, expected_result):
    prod = az.getServiceDetails(prod_id)
    assert type(prod) is dict
    print('keys', prod.keys())
    assert (len(prod.keys()) > 0) == expected_result


@pytest.mark.parametrize("prod_id, expected_result", [
    ('API Management', False),  # service
    ('AI Builder', True),  # capability
    ('', False),  # empty
    (None, False)  # None
])
def test_getCapabilityDetails(az, prod_id, expected_result):
    prod = az.getCapabilityDetails(prod_id)
    assert type(prod) is dict
    print('keys', prod.keys())
    assert (len(prod.keys()) > 0) == expected_result


def test_getServiceDetailsDeep(az):
    cog = az.getServiceDetailsDeep("Azure Cognitive Services")

    assert cog['prod-id'] == "Azure Cognitive Services"
    assert type(cog['capabilities']) is dict
    assert 'Personalizer' in cog['capabilities']
    assert type(cog['capabilities']['Personalizer']) is dict


@pytest.mark.parametrize("cat_id, expected_result", [
    ('Compute', True),
    ('SUPER LASERS', False),
    #('', True),                                                     # strange azure arc case
    #(None, False)                                                   
])
def test_getCategoryServiceList(az, cat_id, expected_result):

    list = az.getCategoryServiceList(cat_id)

    assert (len(list) > 0) == expected_result


@pytest.mark.parametrize("cat_id, expected_result", [
    ('Compute', True),
    ('SUPER LASERS', False),
    #('', True),                                                     # strange azure arc case
    #(None, False)                                                   
])
def test_getCategoryServices(az, cat_id, expected_result):
    c = az.getCategoryServices(cat_id)
    assert (type(c) is dict) == True
    assert (len(c.keys()) > 0) == expected_result


# New from PbR


@pytest.mark.parametrize("service, cloud, expected_result", [
    ("Azure Databricks", "azure-government", True),
    ("Microsoft Genomics", "azure-government", False),
    ('Azure Blueprints', "azure-government", False),
    ('Windows Virtual Desktop', "azure-government", False)
])
def test_isServiceAvailable(az, service, cloud, expected_result):
    assert az.isServiceAvailable(service, cloud) == expected_result


@pytest.mark.parametrize("capability, cloud, expected_result", [
    ("H-series", "azure-government", True),
    ("Hb-series", "azure-government", False),
    ("Hc-series", "azure-government", True)
])
def test_isCapabilityAvailable(az, capability, cloud, expected_result):
    assert az.isCapabilityAvailable(
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
    ("Hc-series", True)

])
def test_isProductAvailableAzureGovernment(az, product, expected_result):
    assert az.isProductAvailable(
        product, "azure-government") == expected_result


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
def test_isProductAvailableInRegion(az, prod, region, expected_result):
    assert az.isProductAvailableInRegion(prod, region) == expected_result


@pytest.mark.parametrize("product, cloud", [
    ('Windows Virtual Desktop', 'azure-government'),
    #    ('Anomoly Detector', 'usgov-arizona'),
    #    ('Anomoly Detector', 'usgov-virginia'),
    #    ('Microsoft Genomics', False),
])
def test_isProductInPreview(az, product, cloud):
    assert len(az.getProductPreviewRegions(product, cloud)) > 0


@pytest.mark.parametrize("product, expected_result", [
    ('Windows Virtual Desktop', 'usgov-non-regional'),
    #    ('Anomoly Detector', 'usgov-arizona'),
    #    ('Anomoly Detector', 'usgov-virginia'),
    #    ('Microsoft Genomics', False),
])
def test_isProductInPreviewInRegion(az, product, expected_result):
    assert expected_result in az.getProductPreviewRegions(product)
    #assert True
    # previewList = availList.isProductInPreview(product)

    # if expected_result != False:
    #     assert expected_result in previewList.keys()
    # else :
    #     assert previewList == False


@pytest.mark.parametrize("product, scope, cloud, expected_result", [
    ('','','', False),
    ('', 'DoD CC SRG IL 2', 'azure-public', False),
    ('', 'FedRAMP Moderate', 'azure-public', False),
    ('', 'FedRAMP High', 'azure-public', False),
    ('', 'Planned 2021', 'azure-public', False),

    ('API Management', 'DoD CC SRG IL 2', '', True),
    ('API Management', 'FedRAMP Moderate', 'c', True),
    ('API Management', 'FedRAMP High', None, True),
    ('API Management', 'Planned 2021', None, False),

    ('API Management', 'DoD CC SRG IL 2', 'azure-public', True),
    ('API Management', 'FedRAMP Moderate', 'azure-public', True),
    ('API Management', 'FedRAMP High', 'azure-public', True),
    ('API Management', 'Planned 2021', 'azure-public', False),

    ('Azure Data Lake Storage', 'Planned 2021', 'azure-public',  True),

    ('Azure Data Box', 'FedRAMP High', 'azure-public', True),

    ('', 'DoD CC SRG IL 2', 'azure-government', False),
    ('', 'DoD CC SRG IL 4', 'azure-government', False),
    ('', 'DoD CC SRG IL 5', 'azure-government', False),
    ('', 'FedRAMP High', 'azure-government', False),
    ('', 'DoD CC SRG IL 6', 'azure-government', False),

    ('Application Gateway', 'DoD CC SRG IL 2', 'azure-government', True),
    ('Application Gateway', 'DoD CC SRG IL 4', 'azure-government', True),
    ('Application Gateway', 'DoD CC SRG IL 5 (Azure Gov)', 'azure-government', True),
    ('Application Gateway', 'DoD CC SRG IL 5 (Azure DoD)', 'azure-government', True),
    ('Application Gateway', 'FedRAMP High', 'azure-government', True),
    ('Application Gateway', 'DoD CC SRG IL 6', 'azure-government', True),

    ('Azure Stream Analytics', 'DoD CC SRG IL 2', 'azure-government', True),
    ('Azure Stream Analytics', 'DoD CC SRG IL 4', 'azure-government', True),
    ('Azure Stream Analytics', 'DoD CC SRG IL 5 **', 'azure-government', False),
    ('Azure Stream Analytics', 'FedRAMP High', 'azure-government', True),
    ('Azure Stream Analytics', 'DoD CC SRG IL 6', 'azure-government', False),

])
def test_isAtAuditScope(az, product, scope, cloud, expected_result):
    az.isAtAuditScope(product, scope, cloud) == expected_result
