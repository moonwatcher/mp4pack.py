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
        
    
    def parse(self, query):
        for source in query['source']:
            try:
                document = json.load(source)
            except ValueError, e:
                self.log.warning(u'Failed to decode JSON document %s', query['remote url'])
                self.log.debug(u'Exception raised %s', unicode(e))
            else:
                if 'error' in document:
                    self.log.warning(u'API error: %s', document['error'])
                else:
                    entry = {
                        'branch':query['branch'],
                        'record':{
                            u'head':{ u'genealogy':query['parameter'].project('ns.service.genealogy'), },
                            u'body':{ u'original':document },
                        }
                    }
                    
                    # Rotten tomatoes specific overrides
                    if entry['branch']['name'] == 'service.remote.rottentomatoes.movie':
                        # Rotten tomatoes holds the imdb id without the tt prefix, inside the alternate_ids dictionary
                        if 'alternate_ids' in document and 'imdb' in document['alternate_ids'] and document['alternate_ids']['imdb']:
                            document[u'imdb_id'] = u'tt{0}'.format(document['alternate_ids']['imdb'])
                            
                        # Flatten the release date
                        if 'release_dates' in document and 'theater' in document['release_dates']:
                            document[u'release_date'] = document['release_dates']['theater']
                        
                    if entry['branch']['name'] == 'service.remote.rottentomatoes.movie.review' and 'reviews' in document:
                        # Flatten the review links
                        for r in document['reviews']:
                            if 'links' in r and 'review' in r['links']: r['review_link'] = r['links']['review']
                        

                    # make a caonical node
                    entry['record']['body']['canonical'] = Ontology(self.env, entry['branch']['namespace'])
                    entry['record']['body']['canonical'].decode_all(entry['record']['body']['original'], self.name)

                    # Movie ratings are stored in a sub container, simply decode them directly from there
                    if entry['branch']['name'] == 'service.remote.rottentomatoes.movie':
                        if 'ratings' in document:
                            canonical.decode_all(document['ratings'], 'rottentomatoes')
    
                    # Copy indexed values from the canonical node to the genealogy
                    if 'index' in entry['branch']:
                        for index in entry['branch']['index']:
                            if index in entry['record']['body']['canonical']:
                                entry['record'][u'head'][u'genealogy'][index] = entry['record']['body']['canonical'][index]
    
                    query['result'].append(entry)
    

