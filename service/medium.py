# -*- coding: utf-8 -*-

import json
import uuid
from urllib2 import Request, urlopen, URLError, HTTPError
from service import ResourceHandler
from crawler import Crawler
from ontology import Ontology

class MediumHandler(ResourceHandler):
    def __init__(self, resolver, node):
        ResourceHandler.__init__(self, resolver, node)
        
    def fetch(self, query):
        if query['branch']['type'] == 'crawl':
            if query['location']:
                # If we don't have the home id but we can construct one of the home URIs
                # we can resolve the home record and get the home id
                if 'home id' not in query['location'] and 'home uri' in query['location']:
                    home = self.resolver.resolve(query['location']['home uri'])
                    if home is not None:
                        query['location']['home id'] = home['head']['genealogy']['home id']
                        
                # If we identified the home id we proceed to crawl
                if 'home id' in query['location']:
                    crawler = Crawler(query['location'])
                    if crawler.valid:
                        self.log.debug(u'Crawling %s', query['location']['path'])
                        query['sources'].append(crawler)
                        
        elif query['branch']['type'] == 'reference':
            node = {'reference':{},}
            collection = query['repository'].database['medium_resource']
            
            # create the asset node: references to all resources of this asset
            if query['branch']['name'] == 'service/medium/asset':
                resources = collection.find({u'head.genealogy.home id':query['parameter']['home id']})
                
            # create the fragment node: references to all resources that are fragments of this resource
            elif query['branch']['name'] == 'service/medium/resource/fragment':
                resources = collection.find(
                    {
                        u'head.genealogy.resource path digest':query['parameter']['path digest'],
                        u'head.genealogy.routing type':'fragment',
                    }
                )
                
            for resource in resources:
                node['reference'][resource['head']['canonical']] = resource['head']
            query['sources'].append(node)
            
    def parse(self, query):
        if query['branch']['type'] == 'crawl':
            for crawler in query['sources']:
                entry = {
                    u'branch':query['branch'],
                    'record':{
                        u'head':{ u'genealogy':query['location'].project('ns.service.genealogy'), },
                        u'body':crawler.node,
                    },
                }
                query['entires'].append(entry)
                
                # Hack to force path digest
                entry['record'][u'head'][u'genealogy']['path digest']
                
        elif query['branch']['type'] == 'reference':
            for node in query['sources']:
                entry = {
                    u'branch':query['branch'],
                    'record':{
                        u'head':{ u'genealogy':query['parameter'].project('ns.service.genealogy'), },
                        u'body':node,
                    },
                }
                query['entires'].append(entry)
                

