# -*- coding: utf-8 -*-

import re
import logging

from ontology import Ontology

class Resolver(object):
    def __init__(self, env):
        self.log = logging.getLogger('Resolver')
        self.env = env
        self.handlers = {}
        self.pool = {}
        
        from tmdb import TMDbHandler
        self.handlers['tmdb'] = TMDbHandler(self, self.env.service['tmdb'])
        
        from tvdb import TVDbHandler
        self.handlers['tvdb'] = TVDbHandler(self, self.env.service['tvdb'])
    
    
    def open(self):
        self.log.debug(u'Starting resolver')
    
    
    def close(self):
        for handle in self.pool.values():
            handle.close()
    
    
    def find_database_handle(self, host):
        result = None
        if host in self.pool:
            result = self.pool[host]
        else:
            result = MongoConnection(self.env, host)
            self.pool[host] = result
            result.open()
        return result
    
    
    def remove(self, uri):
        for handler in self.handlers:
            if handler.match(uri):
                handler.remove(uri)
                break
    
    
    def resolve(self, uri):
        result = None
        for handler in self.handlers:
            if handler.match(uri):
                result = handler.resolve(uri)
                break
                
        return result
    


class MongoConnection(object):
    def __init__(self, env, host):
        self.log = logging.getLogger('mongodb')
        self.env = env
        self.ontology = None
        self.connection = None
        self.database = None
        
        if host in self.env.repository and \
        'mongodb' in self.env.repository[host]:
            self.ontology = Ontology(self.env.repository[host]['mongodb'])
    
    
    def open(self):
        if self.ontology and 'mongodb url' in self.ontology:
            try:
                self.log.debug(u'Connecting to %s', self.ontology['mongodb url'])
                self.connection = pymongo.Connection(self.ontology['mongodb url'])
            except pymongo.errors.AutoReconnect as err:
                self.log.warning(u'Failed to connect to %s', self.ontology['mongodb url'])
                self.log.debug(u'Exception raised: %s', err)
            else:
                self.log.debug(u'Connection established with %s', self.ontology['host'])
                self.database = self.connection[self.ontology['database']]
    
    
    def close(self):
        self.log.debug(u'Closing mongodb connection to %s', self.ontology['host'])
        self.connection.close()
    


class ResourceHandler(object):
    def __init__(self, resolver, node):
        self.resolver = resolver
        self.node = node
        self.pattern = re.compile(self.node['match'])
        self.branch = {}
        
        for namespace, branch in self.node['branch'].iteritems():
            branch['namespace'] = namespace
            branch['pattern'] = re.compile(branch['match'])
            self.branch[namespace] = branch
    
    
    @property
    def env(self):
        return self.resolver.env
    
    
    @property
    def name(self):
        return self.node['name']
    
    
    @property
    def spaces(self):
        return self.env.prototype[self.name]
    
    
    def resolve(self, uri):
        result = None
        for branch in self.branch:
            match = self.branch['pattern'].search(uri)
            # Only branches with a collection definition are resolvable
            if match is not None and 'collection' in branch:
                param = match.groupdict()
                if 'host' in param:
                    handle = self.resolver.find_database_handle(param['host'])
                    if handle:
                        collection = handle.database[branch['collection']]
                        result = collection.find_one({u'uri':uri})
                        if result is None:
                            self.cache(uri)
                            result = collection.find_one({u'uri':uri})
                break
        return result
    
    
    def cache(self, uri):
        if uri:
            for branch in self.branch.values():
                match = self.branch['pattern'].search(uri)
                if match is not None:
                    query = {
                        'namespace':branch['namespace'],
                        'uri':uri,
                        'type':branch['type'],
                        'parameter':{},
                        'result':{},
                        'stream':{},
                    }
                    
                    if 'api key' in self.node:
                        query['api key'] = self.node['api key']
                        
                    # extract and cast parameters
                    if 'space' in branch and branch['space'] in self.spaces:
                        space = self.spaces[branch['space']]
                        for k,v in match.groupdict().iteritems():
                            prototype = space.search(k)
                            query['parameter'][prototype.key] = prototype.cast(v)
                            
                    if 'remote' in branch:
                        query['remote url'] = branch['remote'].format(**query['parameter'])
                        
                    self.fetch(query)
                    self.parse(query)
                    break
    
    
    def remove(self, uri):
        for branch in self.branch.values():
            match = self.branch['pattern'].search(uri)
            if match is not None and 'collection' in branch:
                param = match.groupdict()
                if 'host' in param:
                    handle = self.resolver.find_database_handle(param['host'])
                    if handle:
                        collection = handle.database[branch['collection']]
                        collection.remove({u'uri':uri})
                break
    
    
    def store(self, entry):
        if entry and 'uri' in entry and 'host' in entry and \
        'namespace' in entry and entry['namespace'] in self.branch:
            branch = self.branch[entry['namespace']]
            if 'collection' in branch:
                handle = self.resolver.find_database_handle(entry['host'])
                if handle:
                    collection = handle.database[branch['collection']]
                    current = collection.find_one({u'uri':entry[u'uri']})
                    now = datetime.utcnow()
                    if current is None:
                        current = entry
                        current[u'created'] = now
                    else:
                        current[u'document'] = entry[u'document']
                        
                    current['modified'] = now
                    collection.save(current)
    
    
    def match(self, uri):
        return self.pattern.match(uri)
    
    
    def fetch(self, query):
        pass
    
    
    def parse(self, query):
        pass
    
    

