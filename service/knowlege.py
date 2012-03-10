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
                self.log.warning(u'Could not decode JSON from %s: %s', remote, e)
            else:
                # Check if we got a TMDB error document
                if 'status_code' in document and document['status_code'] != 1:
                    self.log.warning(u'Failed to fetch %s %s', remote, document['status_message'])
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
    

