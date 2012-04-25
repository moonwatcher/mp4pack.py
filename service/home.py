# -*- coding: utf-8 -*-

import json
from StringIO import StringIO
from urllib2 import Request, urlopen, URLError, HTTPError

class HomeHandler(ResourceHandler):
    def __init__(self, node):
        ResourceHandler.__init__(self, node)
    
    
    def fetch(self, query):
        if 'depend' in query['match']:
            document = self.resolver.resolve(query['match']['depend'].format(**query['parameter']))
            if document is not None:
                query['stream'].append(document)
    
    
    def parse(self, query):
        for stream in query['stream']:
                 entry = {
                     u'branch':query['branch'],
                     u'parameter':query['parameter'],
                     u'head':{},
                     u'body':document,
                 }
                 
                 # update index
                 ns = self.env.namespace[entry['branch']['namespace']]
                 if 'index' in query['branch']:
                     for index in query['branch']['index']:
                         prototype = ns.find(index)
                         if prototype and prototype.node['tmdb'] in document:
                             entry[u'parameter'][index] = prototype.cast(document[prototype.node['tmdb']])
                             
                 query['result'].append(entry)
    

