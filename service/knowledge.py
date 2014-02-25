# -*- coding: utf-8 -*-

import json
from urllib2 import Request, urlopen, URLError, HTTPError
from service import ResourceHandler
from ontology import Ontology

class KnowledgeBaseHandler(ResourceHandler):
    def __init__(self, resolver, node):
        ResourceHandler.__init__(self, resolver, node)
        
    def fetch(self, query):
        if 'depend' in query['match']:
            
            # ensure default language
            query['parameter']['language']
            
            # Resolve the dependency document and make sure it is present
            dependee = self.resolver.resolve(query['match']['depend'].format(**query['parameter']))
            if dependee is not None:
                
                # collect the aggregate documents
                if 'aggregate' in query['branch']:
                    for reference in query['branch']['aggregate']:
                        try:
                            related = self.resolver.resolve(reference['uri'].format(**query['parameter']))
                        except KeyError, e:
                            self.log.debug(u'Could not create referenced uri for pattern %s because parameter %s was missing', reference['uri'], e)
                        else:
                            if related is not None:
                                query['sources'].append(related)
                                
    def parse(self, query):
        # Only create a new home document if the dependency is satisfied
        if query['sources']:
            if 'namespace' in query['branch']:
                entry = {
                    'branch':query['branch'],
                    'record':{
                        u'head':{ u'genealogy':query['parameter'].project('ns.service.genealogy'), },
                        u'body':None,
                    }
                }
                
                entry['record']['body'] = Ontology(self.env, entry['branch']['namespace'])
                for source in query['sources']:
                    if 'body' in source and source['body']:
                        entry['record']['body'].merge_all(source['body']['canonical'])
                        
                query['entires'].append(entry)
                
