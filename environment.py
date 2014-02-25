# -*- coding: utf-8 -*-

import os
import re
import logging
import copy
import hashlib
import json
import pickle

from StringIO import StringIO
from subprocess import Popen, PIPE
from datetime import timedelta, datetime
from chardet.universaldetector import UniversalDetector

from ontology import Ontology, Enumeration, PrototypeSpace, Rule, Space, Umid
from model import Timestamp
from model.caption import CaptionFilterCache
from service import Resolver
from argparse import ArgumentParser

check = lambda node: "enable" not in node or node["enable"]

class Cache(object):
    def __init__(self):
        self.log = logging.getLogger('Environment')
        self.home = u'/etc/mpk'
        self.node = None
        self.state = dict()
        self.path = None
        self.dirty = False
        self.relative = os.path.dirname(__file__)
        
        # correct the home directory from the environment variable
        home = os.getenv('MPK_HOME')
        if home and os.path.isdir(home):
            self.home = home
            
        self.log.debug(u'home directory is %s', home)
        self.path = os.path.join(self.home, u'cache.db')
        self.open()
        
    def get(self, path):
        result = None
        path = os.path.expanduser(os.path.expandvars(path))
        key = hashlib.sha1(path).hexdigest()
        
        if key not in self.state: self.state[key] = dict()
        state = self.state[key]
        
        if key not in self.node['record']: self.node['record'][key] = dict()
        record = self.node['record'][key]
        
        if 'file sha1' not in state:
            if os.path.isfile(path):
                try:
                    content = StringIO(open(path, 'rb').read())
                    state['file sha1'] = hashlib.sha1(content.read()).hexdigest()
                except IOError, e:
                    self.log.warning(u'Failed to load configuration file %s', path)
                    self.log.debug(u'Exception raised: %s', unicode(e))
                else:
                    if 'cached sha1' not in record or (state['file sha1'] != record['cached sha1']):
                        self.dirty = True
                        if 'node' in record:
                            del record['node']
                            self.log.debug(u'Removed old cached entry for %s', path)
                            
                        extension = os.path.splitext(path)[1]
                        content.seek(0)
                        try:
                            if extension == u'.json':
                                record['node'] = json.load(content)
                                self.log.debug(u'Loaded JSON configuration dictionary from %s with sha1 %s', path, state['file sha1'])
                            elif extension == u'.py':
                                record['node'] = eval(content.read())
                                self.log.debug(u'Loaded Python configuration dictionary from %s with sha1 %s', path, state['file sha1'])
                            else:
                                self.log.error(u'Uknown configuration type %s for %s', extension, path)
                                
                        except SyntaxError, e:
                            self.log.warning(u'Syntax error in configuration file %s', path)
                            self.log.debug(u'Exception raised: %s', unicode(e))
                        else:
                            if 'node' in record:
                                if isinstance(record['node'], dict):
                                    # if everything is fine cache the record
                                    # and set the cached sha1 to match the file we loaded
                                    record['cached sha1'] = state['file sha1']
                                    
                                    # than apply any postprocessing
                                    self.load(record)
                                else:
                                    del record['node']
                                    del record['cached sha1']
                                    self.log.warning(u'No valid dictionary in configuration file %s', path)
            else:
                self.log.warning(u'Configuration file at %s does not exists', path)
                
        if 'node' in record:
            result = copy.deepcopy(record['node'])
        return result
        
    def load(self, record):
        def load_dictionary(node, name, key='key'):
            temp = node[name]
            node[name] = {}
            for k,e in temp.iteritems():
                if check(e):
                    e[key] = k
                    node[name][k] = e
                    
        node = record['node']
        if node:
            if 'archetype' in node:
                load_dictionary(node, 'archetype')
                
            if 'enumeration' in node:
                load_dictionary(node, 'enumeration')
                
            if 'namespace' in node:
                load_dictionary(node, 'namespace')
                
            if 'rule' in node:
                load_dictionary(node, 'rule')
                self.load_rule_node(node['rule'])
                
            if 'service' in node:
                load_dictionary(node, 'service', 'name')
                
            if 'table' in node:
                load_dictionary(node, 'table', 'name')
                
            if 'expression' in node:
                load_dictionary(node, 'expression', 'key')
                self.load_expression_node(node['expression'])
                
            if 'command' in node:
                load_dictionary(node, 'command', 'name')
                self.load_command_node(node['command'])
                
            if 'preset' in node:
                load_dictionary(node, 'preset', 'name')
                
            if 'repository' in node:
                load_dictionary(node, 'repository', 'host')
                self.load_repository_node(node['repository'])
                
            if 'subtitle filter' in node:
                load_dictionary(node, 'subtitle filter', 'name')
                
            if 'interface' in node:
                load_dictionary(node, 'interface')
                self.load_interface_node(node['interface'])
                
    def open(self):
        if os.path.exists(self.path):
            try:
                self.node = pickle.load(open(self.path, 'rb'))
            except KeyError:
                self.log.warning(u'Failed to load pickled cache from %s', self.path)
                self.node = None
                
        if self.node is None:
            self.node = { 'record':{} }
            
    def close(self):
        if self.dirty:
            try:
                pickle.dump(self.node, open(self.path, 'wb'))
                self.log.debug(u'Saved pickled cache to %s', self.path)
            except IOError, e:
                self.log.warning(u'Failed to write cache to %s', self.path)
                self.log.debug(u'Exception raised: %s', unicode(e))
                
    def load_rule_branch(self, branch):
        if 'requires' in branch:
            branch['requires'] = set(branch['requires'])
            
        if 'match' in branch:
            if 'flags' not in branch['match']:
                branch['match']['flags'] = re.UNICODE
            
        if 'decode' in branch:
            for c in branch['decode']:
                if 'flags' not in c:
                    c['flags'] = re.UNICODE
                    
    def load_rule_node(self, node):
        for k,e in node.iteritems():
            if 'provide' in e:
                e['provide'] = set(e['provide'])
                
            if 'branch' not in e:
                e['branch'] = []
                
            else:
                for branch in e['branch']:
                    self.load_rule_branch(branch)
                    
    def load_expression_node(self, node):
        for k,e in node.iteritems():
            if 'flags' not in e:
                e['flags'] = 0
                
    def load_command_node(self, node):
        for k,e in node.iteritems():
            self.which(e)
            
    def load_interface_node(self, node):
        for k,e in node.iteritems():
            for argument in e['prototype'].values():
                if 'type' in argument['parameter']:
                    # eval the type
                    argument['parameter']['type'] = eval(argument['parameter']['type'])
                    
    def load_repository_node(self, node):
        for k,e in node.iteritems():
            if 'routing' not in e: e['routing'] = []
            if 'default' not in e: e['default'] = []
            if 'mapping' not in e: e['mapping'] = []
            
            # expand path mappings
            temp = e['mapping']
            e['mapping'] = list()
            for mapping in temp:
                if check(mapping):
                    self.log.debug(u'Expanding path %s', mapping['path'])
                    mapping['real'] = os.path.realpath(os.path.expanduser(os.path.expandvars(mapping['path'])))
                    
                    alternate = set()
                    for alt in mapping['alternate']:
                        self.log.debug(u'Expanding path %s', alt)
                        alternate.add(os.path.realpath(os.path.expanduser(os.path.expandvars(alt))))
                    mapping['alternate'] = list(alternate)
                    e['mapping'].append(mapping)
                    
            # expand volume paths
            temp = e['volume']['element']
            e['volume']['element'] = dict()
            for key, volume in temp.iteritems():
                if check(volume):
                    self.log.debug(u'Expanding path %s', volume['path'])
                    volume['real'] = os.path.realpath(os.path.expanduser(os.path.expandvars(volume['path'])))
                    e['volume']['element'][key] = volume
                    
    def which(self, command):
        def is_executable(fpath):
            return os.path.isfile(fpath) and os.access(fpath, os.X_OK)
            
        command['path'] = None
        fpath, fname = os.path.split(command['binary'])
        if fpath:
            if is_executable(command['binary']):
                command['path'] = command['binary']
        else:
            for path in os.environ['PATH'].split(os.pathsep):
                bpath = os.path.join(path, command['binary'])
                if is_executable(bpath):
                    command['path'] = bpath
                    


class Environment(object):
    def __init__(self):
        self.log = logging.getLogger('Environment')
        self.ontology = None
        self.cache = Cache()
        self.state = {
            'config':[
                {
                    'name':'system',
                    'path':'config/system.json',
                },
                {
                    'name':'expression',
                    'path':'config/expression.json',
                },
                {
                    'name':'interface',
                    'path':'config/interface.json',
                },
                {
                    'name':'enumeration',
                    'path':'config/enumeration.py',
                },
                {
                    'name':'archetype',
                    'path':'config/archetype.json',
                },
                {
                    'name':'rule',
                    'path':'config/rule.json',
                },
                {
                    'name':'namespace',
                    'path':'config/namespace.json',
                },
                {
                    'name':'service',
                    'path':'config/service.json',
                },
                {
                    'name':'table',
                    'path':'config/table.json',
                },
                {
                    'name':'material',
                    'path':'config/material.json',
                },
                {
                    'name':'subtitle',
                    'path':'config/subtitle.py',
                },
            ],
            'system':{},
            'archetype':{},
            'enumeration':{},
            'namespace':{},
            'rule':{},
            'service':{},
            'expression':{},
            'constant':{},
            'command':{},
            'preset':{},
            'repository':{},
            'interface':{},
            'subtitle filter':{},
            'table':{},
        }
        self._resolver = None
        self._caption_filter = None
        self.load()
        
    def __unicode__(self):
        return unicode(u'{}:{}'.format(self.domain, self.host))
        
    @property
    def document(self):
        return json.dumps(self.state, ensure_ascii=False, sort_keys=True, indent=4,  default=self.environment_json_handler)
        
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
        
    @property
    def config(self):
        return self.state['config']
        
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
    def repository(self):
        return self.state['repository']
        
    @property
    def interface(self):
        return self.state['interface']
        
    @property
    def subtitle_filter(self):
        return self.state['subtitle filter']
        
    @property
    def table(self):
        return self.state['table']
        
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
        
    def close(self):
        if self.cache is not None:
            self.cache.close()
            
    def load(self):
        # calculate a relative address for config files
        relative = os.path.dirname(__file__)
        
        # load the config files
        for config in self.config:
            # caluclate an absolute address
            config['path'] = os.path.join(relative, config['path'])
            self.load_configuration_node(self.cache.get(config['path']))
            
        # Override the default home folder from env
        self.system['home'] = self.cache.home
        
        # Load the settings file
        self.load_configuration_node(self.cache.get(os.path.join(self.home, u'settings.json')))
        
    def load_interactive(self, ontology):
        self.ontology = ontology
        
        # Load config file from command line argument
        if 'configuration path' in self.ontology:
            self.ontology['configuration path'] = os.path.expanduser(os.path.expandvars(self.ontology['configuration path']))
            self.load_configuration_node(self.cache.get(self.ontology['configuration path']))
            
        # Override some value from command line
        for e in ('domain', 'host', 'language'):
            if e in self.ontology:
                self.system[e] = self.ontology[e]
        self.ontology['host'] = self.host
        self.load_dynamic_rules()
        
    def load_configuration_node(self, node):
        if node:
            if 'system' in node:
                for k,e in node['system'].iteritems():
                    self.system[k] = e
                    
            if 'archetype' in node:
                for k,e in node['archetype'].iteritems():
                    self.archetype[k] = e
                    
            if 'enumeration' in node:
                for k,e in node['enumeration'].iteritems():
                    self.enumeration[k] = Enumeration(self, e)
                    
            if 'namespace' in node:
                for k,e in node['namespace'].iteritems():
                    self.namespace[k] = PrototypeSpace(self, e)
                    
            if 'rule' in node:
                for k,e in node['rule'].iteritems():
                    self.rule[k] = Rule(self, e)
                    
            if 'service' in node:
                for k,e in node['service'].iteritems():
                    self.service[k] = e
                    
            if 'table' in node:
                for k,e in node['table'].iteritems():
                    self.table[k] = e
                    
            if 'expression' in node:
                for k,e in node['expression'].iteritems():
                    self.expression[k] = re.compile(e['definition'], e['flags'])
                    
            if 'constant' in node:
                for k,e in node['constant'].iteritems():
                    self.constant[k] = e
                    
            if 'command' in node:
                for k,e in node['command'].iteritems():
                    self.command[k] = e
                    
            if 'preset' in node:
                for k,e in node['preset'].iteritems():
                    self.preset[k] = e
                    
            if 'repository' in node:
                for k,e in node['repository'].iteritems():
                    self.repository[k] = Repository(self, e)
                    
            if 'subtitle filter' in node:
                for k,e in node['subtitle filter'].iteritems():
                    self.subtitle_filter[k] = e
                    
            if 'interface' in node:
                for k,e in node['interface'].iteritems():
                    self.interface[k] = e
                    
    def load_dynamic_rules(self):
        node = { 'rule':{}, }
        
        # Default host
        node['rule']['rule.system.default.host'] = {
            'name':'Default host',
            'provide':['host'],
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
            'provide':['language'],
            'branch':[
                {
                    'apply':(
                        {'property':'language', 'value':self.language},
                    ), 
                },
            ],
        }
        
        # Temp location
        node['rule']['rule.system.temp.location'] = {
            'name':'Temp location',
            'provide':['temp path'],
            'branch':[],
        }
        for repository in self.repository.values():
            node['rule']['rule.system.temp.location']['branch'].append(
                {
                    'requires':['host', 'domain'],
                    'equal':{'host':repository.host, 'domain':repository.domain},
                    'apply':(
                        {'property':'temp path', 'value':repository.node['temp']['path']},
                    ),
                }
            )
        
        # Volume location
        node['rule']['rule.system.volume.location'] = {
            'name':'Volume location',
            'provide':['volume path'],
            'branch':[],
        }
        for repository in self.repository.values():
            for volume in repository.volume.element.values():
                node['rule']['rule.system.volume.location']['branch'].append(
                    {
                        'requires':['volume', 'host', 'domain'],
                        'equal':{'volume':volume.key, 'host':repository.host, 'domain':repository.domain},
                        'apply':(
                            {'property':'volume path', 'value':volume.node['real']},
                        ),
                    }
                )
        self.cache.load({'node':node})
        self.load_configuration_node(node)
        
    def cleanup_path(self, path):
        if path and os.path.isfile(path):
            os.remove(path)
            try:
                os.removedirs(os.path.dirname(path))
            except OSError:
                pass
                
    def check_path_availability(self, path, overwrite=False):
        if path:
            if os.path.exists(path) and not overwrite:
                self.log.warning(u'Refusing to overwrite %s', path)
                return False
            else:
                self.varify_directory(path)
                return True
        else:
            return False
            
    def varify_directory(self, path):
        try:
            directory = os.path.dirname(path)
            if not os.path.exists(directory):
                self.log.debug(u'Creating directory %s', directory)
                os.makedirs(directory)
                
        except OSError as err:
            self.log.error(u'Failed to create directory %s', directory)
            self.log.debug(unicode(err))
            
    def purge_if_not_exist(self, path):
        if path and not os.path.exists(path):
            try:
                os.removedirs(os.path.dirname(path))
            except OSError, oserr:
                self.log.debug(oserr)
                
    def environment_json_handler(self, o):
        result = None
        from bson.objectid import ObjectId
        if isinstance(o, datetime):
            result = o.isoformat()
        if isinstance(o, ObjectId):
            result = str(o)
        if isinstance(o, Rule):
            result = o.node
        if isinstance(o, Repository):
            result = o.node
        if isinstance(o, Space):
            result = o.node
        if isinstance(o, set):
            result = list(o)
        return result
        
    def default_json_handler(self, o):
        result = None
        from bson.objectid import ObjectId
        if isinstance(o, datetime):
            result = o.isoformat()
        if isinstance(o, ObjectId):
            result = str(o)
        if isinstance(o, set):
            result = list(o)
            
        return result
        
    def initialize_command(self, command, log):
        if command in self.command and self.command[command]['path']:
            return [ self.command[command]['path'] ]
        else:
            log.debug(u'Command %s is unavailable', command)
            return None
            
    def encode_command(self, command):
        c = []
        for e in command:
            if self.constant['space'] in e: c.append(u'"{0}"'.format(e))
            else: c.append(e)
        return self.constant['space'].join(c)
        
    def execute(self, command, message=None, debug=False, pipeout=True, pipeerr=True, log=None):
        report = None
        if command:
            if not debug:
                # if a logger was provided, use it. Otherwise default to the local
                if log == None: log = self.log
                    
                log.debug(u'Execute: %s', self.encode_command(command))
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
                if message: log.info(message)
                print self.encode_command(command)
        return report
        
    def encode_json(self, node):
        # Can't use ensure_ascii=False because the logging library seems to break when fed utf8 with non ascii characters
        return json.dumps(node, sort_keys=True, indent=4, default=self.default_json_handler)
        


class Repository(object):
    def __init__(self, env, node):
        self.log = logging.getLogger('Repository')
        self.env = env
        self.node = node
        self.mongodb = Ontology(self.env, 'ns.system.mongodb', self.node['mongodb'])
        self._volume = None
        self._mapping = None
        self._connection = None
        
    def __unicode__(self):
        return unicode(u'{}:{}'.format(self.domain, self.host))
        
    @property
    def valid(self):
        return self.connection is not None
        
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
            except pymongo.errors.PyMongoError, e:
                self.log.error(u'Could not establish connection with %s because %s', self.mongodb['mongodb url'], e)
            else:
                self.log.debug(u'Connection established with %s', self.host)
        return self._connection
        
    @property
    def database(self):
        if self.connection is not None:
            return self._connection[self.mongodb['database']]
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
            for alt in mapping['alternate']:
                if alt not in self._mapping:
                    self._mapping[alt] = mapping['real']
                else:
                    self.log.warning(u'Path %s on %s already mapped to %s', alt, self.host, self._mapping[alt])
                    
        # Load the volume enumeration
        self._volume = Enumeration(self.env, self.node['volume'])
        
        # Load routing rules
        routing = self.env.rule['rule.system.default.routing']
        for branch in self.node['routing']['volume.default']:
            if 'host' not in branch['requires']:
                branch['requires'].append('host')
            branch['equal']['host'] = self.host
            self.env.cache.load_rule_branch(branch)
            routing.add_branch(branch)
        default = self.env.rule['rule.task.default.preset']
        for branch in self.node['routing']['preset.default']:
            if 'host' not in branch['requires']:
                branch['requires'].append('host')
            branch['equal']['host'] = self.host
            self.env.cache.load_rule_branch(branch)
            default.add_branch(branch)
                
    def decode_resource_path(self, path):
        result = None
        if path:
            decoded = Ontology(self.env, 'ns.medium.resource.url.decode')
            decoded['directory'], decoded['file name'] = os.path.split(path)
            if 'file name' in decoded and 'directory' in decoded:
                
                # Normalize the directory
                # This will replace path framents with canonic values
                decoded['directory'] = self.normalize(decoded['directory'])
                
                # Check if the directory resides in a volume
                for volume in self.volume.element.values():
                    if os.path.commonprefix((volume.node['real'], decoded['directory'])) == volume.node['real']:
                        decoded['volume'] = volume.key
                        
                # If a UMID was encoded in the name, infer the home id and media kind
                # This will also trigger rule.medium.resource.filename.parse
                if 'umid' in decoded:
                    umid = Umid.decode(decoded['umid'])
                    if umid:
                        decoded['media kind'] = umid.media_kind
                        decoded['home id'] = umid.home_id
                        
                # Make the elements of the decoded onlology kernel elements of the result
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
                    break
        return result
        
    def rebuild_index(self, name, definition):
        if name is not None and name in self.env.table:
            if 'name' in definition:
                table = self.database[self.env.table[name]['collection']]
                if 'unique' not in definition: definition['unique'] = False
                if 'dropDups' not in definition: definition['dropDups'] = False
                
                existing = table.index_information()
                
                if definition['name'] in existing:
                    self.log.info(u'Dropping index %s on collection %s', definition['name'], name)
                    table.drop_index(definition['name'])
                    
                self.log.info(u'Rebuilding index %s on collection %s', definition['name'], name)
                table.create_index(
                    definition['key'],
                    name=definition['name'],
                    unique=definition['unique'],
                    dropDups=definition['dropDups']
                )
            else:
                self.log.error(u'Refusing to handle unnamed index for collection %s', name)
        else:
            self.log.error(u'Unknown collection %s', name)
            


class CommandLineParser(object):
    def __init__(self, env, node):
        self.env = env
        self.node = node
        self.parser = ArgumentParser()
        self.load()
        
    def load(self):
        def add_argument(parser, name):
            node = self.node['prototype'][name]
            parser.add_argument(*node['flag'], **node['parameter'])
            
        for argument in self.node['prototype'].values():
            if 'dest' in argument['parameter']:
                archetype = self.env.archetype[argument['parameter']['dest']]
                
                # Add the enumeration constrains
                if archetype['type'] == 'enum':
                    enumeration = self.env.enumeration[archetype['enumeration']]
                    argument['parameter']['choices'] = enumeration.synonym[argument['axis']].keys()
                    
        # Add global arguments
        for argument in self.node['global']['argument']:
            add_argument(self.parser, argument)
            
        # Add individual command sections
        s = self.parser.add_subparsers(dest='action')
        for action in self.node['action']:
            action_parser = s.add_parser(**action['instruction'])
            for argument in action['argument']:
                add_argument(action_parser, argument)
                
            # Add groups of arguments, if any.
            if 'group' in action:
                for group in action['group']:
                    group_parser = action_parser.add_argument_group(**group['instruction'])
                    for argument in group['argument']:
                        add_argument(group_parser, argument)
                        
    def parse(self):
        arguments = vars(self.parser.parse_args())
        ontology = Ontology(self.env, self.node['namespace'])
        for k,v in arguments.iteritems():
            ontology.decode(k, v)
        return ontology
        

