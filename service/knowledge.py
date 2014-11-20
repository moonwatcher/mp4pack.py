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
                        except KeyError as e:
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
                        u'body':{u'canonical':None, u'original':None},
                    }
                }
                
                entry['record']['body']['canonical'] = Ontology(self.env, entry['branch']['namespace'])
                for source in query['sources']:
                    if 'body' in source and 'canonical' in source['body'] and source['body']['canonical']:
                        entry['record']['body']['canonical'].merge_all(Ontology(self.env, entry['branch']['namespace'], source['body']['canonical']))
                        
                self.expand(entry['record']['body']['canonical'])
                query['entires'].append(entry)
                
    def expand(self, ontology):
        def discover(o):
            for k,v in o.iteritems():
                prototype = o.namespace.find(k)
                if prototype and prototype.type == 'embed':
                    discovered.append({'prototype':prototype, 'ontology':o[k]})
                    
        # start a queue
        discovered = []
        
        # discover the root ontology
        discover(ontology)
        
        while discovered:
            node = discovered.pop(0)
            if node['prototype'] is not None:
                if node['prototype'].plural is None:
                    discover(node['ontology'])
                    
                elif node['prototype'].plural == 'list':
                    for i,e in enumerate(node['ontology']):
                        h = e.project('ns.service.genealogy')
                        if h['home uri']:
                            home = self.resolver.resolve(h['home uri'])
                            if home is not None:
                                e.merge_all(Ontology(self.env, 'ns.service.genealogy', home['head']['genealogy']))
                                if e['knowledge uri']:
                                    knowledge = self.resolver.resolve(e['knowledge uri'])
                                    if knowledge is not None:
                                        e.merge_all(Ontology(self.env, node['prototype'].node['namespace'], knowledge['body']['canonical']))
                        discover(e)
                
