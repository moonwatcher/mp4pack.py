# -*- coding: utf-8 -*-

import os
import re
import logging
import copy
import hashlib
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
        self.ontology = None
        self.state = {
            'system':{},
            'archetype':{},
            'enumeration':{},
            'namespace':{},
            'rule':{},
            'service':{},
            'expression':{},
            'constant':{},
            'command':{},
            'profile':{},
            'preset':{},
            'repository':{},
            'interface':{},
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
    
    
    # Environment configuration
    @property
    def system(self):
        return self.state['system']
    
    
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
    def preset(self):
        return self.state['preset']
    
    
    @property
    def profile(self):
        return self.state['profile']
    
    
    @property
    def repository(self):
        return self.state['repository']
    
    
    @property
    def interface(self):
        return self.state['interface']
    
    
    @property
    def subtitle_filter(self):
        return self.state['subtitle filter']
    
    
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

    
    def load(self):
        relative = os.path.dirname(__file__)
        self.load_config(os.path.join(relative,'config/system.py'))
        self.load_config(os.path.join(relative,'config/namespace.py'))
        self.load_config(os.path.join(relative,'config/service.py'))
        self.load_config(os.path.join(relative,'config/resource.py'))
        
        # Override the default home folder from env if specified and valid
        home = os.getenv('MPK_HOME')
        if home:
            home = os.path.expanduser(os.path.expandvars(home))
            if os.path.isdir(home):
                self.system['home'] = home
        self.system['conf'] = os.path.join(self.home, u'mpk.conf')
        
        self.load_config(self.system['conf'])
    
    
    
    def load_config(self, path):
        if path and os.path.isfile(path):
            try:
                node = eval(open(path, 'r').read())
                self.log.debug(u'Loading configuration dictionary %s', path)
            except IOError, e:
                self.log.warning(u'Failed to load configuration file %s', path)
                self.log.debug(u'Exception raised: %s', unicode(e))
            else:
                if isinstance(node, dict):
                    self._load_config_node(node)
                else:
                    self.log.warning(u'Configuration file %s does not contain a valid dictionary', path)
    
    
    def load_interactive(self, ontology):
        self.ontology = ontology
        
        # Load conf file from command line argument
        if 'configuration path' in self.ontology:
            self.ontology['configuration path'] = os.path.expanduser(os.path.expandvars(self.ontology['configuration path']))
            self.load_config(self.ontology['configuration path'])
            
        # Override some value from command line
        for e in ('domain', 'host', 'language'):
            if e in self.ontology:
                self.system[e] = self.ontology[e]
        self.ontology['host'] = self.host
        self._load_dynamic_rules()
    
    
    def _load_config_node(self, node):
        if node:
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
                    
            if 'profile' in node:
                for k,e in node['profile'].iteritems():
                    e['name'] = k
                    self.profile[k] = e
                            
            if 'preset' in node:
                for k,e in node['preset'].iteritems():
                    e['name'] = k
                    self.preset[k] = e
                            
            if 'repository' in node:
                for k,e in node['repository'].iteritems():
                    e['host'] = k
                    self.repository[k] = Repository(self, e)
                    
            if 'subtitle filter' in node:
                for k,e in node['subtitle filter'].iteritems():
                    e['name'] = k
                    self.subtitle_filter[k] = e
                    
            if 'interface' in node:
                for k,e in node['interface'].iteritems():
                    e['key'] = k
                    self.interface[k] = e
    
    
    
    
    def _load_dynamic_rules(self):
        node = { 'rule':{}, }
        
        # Default host
        node['rule']['rule.system.default.host'] = {
            'name':'Default host',
            'provide':set(('host',)),
            'branch':[
                {
                    'apply':(
                        {'property':'host', 'value':self.host},
                    ),
                },
            ],
        }
        
        # Default language
        node['rule']['rule.system.default.language'] = {
            'name':'Default language',
            'provide':set(('language',)),
            'branch':[
                {
                    'apply':(
                        {'property':'language', 'value':self.language},
                    ), 
                },
            ],
        }
        
        # Volume location
        node['rule']['rule.system.volume.location'] = {
            'name':'Volume location',
            'provide':set(('volume path', )),
            'branch':[],
        }
        for repository in self.repository.values():
            for volume in repository.volume.element.values():
                node['rule']['rule.system.volume.location']['branch'].append(
                    {
                        'requires':set(('volume', 'host', 'domain')),
                        'equal':{'volume':volume.key, 'host':repository.host, 'domain':repository.domain},
                        'apply':(
                            {'property':'volume path', 'value':volume.node['real']},
                        ),
                    }
                )
        
        self._load_config_node(node)
    
    
    
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
                except OSError, oserr:
                    self.log.debug(oserr)
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
    
    
    def default_json_handler(self, o):
        result = None
        from bson.objectid import ObjectId
        if isinstance(o, datetime):
            result = o.isoformat()
        if isinstance(o, ObjectId):
            result = str(o)
            
        return result
    


class Repository(object):
    def __init__(self, env, node):
        self.log = logging.getLogger('repository')
        self.env = env
        self.node = node
        self.mongodb = Ontology(self.env, 'ns.system.mongodb', self.node['mongodb'])
        self._volume = None
        self._mapping = None
        self._connection = None
        if 'routing' not in self.node:
            self.node['routing'] = []
        if 'mapping' not in self.node:
            self.node['mapping'] = []
        
    
    
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
    def mapping(self):
        if self._mapping is None:
            self.reload()
        return self._mapping
    
    
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
        # Load path mappings
        self._mapping = {}
        for mapping in self.node['mapping']:
            mapping['real'] = os.path.realpath(os.path.expanduser(os.path.expandvars(mapping['path'])))
            for alt in mapping['alternate']:
                alternate = os.path.realpath(os.path.expanduser(os.path.expandvars(alt)))
                if alternate not in self._mapping:
                    self._mapping[alternate] = mapping['real']
                else:
                    self.log.warning('Path %s on %s already mapped to %s', alternate, self.host, self._mapping[alternate])
                    
        # Load the volume enumeration
        for key, volume in self.node['volume']['element'].iteritems():
            volume['real'] = os.path.realpath(os.path.expanduser(os.path.expandvars(volume['path'])))
        self._volume = Enumeration(self.env, self.node['volume'])
        
        # Load routing rules
        routing = self.env.rule['rule.system.default.routing']
        for branch in self.node['routing']:
            routing.add_branch(branch)
    
    
    def parse_path(self, path):
        result = None
        if path:
            decoded = Ontology(self.env, 'ns.medium.resource.url.decode')
            
            # Set directory and file name
            decoded['directory'], decoded['file name'] = os.path.split(path)
            
            if 'file name' in decoded and 'directory' in decoded:
                # Normalize the directory
                decoded['directory'] = self.normalize(decoded['directory'])
            
                # Check if the directory resides in a volume
                for volume in self.volume.element.values():
                    if os.path.commonprefix((volume.node['real'], decoded['directory'])) == volume.node['real']:
                        decoded['volume'] = volume.key
            
                # Hack to trigger rule.medium.resource.filename.parse
                decoded['kind']
                # Hack to trigger rule.medium.resource.directory.parse
                decoded['profile']
                
                result = decoded.project('ns.medium.resource.location')
                for k,v in decoded.iteritems(): result[k] = v
                
                result['host'] = self.host
                result['domain'] = self.domain
        return result
    
    
    def normalize(self, path):
        result = path
        # If the repository has mappings defined
        # check if the path is in an alternate location
        # and replace the prefix with the canonical one
        if path and self.mapping:
            for alt, real in self.mapping.iteritems():
                if os.path.commonprefix((alt, path)) == alt:
                    result = path.replace(alt, real)
                    # result = os.path.join(real, os.path.relpath(path, alt))
                    break
        return result

    
    

