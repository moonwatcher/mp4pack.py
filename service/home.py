# -*- coding: utf-8 -*-

from datetime import datetime
from service import ResourceHandler

class HomeHandler(ResourceHandler):
    def __init__(self, resolver, node):
        ResourceHandler.__init__(self, resolver, node)
        
    def fetch(self, query):
        # ensure default language
        query['parameter']['language']
        
        if 'depend' in query['match']:
            # Resolve the dependency document
            dependee = self.resolver.resolve(query['match']['depend'].format(**query['parameter']))
            
            # If the document was resolved
            if dependee is not None:
                # and the branch has indexed parameters
                # copy indexed parameters from the dependee's genealogy to the query parameter ontology
                if 'index' in query['branch']:
                    for index in query['branch']['index']:
                        if index in dependee[u'head'][u'genealogy']:
                            query['parameter'][index] = dependee[u'head'][u'genealogy'][index]
                            
                # append the resolved dependee to the sources list
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
            

