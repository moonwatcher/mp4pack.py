# -*- coding: utf-8 -*-

import re
import logging
import copy
import json
import urlparse
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
        
        from rottentomatoes import RottenTomatoesHandler
        self.handlers['rottentomatoes'] = RottenTomatoesHandler(self, self.env.service['rottentomatoes'])
        
        from home import HomeHandler
        self.handlers['home'] = HomeHandler(self, self.env.service['home'])
        
    
    
    def resolve(self, uri, location=None):
        result = None
        if uri is not None:
            repository = None
            p = urlparse.urlparse(uri)
            if p.hostname is not None:
                if p.hostname in self.env.repository:
                    repository = self.env.repository[p.hostname]
                else:
                    self.log.warning(u'Unresolvable host name %s', p.hostname)
            else:
                repository = self.env.repository[self.env.host]
                
            if repository is not None:
                for handler in self.handlers.values():
                    if handler.match(p.path):
                        result = handler.resolve(p.path, repository, location)
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
            branch['name'] = name
            branch['persistent'] = 'collection' in branch
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
    
    
    # Resolve attempts to locate the record by uri
    def resolve(self, uri, repository, location):
        result = None
        taken = False
        for branch in self.branch.values():
            for match in branch['match']:
                m = match['pattern'].search(uri)
                if m is not None:
                    taken = True
                    if branch['persistent']:
                        collection = repository.database[branch['collection']]
                        result = collection.find_one({u'head.uri':uri})
                        
                        # If record does not exists try to produce it and lookup again
                        if result is None:
                            self.produce(uri, repository, location)
                            result = collection.find_one({u'head.uri':uri})
                    else:
                        self.produce(uri, repository, location)
                        
                    break
            if taken: break
        return result
    
    
    # Produce will attempt to create the record out of available resources
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
                        'match':match,
                        'uri':uri,
                        'parameter':None,
                        'source':[],
                        'result':[],
                    }
                    
                    # decode parameters from the uri
                    query['parameter'] = Ontology(self.env, 'ns.service.genealogy')
                    for k,v in m.groupdict().iteritems():
                        query['parameter'].decode(k,v)
                        
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
            record = None
            collection = query['repository'].database[entry['branch']['collection']]
            
            # Make a pseudo empty body for bodyless records
            if u'body' not in entry['record']:
                entry['record'][u'body'] = None
                
            # Build all the resolvable URIs from the genealogy
            entry['record'][u'head'][u'uri'] = []
            for resolvable in entry['branch']['resolvable']:
                try:
                    entry['record'][u'head']['uri'].append(resolvable['format'].format(**entry['record'][u'head'][u'genealogy']))
                except KeyError, e:
                    self.log.debug(u'Could not create uri for %s because %s was missing from the genealogy', resolvable['name'], e)
                    
            # Set the modified date
            entry['record'][u'head'][u'modified'] = datetime.utcnow()
            
            # Try to locate an existing record
            for uri in entry['record'][u'head'][u'uri']:
                record = collection.find_one({u'head.uri':uri})
                if record is not None:
                    break
                    
            # This is an update, we already have an existing record
            if record is not None:
                # Compute the union of the two uri lists
                record[u'head'][u'uri'] = list(set(record[u'head'][u'uri']).union(entry['record'][u'head'][u'uri']))
                
                # Compute the union of the two genealogy dictionaries
                # New computed genealogy overrides the existing
                record[u'head'][u'genealogy'] = dict(record[u'head'][u'genealogy'].items() + entry['record'][u'head'][u'genealogy'].items())
                
                # New body overrides the existing
                record[u'body'] = entry['record'][u'body']
                
            # This is an insert, no previous existing record was found
            else:
                record = entry['record']
                record[u'head'][u'created'] = record[u'head'][u'modified']
                
                # Issue a new id if a generator is specified
                if 'generate' in entry['branch']:
                    record[u'head'][u'genealogy'][entry['branch']['generate']['key']] = self.resolver.issue(query['repository'].host, entry['branch']['generate']['name'])
                    
                    # Build all the resolvable URIs from the genealogy again to account for the generated one
                    record[u'head'][u'uri'] = []
                    for resolvable in entry['branch']['resolvable']:
                        try:
                            record[u'head']['uri'].append(resolvable['format'].format(**record[u'head'][u'genealogy']))
                        except KeyError, e:
                            self.log.debug(u'Could not create uri for %s because %s was missing from the genealogy', resolvable['name'], e)
                            
            # Save the record to database
            self.log.debug(u'Storing %s', unicode(record[u'head']))
            collection.save(record)
    
    
    
    
    def remove(self, uri, repository):
        taken = False
        for branch in self.branch.values():
            for match in branch['match']:
                m = match['pattern'].search(uri)
                if m is not None:
                    taken = True
                    if branch['persistent']:
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
                        if branch['persistent']:
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
    

