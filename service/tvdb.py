# -*- coding: utf-8 -*-

from io import BytesIO
from StringIO import StringIO
from zipfile import BadZipfile, ZipFile
from xml.etree import  cElementTree as ElementTree
from urllib2 import Request, urlopen, URLError, HTTPError

from service import ResourceHandler
from ontology import Ontology

class TVDbHandler(ResourceHandler):
    def __init__(self, resolver, node):
        ResourceHandler.__init__(self, resolver, node)
        
        for branch in self.branch.values():
            branch['reference'] = []
            if 'produce' in branch:
                for ref in branch['produce']:
                    branch['reference'].append(self.branch[ref])
    
    
    def fetch(self, query):
        # Add TVDB api key to the parameter list
        query['parameter']['api key'] = self.node['api key']
        
        # calculate a remote url if the match specifies one
        if 'remote' in query['match']:
            query['remote url'] = query['match']['remote'].format(**query['parameter'])
            
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
                        # TVDB returns gzip encoded response or just plain xml
                        if 'content-encoding' in response.info() and response.info()['content-encoding'] == 'gzip':
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
                for branch in query['branch']['reference']:
                    ns = self.env.namespace[branch['namespace']]
                    entry = {
                        'branch':branch,
                        'record':{
                            u'head':{ u'genealogy':query['parameter'].project('ns.service.genealogy') },
                        }
                    }
                    
                    # Collect all elements of this type into a list
                    if ns.node['coalesce']:
                        entry['record'][u'body'] = []
                        
                        for node in element.findall(ns.node['tag']):
                            
                            # Build an ontology from each xml node that matches the tag
                            # and add it to the record's body
                            o = Ontology(self.env, branch['namespace'])
                            for item in node.getchildren():
                                o.decode(item.tag, item.text)
                            entry['record'][u'body'].append(o.node)
                            
                        if entry['record'][u'body']:
                            query['result'].append(entry)
                            
                    # Treat every element as an individual record
                    else:
                        for node in element.findall(ns.node['tag']):
                            
                            # Build an ontology from the xml node
                            # based on the declared namespace for the branch
                            o = Ontology(self.env, branch['namespace'])
                            for item in node.getchildren():
                                o.decode(item.tag, item.text)
                                
                            # Augment the genealogy with stuff from the ontology
                            if 'index' in branch:
                                for index in branch['index']:
                                    if index in o:
                                        entry['record'][u'head'][u'genealogy'][index] = o[index]
                                        
                            # Set the ontology's node as the record's body
                            entry['record'][u'body'] = o.node
                            query['result'].append(entry)
    

