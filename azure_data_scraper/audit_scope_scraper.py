from lxml import html
from azure_data_scraper import data_mapping as maps

import requests
# import pprint
import logging
from re import split
import json

# Constants

# AZGOV_AUDIT_SCOPE_LIST = "https://docs.microsoft.com/en-us/azure/azure-government/compliance/azure-services-in-fedramp-auditscope#azure-government-services-by-audit-scope"
AZ_AUDIT_SCOPE_URL = "https://docs.microsoft.com/en-us/azure/azure-government/compliance/azure-services-in-fedramp-auditscope"


# Helpers

# Gets text from an HTML element

def text(elt):
    return elt.text_content().replace(u'\xa0', u' ').replace('✔️', "Check")


def camelize(string):
    tmp = ''.join(a.capitalize() for a in split('([^a-zA-Z0-9])', string) if a.isalnum())
    return tmp[0].lower() + tmp[1:] 


class AuditScopes:
    def __init__(self):
        self.__audit_scope_dictionary = {}

        logging.info("AuditScopes - Starting Initialization")

        self.__init_html_tables()

        self.__init_audit_scope_dictionary()
        self.__hydrate_audit_scope_dictionary(self.__azpub_html_table, 'azure-public')
        self.__hydrate_audit_scope_dictionary(self.__azgov_html_table, 'azure-government')       

        logging.info("AuditScopes - Initialization Complete")

    def __init_html_tables(self):
        logging.debug("AuditScopes - Retrieving URL", AZ_AUDIT_SCOPE_URL)

        page = requests.get(AZ_AUDIT_SCOPE_URL)
        tree = html.fromstring(page.content)

        logging.debug("AuditScopes - Page retrieved")

        html_tables = tree.xpath('//table')

        logging.debug("AuditScope - HTML Tables found: Length %d",
                      len(html_tables))

        self.__azpub_html_table = html_tables[0]
        self.__azgov_html_table = html_tables[1]

    def __init_audit_scope_dictionary(self):

        logging.debug("AuditScopes - Audit Scope Dictionary - Starting Init")
        self.__audit_scope_dictionary = {svc: {} for svc in (maps.service_list + maps.capability_list)}
        
        for svc in maps.service_list:           
            self.__audit_scope_dictionary[svc] = self.__init_blank_helper(svc,'service')


        for cap in maps.capability_list:           
            self.__audit_scope_dictionary[cap] = self.__init_blank_helper(cap,'capability')

        logging.debug("AuditScopes - Audit Scope Dictionary - Initialized")

    def __init_blank_helper (self, id, type) -> dict:
        return {
            'prod-id': id,
            'type': type,
            'azure-public': {'scopes': []},
            'azure-government': {'scopes': []},
            'doc-type': 'audit-scope'
        }           

    def __hydrate_audit_scope_dictionary(self, html_table, cloud):

        logging.debug("AuditScopes - Audit Scope Dictionary - Hydrating")

        az_dict = self.__dict_from_html_table(html_table)

        for id, svc in az_dict.items():
            for scope, value in svc.items():
                if value == "Check":
                    self.__audit_scope_dictionary[id][cloud]['scopes'].append(scope)   

                    """ CODE FOR CAMELIZING
                        tmp = camelize(scope)            
                        self.__audit_scope_dictionary[svc][cloud]['scopes'].append(tmp)
                    """
        
        logging.debug("AuditScopes - Audit Scope Dictionary - Hydration Complete")

    def __dict_from_html_table(self, table) -> dict:
        table_as_list = list(table)

        table_headers = [col.text.strip() for col in table_as_list[0][0]]

        table_as_list_of_dicts = [dict(zip(table_headers, [text(col) for col in row]))
               for row in table_as_list[1][0:]]
        
        return_dict = {}

        for i in table_as_list_of_dicts:
            svc_name = maps.clean_product_name(i.pop('Azure Service'))
            return_dict[svc_name] = i

        return return_dict

    def __dump_audit_scopes (self):
        print (json.dumps(self.__audit_scope_dictionary))

    def getAuditScopeDictionary(self) -> dict:
        return self.__audit_scope_dictionary

    def isAtAuditScope(self, svc, scope) -> bool:
        logging.debug('isAtAuditScope - Checking [' + svc + '] at [' + scope + ']')

        azPub = self.isAtAuditScopeInCloud(svc, scope, "azure-public")
        azGov = self.isAtAuditScopeInCloud(svc, scope, "azure-government")

        logging.debug('isAtAuditScope - [%s] at [%s]. Azure Public [%s], Azure Gov [%s]',
                      svc, scope, azPub, azGov)

        return (azPub | azGov)

    def isAtAuditScopeInCloud(self, svc, scope, cloud) -> bool:

        logging.debug('isAtAuditScopeForCloud - Checking [%s] at [%s] in [%s]',
                      svc, scope, cloud)

        try:
            if svc not in self.__audit_scope_dictionary.keys():
                logging.info(
                    'isAtAuditScopeForCloud - [' + svc + '] is not in the audit_scope_dicitonary')
                return False

            if scope in self.__audit_scope_dictionary[svc][cloud]['scopes']:
                logging.info(
                    'isAtAuditScopeForCloud - [%s] lists \'%s\' for %s', svc, scope, cloud)
                return True

            logging.info(
                'isAtAuditScopeForCloud - [%s] does not list \'%s\' for %s', svc, scope, cloud)

        except KeyError as e:
            logging.error (e)
            pass

        return False
