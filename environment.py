# -*- coding: utf-8 -*-

import os
import re
import logging
import copy
import urlparse
from subprocess import Popen, PIPE
from datetime import timedelta, datetime
from chardet.universaldetector import UniversalDetector

from ontology import Ontology, Enumeration, PrototypeSpace, Rule
from model import Timestamp
from model.caption import CaptionFilterCache
from service import Resolver

class Environment(object):
    def __init__(self):
        self.log = logging.getLogger('environment')
        
        from config import configuration
        self.node = configuration
        
        self.ontology = None
        self.state = {
            'default':{},
            'system':{},
            'archetype':{},
            'enumeration':{},
            'namespace':{},
            'rule':{},
            'service':{},
            'expression':{},
            'constant':{},
            'command':{},
            'action':{},
            'kind':{},
            'profile':{},
            'repository':{},
            'subtitle filter':{},
        }
        
        self._resolver = None
        self._caption_filter = None
        self._universal_detector = None
        
        self.load()
    
    
    def __unicode__(self):
        return unicode(u'{}:{}'.format(self.domain, self.host))
    
    
    # Runtime properties
    @property
    def system(self):
        return self.state['system']
    
    
    @property
    def home(self):
        return self.system['home']
    
    
    @property
    def host(self):
        return self.system['host']
    
    
    @property
    def domain(self):
        return self.system['domain']
    
    
    @property
    def language(self):
        return self.system['language']
    
    
    
    # Lazy loaders for processors
    @property
    def resolver(self):
        if self._resolver is None:
            self._resolver = Resolver(self)
        return self._resolver
    
    
    @property
    def caption_filter(self):
        if  self._caption_filter is None:
            self._caption_filter = CaptionFilterCache(self)
        return self._caption_filter
    
    
    @property
    def universal_detector(self):
        if self._universal_detector is None:
            self._universal_detector = UniversalDetector()
        return self._universal_detector
    
    
    @property
    def default(self):
        return self.state['default']
    
    
    @property
    def archetype(self):
        return self.state['archetype']
    
    
    @property
    def enumeration(self):
        return self.state['enumeration']
    
    
    @property
    def namespace(self):
        return self.state['namespace']
    
    
    @property
    def rule(self):
        return self.state['rule']
    
    
    @property
    def service(self):
        return self.state['service']
    
    
    @property
    def expression(self):
        return self.state['expression']
    
    
    @property
    def constant(self):
        return self.state['constant']
    
    
    @property
    def command(self):
        return self.state['command']
    
    
    @property
    def action(self):
        return self.state['action']
    
    
    @property
    def kind(self):
        return self.state['kind']
    
    
    @property
    def profile(self):
        return self.state['profile']
    
    
    @property
    def repository(self):
        return self.state['repository']
    
    
    @property
    def subtitle_filter(self):
        return self.state['subtitle filter']
    
    
    def load_node(self, node):
        if 'default' in node:
            for k,e in node['default'].iteritems():
                self.default[k] = e
                
        if 'system' in node:
            for k,e in node['system'].iteritems():
                self.system[k] = e
                
        if 'archetype' in node:
            for k,e in node['archetype'].iteritems():
                e['key'] = k
                self.archetype[k] = e
                
        if 'enumeration' in node:
            for k,e in node['enumeration'].iteritems():
                e['key'] = k
                self.enumeration[k] = Enumeration(self, e)
                
        if 'namespace' in node:
            for k,e in node['namespace'].iteritems():
                e['key'] = k
                self.namespace[k] = PrototypeSpace(self, e)
                
        if 'rule' in node:
            for k,e in node['rule'].iteritems():
                e['key'] = k
                self.rule[k] = Rule(self, e)
                
        if 'service' in node:
            for k,e in node['service'].iteritems():
                e['name'] = k
                self.service[k] = e
                
        if 'expression' in node:
            for e in node['expression']:
                if 'flags' not in e: e['flags'] = 0
                self.expression[e['name']] = re.compile(e['definition'], e['flags'])
                
        if 'constant' in node:
            for k,v in node['constant'].iteritems():
                self.constant[k] = v
                
        if 'command' in node:
            for e in node['command']:
                self.command[e['name']] = e
                self.which(e)
                
        if 'action' in node:
            for e in node['action']:
                self.action[e['name']] = e
                
        if 'kind' in node:
            for k,e in node['kind'].iteritems():
                e['name'] = k
                self.kind[k] = e
                
        if 'profile' in node:
            for k,e in node['profile'].iteritems():
                e['name'] = k
                self.profile[k] = e
                for action in self.default['profile']:
                    if action not in e:
                        e[action] = self.default['profile'][action]
                        
        if 'repository' in node:
            for k,e in node['repository'].iteritems():
                e['host'] = k
                self.repository[k] = Repository(self, e)
                
        if 'subtitle filter' in node:
            for k,e in node['subtitle filter'].iteritems():
                e['name'] = k
                self.subtitle_filter[k] = e
                
        # if 'available' in node:
        # if 'report' in node:
        # if 'format' in node:
    
    
    # Load environment
    
    def load(self):
        self.load_node(self.node)
        
        # Override the default home folder from env if specified
        home = os.getenv('MPK_HOME')
        if home:
            home = os.path.realpath(os.path.expanduser(os.path.expandvars(home)))
            if os.path.isdir(home):
                self.system['home'] = home
                
        self.system['conf'] = os.path.join(self.home, u'mpk.conf')
        self.load_external(self.system['conf'])
    
    
    def load_interactive(self, arguments):
        self.ontology = Ontology(self, 'system.job', arguments)
        
        # Load conf file from command line argument
        if 'conf' in self.ontology:
            self.ontology['conf'] = os.path.realpath(os.path.expanduser(os.path.expandvars(self.ontology['conf'])))
            self.load_external(self.ontology['conf'])
            
        # Override some value from command line
        for e in ('domain', 'host', 'language'):
            if e in self.ontology:
                self.system[e] = self.ontology[e]
        # self._load_dynamic_rules()
    
    
    def load_external(self, path):
        if path and os.path.isfile(path):
            try:
                external = eval(open(path).read())
                self.log.debug(u'Load external config file %s', path)
                self.load_node(external)
            except IOError, e:
                self.log.warning(u'Failed to load config file %s', path)
                self.log.debug(u'Exception raised: %s', unicode(e))
    
    
    def _load_dynamic_rules(self):
        # default host
        rule = {
            'name':'default host',
            'provide':set(('host',)),
            'branch':[
                {
                    'apply':(
                        {'property':'host', 'value':self.host},
                    ),
                },
            ],
        }
        self._load_rule(rule)
        
        # default language
        rule = {
            'name':'default language',
            'provide':set(('language',)),
            'branch':[
                {
                    'apply':(
                        {'property':'language', 'value':self.language},
                    ),
                },
            ],
        }
        self._load_rule(rule)
        
        # volume location
        rule = {
            'name':'volume location',
            'provide':set(('volume path', 'domain')),
            'branch':[],
        }
        for volume in self.volume.values():
            branch = {
                'requires':set(('volume', 'host')),
                'equal':{'volume':volume['name'], 'host':volume['host']},
                'apply':(
                    {'property':'domain', 'value':volume['domain']},
                    {'property':'volume path', 'value':volume['path']},
                ),
            }
            rule['branch'].append(branch)
        self._load_rule(rule)
        
        # cache
        rule = {
            'name':'cache location',
            'provide':set(('cache root',)),
            'branch':[
                {
                    'apply':({'property':'cache root', 'value':self.repository[self.host]['cache']['path']},),
                }
            ],
        }
        self._load_rule(rule)
        
        rule = {
            'name':'container for kind',
            'provide':set(('container',)),
            'branch':[],
        }
        for kind in self.kind.values():
            branch = {
                'requires':set(('kind',)),
                'equal':{'kind':kind['name'] },
                'apply':(
                    {'property':'container', 'value':kind['container']},
                ),
            }
            rule['branch'].append(branch)
        self._load_rule(rule)
        
    
    
    # Path manipulation
    def parse_url(self, url):
        result = None
        if url:
            parsed = urlparse.urlparse(url)
            if parsed.path:
                decoded = Ontology(self, 'resource.decode.url')
                decoded['directory'], decoded['file name'] = os.path.split(parsed.path)
                if 'file name' in decoded and 'directory' in decoded:
                    decoded['media kind']
                    result = Ontology(self, 'resource.file.url')
                    result['url'] = url
                    result['path'] = parsed.path
                    result['scheme'] = parsed.scheme or u'file'
                    result['host'] = parsed.hostname or self.host
                    for k,v in decoded.iteritems(): result[k] = v
                    if result['host'] in self.repository and 'volume path' in result:
                        result['volume'] = self.repository[result['host']].volume.parse(result['volume path'])
                        del result['volume path']
        return result
    
    
    def canonic_path_for(self, path):
        result = path
        real_path = os.path.realpath(os.path.abspath(path))
        for vol_path, vol in self.lookup['volume'].iteritems():
            if os.path.commonprefix([vol_path, real_path]) == vol_path:
                result = real_path.replace(vol_path, vol['path'])
                break
        return result
    
    
    def varify_directory(self, path):
        result = False
        try:
            dirname = os.path.dirname(path)
            if not os.path.exists(dirname):
                self.log.debug(u'Creating directory %s', dirname)
                os.makedirs(dirname)
                result = True
        except OSError as err:
            self.log.error(unicode(err))
            result = False
        return result
    
    
    def purge_path(self, path):
        if path and os.path.isfile(path):
            os.remove(path)
            try:
                os.removedirs(os.path.dirname(path))
            except OSError:
                pass
    
    
    def is_path_available(self, path, overwrite=False):
        result = True
        if path:
            if os.path.exists(path) and not overwrite:
                self.log.warning(u'Refusing to overwrite %s', path)
                result = False
        else:
            result = False
        return result
    
    
    def varify_path_is_available(self, path, overwrite=False):
        result = self.is_path_available(path, overwrite)
        if result: self.varify_directory(path)
        return result
    
    
    def purge_if_not_exist(self, path):
        result = True
        if path:
            if not os.path.exists(path):
                result = False
                try:
                    os.removedirs(os.path.dirname(path))
                except OSError:
                    pass
        else:
            result = False
        return result
    
    
    # Command execution
    def initialize_command(self, command, log):
        if command in self.command and self.command[command]['path']:
            return [ self.command[command]['path'] ]
        else:
            log.debug(u'Command %s is unavailable', command)
            return None
    
    
    def execute(self, command, message=None, debug=False, pipeout=True, pipeerr=True, log=None):
        def encode_command(command):
            c = []
            for e in command:
                if u' ' in e: c.append(u'"{0}"'.format(e))
                else: c.append(e)
            return u' '.join(c)
        
        
        report = None
        if command:
            if not debug:
                if log == None: log = self.log
                log.debug(u'Execute: %s', encode_command(command))
                if message: log.info(message)
                
                if pipeout and pipeerr:
                    proc = Popen(command, stdout=PIPE, stderr=PIPE)
                elif pipeout and not pipeerr:
                    proc = Popen(command, stdout=PIPE)
                elif not pipeout and pipeerr:
                    proc = Popen(command, stderr=PIPE)
                elif not pipeout and not pipeerr:
                    proc = Popen(command)
                    
                report = proc.communicate()
            else:
                log.info(message)
                print encode_command(command)
        return report
    
    
    def which(self, command):
        def is_executable(fpath):
            return os.path.isfile(fpath) and os.access(fpath, os.X_OK)
        
        
        command['path'] = None
        fpath, fname = os.path.split(command['binary'])
        if fpath:
            if is_executable(command['binary']):
                command['path'] = command['binary']
        else:
            for path in os.environ["PATH"].split(os.pathsep):
                bpath = os.path.join(path, command['binary'])
                if is_executable(bpath):
                    command['path'] = bpath
    
    
    def detect_encoding(self, content):
        # This will not survive a multi threaded environment
        self.universal_detector.reset()
        for line in content:
            self.universal_detector.feed(line)
            if self.universal_detector.done:
                break
        self.universal_detector.close()
        return self.universal_detector.result
    


class Repository(object):
    def __init__(self, env, node):
        self.log = logging.getLogger('repository')
        self.env = env
        self.node = node
        self.mongodb = Ontology(self.env, 'system.mongodb', self.node['mongodb'])
        self._volume = None
        self._connection = None
        if 'routing' not in self.node:
            self.node['routing'] = []
    
    
    @property
    def valid(self):
        return True
    
    
    @property
    def host(self):
        return self.node['host']
    
    
    @property
    def domain(self):
        return self.node['domain']
    
    
    @property
    def volume(self):
        if self._volume is None:
            self.reload()
        return self._volume
    
    
    @property
    def connection(self):
        if self._connection is None and 'mongodb url' in self.mongodb:
            try:
                import pymongo
                self.log.debug(u'Connecting to %s', self.mongodb['mongodb url'])
                self._connection = pymongo.Connection(self.mongodb['mongodb url'])
            except pymongo.errors.AutoReconnect, e:
                self.log.warning(u'Failed to connect to %s', self.mongodb['mongodb url'])
                self.log.debug(u'Exception raised: %s', e)
            else:
                self.log.debug(u'Connection established with %s', self.host)
        return self._connection
    
    
    @property
    def database(self):
        if self.connection is not None:
            return self.connection[self.mongodb['database']]
        else:
            return None
    
    
    def close(self):
        if self._connection is not None:
            self.log.debug(u'Closing mongodb connection to %s', self.host)
            self._connection.disconnect()
    
    
    def reload(self):
        # reload the volume enumeration
        for key, volume in self.node['volume'].iteritems():
            volume['host'] = self.host
            volume['domain'] = self.domain
            volume['virtual'] = u'/{0}'.format(key)
            volume['real'] = os.path.realpath(os.path.expanduser(os.path.expandvars(volume['path'])))
            
            volume['alternative'] = set()
            volume['alternative'].add(volume['real'])
            volume['alternative'].add(volume['virtual'])
            for alias in volume['alias']:
                volume['alternative'].add(os.path.realpath(os.path.expanduser(os.path.expandvars(alias))))
                
        self._volume = Enumeration(self.env, self.node['volume'])
        
        for key, volume in self.node['volume'].iteritems():
            for alt in volume['alternative']:
                if self._volume.search(alt) is None:
                    self._volume.map(key, alt)
                else:
                    self.log.error('Alias %s for %s on %s already mapped to volume %s', alt, key, self.host, self._volume.search(alt)['key'])
                    
        # reload routing rules
        routing = self.env.deduction.find('rule.system.default.routing')
        for branch in self.node['routing']:
            routing.add_branch(branch)
    

