# -*- coding: utf-8 -*-

import json
from StringIO import StringIO
from urllib2 import Request, urlopen, URLError, HTTPError

class KnowlegeBaseHandler(ResourceHandler):
    def __init__(self, node):
        ResourceHandler.__init__(self, node)
    
    
    def fetch(self, query):
        pass
    
    
    def parse(self, query):
        for stream in query['stream']:
            try:
                document = json.load(stream)
            except ValueError, e:
                self.log.warning(u'Failed to decode JSON document %s', query['remote url'])
                self.log.debug(u'Exception raised %s', unicode(e))
            else:
                entry = {
                    u'branch':query['branch'],
                    u'parameter':Ontology(self.env, query['parameter']),
                    u'body':document,
                }
                
                # update index
                ns = self.namespaces[query['branch']['namespace']]
                if 'index' in query['branch']:
                    for index in query['branch']['index']:
                        prototype = ns.find(index)
                        if prototype and prototype.node['tmdb'] in document:
                            entry[u'parameter'][index] = prototype.cast(document[prototype.node['tmdb']])
                            
                query['result'].append(entry)
    

