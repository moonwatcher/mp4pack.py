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

class TVDbHandler(ResourceHandler):
    def __init__(self, resolver, node):
        ResourceHandler.__init__(self, resolver, node)
        
        for branch in self.branch.values():
            if 'produce' in branch:
                for product in branch['produce']:
                    product['branch'] = self.branch[product['reference']]
    
    
    def fetch(self, query):
        # Add TVDB api key to the parameter list
        query['parameter']['api key'] = self.node['api key']
        
        # calculate a remote url if the match specifies one
        if 'remote' in query['match']:
            query['remote url'] = os.path.join(self.node['remote base'], query['match']['remote'].format(**query['parameter']))
            
            self.log.debug(u'Fetching %s', query['remote url'])
            request = Request(query['remote url'])
            
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
                            query['source'].append(StringIO(gzip.GzipFile(fileobj=BytesIO(response.read())).read()))
                        else:
                            query['source'].append(StringIO(response.read()))
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
                                    query['source'].append(StringIO(archive.open(filename, 'rU').read()))
                                except Exception:
                                    self.log.warning(u'Failed to load document %s from archive %s', filename, query['remote url'])
                            archive.close()
                            bytes.close()
    
    
    def parse(self, query):
        for source in query['source']:
            try:
                element = ElementTree.parse(source)
            except SyntaxError, e:
                self.log.warning(u'Failed to decode xml document %s', query['remote url'])
                self.log.warning(u'Exception raised %s', unicode(e))
            else:
                for product in query['branch']['produce']:
                    if product['coalesce']:
                        # Coalescing records all collect under a single document
                        # i.e. images and cast for a show
                        entry = {
                            'branch':product['branch'],
                            'record':{
                                u'head':{ u'genealogy':query['parameter'].project('ns.service.genealogy') },
                                u'body':[],
                            }
                        }
                        for node in element.findall(product['tag']):
                            o = Ontology(self.env, product['branch']['namespace'])
                            for item in node.getchildren():
                                o.decode(item.tag, item.text, 'tvdb')
                            entry['record'][u'body'].append(o.node)
                            
                        if entry['record'][u'body']:
                            query['result'].append(entry)
                            
                    else:
                        batch = []
                        for node in element.findall(product['tag']):
                            
                            # Decode concepts from the element and populate the ontology
                            o = Ontology(self.env, product['branch']['namespace'])
                            for item in node.getchildren():
                                o.decode(item.tag, item.text, 'tvdb')
                                
                            entry = {
                                'branch':product['branch'],
                                'record':{
                                    u'head':{ u'genealogy':query['parameter'].project('ns.service.genealogy') },
                                    u'body':o,
                                }
                            }
                            
                            # Augment the genealogy with stuff from the ontology
                            if 'index' in product['branch']:
                                for index in product['branch']['index']:
                                    if index in o:
                                        entry['record'][u'head'][u'genealogy'][index] = o[index]
                                        
                            batch.append(entry)
                            
                        # TVDB does not explicitly define a tv season, however, it does assign it an id.
                        # When processing episodes we need to deduce the existence of a season
                        # The season record will be created before the episodes
                        if batch and product['branch']['name'] == 'service.remote.tvdb.episode':
                            seasons = {}
                            for entry in batch:
                                o = entry['record'][u'body']
                                if o['tvdb tv season id'] not in seasons:
                                    genealogy = Ontology(self.env, 'ns.service.genealogy')
                                    genealogy['tvdb tv season id'] = o['tvdb tv season id']
                                    genealogy['tvdb tv show id'] = o['tvdb tv show id']
                                    genealogy['disk position'] = o['disk position']
                                    genealogy['language'] = o['language']
                                    seasons[o['tvdb tv season id']] = genealogy
                            for genealogy in seasons.values():
                                query['result'].append(
                                    {
                                        'branch':self.branch['service.remote.tvdb.season'],
                                        'record':{
                                            u'head':{ u'genealogy':genealogy },
                                        }
                                    }
                                )
                                
                        # make an entry out of each ontology and append to the query result
                        for entry in batch:
                            entry['record'][u'body'] = entry['record'][u'body'].node
                            query['result'].append(entry)
    


