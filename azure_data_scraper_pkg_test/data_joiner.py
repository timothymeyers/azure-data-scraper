from azure_data_scraper.audit_scope_scraper import AuditScopes
from azure_data_scraper.product_by_region_scraper import ProductsByRegion
from azure_data_scraper import data_mapping as maps

import json
import logging


class DataJoiner:

    def __init__(self, audit_scopes=AuditScopes(), product_availability=ProductsByRegion()):
        # self.__product_availability = AzGovProductAvailabilty()
        # self.__audit_scopes = AuditScopeList()

        self.__product_availability = product_availability
        self.__audit_scopes = audit_scopes
        #self.__joined_data = self.__join(
        #    self.__audit_scopes, self.__product_availability)

        #self.__scope_lookup = self.__hydrate_scope_lookups()
        #self.__region_lookup = self.__hydrate_region_lookups()

    def __join(self, sc, av):

        blankCloud = {
            "available": False,
            "scopes": [],
            "ga": [],
            "preview": [],
            "planned-active": []
        }

        merged_services = {svc: {
            'prod-id': svc,
            'type': 'service',
            'capabilities': [],
            'categories': [],
            'azure-public': blankCloud.copy(),
            'azure-government': blankCloud.copy()
        } for svc in maps.service_list}

        merged_capabilities = {cap: {
            'prod-id': cap,
            'type': 'capability',
            'service': maps.capability_service_map[cap],
            'categories': [],
            'azure-public': blankCloud.copy(),
            'azure-government': blankCloud.copy()
        } for cap in maps.capability_list}

        scList = sc.getCosmosJsonMerged()
        avList = av.getProductAvailabilityJson()

        # initialize using availability list

        for p in (avList['services'] + avList['capabilities']):

            # ugh special Data Box capability case
            if (p['prod-id'] == "Data Box" and p['type'] == "capability-row"):
                pId = p['prod-id']
            else:
                pId = maps.clean_product_name(p['prod-id'])

            try:
                if (pId in maps.service_list):

                    merged_services[pId]['capabilities'] = p['capabilities'][:]
                    merged_services[pId]['categories'] = list(p['categories'])

                    merged_services[pId]['azure-public']['ga'] = p['azure-public']['ga'][:]
                    merged_services[pId]['azure-public']['available'] = (
                        len(p['azure-public']['ga']) > 0)
                    merged_services[pId]['azure-public']['preview'] = list(
                        p['azure-public']['preview'])
                    merged_services[pId]['azure-public']['planned-active'] = list(
                        p['azure-public']['planned-active'])

                    merged_services[pId]['azure-government']['ga'] = list(
                        p['azure-government']['ga'])
                    merged_services[pId]['azure-government']['available'] = (
                        len(p['azure-government']['ga']) > 0)
                    merged_services[pId]['azure-government']['preview'] = list(
                        p['azure-government']['preview'])
                    merged_services[pId]['azure-government']['planned-active'] = list(
                        p['azure-government']['planned-active'])

                elif (pId in maps.capability_list):
                    merged_capabilities[pId]['categories'] = list(
                        p['categories'])

                    merged_capabilities[pId]['azure-public']['ga'] = list(
                        p['azure-public']['ga'])
                    merged_capabilities[pId]['azure-public']['available'] = (
                        len(p['azure-public']['ga']) > 0)
                    merged_capabilities[pId]['azure-public']['preview'] = list(
                        p['azure-public']['preview'])
                    merged_capabilities[pId]['azure-public']['planned-active'] = list(
                        p['azure-public']['planned-active'])

                    merged_capabilities[pId]['azure-government']['ga'] = list(
                        p['azure-government']['ga'])
                    merged_capabilities[pId]['azure-government']['available'] = (
                        len(p['azure-government']['ga']) > 0)
                    merged_capabilities[pId]['azure-government']['preview'] = list(
                        p['azure-government']['preview'])
                    merged_capabilities[pId]['azure-government']['planned-active'] = list(
                        p['azure-government']['planned-active'])

            except KeyError as e:
                print("Error")
                print('\te', e)
                print('\tpId', pId)

        for pId, p in scList.items():
            pId = maps.clean_product_name(pId)

            try:

                if (pId in maps.service_list and "azure-public" in p and len(p['azure-public']['scopes']) > 0):
                    merged_services[pId]['azure-public']['scopes'] = list(
                        p['azure-public']['scopes'])
                if (pId in maps.service_list and "azure-government" in p and len(p['azure-government']['scopes']) > 0):
                    merged_services[pId]['azure-government']['scopes'] = list(
                        p['azure-government']['scopes'])

                if (pId in maps.capability_list and "azure-public" in p and len(p['azure-public']['scopes']) > 0):
                    merged_capabilities[pId]['azure-public']['scopes'] = list(
                        p['azure-public']['scopes'])
                if (pId in maps.capability_list and "azure-government" in p and len(p['azure-government']['scopes']) > 0):
                    merged_capabilities[pId]['azure-government']['scopes'] = list(
                        p['azure-government']['scopes'])

            except KeyError as e:
                print("Error")
                print('\te', e)
                print('\tpId', pId)
                if (pId in maps.service_list):
                    print('\tsvc', merged_services[pId])
                if (pId in maps.capability_list):
                    print('\tcap', merged_capabilities[pId])
                print('\ts-p', p)

        # print(json.dumps({'svc': merged_services,'cap': merged_capabilities}))

        return self.__map_capabilities_to_services(merged_services, merged_capabilities)

    def __map_capabilities_to_services(self, svc, caps):

        merged = {}
        merged_c = {}

        i = 0
        for s, doc in svc.items():
            merged[s] = {}
            merged[s].update(doc)
            merged[s]['id'] = 's-' + str(i)

            try:
                merged[s]['capabilities'].clear()
            except KeyError as e:
                merged[s]['capabilities'] = []

            i = i + 1

        i = 0
        for c, doc in caps.items():
            try:
                sId = doc['service']

                merged_c[c] = {}
                merged_c[c].update(doc)
                merged_c[c]['id'] = 'c-' + str(i)

                merged[sId]['capabilities'].append(c)
            except KeyError as e:
                print("KeyError:")
                print("\t", e)
                print("\t", c)
                print("\t", json.dumps(doc))

            i = i + 1

        return {**merged, **merged_c}

    def __hydrate_scope_lookups(self):

        sl = {svc: [] for svc in (maps.us_scopes + maps.usgov_scopes)}

        for id, prod in self.__joined_data.items():

            {sl[pub].append(id) for pub in prod['azure-public']['scopes']}
            {sl[gov].append(id) for gov in prod['azure-government']['scopes']}

        return sl

    def __hydrate_region_lookups(self):

        rl = {svc: [] for svc in (maps.us_regions + maps.usgov_regions)}

        for id, prod in self.__joined_data.items():
            {rl[pub].append(id) for pub in prod['azure-public']['ga']}
            {rl[gov].append(id) for gov in prod['azure-government']['ga']}

        return rl

    def getJoinedData(self):
        return self.__joined_data

    def qnaGetAvailable(self):

        for id, prod in self.__joined_data.items():
            q = "Is %s available? \t " % id
            print(q, self.answer_isGa(id, prod))
            q = "Is %s ga? \t " % id
            print(q, self.answer_isGa(id, prod))
            q = "Is %s available in Azure Commercial? \t " % id
            print(q, self.answer_isGaIn(
                id, "Azure Commercial", prod['azure-public']))
            q = "Is %s ga in Azure Commercial? \t " % id
            print(q, self.answer_isGaIn(
                id, "Azure Commercial", prod['azure-public']))
            q = "Is %s available in Azure Government? \t " % id
            print(q, self.answer_isGaIn(
                id, "Azure Government", prod['azure-government']))
            q = "Is %s ga in Azure Government? \t " % id
            print(q, self.answer_isGaIn(
                id, "Azure Government", prod['azure-government']))
            q = "Is %s available in MAG? \t " % id
            print(q, self.answer_isGaIn(
                id, "Azure Government", prod['azure-government']))
            q = "Is %s ga in MAG? \t " % id
            print(q, self.answer_isGaIn(
                id, "Azure Government", prod['azure-government']))

            q = "Is %s in preview? \t " % id
            print(q, self.answer_isPreview(id, prod))
            q = "Is %s in preview in Azure Commercial? \t " % id
            print(q, self.answer_isPreviewIn(
                id, "Azure Commercial", prod['azure-public']))
            q = "Is %s in preview in Azure Government? \t " % id
            print(q, self.answer_isPreviewIn(
                id, "Azure Government", prod['azure-government']))

            q = "When is %s expected to be available? \t" % id
            print(q, self.answer_isExpectedToBeGa(id, prod))
            q = "When is %s expected to be available in Azure Government? \t" % id
            print(q, self.answer_isExpectedToBeGaIn(
                id, "Azure Government", prod['azure-government']))
            q = "When is %s expected to be available in Azure Commercial? \t" % id
            print(q, self.answer_isExpectedToBeGaIn(
                id, "Azure Commercial", prod['azure-public']))

            q = "What regions are %s available in? \t" % id
            print(q, self.answer_whatRegionsGa(id, prod))
            q = "What regions are %s available in Azure Commercial? \t" % id
            print(q, self.answer_whatRegionsGaIn(
                id, "Azure Commercial", prod['azure-public']))
            q = "What regions are %s available in Azure Government? \t" % id
            print(q, self.answer_whatRegionsGaIn(
                id, "Azure Government", prod['azure-government']))

            svc = ""
            if 'service' in prod.keys():
                svc = prod['service']

            q = "What scopes is %s available at? \t" % id
            print(q, self.answer_whatScopes(id, prod))
            q = "What scopes is %s available at in Azure Commercial? \t" % id
            print(q, self.answer_whatScopesIn(
                id, "Azure Commercial", prod['azure-public'], svc))
            q = "What scopes is %s available at in Azure Government? \t" % id
            print(q, self.answer_whatScopesIn(
                id, "Azure Government", prod['azure-government'], svc))

        return {}

    """
    Is XXX available?
    Is XXX ga?
    Is XXX ga in Azure Government?
    Is XXX ga in Azure Commercial?
    Is XXX available in Azure Government?
    Is XXX available in Azure Commercial?
    """

    def answer_isGa(self, id, prod):
        azpub = prod['azure-public']['available']
        azgov = prod['azure-government']['available']

        if (azpub and azgov):
            return (
                "**%s** is in both Azure Commercial and Azure Government.\\n\\n" % id
                + self.answer_whatRegionsGaIn(id, "Azure Commercial", prod['azure-public']) + "\\n\\n"
                + self.answer_whatRegionsGaIn(id, "Azure Government", prod['azure-government'])
            )
        elif azpub:
            return (
                "**%s** is available in Azure Commercial, but not Azure Government.\\n\\n" % id
                + self.answer_whatRegionsGaIn(id, "Azure Commercial", prod['azure-public'])
            )
        elif azgov:
            return (
                "**%s** is available in Azure Government, but not Azure Commercial.\\n\\n" % id
                + self.answer_whatRegionsGaIn(id, "Azure Government", prod['azure-government'])
            )

        # return "**%s** is not available in either Azure Commercial or Azure Government" % id
        return (self.answer_whatRegionsGaIn(id, "Azure Commercial", prod['azure-public']) + "\\n\\n"
                + self.answer_whatRegionsGaIn(id, "Azure Government", prod['azure-government']))

    def answer_isGaIn(self, id, cloud_name, cloud_json):
        if cloud_json['available']:
            return (
                "Yes. " +
                self.answer_whatRegionsGaIn(id, cloud_name, cloud_json)
            )

        return self.answer_whatRegionsGaIn(id, cloud_name, cloud_json)

    """
    When is XXX expected to be available?
    When is XXX expected to be available in Azure Government?
    When is XXX expected to be available in Azure Commercial?
    """

    def answer_isExpectedToBeGa(self, id, prod):
        return (
            self.answer_isExpectedToBeGaIn(
                id, "Azure Commercial", prod['azure-public']) + "\\n\\n"
            + self.answer_isExpectedToBeGaIn(id, "Azure Government", prod['azure-government'])
        )

    def answer_isExpectedToBeGaIn(self, id, cloud_name, cloud_json):
        avail = cloud_json['available']
        exp = cloud_json['planned-active']
        a = ""

        if avail:
            a = "**%s** is already available in *%s* in %s" % (
                id, cloud_name, self.__listToMarkdownList(cloud_json['ga']))

        if avail and len(exp) == 0:
            return a
        if len(exp) > 0:
            return (a + "\\n\\n"
                    "GA for **%s** in *%s* is currently targeted for: %s" % (
                        id, cloud_name, self.__listToMarkdownList(exp))
                    )

        return "**%s** is not currently scheduled for GA in *%s*. " % (id, cloud_name)

    """
    What regions are XXX available in?
    What regions are XXX available in Azure Commercial?
    What regions are XXX available in Azure Government?
    """

    def answer_whatRegionsGa(self, id, prod):
        return (
            self.answer_whatRegionsGaIn(
                id, "Azure Commercial", prod['azure-public']) + "\\n\\n"
            + self.answer_whatRegionsGaIn(id, "Azure Government", prod['azure-government'])
        )

    def answer_whatRegionsGaIn(self, id, cloud_name, cloud_json):
        regions = cloud_json['ga']
        preview = cloud_json['preview']

        if len(regions) > 0:
            return "**%s** is GA in *%s* in: %s" % (id, cloud_name, self.__listToMarkdownList(regions))
        else:
            a = "**%s** is not currently GA in *%s*. " % (id, cloud_name)

            if len(preview) > 0:
                a = a + \
                    "However, it is ***in preview*** in %s" % self.__listToMarkdownList(
                        preview)

            return a + self.answer_isExpectedToBeGaIn(id, cloud_name, cloud_json)

    """
    Is XXX in preview?
    Is XXX in preview in Azure Government?
    Is XXX in preview in Azure Commercial?
    """

    def answer_isPreview(self, id, prod):
        return (
            self.answer_isPreviewIn(
                id, "Azure Commercial", prod['azure-public']) + "\\n\\n"
            + self.answer_isPreviewIn(id, "Azure Government",
                                      prod['azure-government'])
        )

    def answer_isPreviewIn(self, id, cloud_name, cloud_json):
        avail = cloud_json['available']
        preview = cloud_json['preview']
        a = ""

        if avail:
            a = "**%s** is already available in *%s* in %s" % (
                id, cloud_name, self.__listToMarkdownList(cloud_json['ga']))

        if avail and len(preview) == 0:
            return a
        if len(preview) > 0:
            return (a + "\\n\\n"
                    "**%s** is in preview in *%s* in %s" % (
                        id, cloud_name, self.__listToMarkdownList(preview))
                    )

        return "**%s** is not currently in preview in *%s*. " % (id, cloud_name)

    """
    What scopes is XXX available at?
    What scopes is XXX available at in Azure Commercial?
    What scopes is XXX available at in Azure Government?
    """

    def answer_whatScopes(self, id, prod):
        if 'service' in prod.keys():
            return (
                self.answer_whatScopesIn(
                    id, "Azure Commercial", prod['azure-public'], prod['service'])
                + "\\n\\n"
                + self.answer_whatScopesIn(id, "Azure Government",
                                           prod['azure-government'], prod['service'])
            )

        return (
            self.answer_whatScopesIn(
                id, "Azure Commercial", prod['azure-public'])
            + "\\n\\n"
            + self.answer_whatScopesIn(id, "Azure Government",
                                       prod['azure-government'])
        )

    def answer_whatScopesIn(self, id, cloud_name, cloud_json, svc=""):
        scopes = cloud_json['scopes']

        if len(scopes) > 0:
            return "In *%s*, **%s** is available at %s" % (cloud_name, id, self.__listToMarkdownList(scopes))

        else:
            a = "I don't have any audit scope or impact level information about **%s** in *%s*. " % (
                id, cloud_name)

            if svc != "":
                if (cloud_name.__contains__("ov") or cloud_name.__contains__("MAG")):
                    svc_json = self.__joined_data[svc]['azure-government']
                else:
                    svc_json = self.__joined_data[svc]['azure-public']

                return (a + " However, it is a capability of %s. " % svc
                        + "Here is what I know about *%s*'s audit scopes and impact levels:\\n\\n" % svc
                        + self.answer_whatScopesIn(svc, cloud_name, svc_json)
                        )

            return a

    """
    Is %s at %s?
    Is %s at %s in %s?
    """

    def qnaGetScope(self):

        for id in (maps.service_list + maps.capability_list):            
            for scope in (maps.us_scopes + maps.usgov_scopes) :
                if not scope.__contains__("Il5"):
                    print ("Is %s at %s? \t" % (id, maps.scope_map[scope]), self.answer_isAtScope(id, scope))

            ## Special IL5 Use Case
            print ("Is %s at IL5? \t" % id, self.answer_isAtIL5(id))

        return   

    def answer_isAtScope (self, id, scope):      

        if (id in self.__scope_lookup[scope]):
            return "Yes. **%s** is %s" % (id, maps.scope_map[scope])

        return "No. **%s** is not at %s yet" % (id, maps.scope_map[scope])

    def answer_isAtIL5 (self, id):
        # 'dodCcSrgIl5AzureGov': 'IL5 in Gov Regions',
        # 'dodCcSrgIl5AzureDod': 'IL5 in DoD Regions',
        gov = id in self.__scope_lookup['dodCcSrgIl5AzureGov']
        dod = id in self.__scope_lookup['dodCcSrgIl5AzureDod']

        if (gov and dod): return "Yes, **%s** is IL5 in ***both*** Gov and DoD regions" % id
        if (gov): return "Yes. However, **%s** is IL5 ***in Gov regions only***." % id
        if (dod): return "Yes. However, **%s** is IL5 ***in DoD regions only***." % id

        return "No. **%s** is not at IL5 yet" % id

    def qnaGetRegions(self):
        for id in (maps.service_list + maps.capability_list):
            for region in (maps.us_regions + maps.usgov_regions + maps.usdod_regions):
                if not region.__contains__("non-regional"):
                    print ("Is %s in %s? \t" % (id, region), self.answer_isInRegion(id,region))

    def answer_isInRegion(self, id, region):

        if id in self.__region_lookup[region]:
            return "Yes. **%s** is in %s" % (id, region)

        if region in maps.us_regions:
            if id != "non-regional" and id in self.__region_lookup['non-regional']:
                return "Yes. **%s** is in %s. It is *Non-Regional* in Azure Commercial." % (id, region)
            else:
                return self.answer_whatRegionsGaIn(id, "Azure Commercial", self.__joined_data[id]['azure-public'])

        if region in maps.usgov_regions:
            if id != "usgov-non-regional" and id in self.__region_lookup['usgov-non-regional']:
                return "Yes. **%s** is in %s. It is *Non-Regional* in Azure Government." % (id, region)
            else:
                return self.answer_whatRegionsGaIn(id, "Azure Government", self.__joined_data[id]['azure-government'])

        return "No. **%s** is not in %s yet. And, I'm confused by the question." % (id, region)


    def __listToMarkdownList(self, inList):
        a = ""
        for item in inList:
            a = a + "\\n * %s" % item
        a = a + "\\n\\n"
        return a


"""
What can you tell me about XXX?"

What is available in XXX region?

What is available at XXX scope?
What is available at XXX scope in Azure Commercial?
What is available at XXX scope in Azure Government?
"""
