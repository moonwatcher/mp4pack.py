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
    
    def fetch(self, query):
        if 'remote url' in query:
            request = Request(query['remote url'], None, {'Accept': 'application/json'})
            self.log.debug(u'Fetching %s', query['remote url'])
            
            try:
                response = urlopen(request)
            except HTTPError, e:
                self.log.warning(u'Server returned an error when requesting %s: %s', query['remote url'], e.code)
            except URLError, e:
                self.log.warning(u'Could not reach server when requesting %s: %s', query['remote url'], e.reason)
            else:
                query['source'].append(StringIO(response.read()))
    
    
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
                                
                                # Initialize the genealogy by projecting the query parameter space on the ns.service.genealogy namespace
                                # This will get rid of the api key
                                entry = {
                                    'branch':product['branch'],
                                    'record':{
                                        u'head':{ u'genealogy':query['parameter'].project('ns.service.genealogy'), },
                                        u'body':{ u'original':element },
                                    }
                                }
                                
                                # Use the decalred namespace for the branch to decode stuff 
                                # from the document and augment the genealogy
                                ns = self.env.namespace[entry['branch']['namespace']]
                                if 'index' in query['branch']:
                                    for index in query['branch']['index']:
                                        prototype = ns.find(index)
                                        if prototype and prototype.node['itunes'] in element:
                                            entry['record'][u'head'][u'genealogy'][index] = prototype.cast(element[prototype.node['itunes']])
                                            
                                # make a caonical node
                                canonical = Ontology(self.env, entry['branch']['namespace'])
                                canonical.decode_all(element, 'itunes')
                                entry['record']['body']['canonical'] = canonical.node
                                query['result'].append(entry)
    
        
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
                            
    


