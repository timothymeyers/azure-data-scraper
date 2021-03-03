from lxml import html, etree
from bs4 import BeautifulSoup
import requests
import pprint
import logging
from datetime import datetime
import re
import azure_data_scraper.data_mapping as maps

# Constants
AZGOV_PRODS_BY_REGION = "https://service.prerender.io/https://azure.microsoft.com/en-us/global-infrastructure/services/?products=all&regions=usgov-non-regional,us-dod-central,us-dod-east,usgov-arizona,usgov-texas,usgov-virginia"
AZ_US_PRODS_BY_REGION = "https://service.prerender.io/https://azure.microsoft.com/en-us/global-infrastructure/services/?products=all&regions=usgov-non-regional,us-dod-central,us-dod-east,usgov-arizona,usgov-texas,usgov-virginia,non-regional,us-central,us-east,us-east-2,us-north-central,us-south-central,us-west-central,us-west,us-west-2"

# Helpers

# Gets text from an HTML element

class ProductsByRegion:
    def __init__(self, src='web'):
        self.__products_dictionary = {}

        logging.info("ProductsByRegion - Starting Initialization")

        self.__init_products_dictionary()

        soup = self.__init_soup_parser(src)
        self.__hydrate_products_dictionary(soup)

        #print(json.dumps(self.__products_dictionary))

    def __init_soup_parser(self, src='web') -> BeautifulSoup:

        if src == "web":
            page = requests.get(AZ_US_PRODS_BY_REGION)
            soup = BeautifulSoup(page.content, features='lxml')
        elif src == "local":
            with open("render-all-us.html", encoding='utf-8') as f:
                render = html.document_fromstring(f.read())
                render = html.tostring(render)
            soup = BeautifulSoup(render, features='lxml')
        else:
            logging.error("ProductsByRegion - Unknown data source", src)

        soup = soup.find(attrs={"class": "primary-table"})

        soup = self.__helper_replace_soup_image(
            soup, "preview-active.svg", "preview-active")
        soup = self.__helper_replace_soup_image(
            soup, "planned-active.svg", "planned-active")
        soup = self.__helper_replace_soup_image(soup, "preview.svg", "preview")
        soup = self.__helper_replace_soup_image(soup, "ga.svg", "check")
        soup = self.__helper_remove_tooltip_content_from_soup(soup)

        return soup

    def __helper_replace_soup_image(self, soup, img_file_name, text):
        imgs = soup.find_all(name="img", attrs={
            "src": re.compile(img_file_name)
        }, recursive=True)

        for img in imgs:
            img.name = "p"
            del img['src']
            del img['role']
            del img['alt']
            if (text.__contains__("-active")):
                img['ga-expected'] = img.parent.get_text(
                    " ", strip=True).replace("GA expected ", "")

            img.string = text

        return soup

    def __helper_remove_tooltip_content_from_soup(self, soup):
        table_tooltips = soup.find_all(
            "span", attrs={"class": "table-tooltip"})
        tooltip_content = soup.find_all(
            "span", attrs={"class": "tooltip-content"})
        hide_text = soup.find_all("span", attrs={"class": "tooltip-content"})

        for tiptag in (table_tooltips + tooltip_content+hide_text):
            tiptag.decompose()

        return soup

    def __init_products_dictionary(self):
        logging.debug(
            "ProductsByRegion: __init_products_dictionary - starting")

        self.__products_dictionary = {i: {} for i in (
            maps.service_list + maps.capability_list)}

        for svc in maps.service_list:
            self.__products_dictionary[svc] = self.__init_blank_helper(svc, 'service')

        for cap in maps.capability_list:
            self.__products_dictionary[cap] = self.__init_blank_helper(cap, 'capability')

        logging.debug(
            "ProductsByRegion: __init_products_dictionary - initialized")

    def __init_blank_helper(self, id, type) -> dict:
        return {
            'prod-id': id,
            'type': type,
            'capabilities': [],
            'categories': [],
            'azure-public': {
                "available": False,
                "scopes": [],
                "ga": [],
                "preview": [],
                "planned-active": []
            },
            'azure-government': {
                "available": False,
                "scopes": [],
                "ga": [],
                "preview": [],
                "planned-active": []
            },
            'doc-type':''
        }

    def __hydrate_products_dictionary(self, soup):
        rows = soup.find_all('tr')

        lastCat = ""
        for row in rows[2:]:                      
            row_class = row['class'][0]

            # Category
            if row_class.__contains__("category"):
                prod_id = self.__hydrate_product_row(row, row_class)
                lastCat = maps.clean_product_name(prod_id, row_class)
            else:
                prod_id = self.__hydrate_product_row(row, row_class, lastCat)
        
        #update service field for capabilities
        for id, prod in self.__products_dictionary.items():
            if prod['type'] == 'capability' and 'service' in prod:
                svc = prod['service']
                self.__products_dictionary[svc]['capabilities'].append(id)
                prod.pop('capabilities')

    def __hydrate_product_row(self, row, row_class, category="") -> str:
        cols = row.find_all(['th', 'td'])        

        prod_id = maps.clean_product_name(cols[0].text, row_class)

        ## Ignore category rows
        if (row_class.__contains__("category")):
            return prod_id

        ## Ignore if already hydrated
        if self.__products_dictionary[prod_id]['doc-type'] == "availability":            
            return prod_id 

        # do i really need this?
        # if prodId not in self.__products_dictionary:
        #     logging.error("%s is not in product dictionary" % prodId)
        #     raise Exception("'%s' is not in product dictionary" % prodId)
        
        if self.__products_dictionary[prod_id]['doc-type'] == "availability":
            ## No need to process this row
            return prod_id
        
        self.__products_dictionary[prod_id]['doc-type'] = "availability"

        for col in cols[1:]:  # skip first col, it is just the prod id

            self.__hydrate_region_col(prod_id,col)

        if (len( self.__products_dictionary[prod_id]['azure-public']['ga']) > 0):
            self.__products_dictionary[prod_id]['azure-public']['available'] = True
        if (len( self.__products_dictionary[prod_id]['azure-government']['ga']) > 0):
            self.__products_dictionary[prod_id]['azure-government']['available'] = True

        self.__products_dictionary[prod_id]['categories'].append(category)

        if row_class.__contains__("capability"):
            self.__products_dictionary[prod_id]['service'] = maps.capability_service_map[prod_id]
            

        return prod_id

    def __hydrate_region_col(self, prodId, col):
        col_text = col.text.strip()
        region = col['data-region-slug']

        if region in maps.us_regions:
            cloud = 'azure-public'
        elif region in maps.usgov_regions:
            cloud = 'azure-government'
        else:
            logging.error("Unknown region [%s]" % region)
            raise Exception("Unknown region [%s]" % region)

        ## row is GA in region
        if col_text == "check":
            self.__products_dictionary[prodId][cloud]['ga'].append(region)

        ## row is Preview in region
        if "preview" in col_text:
            self.__products_dictionary[prodId][cloud]['preview'].append(
                region)

        # row has target active date
        if col_text.__contains__("-active"):
            p = col.find('p')
            ga_expected = p['ga-expected']

            active = {
                'region': region,
                'ga-expected': ga_expected
            }

            self.__products_dictionary[prodId][cloud]['planned-active'].append(active)

    def getProductsAvailabilityDictionary(self) -> dict:
        return self.__products_dictionary

    def getServicesList(self) -> list:
        return [id for id, prod in self.__products_dictionary.items() if prod['type'] == 'service']

    def getCapabilitiesList(self) -> list:
        return [id for id, prod in self.__products_dictionary.items() if prod['type'] == 'capability']

    def isProductAvailable(self, prod, cloud="") -> bool:

        if prod in self.__products_dictionary:
            az_pub = self.__products_dictionary[prod]['azure-public']['available']
            az_gov = self.__products_dictionary[prod]['azure-government']['available']
        
            if (cloud == 'azure-public'): return az_pub
            if (cloud == 'azure-government'): return az_gov

            return (az_pub or az_gov)

        return False

    def isProductAvailableInRegion(self, prod, region) -> bool:

        if prod in self.__products_dictionary:
            az_pub = region in self.__products_dictionary[prod]['azure-public']['ga']
            az_gov = region in self.__products_dictionary[prod]['azure-government']['ga']

            return (az_pub or az_gov)

        return False

    def isServiceAvailable(self, svc, cloud="") -> bool:
        return self.isProductAvailable(svc,cloud)

    def isServiceAvailableInRegion(self, svc, region) -> bool:
        return self.isProductAvailableInRegion(svc,region)

    def isCapabilityAvailable(self, cap, cloud="") -> bool:
        return self.isProductAvailable(cap,cloud)
    
    def isCapabilityAvailableInRegion(self, cap, region) -> bool:
        return self.isProductAvailableInRegion(cap,region)

    def getProductPreviewRegions(self, prod, cloud="") -> list:
        return self.__helper_get_product_cloud_lists(prod, cloud, 'preview')

    def getProductRegionsGATargets(self, prod, cloud="") -> list:
        return self.__helper_get_product_cloud_lists(prod, cloud, 'planned-active')

    def __helper_get_product_cloud_lists(self, prod, cloud, which_list):

        if prod in self.__products_dictionary:
            az_pub_regions = self.__products_dictionary[prod]['azure-public'][which_list]
            az_gov_regions = self.__products_dictionary[prod]['azure-government'][which_list]

            if (cloud == 'azure-public'): return az_pub_regions
            if (cloud == 'azure-government'): return az_gov_regions
            return az_pub_regions + az_gov_regions

        return []
