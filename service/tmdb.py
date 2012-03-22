# -*- coding: utf-8 -*-

import json
from StringIO import StringIO
from urllib2 import Request, urlopen, URLError, HTTPError

from service import ResourceHandler
from ontology import Ontology


class TMDbHandler(ResourceHandler):
    def __init__(self, resolver, node):
        ResourceHandler.__init__(self, resolver, node)
    
    
    def fetch(self, query):
        self.log.debug(u'Fetching %s', query['remote url'])
        request = Request(query['remote url'], None, {'Accept': 'application/json'})
        
        try:
            response = urlopen(request)
        except HTTPError, e:
            self.log.warning(u'Server returned an error when requesting %s: %s', query['remote url'], e.code)
        except URLError, e:
            self.log.warning(u'Could not reach server when requesting %s: %s', query['remote url'], e.reason)
        else:
            query['stream'].append(StringIO(response.read()))
    
    
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
                    u'parameter':Ontology.clone(query['parameter']),
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
    

