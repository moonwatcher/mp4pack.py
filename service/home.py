# -*- coding: utf-8 -*-

from service import ResourceHandler

class HomeHandler(ResourceHandler):
    def __init__(self, resolver, node):
        ResourceHandler.__init__(self, resolver, node)
    
    
    def fetch(self, query):
        if 'depend' in query['match']:
            
            # ensure default language
            query['parameter']['language']
            
            # fetch dependencies
            for dependency in query['match']['depend']:
                document = self.resolver.resolve(dependency.format(**query['parameter']))
                if document is not None:
                    query['source'].append(document)
    
    
    def parse(self, query):
        entry = {
            'branch':query['branch'],
            'record':{
                u'head':{ u'genealogy':query['parameter'].project('ns.service.genealogy'), },
                u'body':None,
            }
        }
        
        # Collect concepts from the genealogy in the head of source documents
        if 'index' in query['branch']:
            for source in query['source']:
                for index in query['branch']['index']:
                    if index in source[u'head'][u'genealogy']:
                        entry['record'][u'head'][u'genealogy'][index] = source[u'head'][u'genealogy'][index]
                        
        # Issue a new id if a generator is specified
        if 'generate' in entry['branch']:
            entry['record'][u'head'][u'genealogy'][entry['branch']['generate']['key']] = self.resolver.issue(query['repository'].host, entry['branch']['generate']['name'])
            
        query['result'].append(entry)
    

