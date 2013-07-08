# -*- coding: utf-8 -*-

from datetime import datetime
from service import ResourceHandler

class HomeHandler(ResourceHandler):
    def __init__(self, resolver, node):
        ResourceHandler.__init__(self, resolver, node)
    
    
    def fetch(self, query):
        if 'depend' in query['match']:
            
            # ensure default language
            query['parameter']['language']
            
            if 'index' in query['branch']:
                # Resolve the dependency document
                dependee = self.resolver.resolve(query['match']['depend'].format(**query['parameter']))
                if dependee is not None:
                    for index in query['branch']['index']:
                        if index in dependee[u'head'][u'genealogy']:
                            query['parameter'][index] = dependee[u'head'][u'genealogy'][index]
                            
                    query['sources'].append(dependee)
    
    
    def parse(self, query):
        # Only create a new home document if the dependency is satisfied
        if query['sources']:
            entry = {
                'branch':query['branch'],
                'record':{
                    u'head':{ u'genealogy':query['parameter'].project('ns.service.genealogy'), },
                }
            }
            
            query['entires'].append(entry)
    

