# -*- coding: utf-8 -*-

import json
import uuid
from StringIO import StringIO
from urllib2 import Request, urlopen, URLError, HTTPError
from service import ResourceHandler
from crawler import Crawler
from ontology import Ontology

class MediumHandler(ResourceHandler):
    def __init__(self, resolver, node):
        ResourceHandler.__init__(self, resolver, node)
    
    
    def fetch(self, query):
        if query['branch']['type'] == 'crawl':
            # First try and locate the home record with the home uri
            # If the home is resolvable we can get the home id
            if query['location'] and 'home uri' in query['location']:
                home = self.resolver.resolve(query['location']['home uri'])
                if home is not None:
                    query['location']['home id'] = home['head']['genealogy']['home id']
                    
                    # Now use the crawler to build a record
                    crawler = Crawler(query['location'])
                    if crawler.valid:
                        self.log.debug(u'Crawling %s', query['location']['path'])
                        query['source'].append(crawler)
                    
        elif query['branch']['type'] == 'reference':
            # For assets, query the resource collection to collect the relevent resources
            collection = query['repository'].database['medium_resource']
            resources = collection.find({u'head.genealogy.home id':query['parameter']['home id']})
            node = {'reference':{},}
            for resource in resources:
                node['reference'][resource['head']['canonical']] = resource['head']
            query['source'].append(node)
    
    
    def parse(self, query):
        if query['branch']['type'] == 'crawl':
            for crawler in query['source']:
                entry = {
                    u'branch':query['branch'],
                    'record':{
                        u'head':{ u'genealogy':query['location'].project('ns.service.genealogy'), },
                        u'body':crawler.node,
                    },
                }
                query['result'].append(entry)
                
        elif query['branch']['type'] == 'reference':
            for node in query['source']:
                entry = {
                    u'branch':query['branch'],
                    'record':{
                        u'head':{ u'genealogy':query['parameter'].project('ns.service.genealogy'), },
                        u'body':node,
                    },
                }
                query['result'].append(entry)
    

