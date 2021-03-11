from azure_data_scraper.audit_scope_scraper import AuditScopes
from azure_data_scraper.product_by_region_scraper import ProductsByRegion
from azure_data_scraper import data_mapping as maps

import json
import logging


class AzProductInfo:
    def __init__(self, audit_scopes=AuditScopes(), products_by_region=ProductsByRegion(), src="web"):
        #self.__audit_scopes = audit_scopes
        #self.__products_by_region = products_by_region

        if src == "web":
            self.__product_dict = self.__hydrate_product_dict(audit_scopes.getAuditScopeDictionary(), products_by_region.getProductsAvailabilityDictionary())
        else:
            self.__product_dict = self.__hydrate_product_dict_from_file(src)
        self.__category_dict = self.__hydrate_category_dict()

    def __hydrate_product_dict(self, audit_scopes, products_by_region) -> dict:

        product_dict = products_by_region.copy()

        for i, prod in product_dict.items():

            if i in audit_scopes:
                prod['azure-public']['scopes'] = audit_scopes[i]['azure-public']['scopes'].copy()
                prod['azure-government']['scopes'] = audit_scopes[i]['azure-government']['scopes'].copy()

            if 'doc-type' in prod: prod.pop('doc-type')

        return product_dict

    def __hydrate_product_dict_from_file(self, src) -> dict:
        with open(src) as f:
            return json.load(f)

    def __hydrate_category_dict(self):
        cat_set = set()

        for prod in self.__product_dict.values():
            for cat in prod['categories']:
                cat_set.add(cat)

        #print ("cat_set", cat_set)

        categories = {cat: [] for cat in cat_set}

        for id, prod in self.__product_dict.items():
            {categories[cat].append(
                id) for cat in prod['categories'] if prod['type'] == "service"}

        #print ("categories", categories)

        return categories

    def getJoinedData(self) -> dict:
        return self.products()

    def getProductDictionary(self) -> dict:
        return self.products()

    def products(self) -> dict:
        return self.__product_dict.copy()


#    def audit_scopes(self) -> AuditScopes:
#        return self.__audit_scopes

#    def product_availability(self) -> ProductsByRegion:
#        return self.__products_by_region

    def categories(self) -> dict:
        return self.__category_dict.copy()


    def getCategoryDictionary(self) -> dict:
        return self.__category_dict.copy()

    def getProductDetails(self, prod_id) -> dict:
        if prod_id in self.__product_dict:
            return self.__product_dict[prod_id].copy()
        return {}

    def getServiceDetails(self, prod_id) -> dict:
        if prod_id in self.__product_dict and self.__product_dict[prod_id]['type'] == "service":
            return self.getProductDetails(prod_id)
        return {}

    def getCapabilityDetails(self, prod_id) -> dict:
        if prod_id in self.__product_dict and self.__product_dict[prod_id]['type'] == "capability":
            return self.getProductDetails(prod_id)
        return {}

    def getServiceDetailsDeep(self, prod_id) -> dict:        
        svc = self.getServiceDetails(prod_id)
        if 'capabilities' in svc:           
            new_cap_dict = {cap: self.getProductDetails(cap) for cap in svc['capabilities']}
            svc['capabilities'] = new_cap_dict
        return svc

        """
        if prod_id in self.__product_dict and self.__product_dict[prod_id]['type'] == "service":
            return_prod = self.__product_dict[prod_id].copy()
            new_cap_dict = {cap: self.getProductDetails(
                cap) for cap in return_prod['capabilities']}
            return_prod['capabilities'] = new_cap_dict
            return return_prod
        return {}
        """

    def getCategoryServiceList(self, cat_id) -> list:
        if cat_id in self.__category_dict:
            return self.__category_dict[cat_id]
        return []

    def getCategoryServices(self, cat_id) -> dict:
        if cat_id in self.__category_dict:
            return {svc: self.getServiceDetails(svc) for svc in self.__category_dict[cat_id]}
        return {}

    def getCategoryServicesDeep(self, cat_id) -> dict:
        if cat_id in self.__category_dict:
            return {svc: self.getServiceDetailsDeep(svc) for svc in self.__category_dict[cat_id]}
        return {}

    #### Get Summary Data

    def categories_list(self) -> list:
        return self.categories().keys()

    def products_list(self) -> list:
        return self.products().keys()

    def services_list(self) -> list:
        return [id for id, prod in self.__product_dict.items() if prod['type'] == 'service']

    def capabilities_list(self) -> list:
        return [id for id, prod in self.__product_dict.items() if prod['type'] == 'capability']


    #### Question and Answer
    def isProductAvailable(self, prod, cloud="") -> bool:

        if prod in self.__product_dict:
            az_pub = self.__product_dict[prod]['azure-public']['available']
            az_gov = self.__product_dict[prod]['azure-government']['available']
        
            if (cloud == 'azure-public'): return az_pub
            if (cloud == 'azure-government'): return az_gov

            return (az_pub or az_gov)

        return False

    def isProductAvailableInRegion(self, prod, region) -> bool:
        az_pub = region in self.getProductAvailableRegions(prod,'azure-public')
        az_gov = region in self.getProductAvailableRegions(prod,'azure-government')

        return (az_pub or az_gov)

    def isAtAuditScope(self,prod, scope, cloud="") -> bool:
        az_pub = scope in self.getProductScopes(prod,'azure-public')
        az_gov = scope in self.getProductScopes(prod,'azure-government')

        if (cloud == 'azure-public'): return az_pub
        if (cloud == 'azure-government'): return az_gov

        return (az_pub or az_gov)

    def isServiceAvailable(self, svc, cloud="") -> bool:
        return self.isProductAvailable(svc,cloud)

    def isServiceAvailableInRegion(self, svc, region) -> bool:
        return self.isProductAvailableInRegion(svc,region)

    def isCapabilityAvailable(self, cap, cloud="") -> bool:
        return self.isProductAvailable(cap,cloud)
    
    def isCapabilityAvailableInRegion(self, cap, region) -> bool:
        return self.isProductAvailableInRegion(cap,region)

    def getProductAvailableRegions(self, prod, cloud="") -> list:
        return self.__helper_get_product_cloud_lists(prod, cloud, 'ga')

    def getProductPreviewRegions(self, prod, cloud="") -> list:
        return self.__helper_get_product_cloud_lists(prod, cloud, 'preview')

    def getProductRegionsGATargets(self, prod, cloud="") -> list:
        return self.__helper_get_product_cloud_lists(prod, cloud, 'planned-active')

    def getProductScopes(self, prod, cloud="") -> list:
        return self.__helper_get_product_cloud_lists(prod, cloud, 'scopes')

    def __helper_get_product_cloud_lists(self, prod, cloud, which_list):

        if prod in self.__product_dict:
            az_pub_regions = self.__product_dict[prod]['azure-public'][which_list]
            az_gov_regions = self.__product_dict[prod]['azure-government'][which_list]

            if (cloud == 'azure-public'): return az_pub_regions
            if (cloud == 'azure-government'): return az_gov_regions
            return az_pub_regions + az_gov_regions

        return []
