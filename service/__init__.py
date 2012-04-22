# -*- coding: utf-8 -*-

import re
import logging
import copy
import json
from datetime import datetime
from ontology import Ontology
from pymongo import json_util
from bson.objectid import ObjectId

class Resolver(object):
    def __init__(self, env):
        self.log = logging.getLogger('Resolver')
        self.env = env
        self.handlers = {}
        
        self.log.debug(u'Starting resolver')
        
        from tmdb import TMDbHandler
        self.handlers['tmdb'] = TMDbHandler(self, self.env.service['tmdb'])
        
        from tvdb import TVDbHandler
        self.handlers['tvdb'] = TVDbHandler(self, self.env.service['tvdb'])
    
    
    def resolve(self, uri, location=None):
        result = None
        for handler in self.handlers.values():
            match = handler.match(uri)
            if match is not None:
                parsed = match.groupdict()
                if parsed['host'] in self.env.repository:
                    result = handler.resolve(parsed['relative'], self.env.repository[parsed['host']], location)
                break
        return result
    
    
    def remove(self, uri):
        for handler in self.handlers.values():
            match = handler.match(uri)
            if match is not None:
                parsed = match.groupdict()
                if parsed['host'] in self.env.repository:
                    handler.remove(parsed['relative'], self.env.repository[parsed['host']])
                break
    
    
    def save(self, node):
        for handler in self.handlers.values():
            for uri in node['head']['uri']:
                match = handler.match(uri)
                if match is not None:
                    parsed = match.groupdict()
                    if parsed['host'] in self.env.repository:
                        handler.save(node, self.env.repository[parsed['host']])
                    break
    
    
    def issue(self, host, name):
        result = None
        if host in self.env.repository:
            repository = self.env.repository[host]
            issued = repository.database.counters.find_and_modify(query={u'_id':name}, update={u'$inc':{u'next':1}, u'$set':{u'modified':datetime.now()}}, new=True, upsert=True)
            if issued is not None:
                self.log.debug(u'New key %d issued for key pool %s', issued[u'next'], issued[u'_id'])
                result = issued[u'next']
        return result
    


class ResourceHandler(object):
    def __init__(self, resolver, node):
        self.log = logging.getLogger('Resolver')
        self.resolver = resolver
        self.node = node
        self.pattern = re.compile(self.node['match'])
        self.branch = {}
        
        for name, branch in self.node['branch'].iteritems():
            if 'namespace' in branch:
                branch['name'] = name
                branch['persistant'] = 'collection' in branch
                for match in branch['match']:
                    match['pattern'] = re.compile(match['filter'])
                self.branch[name] = branch
    
    
    @property
    def env(self):
        return self.resolver.env
    
    
    @property
    def name(self):
        return self.node['name']
    
    
    def match(self, uri):
        return self.pattern.search(uri)
    
    
    def resolve(self, uri, repository, location):
        result = None
        taken = False
        for branch in self.branch.values():
            for match in branch['match']:
                m = match['pattern'].search(uri)
                if m is not None:
                    taken = True
                    if branch['persistant']:
                        collection = repository.database[branch['collection']]
                        result = collection.find_one({u'head.uri':uri})
                        
                        # If record does not exists try to produce it and lookup again
                        if result is None:
                            self.produce(uri, repository, location)
                            result = collection.find_one({u'head.uri':uri})
                    break
            if taken: break
        return result
    
    
    def produce(self, uri, repository, location):
        taken = False
        for branch in self.branch.values():
            for match in branch['match']:
                m = match['pattern'].search(uri)
                if m is not None:
                    query = {
                        'repository':repository,
                        'location':location,
                        'branch':branch,
                        'uri':uri,
                        'parameter':None,
                        'stream':[],
                        'result':[],
                    }
                    
                    # parse the parameters from the uri
                    query['parameter'] = Ontology(self.env, branch['namespace'])
                    for k,v in m.groupdict().iteritems():
                        query['parameter'].decode(k,v)
                        
                    # add an api key if one is specified for the handler
                    if 'api key' in self.node:
                        query['parameter']['api key'] = self.node['api key']
                        
                    # calculate a remote url if the match specifies one
                    if 'remote' in match:
                        query['remote url'] = match['remote'].format(**query['parameter'])
                        
                    self.fetch(query)
                    self.parse(query)
                    self.store(query)
                    break
    
    
    def store(self, query):
        for entry in query['result']:
            record = None
            collection = query['repository'].database[entry['branch']['collection']]
            
            # Build all the resolvable URIs
            entry[u'head'][u'uri'] = []
            for resolvable in entry['branch']['resolvable']:
                try:
                    entry[u'head']['uri'].append(resolvable['format'].format(**entry['parameter']))
                except KeyError, e:
                    self.log.debug(u'Could not create uri for %s because %s was missing', resolvable['name'], e)
                    
            # set the modified date
            entry[u'head'][u'modified'] = datetime.utcnow()
            
            # try to locate an existing record
            for uri in entry[u'head'][u'uri']:
                record = collection.find_one({u'head.uri':uri})
                if record is not None:
                    break
                    
            if record is not None:
                # This is an update, we already have an existing record
                for k,v in entry['head']:
                    record[u'head'][k] = v
            else:
                # This is an insert, no previous existing record was found
                record = { u'head':entry[u'head'] }
                record[u'head'][u'created'] = record[u'head'][u'modified']
                
                # issue a new id if a generator is specified,
                # otherwise create a new mongodb ObjectId
                if 'key generator' in entry['branch']:
                    record['_id'] = self.resolver.issue(query['repository'].host, entry['branch']['key generator'])
                else:
                    record['_id'] = ObjectId()
                    
            # update the record's body
            record[u'body'] = entry[u'body']
            
            # save the record to database
            self.log.debug(u'Storing %s', unicode(record[u'head']))
            collection.save(record)
    
    
    def remove(self, uri, repository):
        taken = False
        for branch in self.branch.values():
            for match in branch['match']:
                m = match['pattern'].search(uri)
                if m is not None:
                    taken = True
                    if branch['persistant']:
                        self.log.debug(u'Dropping %s', uri)
                        collection = repository.database[branch['collection']]
                        collection.remove({u'head.uri':uri})
                    break
            if taken: break
    
    
    def save(self, node, repository):
        result = None
        taken = False
        for branch in self.branch.values():
            for uri in node['head']['uri']:
                for match in branch['match']:
                    m = match['pattern'].search(uri)
                    if m is not None:
                        taken = True
                        if branch['persistant']:
                            collection = repository.database[branch['collection']]
                            result = collection.find_one({u'head.uri':uri})
                            if result is not None: break
                if result is not None: break
                
            if taken:
                now = datetime.utcnow()
                if result is None:
                    result = { u'head':{ u'created':now, }, }
                result[u'body'] = node[u'body']
                
                # always update the modified field
                result[u'head'][u'modified'] = now
                
                # save the entry to db
                collection.save(result)
                break
        return result
    
    
    def fetch(self, query):
        pass
    
    
    def parse(self, query):
        pass
    
    

