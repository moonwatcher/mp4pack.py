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
        for source in query['source']:
            try:
                document = json.load(source)
            except ValueError, e:
                self.log.warning(u'Failed to decode JSON document %s', query['remote url'])
                self.log.debug(u'Exception raised %s', unicode(e))
            else:
                if 'process' in query['branch']:
                
                    # locate a method that implements the action
                    action = getattr(self, query['branch']['process'], None)
                    if action is not None:
                        document = {'results':action(document)}
                        document['resultCount'] = len(document['results'])
                    else:
                        self.log.warning(u'Ignoring unknown process function %s', query['branch']['process'])
                        
                if not document['resultCount'] > 0:
                    self.log.warning(u'No results found for query %s', query['remote url'])
                else:
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
                                canonical = Ontology(self.env, entry['branch']['namespace'])
                                canonical.decode_all(element, 'itunes')
                                entry['record']['body']['canonical'] = canonical.node
                                query['result'].append(entry)
                                
                                # Copy indexed values from the canonical node to the genealogy
                                if 'index' in query['branch']:
                                    for index in query['branch']['index']:
                                        if index in canonical:
                                            entry['record'][u'head'][u'genealogy'][index] = canonical[index]
                                
                                
                                # Only produce once for each element
                                break
    
        
    def parse_itunes_genres(self, document, parent=None):
        result = []
        if document:
            for key,element in document.iteritems():
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
                        result.extend(self.parse_itunes_genres(element['subgenres'], geID))
        return result
                            
    


