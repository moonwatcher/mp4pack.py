# -*- coding: utf-8 -*-

import os
from io import BytesIO
from StringIO import StringIO
import gzip
from zipfile import BadZipfile, ZipFile
from xml.etree import  cElementTree as ElementTree
from urllib2 import Request, urlopen, URLError, HTTPError

from service import ResourceHandler
from ontology import Ontology

def xml_to_dictionary(element):
    node = {}
    if element is not None:
        for child in element:
            if child:
                if not child.tag in node:
                    node[child.tag] = []
                node[child.tag].append(xml_to_dictionary(child))
                
            else:
                node[child.tag] = child.text
    return node

class TVDbHandler(ResourceHandler):
    def __init__(self, resolver, node):
        ResourceHandler.__init__(self, resolver, node)
        
        for branch in self.branch.values():
            if 'produce' in branch:
                for product in branch['produce']:
                    product['branch'] = self.branch[product['reference']]
                    
    def fetch(self, query):
        if 'remote url' in query:
            request = Request(query['remote url'])
            self.log.debug(u'Fetching %s', query['remote url'])
            
            try:
                response = urlopen(request)
            except HTTPError, e:
                self.log.warning(u'Server returned an error when requesting %s: %s', query['remote url'], e.code)
            except URLError, e:
                self.log.warning(u'Could not reach server when requesting %s: %s', query['remote url'], e.reason)
            else:
                if query['branch']['type'] == 'xml':
                    try:
                        # TVDB returns xml that is sometimes gzip encoded
                        if 'content-encoding' in response.info() and response.info()['content-encoding'] == 'gzip':
                            self.log.debug(u'Got gzip encoded response from server when fetching %s', query['remote url'])
                            query['sources'].append(StringIO(gzip.GzipFile(fileobj=BytesIO(response.read())).read()))
                        else:
                            query['sources'].append(StringIO(response.read()))
                    except Exception:
                        self.log.warning(u'Failed to load document %s', query['remote url'])
                    
                elif query['branch']['type'] == 'zip':
                    try:
                        bytes = BytesIO(response.read())
                    except IOError, e:
                        self.log.warning(u'Failed to read source from archive %s', query['remote url'])
                        self.log.debug(u'Exception raised %s', unicode(e))
                    else:
                        try:
                            archive = ZipFile(bytes)
                        except BadZipfile, e:
                            self.log.warning(u'Failed to decode zip archive %s', query['remote url'])
                            self.log.debug(u'Exception raised %s', unicode(e))
                            bytes.close()
                        else:
                            for filename in archive.namelist():
                                try:
                                    query['sources'].append(StringIO(archive.open(filename, 'rU').read()))
                                except Exception:
                                    self.log.warning(u'Failed to load document %s from archive %s', filename, query['remote url'])
                            archive.close()
                            bytes.close()
                            
    def parse(self, query):
        for source in query['sources']:
            try:
                document = xml_to_dictionary(ElementTree.parse(source).getroot())
            except SyntaxError, e:
                self.log.warning(u'Failed to decode xml document %s', query['remote url'])
                self.log.warning(u'Exception raised %s', unicode(e))
            else:
                if query['branch']['query type'] == 'lookup':
                    for product in query['branch']['produce']:
                        if product['tag'] in document:
                            if product['coalesce']:
                                # Coalescing records all collect under a single document
                                # i.e. images and cast for a show
                                entry = {
                                    'branch':product['branch'],
                                    'record':{
                                        u'head':{ u'genealogy':query['parameter'].project('ns.service.genealogy') },
                                        u'body':{ u'original':{ product['tag']:document[product['tag']] } },
                                    }
                                }
                                
                                # make a caonical node
                                entry['record']['body']['canonical'] = Ontology(self.env, entry['branch']['namespace'])
                                entry['record']['body']['canonical'].decode_all(entry['record']['body']['original'], self.name)
                                query['entires'].append(entry)
                                
                            else:
                                batch = []
                                for element in document[product['tag']]:
                                    entry = {
                                        'branch':product['branch'],
                                        'record':{
                                            u'head':{ u'genealogy':query['parameter'].project('ns.service.genealogy') },
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
                                                
                                    batch.append(entry)
                                    
                                # TVDB does not explicitly resolve TV seasons, however, it does assign them an id.
                                # When processing episodes we deduce the existence of a season
                                # Seasons are added to the query results before the episodes
                                if batch and product['branch']['name'] == 'service.document.tvdb.tv.episode':
                                    
                                    # Collect all the referenced seasons in the episodes
                                    # Make sure we only create every season once
                                    seasons = {}
                                    for entry in batch:
                                        episode = entry['record'][u'head'][u'genealogy']
                                        if episode['tvdb tv season id'] not in seasons:
                                            seasons[episode['tvdb tv season id']] = \
                                                episode.project('ns.knowledge.tv.season').project('ns.service.genealogy')
                                                
                                    # Make an entry for every season we find
                                    for season in seasons.values():
                                        query['entires'].append(
                                            {
                                                'branch':self.branch['service.document.tvdb.tv.season'],
                                                'record':{ u'head':{ u'genealogy':season }, }
                                            }
                                        )
                                        
                                # Add the entries in the batch to the query results
                                query['entires'].extend(batch)
                                
                elif query['branch']['query type'] == 'search':
                    for trigger in query['branch']['trigger']:
                        if trigger['tag'] in document:
                            for element in document[trigger['tag']]:
                                # Decode concepts from the element and populate the ontology
                                o = Ontology(self.env, trigger['namespace'])
                                o.decode_all(element, self.name)
                                
                                # Make a URI and trigger a resolution
                                ref = o.project('ns.service.genealogy')
                                ref['language']
                                uri = trigger['format'].format(**ref)
                                self.log.debug(u'Trigger %s resolution', uri)
                                self.resolver.resolve(uri)
                                

