import pytest
from azure_data_scraper.product_by_region_scraper import ProductsByRegion

# "Constaints"

# "Fixtures"


@pytest.fixture(scope="session")
def al ():
    return ProductsByRegion('web').products()

# Tests


def test_isInitialized(al):
    assert len(al.keys()) > 0


@pytest.mark.parametrize("service, cloud, expected_result", [
    ("Azure Databricks", "azure-government", True),
    ("Microsoft Genomics", "azure-government", False),
    ('Azure Blueprints', "azure-government", False),
    ('Windows Virtual Desktop', "azure-government", False)
])
def test_isServiceAvailable(al, service, cloud, expected_result):
    assert True


@pytest.mark.parametrize("capability, cloud, expected_result", [
    ("H-series", "azure-government", True),
    ("Hb-series", "azure-government", False),
    ("Hc-series", "azure-government", True),
    ("Azure Arc enabled servers","azure-government", True),
])
def test_isCapabilityAvailable(al, capability, cloud, expected_result):
    assert capability in al
    cap = al[capability][cloud]
    assert cap["available"] == expected_result


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
def test_isProductAvailableAzureGovernment(al, product, expected_result):
    assert True


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
def test_isProductAvailableInRegion(al, prod, region, expected_result):
    assert True

@pytest.mark.parametrize("product, cloud", [
    ('Windows Virtual Desktop', 'azure-government'),
    #    ('Anomoly Detector', 'usgov-arizona'),
    #    ('Anomoly Detector', 'usgov-virginia'),
    #    ('Microsoft Genomics', False),
])
def test_isProductInPreview(al, product, cloud):
    assert True


@pytest.mark.parametrize("product, expected_result", [
    ('Windows Virtual Desktop', 'usgov-non-regional'),
    #    ('Anomoly Detector', 'usgov-arizona'),
    #    ('Anomoly Detector', 'usgov-virginia'),
    #    ('Microsoft Genomics', False),
])
def test_isProductInPreviewInRegion(al, product, expected_result):
    assert True
  
