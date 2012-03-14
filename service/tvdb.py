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
    
    
    def fetch(self, query, handle):
        self.log.debug(u'Retrieve %s', query['remote url'])
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
                    query['stream'].append(StringIO(response.read()))
                except Exception:
                    self.log.warning(u'Failed to load document %s', query['remote url'])
                    
            elif query['branch']['type'] == 'zip':
                try:
                    bytes = BytesIO(response.read())
                    archive = ZipFile(bytes)
                except BadZipfile, e:
                    self.log.warning(u'Failed to decode zip archive %s', query['remote url'])
                    self.log.debug(u'Exception raised %s', unicode(e))
                else:
                    for filename in archive.namelist():
                        try:
                            query['stream'].append(StringIO(archive.open(filename, 'rU').read()))
                        except Exception:
                            self.log.warning(u'Failed to load document %s from archive %s', filename, query['remote url'])
                    archive.close()
                    bytes.close()
    
    
    def parse(self, query, handle):
        for stream in query['stream']:
            try:
                element = ElementTree.parse(stream)
            except SyntaxError, e:
                self.log.warning(u'Failed to decode xml document %s', query['remote url'])
                self.log.warning(u'Exception raised %s', unicode(e))
            else:
                for branch in query['branch']['reference']:
                    ns = self.namespaces[branch['namespace']]
                    if ns.node['coalesce']:
                        entry = {
                            u'collection':branch['collection'],
                            u'uri':branch['uri pattern'].format(**query['parameter']),
                            u'document':[],
                        }
                        
                        # update index
                        if 'index' in branch:
                            entry[u'index'] = {}
                            for index in branch['index']:
                                if index in query['parameter']:
                                    entry[u'index'][index] = query['parameter'][index]
                                    
                        for node in element.findall(ns.node['tag']):
                            o = Ontology(self.env)
                            for item in node.getchildren():
                                prototype = ns.search(item.tag)
                                if prototype:
                                    o[prototype.key] = prototype.cast(item.text)
                            entry[u'document'].append(o.node)
                            
                        if entry[u'document']:
                            query['result'].append(entry)
                    else:
                        for node in element.findall(ns.node['tag']):
                            o = Ontology(self.env)
                            for item in node.getchildren():
                                prototype = ns.search(item.tag)
                                if prototype:
                                    o[prototype.key] = prototype.cast(item.text)
                                    
                            entry = {
                                u'collection':branch['collection'],
                                u'uri':branch['uri pattern'].format(**o.node),
                                u'document':o.node,
                            }
                            
                            # update index
                            if 'index' in branch:
                                entry[u'index'] = {}
                                for index in branch['index']:
                                    if index in o:
                                        entry[u'index'][index] = o[index]
                                        
                            query['result'].append(entry)
    

