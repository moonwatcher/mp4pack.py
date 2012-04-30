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
        # Add TMDB api key to the parameter list
        query['parameter']['api key'] = self.node['api key']
        
        # Try to build the remote url and get the resource
        if 'remote' in query['match']:
            query['remote url'] = query['match']['remote'].format(**query['parameter'])
            
            self.log.debug(u'Fetching %s', query['remote url'])
            
            # TMDB requires the request to specify the type of the request as json
            request = Request(query['remote url'], None, {'Accept': 'application/json'})
            
            try:
                response = urlopen(request)
            except HTTPError, e:
                self.log.warning(u'Server returned an error when requesting %s: %s', query['remote url'], e.code)
            except URLError, e:
                self.log.warning(u'Could not reach server when requesting %s: %s', query['remote url'], e.reason)
            else:
                query['source'].append(StringIO(response.read()))
    
    
    def parse(self, query):
        for source in query['source']:
            try:
                document = json.load(source)
            except ValueError, e:
                self.log.warning(u'Failed to decode JSON document %s', query['remote url'])
                self.log.debug(u'Exception raised %s', unicode(e))
            else:
                # Initialize the genealogy by projecting the query parameter space on the ns.service.genealogy namespace
                # This will get rid of the api key
                entry = {
                    'branch':query['branch'],
                    'record':{
                        u'head':{ u'genealogy':query['parameter'].project('ns.service.genealogy'), },
                        u'body':document,
                    }
                }
                
                # Use the decalred namespace for the branch to decode stuff 
                # from the document and augment the genealogy
                ns = self.env.namespace[entry['branch']['namespace']]
                if 'index' in query['branch']:
                    for index in query['branch']['index']:
                        prototype = ns.find(index)
                        if prototype and prototype.node['tmdb'] in document:
                            entry['record'][u'head'][u'genealogy'][index] = prototype.cast(document[prototype.node['tmdb']])
                            
                query['result'].append(entry)
    

