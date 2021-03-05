from azure_data_scraper.audit_scope_scraper import AuditScopes
from azure_data_scraper.product_by_region_scraper import ProductsByRegion
from azure_data_scraper import data_mapping as maps

import json
import logging


class DataJoiner:
    def __init__(self, audit_scopes=AuditScopes(), products_by_region=ProductsByRegion()):
        self.__audit_scopes = audit_scopes
        self.__products_by_region = products_by_region

        self.__product_dict = self.__hydrate_product_dict(audit_scopes.getAuditScopeDictionary(
        ), products_by_region.getProductsAvailabilityDictionary())
        self.__category_dict = self.__hydrate_category_dict()

    def __hydrate_product_dict(self, audit_scopes, products_by_region) -> dict:

        product_dict = products_by_region.copy()

        for i, prod in product_dict.items():

            if i in audit_scopes:
                prod['azure-public']['scopes'] = audit_scopes[i]['azure-public']['scopes'].copy()
                prod['azure-government']['scopes'] = audit_scopes[i]['azure-government']['scopes'].copy()

            prod.pop('doc-type')

        return product_dict

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
        return self.__product_dict

    def product_list(self) -> list:
        return self.products().keys()

    def audit_scopes(self) -> AuditScopes:
        return self.__audit_scopes

    def product_availability(self) -> ProductsByRegion:
        return self.__products_by_region

    def categories(self) -> dict:
        return self.__category_dict

    def category_list(self) -> list:
        return self.categories().keys()

    def getCategoryDictionary(self) -> dict:
        return self.__category_dict

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
        if prod_id in self.__product_dict and self.__product_dict[prod_id]['type'] == "service":
            return_prod = self.__product_dict[prod_id].copy()
            new_cap_dict = {cap: self.getProductDetails(
                cap) for cap in return_prod['capabilities']}
            return_prod['capabilities'] = new_cap_dict
            return return_prod
        return {}

    def getCategoryServiceList(self, cat_id) -> list:
        if cat_id in self.__category_dict:
            return self.__category_dict[cat_id]
        return []

    def getCategoryServices(self, cat_id) -> dict:
        if cat_id in self.__category_dict:
            return {svc: self.getProductDetails(svc) for svc in self.__category_dict[cat_id]}
        return {}

    def getCategoryServicesDeep(self, cat_id) -> dict:
        if cat_id in self.__category_dict:
            return {svc: self.getServiceDetailsDeep(svc) for svc in self.__category_dict[cat_id]}
        return {}
