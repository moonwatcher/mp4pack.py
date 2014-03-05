# -*- coding: utf-8 -*-

from datetime import datetime
from service import ResourceHandler
import json

class SystemHandler(ResourceHandler):
    def __init__(self, resolver, node):
        ResourceHandler.__init__(self, resolver, node)
        
    def fetch(self, query):
        if query['uri'] == '/s/runtime/archetype':
            query['sources'].append(self.env.archetype)
        elif query['uri'] == '/s/runtime/system':
            query['sources'].append(self.env.system)
        elif query['uri'] == '/s/runtime/enumeration':
            query['sources'].append(self.env.enumeration)
        elif query['uri'] == '/s/runtime/namespace':
            query['sources'].append(self.env.namespace)
        elif query['uri'] == '/s/runtime/rule':
            query['sources'].append(self.env.rule)
        elif query['uri'] == '/s/runtime/service':
            query['sources'].append(self.env.service)
        elif query['uri'] == '/s/runtime/expression':
            query['sources'].append(self.env.expression)
        elif query['uri'] == '/s/runtime/constant':
            query['sources'].append(self.env.constant)
        elif query['uri'] == '/s/runtime/command':
            query['sources'].append(self.env.command)
        elif query['uri'] == '/s/runtime/preset':
            query['sources'].append(self.env.preset)
        elif query['uri'] == '/s/runtime/repository':
            query['sources'].append(self.env.repository)
        elif query['uri'] == '/s/runtime/interface':
            query['sources'].append(self.env.interface)
        elif query['uri'] == '/s/runtime/subtitle':
            query['sources'].append(self.env.subtitle)
        elif query['uri'] == '/s/runtime/table':
            query['sources'].append(self.env.table)
            
    def parse(self, query):
        if query['branch']['name'] == 'service/collection/search':
            if query['parameter']['table handle'] in self.env.table:
                # locate the collection
                collection = query['repository'].database[self.env.table[query['parameter']['table handle']]['collection']]
                
                # prepare a return value
                query['return'] = { u'result count':0, u'results':[] }
                
                # prepare the query dictionary
                select = {}
                if query['location']:
                    for k,v in query['location'].iteritems():
                        select[u'head.genealogy.' + unicode(k)] = v
                        
                # collect the results
                cursor = collection.find(select)
                for r in cursor:
                    query['return']['results'].append(r)
                    
                # count the results
                query['return']['result count'] = len(query['return']['results'])
        else:
            if query['sources']:
                entry = {
                    'branch':query['branch'],
                    'record':{
                        u'head':{ u'genealogy':query['parameter'].project('ns.service.genealogy'), },
                        u'body':query['sources'][0],
                    }
                }
                query['return'] = entry['record']
                query['entires'].append(entry)
                

