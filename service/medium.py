# -*- coding: utf-8 -*-

import json
import uuid
from StringIO import StringIO
from urllib2 import Request, urlopen, URLError, HTTPError

class MediumHandler(ResourceHandler):
    def __init__(self, node):t
        ResourceHandler.__init__(self, node)
    
    
    def fetch(self, query):
        if query['branch']['type'] == 'crawl':
            # For resources, use the crawler to build a record
            if query['location']:
                crawler = Crawler(query['location'])
                if crawler.valid:
                    self.log.debug(u'Crawling %s', query['location']['path'])
                    query['source'].append(crawler)
                    
        elif query['branch']['type'] == 'reference':
            # For assets, query the resource collection to collect the relevent resources
            collection = query['repository'].database[entry['branch']['collection reference']]
            resources = collection.find({u'head.asset_uri':})
    
    
    def parse(self, query):
        if query['branch']['type'] == 'crawl':
            for crawler in query['source']:
                entry = {
                    u'branch':query['branch'],
                    u'parameter':Ontology.clone(query['parameter']),
                    u'head':{ u'asset_uri':query['location']['asset uri'], },
                    u'body':crawler.node,
                }
                
                # update index
                ns = self.env.namespace[entry['branch']['namespace']]
                if 'index' in query['branch']:
                    for index in query['branch']['index']:
                        if index in crawler.ontology:
                            entry[u'parameter'][index] = crawler.ontology[index]
                            
                query['result'].append(entry)
                
        elif query['branch']['type'] == 'reference':
            pass
    

