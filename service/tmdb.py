# -*- coding: utf-8 -*-

import json
from StringIO import StringIO
from urllib2 import Request, urlopen, URLError, HTTPError

from service import ResourceHandler

class TMDbHandler(ResourceHandler):
    def __init__(self, resolver, node):
        ResourceHandler.__init__(self, resolver, node)
    
    
    def fetch(self, query):
        self.log.debug(u'Retrieve %s', query['remote url'])
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
                    u'collection':query['branch']['collection'],
                    u'uri':query['uri'],
                    u'document':[document],
                }
                
                # update index
                if 'index' in query['branch']:
                    entry[u'index'] = {}
                    for index in query['branch']['index']:
                        if index in query['parameter']:
                            entry[u'index'][index] = query['parameter'][index]
                query['result'].append(entry)
    

