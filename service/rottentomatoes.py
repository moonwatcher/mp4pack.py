# -*- coding: utf-8 -*-

import os
import json
from StringIO import StringIO
from urllib2 import Request, urlopen, URLError, HTTPError

from service import ResourceHandler
from ontology import Ontology


class RottenTomatoesHandler(ResourceHandler):
    def __init__(self, resolver, node):
        ResourceHandler.__init__(self, resolver, node)
    
    
    def fetch(self, query):
        # Add Rotten Tomatoes api key to the parameter list
        query['parameter']['api key'] = self.node['api key']
        
        query['parameter']['trimmed imdb movie id']
        
        # Try to build the remote url and get the resource
        if 'remote' in query['match']:
            query['remote url'] = os.path.join(self.node['remote base'], query['match']['remote'].format(**query['parameter']))
            
            self.log.debug(u'Fetching %s', query['remote url'])
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
                
                # Rotten tomatoes holds the imdb id without the tt prefix, inside the alternate_ids dictionary
                # This is a unique case so we handle it separately 
                if 'alternate_ids' in document and 'imdb' in document['alternate_ids'] and document['alternate_ids']['imdb']:
                    entry['record'][u'head'][u'genealogy'][u'imdb movie id'] = u'tt{0}'.format(document['alternate_ids']['imdb'])
                    
                # Use the decalred namespace for the branch to decode stuff 
                # from the document and augment the genealogy
                ns = self.env.namespace[entry['branch']['namespace']]
                if 'index' in query['branch']:
                    for index in query['branch']['index']:
                        prototype = ns.find(index)
                        if prototype and prototype.node['rottentomatoes'] in document:
                            entry['record'][u'head'][u'genealogy'][index] = prototype.cast(document[prototype.node['rottentomatoes']])
                            
                query['result'].append(entry)
    

