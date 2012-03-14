# -*- coding: utf-8 -*-

import re
import logging
import copy
import pymongo
from datetime import datetime
from ontology import Ontology

class Resolver(object):
    def __init__(self, env):
        self.log = logging.getLogger('Resolver')
        self.env = env
        self.handlers = {}
        self.pool = {}
    
    
    def open(self):
        self.log.debug(u'Starting resolver')
        
        from tmdb import TMDbHandler
        self.handlers['tmdb'] = TMDbHandler(self, self.env.service['tmdb'])
        
        from tvdb import TVDbHandler
        self.handlers['tvdb'] = TVDbHandler(self, self.env.service['tvdb'])
    
    
    def close(self):
        for handle in self.pool.values():
            handle.close()
    
    
    def find_database_handle(self, host):
        result = None
        if host in self.pool:
            result = self.pool[host]
        else:
            result = MongoConnection(self.env, host)
            result.open()
            self.pool[host] = result
        return result
    
    
    def remove(self, uri):
        for handler in self.handlers.values():
            match = handler.match(uri)
            if match is not None:
                parsed = match.groupdict()
                handle = self.find_database_handle(parsed['host'])
                handler.remove(parsed['relative'], handle)
                break
    
    
    def resolve(self, uri):
        result = None
        for handler in self.handlers.values():
            match = handler.match(uri)
            if match is not None:
                parsed = match.groupdict()
                handle = self.find_database_handle(parsed['host'])
                result = handler.resolve(parsed['relative'], handle)
                break
        return result
    
    
    def cache(self, uri):
        for handler in self.handlers.values():
            match = handler.match(uri)
            if match is not None:
                parsed = match.groupdict()
                handle = self.find_database_handle(parsed['host'])
                handler.cache(parsed['relative'], handle)
                break
    


class MongoConnection(object):
    def __init__(self, env, host):
        self.log = logging.getLogger('mongodb')
        self.env = env
        self.ontology = None
        self.connection = None
        self.database = None
        
        if host in self.env.repository and \
        'mongodb' in self.env.repository[host]:
            self.ontology = Ontology(self.env, self.env.repository[host]['mongodb'])
    
    
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
        self.log = logging.getLogger('Resolver')
        self.resolver = resolver
        self.node = node
        self.pattern = re.compile(self.node['match'])
        self.branch = {}
        
        for name, branch in self.node['branch'].iteritems():
            branch['name'] = name
            branch['pattern'] = re.compile(branch['match'])
            self.branch[name] = branch
    
    
    @property
    def env(self):
        return self.resolver.env
    
    
    @property
    def name(self):
        return self.node['name']
    
    
    @property
    def namespaces(self):
        return self.env.prototype[self.name]
    
    
    def match(self, uri):
        return self.pattern.search(uri)
    
    
    def resolve(self, uri, handle):
        result = None
        for branch in self.branch.values():
            match = branch['pattern'].search(uri)
            if match is not None:
                # Only branches with a collection definition are resolvable
                if 'collection' in branch:
                    collection = handle.database[branch['collection']]
                    result = collection.find_one({u'uri':uri})
                    
                    # If no record exists proceed to caching it
                    if result is None:
                        self.cache(uri, handle)
                        result = collection.find_one({u'uri':uri})
                break
        return result
    
    
    def remove(self, uri, handle):
        for branch in self.branch.values():
            match = branch['pattern'].search(uri)
            if match is not None:
                # Only branches with a collection definition are resolvable
                if 'collection' in branch:
                    collection = handle.database[branch['collection']]
                    result = collection.remove({u'uri':uri})
                break
    
    
    def cache(self, uri, handle):
        for branch in self.branch.values():
            match = branch['pattern'].search(uri)
            if match is not None:
                query = {
                    'branch':branch,
                    'uri':uri,
                    'parameter':{},
                    'stream':[],
                    'result':[],
                }
                
                # extract and cast parameters
                if 'namespace' in branch:
                    ns = self.namespaces[branch['namespace']]
                    for k,v in match.groupdict().iteritems():
                        prototype = ns.search(k)
                        if prototype is not None:
                            query['parameter'][prototype.key] = prototype.cast(v)
                            
                # calculate the remote url
                if 'remote' in branch:
                    if 'api key' in self.node:
                        query['parameter']['api key'] = self.node['api key']
                    query['remote url'] = branch['remote'].format(**query['parameter'])
                    
                self.fetch(query, handle)
                self.parse(query, handle)
                self.store(query, handle)
                break
    
    
    
    def store(self, query, handle):
        for entry in query['result']:
            collection = handle.database[entry['collection']]
            record = collection.find_one({u'uri':entry[u'uri']})
            now = datetime.utcnow()
            if record is None:
                record = {
                    u'uri':entry[u'uri'],
                    u'document':entry[u'document'],
                    u'created':now,
                }
            else:
                record[u'document'] = entry[u'document']
                
            # update index
            if 'index' in entry:
                for k,v in entry['index'].iteritems():
                    record[k] = v
                    
            # update the modified field
            record[u'modified'] = now
            
            # save the entry to db
            collection.save(record)
    
    
    def fetch(self, query, handle):
        pass
    
    
    def parse(self, query, handle):
        pass
    
    

