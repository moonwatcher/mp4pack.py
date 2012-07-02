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
    
    def prepare(self, query):
        query['parameter']['trimmed imdb movie id']
        ResourceHandler.prepare(self, query)
        
    
    def fetch(self, query):
        if 'remote url' in query:
            request = Request(query['remote url'], None, {'Accept': 'application/json'})
            self.log.debug(u'Fetching %s', query['remote url'])
            
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
                        u'body':{ u'original':document },
                    }
                }
                
                # Overrides
                if entry['branch']['name'] == 'service.remote.rottentomatoes.movie':
                    # Rotten tomatoes holds the imdb id without the tt prefix, inside the alternate_ids dictionary
                    if 'alternate_ids' in document and 'imdb' in document['alternate_ids'] and document['alternate_ids']['imdb']:
                        document[u'imdb_id'] = u'tt{0}'.format(document['alternate_ids']['imdb'])
                    if 'release_dates' in document and 'theater' in document['release_dates']:
                        document[u'release_date'] = document['release_dates']['theater']
                    
                if entry['branch']['name'] == 'service.remote.rottentomatoes.movie.review' and 'reviews' in document:
                    # Flatten the review links
                    for r in document['reviews']:
                        if 'links' in r and 'review' in r['links']: r['review_link'] = r['links']['review']
                    
                # Use the decalred namespace for the branch to decode stuff 
                # from the document and augment the genealogy
                ns = self.env.namespace[entry['branch']['namespace']]
                if 'index' in query['branch']:
                    for index in query['branch']['index']:
                        prototype = ns.find(index)
                        if prototype and prototype.node['rottentomatoes'] in document:
                            entry['record'][u'head'][u'genealogy'][index] = prototype.cast(document[prototype.node['rottentomatoes']])
                            
                # make a caonical node
                canonical = Ontology(self.env, entry['branch']['namespace'])
                canonical.decode_all(document, 'rottentomatoes')

                if entry['branch']['name'] == 'service.remote.rottentomatoes.movie':
                    # The ratings are stored in a sub container
                    if 'ratings' in document:
                        canonical.decode_all(document['ratings'], 'rottentomatoes')

                entry['record']['body']['canonical'] = canonical.node
                query['result'].append(entry)
    

