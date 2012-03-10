# -*- coding: utf-8 -*-

from ontology import Ontology

class Resolver(object):
    def __init__(self, env):
        self.log = logging.getLogger('Resolver')
        self.env = env
        self.handlers = []
        self.pool = {}
        
        from tmdb import TMDbHandler
        self.handlers['tmdb'] = TMDbHandler(self, self.env.service['tmdb'])
        
        from tvdb import TVDbHandler
        self.handlers['tvdb'] = TVDbHandler(self, self.env.service['tvdb'])
    
    
    def open(self):
        pass
    
    
    def close(self):
        for host, handle in self.pool.iteritems():
            handle['connection'].close()
    
    
    def find_database_handle(self, host):
        result = None
        if host in self.pool:
            result = self.pool[host]
        elif host in self.env.repository:
            repository = self.env.repository[host]
            o = Ontology(repository['mongodb'])
            handle = {
                'ontology':o,
                'connection':None,
                'database':None,
                'created':datetime.utcnow(),
            }
            
            if 'mongodb url' in o:
                try:
                    self.log.debug(u'Connecting to %s', o['mongodb url'])
                    handle['connection'] = pymongo.Connection(o['mongodb url'])
                except pymongo.errors.AutoReconnect as err:
                    self.log.warning(u'Failed to connect to %s', o['mongodb url'])
                    self.log.debug(u'Exception raised: %s', err)
                else:
                    self.log.debug(u'Connection established with %s', o['host'])
                    handle['database'] = handle['connection'][o['database']]
                    self.pool[host] = handle
                    result = handle
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
                        collection = handle['database'][branch['collection']]
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
                            prototype = space.find('keyword', k)
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
                        collection = handle['database'][branch['collection']]
                        collection.remove({u'uri':uri})
                break
    
    
    def store(self, entry):
        if entry and 'uri' in entry and 'host' in entry \
        'namespace' in entry and entry['namespace'] in self.branch:
            branch = self.branch[entry['namespace']]
            if 'collection' in branch:
                handle = self.resolver.find_database_handle(entry['host'])
                if handle:
                    collection = handle['database'][branch['collection']]
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
    
    


# media kind 'Movie'
# mpk://multivac/kb/movie
# mpk://multivac/kb/movie/imdb/<imdb id>
# mpk://multivac/kb/movie/tmdb/<tmdb id>
#
# media kind 'TV Show'
# mpk://multivac/kb/tvshow
# mpk://multivac/kb/tvshow/show/<show>
# mpk://multivac/kb/tvshow/season/<show>/<season>
# mpk://multivac/kb/tvshow/episode/<show>/<season>/<episode>
#
# media kind 'Music'
# mpk://multivac/kb/music
# mpk://multivac/kb/music/album/<album>
# mpk://multivac/kb/music/disc/<album>/<disc>
# mpk://multivac/kb/music/track/<album>/<disc>/<track>

# mpk://multivac/kb/person
# mpk://multivac/kb/network
# mpk://multivac/kb/studio
# mpk://multivac/kb/job
# mpk://multivac/kb/department
# mpk://multivac/kb/genre
