# -*- coding: utf-8 -*-

from io import BytesIO
from StringIO import StringIO
from xml.etree import  cElementTree as ElementTree
from urllib2 import Request, urlopen, URLError, HTTPError

class TVDbHandler(ResourceHandler):
    def __init__(self, node):
        ResourceHandler.__init__(self, node)
    
    
    def fetch(self, query):
        self.log.debug(u'Retrieve %s', query['remote url'])
        request = Request(query['remote url'])
        
        try:
            response = urlopen(request)
        except HTTPError, e:
            self.log.warning(u'Server returned an error when requesting %s: %s', query['remote url'], e.code)
        except URLError, e:
            self.log.warning(u'Could not reach server when requesting %s: %s', query['remote url'], e.reason)
        else:
            if query['type'] == 'xml':
                try:
                    query['stream'].append(StringIO(response.read()))
                except Error:
                    self.log.warning(u'Failed to load document %s', query['remote url'])
                    
            elif query['type'] == 'zip':
                try:
                    bytes = BytesIO(response.read())
                    archive = zipfile.ZipFile(bytes)
                except Error:
                    self.log.warning(u'Failed to decode zip archive %s', query['remote url'])
                else:
                    for filename in archive.namelist():
                        try:
                            query['stream'].append(StringIO(archive.open(filename, 'rU')))
                        except Error:
                            self.log.warning(u'Failed to load document %s from archive %s', filename, query['remote url'])
                    archive.close()
                    bytes.close()
    
    
    def parse(self, query):
        for stream in query['stream']:
            try:
                element = ElementTree.parse(stream)
            except SyntaxError:
                self.log.warning(u'Failed to decode xml document %s', query['remote url'])
            else:
                for namespace, space in self.spaces.iteritems():
                    branch = self.branch[namespace]
                    if space.node['coalesce']:
                        entry = {
                            u'host':query['parameter']['host'],
                            u'namespace':namespace,
                            u'uri':branch['uri pattern'].format(**query['parameter']),
                            u'document':[],
                        }
                        
                        if 'index' in branch:
                            for index in branch['index']:
                                if index in query['parameter']:
                                    entry[index] = query['parameter'][index]
                                    
                        for node in element.findall(space.node['tag']):
                            o = Ontology(self.env)
                            for item in node.getchildren():
                                prototype = space.search(item.tag)
                                if prototype:
                                    o[prototype.key] = prototype.cast(item.txt)
                            entry[u'document'].append(o.node)
                        query['result'].append(entry)
                        
                    else:
                        for node in element.findall(space.node['tag']):
                            o = Ontology(self.env)
                            for item in node.getchildren():
                                prototype = space.search(item.tag)
                                if prototype:
                                    o[prototype.key] = prototype.cast(item.txt)
                            entry = {
                                u'namespace':namespace,
                                u'uri':branch['uri pattern'].format(**o.node),
                                u'document':o.node,
                            }
                            
                            if 'index' in branch:
                                for index in branch['index']:
                                    if index in o:
                                        entry[index] = o[index]
                                        
                            query['result'].append(entry)
                            
        for entry in query['result']:
            self.store(entry)
    


