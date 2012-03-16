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
        self.databases = {}
    
    
    def open(self):
        self.log.debug(u'Starting resolver')
        
        from tmdb import TMDbHandler
        self.handlers['tmdb'] = TMDbHandler(self, self.env.service['tmdb'])
        
        from tvdb import TVDbHandler
        self.handlers['tvdb'] = TVDbHandler(self, self.env.service['tvdb'])
    
    
    def close(self):
        for database in self.databases.values():
            database.close()
    
    
    def find_database(self, host):
        result = None
        if host in self.databases:
            result = self.databases[host]
        else:
            result = Database(self.env, host)
            result.open()
            self.databases[host] = result
        return result
    
    
    def remove(self, uri):
        for handler in self.handlers.values():
            match = handler.match(uri)
            if match is not None:
                parsed = match.groupdict()
                db = self.find_database(parsed['host'])
                handler.remove(parsed['relative'], db)
                break
    
    
    def resolve(self, uri):
        result = None
        for handler in self.handlers.values():
            match = handler.match(uri)
            if match is not None:
                parsed = match.groupdict()
                db = self.find_database(parsed['host'])
                result = handler.resolve(parsed['relative'], db)
                break
        return result
    
    
    def cache(self, uri):
        for handler in self.handlers.values():
            match = handler.match(uri)
            if match is not None:
                parsed = match.groupdict()
                db = self.find_database(parsed['host'])
                handler.cache(parsed['relative'], db)
                break
    


class Database(object):
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
            for match in branch['match']:
                match['pattern'] = re.compile(match['filter'])
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
    
    
    def resolve(self, uri, db):
        result = None
        taken = False
        for branch in self.branch.values():
            for match in branch['match']:
                m = match['pattern'].search(uri)
                if m is not None:
                    taken = True
                    # Only branches with a collection definition are resolvable
                    if 'collection' in branch:
                        collection = db.database[branch['collection']]
                        result = collection.find_one({u'head.uri':uri})
                        
                        # If record does not exists proceed to caching it
                        if result is None:
                            self.cache(uri, db)
                            result = collection.find_one({u'head.uri':uri})
                    break
            if taken: break
        return result
    
    
    def remove(self, uri, db):
        taken = False
        for branch in self.branch.values():
            for match in branch['match']:
                m = match['pattern'].search(uri)
                if m is not None:
                    taken = True
                    # Only branches with a collection definition are resolvable
                    if 'collection' in branch:
                        self.log.debug(u'Dropping %s', uri)
                        collection = db.database[branch['collection']]
                        result = collection.remove({u'head.uri':uri})
                    break
            if taken: break
    
    
    def cache(self, uri, db):
        taken = False
        for branch in self.branch.values():
            for match in branch['match']:
                m = match['pattern'].search(uri)
                if m is not None:
                    query = {
                        'database':db,
                        'branch':branch,
                        'uri':uri,
                        'parameter':{},
                        'stream':[],
                        'result':[],
                    }
                    
                    # extract and cast parameters
                    if 'namespace' in branch:
                        ns = self.namespaces[branch['namespace']]
                        for k,v in m.groupdict().iteritems():
                            prototype = ns.search(k)
                            if prototype is not None:
                                query['parameter'][prototype.key] = prototype.cast(v)
                                
                    # calculate the remote url
                    if 'api key' in self.node:
                        query['parameter']['api key'] = self.node['api key']
                    query['remote url'] = match['remote'].format(**query['parameter'])
                    
                    self.fetch(query)
                    self.parse(query)
                    self.store(query)
                    break
    
    
    
    
    def fetch(self, query):
        pass
    
    
    def parse(self, query):
        pass
    
    
    def store(self, query):
        for entry in query['result']:
            entry[u'uri'] = []
            # build all the resolvable URIs
            for r in entry['branch']['resolvable']:
                try:
                    entry['uri'].append(r['format'].format(**entry['parameter']))
                except KeyError, e:
                    self.log.debug(u'Could not create uri for %s because %s was missing', r['name'], e)
                    
            collection = query['database'].database[entry['branch']['collection']]
            
            record = None
            now = datetime.utcnow()
            for uri in entry[u'uri']:
                record = collection.find_one({u'head.uri':uri})
                break
                
            if record is None: record = { u'head':{ u'created':now, }, }
            record[u'head'][u'uri'] = entry[u'uri']
            record[u'body'] = entry[u'body']
            
            # always update the modified field
            record[u'head'][u'modified'] = now
            
            # save the entry to db
            self.log.debug(u'Storing %s', uri)
            collection.save(record)
    

