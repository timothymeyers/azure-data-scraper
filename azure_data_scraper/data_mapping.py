

def clean_product_name(name, prod_type = ""):

    name = name.strip().replace(u'\u2013', u'-')

    # Ugh - special Data Box Capability edge case
    if name == "Data Box" and prod_type.__contains__('capability'):
        return name

    if (name in service_map):
        return service_map[name]
    elif (name in capability_map):
        return capability_map[name]
    
    return name

# Brute Force data mapping

service_map = {
    'Azure App Configuration': 'App Configuration',
    'Backup': 'Azure Backup',
    'Azure Cloud Shell': 'Cloud Shell',
    'Azure Data Factory': 'Data Factory',
    'Azure Bot Service': 'Azure Bot Services',
    'Redis Cache': 'Azure Cache for Redis',
    'Azure Cost Management': 'Azure Cost Management and Billing',
    'Azure DevOps (formerly VSTS)': 'Azure DevOps',
    'ExpressRoute': 'Azure ExpressRoute',
    'Functions': 'Azure Functions',
    'IoT Central': 'Azure IoT Central',
    'IoT Hub': 'Azure IoT Hub',
    'Logic Apps': 'Azure Logic Apps',
    'Azure Machine Learning Services': 'Azure Machine Learning',
    'Azure RedHat OpenShift': 'Azure Red Hat OpenShift',
    'SQL Database': 'Azure SQL Database',
    'Stream Analytics': 'Azure Stream Analytics',
    'Time Series Insights': 'Azure Time Series Insights',
    'Azure Intune': 'Intune',
    'Azure Machine Learning studio': 'Machine Learning Studio',
    'Load Balancing':'Load Balancer',
    'Virtual Machines (incl. Reserved Instances)': 'Virtual Machines',
    'Azure DB for MySQL': 'Azure Database for MySQL',
    'Azure DB for PostgreSQL': 'Azure Database for PostgreSQL',
    'Azure DB for MariaDB': 'Azure Database for MariaDB',
    'Azure Event Grid': 'Event Grid',
    'Machine Learning Services': 'Azure Machine Learning',
    'Data Box': 'Azure Data Box',
}

capability_map = {
    'Azure Archive Storage': 'Archive Storage',
    'Azure Stack Edge (Data Box Edge)': 'Data Box Gateway',
    'Azure Arc enabled Servers': 'Azure Arc enabled servers',
    'Cognitive Services Personalizer': 'Personalizer',
    'Cognitive Services: Computer Vision': 'Computer Vision',
    'Cognitive Services: Content Moderator': 'Content Moderator',
    'Cognitive Services: Custom Vision': 'Custom Vision',
    'Cognitive Services: Face': 'Face',
    'Cognitive Services: Form Recognizer': 'Form Recognizer',
    'Cognitive Services: Language Understanding': 'Language Understanding',
    'Cognitive Services: QnA Maker': 'QnA Maker',
    'Cognitive Services: Speech Services': 'Speech Services',
    'Cognitive Services: Text Analytics': 'Text Analytics',
    'Cognitive Services: Translator Text': 'Translator',
    'Cognitive Services: Translator': 'Translator',
    'Cognitive Services: Video Indexer': 'Video Indexer',
    'Microsoft Health Bot': 'Health Bot',
    'Network Watcher Traffic Analytics': 'Traffic Analytics',
    'Network Watcher(Traffic Analytics)': 'Traffic Analytics',
    'Storage: Disks (incl. Managed Disks)': 'Azure Disk Storage',
    'Web Application Firewall)': 'Web Application Firewall',
    'Web Apps (App Service)': 'Web Apps'
}

service_list = [
    'API Management',
    'App Configuration',
    'App Service',
    'App Service (Linux)',
    'Application Gateway',
    'Automation',
    'Azure Active Directory',
    'Azure Active Directory Domain Services',
    'Azure Advanced Threat Protection',
    'Azure Advisor',
    'Azure Analysis Services',
    'Azure API for FHIR',
    'Azure Arc',
    'Azure Automanage',
    'Azure Backup',
    'Azure Bastion',
    'Azure Blockchain Service',
    'Azure Blockchain Tokens',
    'Azure Blueprints',
    'Azure Bot Services',
    'Azure Cache for Redis',
    'Azure Cognitive Search',
    'Azure Cognitive Services',
    'Azure Communication Services',
    'Azure Container Service',
    'Azure Cosmos DB',
    'Azure Cost Management and Billing',
    'Azure Data Explorer',
    'Azure Data Share',
    'Azure Database for MariaDB',
    'Azure Database for MySQL',
    'Azure Database for PostgreSQL',
    'Azure Database Migration Service',
    'Azure Databricks',
    'Azure DDoS Protection',
    'Azure Dedicated HSM',
    'Azure Defender',
    'Azure Defender for IoT',
    'Azure DevOps',
    'Azure DevTest Labs',
    'Azure Digital Twins',
    'Azure DNS',
    'Azure ExpressRoute',
    'Azure Firewall',
    'Azure Firewall Manager',
    'Azure for Education',
    'Azure Front Door',
    'Azure Functions',
    'Azure HPC Cache',
    'Azure Information Protection',
    'Azure Internet Analyzer',
    'Azure IoT Central',
    'Azure IoT Hub',
    'Azure IoT Security',
    'Azure Kubernetes Service (AKS)',
    'Azure Lab Services',
    'Azure Lighthouse',
    'Azure Logic Apps',
    'Azure Machine Learning',
    'Azure Managed Applications',
    'Azure Managed Instance for Apache Cassandra',
    'Azure Maps',
    'Azure Marketplace Portal',
    'Azure Migrate',
    'Azure Monitor',
    'Azure NetApp Files',
    'Azure Open Datasets',
    'Azure Policy',
    'Azure Private Link',
    'Azure Public IP',
    'Azure Purview',
    'Azure Red Hat OpenShift',
    'Azure Resource Graph',
    'Azure Resource Manager',
    'Azure Resource Mover',
    'Azure RTOS',
    'Azure Security Center',
    'Azure Sentinel',
    'Azure Service Health',
    'Azure SignalR Service',
    'Azure Site Recovery',
    'Azure Sphere',
    'Azure Spring Cloud',
    'Azure SQL',
    'Azure SQL Database',
    'Azure Stack Hub',
    'Azure Stream Analytics',
    'Azure Synapse Analytics',
    'Azure Time Series Insights',
    'Azure VMware Solution',
    'Azure VMware Solution by CloudSimple',
    'Batch',
    'Cloud Services',
    'Cloud Shell',
    'Container Instances',
    'Container Registry',
    'Content Delivery Network',
    'Customer Engagement Fabric',
    'Customer Lockbox',
    'Azure Data Box',
    'Data Catalog',
    'Data Factory',
    'Data Lake Analytics',
    'Dynamics 365',
    'Event Grid',
    'Event Hubs',
    'GitHub AE',
    'HDInsight',
    'Import / Export',
    'Intune',
    'Key Vault',
    'Load Balancer',
    'Machine Learning Studio',
    'Media Services',
    'Microsoft Azure Attestation',
    'Microsoft Azure Peering Service',
    'Microsoft Azure portal',
    'Microsoft Cloud App Security',
    'Microsoft Defender for Endpoint',
    'Microsoft Genomics',
    'Microsoft Graph',
    'Microsoft Graph Data Connect',
    'Microsoft Managed Desktop',
    'Microsoft PowerApps',
    'Microsoft Stream',
    'Microsoft Threat Experts',
    'Multi-Factor Authentication',
    'Network Watcher',
    'Notification Hubs',
    'Power Automate',
    'Power BI',
    'Power BI Embedded',
    'Power Platform',
    'Power Virtual Agents',
    'Project Bonsai',
    'Azure Remote Rendering',
    'Scheduler',
    'Security Center',
    'Service Bus',
    'Service Fabric',
    'Spatial Anchors',
    'Object Anchors',
    'SQL Server Stretch Database',
    'Storage Accounts',
    'StorSimple',
    'Traffic Manager',
    'Virtual Machine Scale Sets',
    'Virtual Machines',
    'Virtual Network',
    'Virtual WAN',
    'Visual Studio App Center',
    'Visual Studio Codespaces',
    'VPN Gateway',
    'Windows 10 IoT Core Services',
    'Windows Virtual Desktop'
]

capability_list = [
    'AI Builder',
    'Application Change Analysis',
    'Azure Active Directory (Free and Basic)',
    'Azure Active Directory (Premium P1 + P2)',
    'Azure Active Directory B2C',
    'Azure Active Directory Provisioning Service',
    'Azure Arc enabled servers',
    'Azure Arc enabled Kubernetes',
    'Azure Arc enabled data services',
    'Archive Storage',
    'Data Box',
    'Azure Data Lake Storage',
    'Azure Data Lake Storage Gen1',
    'Azure File Sync',
    'Azure Service Manager (RDFE)',
    'Data Box Gateway',
    'Cognitive Search',
    'Personalizer',
    'Computer Vision',
    'Content Moderator',
    'Custom Vision',
    'Face',
    'Form Recognizer',
    'Language Understanding',
    'QnA Maker',
    'Speech Services',
    'Text Analytics',
    'Translator',
    'Video Indexer',
    'D365 Integrator App',
    'Dynamics 365 Commerce',
    'Dynamics 365 Customer Engagement (Common Data Service)',
    'Dynamics 365 Customer Insights',
    'Dynamics 365 Customer Service',
    'Dynamics 365 Field Service',
    'Dynamics 365 Finance',
    'Dynamics 365 Forms Pro',
    'Dynamics 365 Guides',
    'Dynamics 365 Project Service Automation',
    'Dynamics 365 Sales',
    'Dynamics 365 Service Omni-Channel Engagement Hub',
    'Dynamics 365 Supply Chain',
    'Export to Data Lake service',
    'Flow',
    'Guest Configuration',
    'Log Analytics',
    'Health Bot',
    'Traffic Analytics',
    'Traffic Analytics',
    'Storage: Blobs (Incl. Azure Data Lake Storage Gen2',
    'Azure Disk Storage',
    'Storage: Files',
    'Storage: Queues',
    'Storage: Tables',
    'Virtual Network NAT',
    'Web Application Firewall',
    'Web Apps',
    'A0 - A7',
    'A8 - A11 (Compute Intensive)',
    'Action Groups',
    'Activity Log',
    'Alerts',
    'Alerts (Classic)',
    'Anomaly Detector',
    'Application Insights',
    'AutoScale',
    'Av2',
    'Azure Active Directory External Identities',
    'Azure Dedicated Host',
    'Azure Dev Spaces',
    'Azure SQL Managed Instance',
    'Bing Speech',
    'Bs-series',
    'Consumption plan',
    'Consumption plan Linux',
    'Dasv4-series',
    'Data Box Disk',
    'Data Box Heavy',
    'Data Factory V1',
    'Dav4-series',
    'DCsv2-series',
    'Ddsv4-series',
    'Ddv4-series',
    'Diagnostic Logs',
    'D-series',
    'DS-series',
    'DSv2-series',
    'DSv3-series',
    'Dsv4-series',
    'Dv2-series',
    'Dv3-series',
    'Dv4-series',
    'Easv4-series',
    'Eav4-series',
    'Edsv4-series',
    'Enterprise State Roaming',
    'ESv3-series',
    'Esv4-series',
    'Ev3-series',
    'Ev4-series',
    'ExpressRoute Circuits',
    'ExpressRoute Gateways',
    'F-series',
    'Fs-series',
    'Fsv2-series',
    'G-series',
    'GS-series',
    'Hb-series',
    'HBv2-series',
    'HBv3-series',
    'Hc-series',
    'Hot/Cool Blob Storage Tiers',
    'H-series',
    'Immersive Reader',
    'Import/Export',
    'Instance Level IPs',
    'IoT Hub Device Provisioning Service',
    'Device Update for IoT Hub',
    'Live Video Analytics',
    'Ls-series',
    'Lsv2-series',
    'Managed Disks',
    'Metrics',
    'Metrics Advisor',
    'M-series',
    'Mv2-series',
    'NCasT4v3-series',
    'NC-series',
    'NCsv2-series',
    'NCsv3-series',
    'NDs-series',
    'NDv2-series',
    'NV-series',
    'NVv3-series',
    'NVv4-series',
    'Premium Blob Storage',
    'Premium Files Storage',
    'Premium plan',
    'Premium plan Linux',
    'Premium Tier for Azure Data Lake Storage',
    'Reserved IP',
    'SAP HANA on Azure Large Instances',
    'Snapshot Execution',
    'Speaker Recognition',
    'SQL Data Sync',
    'Static Web Apps',
    'Synapse workspace',
    'Ultra Disk Storage',
    'Web App for Containers',
    'Web Apps Linux',
    'Cognitive Services Containers',
    'Translator'
]

capability_service_map = {
    'Azure File Sync': 'Storage Accounts',
    'Azure Service Manager (RDFE)': 'Cloud Services',
    'Data Box Gateway': 'Azure Data Box',
    'Cognitive Search': 'Azure Cognitive Search',
    'Personalizer': 'Azure Cognitive Services',
    'Computer Vision': 'Azure Cognitive Services',
    'Content Moderator': 'Azure Cognitive Services',
    'Custom Vision': 'Azure Cognitive Services',
    'Face': 'Azure Cognitive Services',
    'Form Recognizer': 'Azure Cognitive Services',
    'Language Understanding': 'Azure Cognitive Services',
    'QnA Maker': 'Azure Cognitive Services',
    'Speech Services': 'Azure Cognitive Services',
    'Text Analytics': 'Azure Cognitive Services',
    'Translator': 'Azure Cognitive Services',
    'Video Indexer': 'Azure Cognitive Services',
    'D365 Integrator App': 'Dynamics 365',
    'Azure Data Lake Storage Gen1': 'Storage Accounts',
    'Azure Data Lake Storage': 'Storage Accounts',
    'Dynamics 365 Commerce': 'Dynamics 365',
    'Dynamics 365 Customer Engagement (Common Data Service)': 'Dynamics 365',
    'Dynamics 365 Customer Insights': 'Dynamics 365',
    'Dynamics 365 Customer Service': 'Dynamics 365',
    'Dynamics 365 Field Service': 'Dynamics 365',
    'Dynamics 365 Finance': 'Dynamics 365',
    'Dynamics 365 Forms Pro': 'Dynamics 365',
    'Dynamics 365 Guides': 'Dynamics 365',
    'Dynamics 365 Project Service Automation': 'Dynamics 365',
    'Dynamics 365 Sales': 'Dynamics 365',
    'Dynamics 365 Service Omni-Channel Engagement Hub': 'Dynamics 365',
    'Dynamics 365 Supply Chain': 'Dynamics 365',
    'Export to Data Lake service': 'Microsoft PowerApps',
    'Archive Storage':	'Storage Accounts',
    'AI Builder':	'Power Platform',
    'Flow': 'Power Automate',
    'Guest Configuration': 'Azure Policy',
    'Log Analytics': 'Azure Monitor',
    'Health Bot': 'Azure Bot Services',
    'Traffic Analytics': 'Network Watcher',
    'Traffic Analytics': 'Network Watcher',
    'Storage: Blobs (Incl. Azure Data Lake Storage Gen2': 'Storage Accounts',
    'Azure Disk Storage': 'Storage Accounts',
    'Storage: Files': 'Storage Accounts',
    'Storage: Queues': 'Storage Accounts',
    'Storage: Tables': 'Storage Accounts',
    'Virtual Network NAT': 'Virtual Network',
    'Web Application Firewall': 'Application Gateway',
    'Web Apps': 'App Service',
    'A0 - A7': 'Cloud Services',
    'A8 - A11 (Compute Intensive)': 'Cloud Services',
    'Action Groups': 'Azure Monitor',
    'Activity Log': 'Azure Monitor',
    'Alerts': 'Azure Monitor',
    'Alerts (Classic)': 'Azure Monitor',
    'Anomaly Detector': 'Azure Cognitive Services',
    'Application Insights': 'Azure Monitor',
    'Application Change Analysis':	'Azure Monitor',
    'AutoScale': 'Azure Monitor',
    'Av2': 'Cloud Services',
    'Azure Active Directory External Identities': 'Azure Active Directory',
    'Azure Dedicated Host': 'Virtual Machines',
    'Azure Dev Spaces': 'Azure Kubernetes Service (AKS)',
    'Azure SQL Managed Instance': 'Azure SQL',
    'Bing Speech': 'Azure Cognitive Services',
    'Bs-series': 'Virtual Machines',
    'Consumption plan': 'Azure Functions',
    'Consumption plan Linux': 'Azure Functions',
    'Dasv4-series': 'Virtual Machines',
    'Data Box Disk': 'Azure Data Box',
    'Data Box Heavy': 'Azure Data Box',
    'Data Factory V1': 'Data Factory',
    'Dav4-series': 'Virtual Machines',
    'DCsv2-series': 'Virtual Machines',
    'Ddsv4-series': 'Virtual Machines',
    'Ddv4-series': 'Virtual Machines',
    'Diagnostic Logs': 'Azure Monitor',
    'D-series': 'Cloud Services',
    'DS-series': 'Virtual Machines',
    'DSv2-series': 'Virtual Machines',
    'DSv3-series': 'Virtual Machines',
    'Dsv4-series': 'Virtual Machines',
    'Dv2-series': 'Cloud Services',
    'Dv3-series': 'Cloud Services',
    'Dv4-series': 'Virtual Machines',
    'Easv4-series': 'Virtual Machines',
    'Eav4-series': 'Virtual Machines',
    'Edsv4-series': 'Virtual Machines',
    'Enterprise State Roaming': 'Azure Active Directory',
    'ESv3-series': 'Virtual Machines',
    'Esv4-series': 'Virtual Machines',
    'Ev3-series': 'Cloud Services',
    'Ev4-series': 'Virtual Machines',
    'ExpressRoute Circuits': 'Azure ExpressRoute',
    'ExpressRoute Gateways': 'Azure ExpressRoute',
    'F-series': 'Virtual Machines',
    'Fs-series': 'Virtual Machines',
    'Fsv2-series': 'Virtual Machines',
    'G-series': 'Cloud Services',
    'GS-series': 'Virtual Machines',
    'Hb-series': 'Virtual Machines',
    'HBv2-series': 'Virtual Machines',
    'HBv3-series': 'Virtual Machines',
    'Hc-series': 'Virtual Machines',
    'Hot/Cool Blob Storage Tiers': 'Storage Accounts',
    'H-series': 'Cloud Services',
    'Immersive Reader': 'Azure Cognitive Services',
    'Import/Export': 'Storage Accounts',
    'Instance Level IPs': 'Cloud Services',
    'IoT Hub Device Provisioning Service': 'Azure IoT Hub',
    'Device Update for IoT Hub':'Azure IoT Hub',
    'Live Video Analytics': 'Media Services',
    'Ls-series': 'Virtual Machines',
    'Lsv2-series': 'Cloud Services',
    'Managed Disks': 'Storage Accounts',
    'Metrics': 'Azure Monitor',
    'Metrics Advisor': 'Azure Cognitive Services',
    'M-series': 'Cloud Services',
    'Mv2-series': 'Virtual Machines',
    'NCasT4v3-series': 'Virtual Machines',
    'NC-series': 'Virtual Machines',
    'NCsv2-series': 'Virtual Machines',
    'NCsv3-series': 'Virtual Machines',
    'NDs-series': 'Virtual Machines',
    'NDv2-series': 'Virtual Machines',
    'NV-series': 'Virtual Machines',
    'NVv3-series': 'Virtual Machines',
    'NVv4-series': 'Virtual Machines',
    'Premium Blob Storage': 'Storage Accounts',
    'Premium Files Storage': 'Storage Accounts',
    'Premium plan': 'Azure Functions',
    'Premium plan Linux': 'Azure Functions',
    'Premium Tier for Azure Data Lake Storage': 'Storage Accounts',
    'Reserved IP': 'Cloud Services',
    'SAP HANA on Azure Large Instances': 'Virtual Machines',
    'Snapshot Execution': 'Azure Data Share',
    'Speaker Recognition': 'Azure Cognitive Services',
    'SQL Data Sync': 'Azure SQL Database',
    'Static Web Apps': 'App Service',
    'Synapse workspace': 'Azure Synapse Analytics',
    'Ultra Disk Storage': 'Storage Accounts',
    'Web App for Containers': 'App Service (Linux)',
    'Web Apps Linux': 'App Service (Linux)',
    'Cognitive Services Containers': 'Azure Cognitive Services',
    'Translator': 'Azure Cognitive Services',
    'AI Builder': 'Power Platform',
    'Application Change Analysis': 'Azure Monitor',
    'Azure Active Directory (Free and Basic)': 'Azure Active Directory',
    'Azure Active Directory (Premium P1 + P2)': 'Azure Active Directory',
    'Azure Active Directory B2C': 'Azure Active Directory',
    'Azure Active Directory Provisioning Service': 'Azure Active Directory',
    'Azure Arc enabled servers': 'Azure Arc',
    'Azure Arc enabled Kubernetes': 'Azure Arc',
    'Azure Arc enabled data services': 'Azure Arc',
    'Archive Storage': 'Storage Accounts',
    'Data Box': 'Azure Data Box',
    'Azure Data Lake Storage': 'Storage Accounts',
    'Azure File Sync': 'Storage Accounts',
    'Azure Service Manager (RDFE)': 'Cloud Services',
    'Data Box Gateway': 'Azure Data Box',
    'D365 Integrator App': 'Dynamics 365',
    'Dynamics 365 Commerce': 'Dynamics 365',
    'Dynamics 365 Customer Engagement (Common Data Service)': 'Dynamics 365',
    'Dynamics 365 Customer Insights': 'Dynamics 365',
    'Dynamics 365 Customer Service': 'Dynamics 365',
    'Dynamics 365 Field Service': 'Dynamics 365',
    'Dynamics 365 Finance': 'Dynamics 365',
    'Dynamics 365 Forms Pro': 'Dynamics 365',
    'Dynamics 365 Guides': 'Dynamics 365',
    'Dynamics 365 Project Service Automation': 'Dynamics 365',
    'Dynamics 365 Sales': 'Dynamics 365',
    'Dynamics 365 Service Omni-Channel Engagement Hub': 'Dynamics 365',
    'Dynamics 365 Supply Chain': 'Dynamics 365',
    'Export to Data Lake service': 'Microsoft PowerApps',
    'Flow': 'Power Automate',
    'Guest Configuration': 'Azure Policy',
    'Log Analytics': 'Azure Monitor',
    'Health Bot': 'Azure Bot Services',
    'Traffic Analytics': 'Network Watcher',
    'Traffic Analytics': 'Network Watcher',
    'Storage: Blobs (Incl. Azure Data Lake Storage Gen2': 'Storage Accounts',
    'Azure Disk Storage': 'Storage Accounts',
    'Storage: Files': 'Storage Accounts',
    'Storage: Queues': 'Storage Accounts',
    'Storage: Tables': 'Storage Accounts',
    'Virtual Network NAT': 'Virtual Network',
    'Web Application Firewall': 'Application Gateway',
    'Web Apps': 'App Service'

}

us_regions = [
    "us-central",
    "us-east",
    "us-east-2",
    "us-north-central",
    "us-south-central",
    "us-west-central",
    "us-west",
    "us-west-2",
    "non-regional"
]

usgov_regions = [
    "us-dod-central",
    "us-dod-east",
    "usgov-arizona",
    "usgov-texas",
    "usgov-virginia",
    "usgov-non-regional"
]

usdod_regions = [
    "us-dod-central",
    "us-dod-east",
    "usgov-non-regional"
]

us_scopes = [
    "dodCcSrgIl2",
    "fedrampModerate",
    "fedrampHigh",
    "planned2021"
]

usgov_scopes = [
    "dodCcSrgIl2",
    "dodCcSrgIl4",
    "dodCcSrgIl5AzureGov",
    "dodCcSrgIl5AzureDod",
    "fedrampHigh",
    "dodCcSrgIl6"
]

scope_map = {
    'dodCcSrgIl2': 'IL2',
    'fedrampModerate': 'Fedramp Moderate',
    'fedrampHigh': 'Fedramp High',
    'planned2021': 'Planned for 2021',
    'dodCcSrgIl4': 'IL4',
    'dodCcSrgIl5AzureGov': 'IL5 in Gov Regions',
    'dodCcSrgIl5AzureDod': 'IL5 in DoD Regions',
    'dodCcSrgIl6': 'IL6'

}
