# -*- coding: utf-8 -*-

import json
import os
from urllib2 import Request, urlopen, URLError, HTTPError
from service import ResourceHandler
from ontology import Ontology

class TMDbHandler(ResourceHandler):
    def __init__(self, resolver, node):
        ResourceHandler.__init__(self, resolver, node)
        
    def parse(self, query):
        for source in query['sources']:
            try:
                document = json.load(source)
            except ValueError as e:
                self.log.warning(u'Failed to decode JSON document %s', query['remote url'])
                self.log.debug(u'Exception raised %s', unicode(e))
            else:
                if 'process' in query['branch']:
                    action = getattr(self, query['branch']['process'], None)
                    if action is not None:
                        document = action(query, document)
                    else:
                        self.log.warning(u'Ignoring unknown process function %s', query['branch']['process'])
                        
                if query['branch']['query type'] == 'lookup':
                    entry = {
                        'branch':query['branch'],
                        'record':{
                            u'head':{ u'genealogy':query['parameter'].project('ns.service.genealogy'), },
                            u'body':{ u'original':document },
                        }
                    }
                    
                    if 'namespace' in query['branch']:
                        # make a caonical node
                        entry['record']['body']['canonical'] = Ontology(self.env, entry['branch']['namespace'])
                        entry['record']['body']['canonical'].decode_all(entry['record']['body']['original'], self.name)
                        
                        # Copy indexed values from the canonical node to the genealogy
                        if 'index' in entry['branch']:
                            for index in entry['branch']['index']:
                                if index in entry['record']['body']['canonical']:
                                    entry['record'][u'head'][u'genealogy'][index] = entry['record']['body']['canonical'][index]
                                    
                    # Append the entry to the query result
                    query['entires'].append(entry)
                    
                elif query['branch']['query type'] == 'search':
                    for trigger in query['branch']['resolve']:
                        for element in document[query['branch']['container']]:
                            # Decode a reference
                            o = Ontology(self.env, trigger['namespace'])
                            o.decode_all(element, self.name)
                            
                            # Make a URI and trigger a resolution
                            ref = o.project('ns.service.genealogy')
                            ref['language']
                            uri = trigger['format'].format(**ref)
                            self.log.debug(u'Trigger %s resolution', uri)
                            self.resolver.resolve(uri)
                            
    def resolve_media_kind(self, query, document):
        def resolve_media_kind_for_reference(node):
            if 'media_type' in node and 'id' in node:
                if node['media_type'] == 'movie':
                    node['media_kind'] = 9
                    node['movie_id'] = node['id']
                    
                elif node['media_type'] == 'tv':
                    node['media_kind'] = 10
                    node['tv_show_id'] = node['id']
                    
                del node['media_type']
                del node['id']
            
        if 'cast' in document:
            for element in document['cast']:
                resolve_media_kind_for_reference(element)
                
        if 'crew' in document:
            for element in document['crew']:
                resolve_media_kind_for_reference(element)
        return document
        
    def expand_tv_season(self, query, document):
        if 'seasons' in document:
            for e in document['seasons']:
                e['tv_show_id'] = document['id']
        return document
        
    def expand_tv_episode(self, query, document):
        if 'episodes' in document:
            for e in document['episodes']:
                e['tv_show_id'] = query['parameter']['tmdb tv show id']
        return document
        
        
        

