# -*- coding: utf-8 -*-

import json
import os
from StringIO import StringIO
from urllib2 import Request, urlopen, URLError, HTTPError
from service import ResourceHandler
from ontology import Ontology

class TMDbHandler(ResourceHandler):
    def __init__(self, resolver, node):
        ResourceHandler.__init__(self, resolver, node)
    
    
    def parse(self, query):
        for source in query['source']:
            try:
                document = json.load(source)
            except ValueError, e:
                self.log.warning(u'Failed to decode JSON document %s', query['remote url'])
                self.log.debug(u'Exception raised %s', unicode(e))
            else:
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
                    query['result'].append(entry)

                elif query['branch']['query type'] == 'search':
                    query['return'] = { u'result count':0, u'results':[], }
                    for result in document['results']:
                        for trigger in query['branch']['trigger']:
                            # Decode a reference
                            o = Ontology(self.env, trigger['namespace'])
                            o.decode_all(result, self.name)

                            # Make a URI and trigger a resolution
                            ref = o.project('ns.service.genealogy')
                            ref['language']
                            uri = trigger['format'].format(**ref)
                            self.log.debug(u'Trigger %s resolution', uri)
                            query['return']['results'].append(self.resolver.resolve(uri))
                    query['return']['result count'] = len(query['return']['results'])
    


