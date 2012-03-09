# -*- coding: utf-8 -*-

class Resolver(object):
    def __init__(self, env, ontology):
        self.log = logging.getLogger('Resolver')
        self.env = env
        self.ontology = ontology
        self.handlers = []
        self.connection = None
        self.db = None
        
        self.log.debug('Loading a model cache for %s', self.host)
        self.log.debug('Using connection url %s', self.ontology['mongodb url'])
        try:
            self.connection = pymongo.Connection(self.ontology['mongodb url'])
        except pymongo.errors.AutoReconnect as err:
            self.log.warning(u'Failed to connect to %s', self.ontology['mongodb url'])
            self.log.debug(u'Exception raised: %s', err)
        else:
            self.db = self.connection[self.ontology['database']]
            
            from tmdb import TmdbResourceHandler
            self.handlers['tmdb'] = TmdbResourceHandler(self, self.env.service['tmdb'])
            
            from tvdb import TvdbResourceHandler
            self.handlers['tvdb'] = TvdbResourceHandler(self, self.env.service['tvdb'])
    
    
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
        self.configuration = node
        self.pattern = re.compile(self.configuration['match'])
        self.branch = {}
        for namespace, branch in self.configuration['branch'].iteritems():
            branch['namespace'] = namespace
            branch['pattern'] = re.compile(branch['match'])
            self.branch[namespace] = branch
    
    
    @property
    def env(self):
        return self.resolver.env
    
    
    @property
    def name(self):
        return self.configuration['name']
    
    
    @property
    def prototype_spaces(self):
        return self.env.prototype[self.name]
    
    
    def resolve(self, uri):
        result = None
        for branch in self.branch:
            match = self.branch['pattern'].search(uri)
            # Only branches with a collection definition are resolvable
            if match is not None and 'collection' in branch:
                collection = self.resolver.db[branch['collection']]
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
                        'parameter':{
                            'host':self.env.host,
                            'api key':self.configuration['api key'],
                        },
                        'remote url':None,
                        'result':{},
                        'stream':{},
                    }
                    
                    # extract and cast parameters
                    if 'space' in branch and branch['space'] in self.prototype_spaces:
                        space = self.prototype_spaces[branch['space']]
                        for k,v in match.groupdict().iteritems():
                            prototype = space.find('keyword', k)
                            query['parameter'][prototype.key] = prototype.cast(v)
                            
                    # compose the remote url
                    query['remote url'] = branch['remote'].format(**query['parameter'])
                    
                    self.fetch(query)
                    self.parse(query)
                    break
    
    
    def remove(self, uri):
        for branch in self.branch.values():
            match = self.branch['pattern'].search(uri)
            if match is not None and 'collection' in branch:
                collection = self.resolver.db[branch['collection']]
                collection.remove({u'uri':uri})
                break
    
    
    def store(self, entry):
        if entry and 'uri' in entry and \
        'namespace' in entry and entry['namespace'] in self.branch:
            branch = self.branch[entry['namespace']]
            if 'collection' in branch:
                collection = self.resolver.db[branch['collection']]
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
