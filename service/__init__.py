# -*- coding: utf-8 -*-

import re
import logging
import copy
from datetime import datetime
from ontology import Ontology

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
    
    
    def remove(self, uri):
        for handler in self.handlers.values():
            match = handler.match(uri)
            if match is not None:
                parsed = match.groupdict()
                if parsed['host'] in self.env.repository:
                    handler.remove(parsed['relative'], self.env.repository[parsed['host']])
                break
    
    
    def resolve(self, uri):
        result = None
        for handler in self.handlers.values():
            match = handler.match(uri)
            if match is not None:
                parsed = match.groupdict()
                if parsed['host'] in self.env.repository:
                    result = handler.resolve(parsed['relative'], self.env.repository[parsed['host']])
                break
        return result
    
    
    def cache(self, uri):
        for handler in self.handlers.values():
            match = handler.match(uri)
            if match is not None:
                parsed = match.groupdict()
                if parsed['host'] in self.env.repository:
                    handler.cache(parsed['relative'], self.env.repository[parsed['host']])
                break
    


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
    
    
    def match(self, uri):
        return self.pattern.search(uri)
    
    
    def resolve(self, uri, repository):
        result = None
        taken = False
        for branch in self.branch.values():
            for match in branch['match']:
                m = match['pattern'].search(uri)
                if m is not None:
                    taken = True
                    # Only branches with a collection definition are resolvable
                    if 'collection' in branch:
                        collection = repository.database[branch['collection']]
                        result = collection.find_one({u'head.uri':uri})
                        
                        # If record does not exists proceed to caching it
                        if result is None:
                            self.cache(uri, repository)
                            result = collection.find_one({u'head.uri':uri})
                    break
            if taken: break
        return result
    
    
    def remove(self, uri, repository):
        taken = False
        for branch in self.branch.values():
            for match in branch['match']:
                m = match['pattern'].search(uri)
                if m is not None:
                    taken = True
                    # Only branches with a collection definition are resolvable
                    if 'collection' in branch:
                        self.log.debug(u'Dropping %s', uri)
                        collection = repository.database[branch['collection']]
                        result = collection.remove({u'head.uri':uri})
                    break
            if taken: break
    
    
    def cache(self, uri, repository):
        taken = False
        for branch in self.branch.values():
            for match in branch['match']:
                m = match['pattern'].search(uri)
                if m is not None:
                    query = {
                        'repository':repository,
                        'branch':branch,
                        'uri':uri,
                        'parameter':None,
                        'stream':[],
                        'result':[],
                    }
                    
                    # extract and cast parameters
                    if 'namespace' in branch:
                        query['parameter'] = Ontology(self.env, branch['namespace'])
                        for k,v in m.groupdict().iteritems():
                            query['parameter'].decode(k,v)
                            
                        if 'api key' in self.node:
                            query['parameter']['api key'] = self.node['api key']
                            
                        # calculate the remote url
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
                    
            collection = query['repository'].database[entry['branch']['collection']]
            
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
    

