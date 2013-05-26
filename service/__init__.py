# -*- coding: utf-8 -*-

import os
import re
import logging
import copy
import json
import urllib
import urlparse
from datetime import datetime
from ontology import Ontology
from bson import json_util
from bson.objectid import ObjectId
from StringIO import StringIO
from urllib2 import Request, urlopen, URLError, HTTPError
from httplib import BadStatusLine

class Resolver(object):
    def __init__(self, env):
        self.log = logging.getLogger('Resolver')
        self.env = env
        self.handlers = {}
        
        self.log.debug(u'Starting resolver')
        
        from tmdb import TMDbHandler
        self.handlers['tmdb'] = TMDbHandler(self, self.env.service['tmdb'])
        
        from itunes import iTunesHandler
        self.handlers['itunes'] = iTunesHandler(self, self.env.service['itunes'])
        
        from tvdb import TVDbHandler
        self.handlers['tvdb'] = TVDbHandler(self, self.env.service['tvdb'])
        
        from rottentomatoes import RottenTomatoesHandler
        self.handlers['rottentomatoes'] = RottenTomatoesHandler(self, self.env.service['rottentomatoes'])
        
        from home import HomeHandler
        self.handlers['home'] = HomeHandler(self, self.env.service['home'])
        
        from medium import MediumHandler
        self.handlers['medium'] = MediumHandler(self, self.env.service['medium'])

        from knowledge import KnowledgeBaseHandler
        self.handlers['knowledge'] = KnowledgeBaseHandler(self, self.env.service['knowledge'])
        
        
    
    def find_repository(self, hostname):
        repository = None
        if hostname is None: 
            hostname = self.env.host
            
        if hostname in self.env.repository:
            repository = self.env.repository[hostname]
        else:
            self.log.warning(u'Unresolvable host name %s', hostname)
            
        if repository and not repository.valid:
            self.log.warning(u'Could not start a repository for %s', hostname)
            repository = None
            
        return repository
    
    
    def resolve(self, uri, location=None):
        result = None
        if uri is not None:
            p = urlparse.urlparse(uri)
            repository = self.find_repository(p.hostname)
            if repository is not None:
                for handler in self.handlers.values():
                    if handler.match(p.path):
                        result = handler.resolve(p.path, repository, location)
                        break
        return result
    
    
    def remove(self, uri):
        if uri is not None:
            p = urlparse.urlparse(uri)
            repository = self.find_repository(p.hostname)
            if repository is not None:
                for handler in self.handlers.values():
                    if handler.match(p.path):
                        result = handler.remove(p.path, repository)
                        break
    
    
    def save(self, node):
        if node:
            if 'canonical' in node[u'head'] and node[u'head']['canonical']:
                uri = node['head']['canonical']
                repository = self.find_repository(self.env.host)
                if repository is not None:
                    for handler in self.handlers.values():
                        match = handler.match(uri)
                        if match is not None:
                            handler.save(node, repository)
                            break
            else:
                self.log.error(u'URIs are missing, refusing to save record %s', unicode(node[u'head']))        
    
    
    def issue(self, hostname, name):
        result = None
        if name == 'oid':
            result = ObjectId()
        else:
            repository = self.find_repository(hostname)
            if repository is not None:
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
        self.procedure = {}
        
        for name, branch in self.node['branch'].iteritems():
            branch['name'] = name
            
            # If a collection is defined, Set the presistence flag
            branch['persistent'] = 'collection' in branch
            
            # Query type defaults to lookup
            if 'query type' not in branch: branch['query type'] = 'lookup'

            for match in branch['match']:
                # Compile match patterns
                match['pattern'] = re.compile(match['filter'])
                
                # Convert query parameters to a set
                if 'query parameter' in match:
                    match['query parameter'] = set(match['query parameter'])
            
            self.branch[name] = branch
    
    
    @property
    def env(self):
        return self.resolver.env
    
    
    @property
    def name(self):
        return self.node['name']
    
    
    def match(self, uri):
        return self.pattern.search(uri)
    
    
    def remove(self, uri, repository):
        taken = False
        for branch in self.branch.values():
            for match in branch['match']:
                m = match['pattern'].search(uri)
                if m is not None:
                    taken = True
                    if branch['query type'] == 'lookup':
                        if branch['persistent']:
                            self.log.debug(u'Dropping %s', uri)
                            collection = repository.database[branch['collection']]
                            collection.remove({u'head.alternate':uri})
                    break
            if taken: break
    
    
    
    def save(self, node, repository):
        taken = False
        uri = node['head']['canonical']
        for branch in self.branch.values():
            for match in branch['match']:
                m = match['pattern'].search(uri)
                if m is not None:
                    taken = True
                    if branch['query type'] == 'lookup':
                        query = {
                            'repository':repository,
                            'location':None,
                            'branch':branch,
                            'match':match,
                            'uri':uri,
                            'parameter':None,
                            'sources':None,
                            'entires':[
                                {
                                    'branch':branch,
                                    'record':node,
                                },
                            ],
                        }
                        self.log.debug(u'Saving %s', query['uri'])
                        self.store(query)
                    break
            if taken: break
    
    
    def resolve(self, uri, repository, location):
        result = None
        taken = False
        for branch in self.branch.values():
            for match in branch['match']:
                m = match['pattern'].search(uri)
                if m is not None:
                    taken = True
                    query = {
                        'repository':repository,
                        'location':location,
                        'branch':branch,
                        'match':match,
                        'uri':uri,
                        'parameter':Ontology(self.env, 'ns.service.genealogy'),
                        'sources':[],
                        'entires':[],
                        'return':None,
                    }
                    
                    # decode parameters from the uri
                    for k,v in m.groupdict().iteritems():
                        query['parameter'].decode(k,v)
                        
                    self.prepare(query)
                    self.locate(query)
                    if not query['return']:
                        self.collect(query)
                        self.fetch(query)
                        self.parse(query)
                        self.store(query)
                        self.locate(query)
                    result = query['return']
                    break
            if taken: break

        return result
    
    
    def prepare(self, query):
        # Add an API Key, if the resolver has one
        if 'api key' in self.node:
            query['parameter']['api key'] = self.node['api key']
            
        # Compute the remote URL, if required
        if 'remote' in query['match']:
            try:
                query['remote url'] = os.path.join(self.node['remote base'], query['match']['remote'].format(**query['parameter']))
            except KeyError, e:
                self.log.error(u'Could not compute remote URL for %s because %s was missing from the genealogy', query['uri'], e)
            else:
                if 'query parameter' in query['match']:
                    query['query parameter'] = Ontology(self.env, 'ns.search.query')
                    
                    # Collect matching parameters from the query parameter
                    for k in query['match']['query parameter']:
                        if k in query['parameter']:
                            query['query parameter'][k] = query['parameter'][k]
                            
                    # Collect matching parameters from the location
                    if query['location']:
                        for k in query['match']['query parameter']:
                            if k in query['location']:
                                query['query parameter'][k] = query['location'][k]
                                
                    # Construct an encoded query URL
                    # First rename the parameters to the resolver's syntax and utf8 encode them 
                    parameters = {}
                    for k,v in query['query parameter'].iteritems():
                        prototype = query['query parameter'].namespace.find(k)
                        if prototype and prototype.node[self.name]:
                            parameters[prototype.node[self.name]] = unicode(v).encode('utf8')
    
                    if parameters:
                        # Break up the URL
                        parsed = list(urlparse.urlparse(query['remote url']))
                        
                        # URL escape the parameters, encode as a query string and convert back to unicode
                        extra = unicode(urllib.urlencode(parameters), 'utf8')
                        
                        # Append the parameters to the existing query fragment
                        if parsed[4]: parsed[4] = u'{}&{}'.format(parsed[4], extra)
                        else: parsed[4] = extra
                            
                        # Reassemble the URL
                        query['remote url'] = urlparse.urlunparse(parsed)
    
    def locate(self, query):
        if query['branch']['persistent']:
            collection = query['repository'].database[query['branch']['collection']]
            if query['branch']['query type'] == 'lookup':
                query['return'] = collection.find_one({u'head.alternate':query['uri']})
                
            elif query['branch']['query type'] == 'search':
                query['return'] = {
                    u'result count':0,
                    u'results':[],
                }
                
                # prepare the query dictionary
                select = {}
                for k,v in query['query parameter'].iteritems():
                    # we only want parameters that have been declared as indexes
                    # when preforming a lookup on the table
                    if k in query['branch']['index']:
                        select[u'head.genealogy.' + unicode(k)] = v
                        
                # process the returned results    
                cursor = collection.find(select)
                for r in cursor:
                    query['return']['results'].append(r)
                
                # return None instead of empty result set
                query['return']['result count'] = len(query['return']['results'])
                if not query['return']['result count'] > 0:
                    query['return'] = None
    
    
    def collect(self, query):
        if 'collect' in query['branch']:
            for pattern in query['branch']['collect']:
                try:
                    related = self.resolver.resolve(pattern.format(**query['parameter']))
                except KeyError, e:
                    self.log.debug(u'Could not create related uri for pattern %s because parameter %s was missing', pattern, e)
                else:
                    if related is not None:
                        for index in query['branch']['index']:
                            if index in related[u'head'][u'genealogy']:
                                query['parameter'][index] = related[u'head'][u'genealogy'][index]
    
    def fetch(self, query):
        if 'remote url' in query:
            request = Request(query['remote url'], None, {'Accept': 'application/json'})
            self.log.debug(u'Fetching %s', query['remote url'])

            try:
                response = urlopen(request)
            except BadStatusLine, e:
                self.log.warning(u'Bad HTTP status error when requesting %s', query['remote url'])
            except HTTPError, e:
                self.log.warning(u'Server returned an error when requesting %s: %s', query['remote url'], e.code)
            except URLError, e:
                self.log.warning(u'Could not reach server when requesting %s: %s', query['remote url'], e.reason)
            else:
                query['sources'].append(StringIO(response.read()))
    
    
    def parse(self, query):
        pass
    
    
    def store(self, query):
        for entry in query['entires']:
            if entry['branch']['persistent']:
            
                # normalize the canonical ontology on the record
                if 'body' in entry['record'] and 'canonical' in entry['record']['body']:
                    entry['record']['body']['canonical'].normalize()

                
                record = None
                collection = query['repository'].database[entry['branch']['collection']]
                entry['record'][u'head'][u'modified'] = datetime.utcnow()
                self._compute_resolvables(entry)
                
                # Make a pseudo empty body for bodyless records
                if u'body' not in entry['record']: entry['record'][u'body'] = None
                
                # Try to locate an existing record
                for uri in entry['record'][u'head'][u'alternate']:
                    record = collection.find_one({u'head.alternate':uri})
                    if record is not None: break
                        
                # This is an update, we already have an existing record
                if record is not None:
                    # Compute the union of the two uri lists
                    record[u'head'][u'alternate'] = list(set(record[u'head'][u'alternate']).union(entry['record'][u'head'][u'alternate']))
                    
                    # Compute the union of the two genealogy dictionaries, new overrides existing
                    record[u'head'][u'genealogy'] = dict(record[u'head'][u'genealogy'].items() + entry['record'][u'head'][u'genealogy'].items())
                    
                    # New body overrides the existing
                    record[u'body'] = entry['record'][u'body']
                    
                # This is an insert, no previous existing record was found
                else:
                    entry['record'][u'head'][u'created'] = entry['record'][u'head'][u'modified']
                    
                    # In case we need to issue keys
                    if 'key generator' in self.node:
                        # Issue a new id
                        entry['record'][u'head'][u'genealogy'][self.node['key generator']['element']] = self.resolver.issue(query['repository'].host, self.node['key generator']['space'])
                        if 'key' in entry['branch']:
                            entry['record'][u'head'][u'genealogy'][entry['branch']['key']] = entry['record'][u'head'][u'genealogy'][self.node['key generator']['element']]
                            
                        # Rebuild all the resolvable URIs from the genealogy again to account for the assigned id
                        self._compute_resolvables(entry)
                        
                    # The new record is the one to save
                    record = entry['record']
                    
                # Check that canonical and alternate are set
                if 'canonical' in record[u'head'] and record[u'head']['canonical'] and 'alternate' in record[u'head'] and record[u'head']['alternate']:
                    self.log.debug(u'Persisting %s', unicode(record[u'head']['canonical']))
                    collection.save(record)
                else:
                    self.log.error(u'URIs are missing, refusing to save record %s', unicode(record[u'head']))
    
    
    def _compute_resolvables(self, entry):
        entry['record'][u'head'][u'alternate'] = []
        entry['record'][u'head']['canonical'] = None
        
        # Build all the resolvable URIs from the genealogy
        for resolvable in entry['branch']['resolvable']:
            try:
                link = resolvable['format'].format(**entry['record'][u'head'][u'genealogy'])
                entry['record'][u'head']['alternate'].append(link)
                if 'canonical' in resolvable and resolvable['canonical']:
                    entry['record'][u'head']['canonical'] = link
                    
            except KeyError, e:
                self.log.debug(u'Could not create uri for %s because %s was missing from the genealogy', resolvable['name'], e)
    

