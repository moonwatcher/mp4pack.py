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
        request = Request(query['remote url'])
        
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
                self.log.warning(u'Failed to decode JSON document %s: %s', query['remote url'], e)
            else:
                # Check if we got a TMDB error document
                if 'status_code' in document and document['status_code'] != 1:
                    self.log.warning(u'Error fetching %s: %s', query['remote url'], document['status_message'])
                else:
                    branch = self.branch[query['namespace']]
                    entry = {
                        u'host':query['parameter']['host'],
                        u'namespace':query['namespace'],
                        u'uri':query['uri'],
                        u'document':[],
                    }
                    
                    if 'index' in branch:
                        for index in branch['index']:
                            if index in query['parameter']:
                                entry[index] = query['parameter'][index]
                                
                    query['result'].append(document)
        for entry in query['result']:
            self.store(entry)
    

