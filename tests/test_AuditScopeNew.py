import pytest
from azure_data_scraper.audit_scope_scraper import AuditScopes, camelize

# "Constaints"

# "Fixtures"
@pytest.fixture(scope="session")
def asl():
    return AuditScopes()

#Tests

def test_isInitialized(asl):   
    assert (len(asl.getAuditScopeDictionary().keys())>0)
    assert camelize('Hello Super 1 Man (World') == 'helloSuper1ManWorld'

def test_isAtAuditScopeForCloud_noCloud(asl):
    assert asl.isAtAuditScopeInCloud('','','') == False

@pytest.mark.parametrize("service, scope, expected_result", [
    ('', 'DoD CC SRG IL 2', False),
    ('', 'FedRAMP Moderate', False),
    ('', 'FedRAMP High', False),
    ('', 'Planned 2021', False),

    ('API Management', 'DoD CC SRG IL 2', True),
    ('API Management', 'FedRAMP Moderate', True),
    ('API Management', 'FedRAMP High', True),
    ('API Management', 'Planned 2021', False),

    ('Azure Data Lake Storage', 'Planned 2021', True),

    ('Azure Data Box', 'FedRAMP High', True),
    
])
def test_checkAzurePublic(asl, service, scope, expected_result):
    asl.isAtAuditScope(service, scope) == expected_result

@pytest.mark.parametrize("service, scope, expected_result", [
    ('', 'DoD CC SRG IL 2', False),
    ('', 'DoD CC SRG IL 4', False),
    ('', 'DoD CC SRG IL 5', False),
    ('', 'FedRAMP High', False),      
    ('', 'DoD CC SRG IL 6', False),

    ('Application Gateway', 'DoD CC SRG IL 2', True),
    ('Application Gateway', 'DoD CC SRG IL 4', True),
    ('Application Gateway', 'DoD CC SRG IL 5 (Azure Gov)', True),
    ('Application Gateway', 'DoD CC SRG IL 5 (Azure DoD)', True),
    ('Application Gateway', 'FedRAMP High', True),    
    ('Application Gateway', 'DoD CC SRG IL 6', True),

    ('Azure Stream Analytics', 'DoD CC SRG IL 2', True),
    ('Azure Stream Analytics', 'DoD CC SRG IL 4', True),
    ('Azure Stream Analytics', 'DoD CC SRG IL 5 **', False),
    ('Azure Stream Analytics', 'FedRAMP High', True),    
    ('Azure Stream Analytics', 'DoD CC SRG IL 6', False),
])

def test_checkAzureGovernment(asl, service, scope, expected_result):
    assert asl.isAtAuditScope(service, scope) == expected_result