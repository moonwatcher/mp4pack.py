# -*- coding: utf-8 -*-

import json
import os
from StringIO import StringIO
from urllib2 import Request, urlopen, URLError, HTTPError

from service import ResourceHandler
from ontology import Ontology

def satisfies(dictionary, condition):
    return all((k in dictionary and dictionary[k] == v) for k,v in condition.iteritems())

class iTunesHandler(ResourceHandler):
    def __init__(self, resolver, node):
        ResourceHandler.__init__(self, resolver, node)
        
        for branch in self.branch.values():
            if 'produce' in branch:
                for product in branch['produce']:
                    product['branch'] = self.branch[product['reference']]    
    
    def parse(self, query):
        for source in query['sources']:
            try:
                document = json.load(source)
            except ValueError, e:
                self.log.warning(u'Failed to decode JSON document %s', query['remote url'])
                self.log.debug(u'Exception raised %s', unicode(e))
            else:
                if 'process' in query['branch']:
                    # Preprocessing the entry.
                    # Method should return a document similar to normal itunes api calls
                    action = getattr(self, query['branch']['process'], None)
                    if action is not None:
                        document = action(document)
                    else:
                        self.log.warning(u'Ignoring unknown process function %s', query['branch']['process'])
                        
                if not document['resultCount'] > 0:
                    self.log.debug(u'No results found for query %s', query['remote url'])
                else:
                    if query['branch']['query type'] == 'lookup':
                        for element in document['results']:
                            for product in query['branch']['produce']:
                                if satisfies(element, product['condition']):
                                    
                                    entry = {
                                        'branch':product['branch'],
                                        'record':{
                                            u'head':{ u'genealogy':Ontology(self.env, 'ns.service.genealogy'), },
                                            u'body':{ u'original':element },
                                        }
                                    }
                                    
                                    # make a caonical node
                                    entry['record']['body']['canonical'] = Ontology(self.env, entry['branch']['namespace'])
                                    entry['record']['body']['canonical'].decode_all(entry['record']['body']['original'], self.name)
    
                                    # Copy indexed values from the canonical node to the genealogy
                                    if 'index' in entry['branch']:
                                        for index in entry['branch']['index']:
                                            if index in entry['record']['body']['canonical']:
                                                entry['record'][u'head'][u'genealogy'][index] = entry['record']['body']['canonical'][index]
                                                
                                    # Only produce once for each element
                                    query['entires'].append(entry)
                                    break
                    
                    
                    elif query['branch']['query type'] == 'search':
                        for trigger in query['branch']['trigger']:
                            for element in document['results']:
                                if satisfies(element, trigger['condition']):
                            
                                    # Decode concepts from the element and populate the ontology
                                    o = Ontology(self.env, trigger['namespace'])
                                    o.decode_all(element, self.name)
                                        
                                    # Make a URI and trigger a resolution
                                    ref = o.project('ns.service.genealogy')
                                    ref['language']
                                    uri = trigger['format'].format(**ref)
                                    self.log.debug(u'Trigger %s resolution', uri)
                                    self.resolver.resolve(uri)
    
    
    def parse_itunes_genres(self, document):
        def _recursive_parse_itunes_genres(node, parent=None):
            result = []
            if node:
                for key,element in node.iteritems():
                    try:
                        geID = int(key)
                    except ValueError, e:
                        self.log.warning(u'Invalid genre id %s', key)
                    else:
                        record = dict([(k,v) for k,v in element.iteritems() if not k == 'subgenres'])
                        record['kind']= 'genre'
                        if parent:
                            record['parentGenreId'] = parent
                        result.append(record)
                        
                        if 'subgenres' in element and element['subgenres']:
                            result.extend(_recursive_parse_itunes_genres(element['subgenres'], geID))
            return result
        
        
        result = { 'results':_recursive_parse_itunes_genres(document) }
        result['resultCount'] = len(result['results'])
        return result
