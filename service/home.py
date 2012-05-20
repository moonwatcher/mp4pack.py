# -*- coding: utf-8 -*-

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
                            
                    if 'collect' in query['branch']:
                        for pattern in query['branch']['collect']:
                            try:
                                related = self.resolver.resolve(pattern.format(**query['parameter']))
                            except KeyError, e:
                                self.log.debug(u'Could not create reference uri for pattern %s because parameter %s was missing', pattern, e)
                                
                            if related is not None:
                                for index in query['branch']['index']:
                                    if index in related[u'head'][u'genealogy']:
                                        query['parameter'][index] = related[u'head'][u'genealogy'][index]
                                        
                                # we only need one of the documents in collect
                                break
                    query['source'].append(dependee)
    
    
    def parse(self, query):
        if query['source']:
            # Only create a new home document if the dependency is satisfied
            entry = {
                'branch':query['branch'],
                'record':{
                    u'head':{ u'genealogy':query['parameter'].project('ns.service.genealogy'), },
                }
            }
            
            query['result'].append(entry)
    

