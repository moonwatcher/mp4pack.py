# -*- coding: utf-8 -*-

import os
import re
import logging
import copy
import hashlib
import json
from subprocess import Popen, PIPE
from datetime import timedelta, datetime
from chardet.universaldetector import UniversalDetector

from ontology import Ontology, Enumeration, PrototypeSpace, Rule, Space, Umid
from model import Timestamp
from model.caption import CaptionFilterCache
from service import Resolver
from argparse import ArgumentParser

class Environment(object):
    def __init__(self):
        self.log = logging.getLogger('Environment')
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
            'preset':{},
            'repository':{},
            'interface':{},
            'subtitle filter':{},
            'table':{},
        }
        self._resolver = None
        self._caption_filter = None
        self._universal_detector = None
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
        
    @property
    def universal_detector(self):
        if self._universal_detector is None:
            self._universal_detector = UniversalDetector()
        return self._universal_detector
        
    def load(self):
        relative = os.path.dirname(__file__)
        self.load_configuration_file(os.path.join(relative,'config/system.json'))
        self.load_configuration_file(os.path.join(relative,'config/expression.json'))
        self.load_configuration_file(os.path.join(relative,'config/interface.json'))
        self.load_configuration_file(os.path.join(relative,'config/enumeration.py'))
        self.load_configuration_file(os.path.join(relative,'config/archetype.json'))
        self.load_configuration_file(os.path.join(relative,'config/rule.json'))
        self.load_configuration_file(os.path.join(relative,'config/namespace.json'))
        self.load_configuration_file(os.path.join(relative,'config/service.json'))
        self.load_configuration_file(os.path.join(relative,'config/table.json'))
        self.load_configuration_file(os.path.join(relative,'config/material.json'))
        self.load_configuration_file(os.path.join(relative,'config/subtitle.py'))
        
        # Override the default home folder from env if specified and valid
        home = os.getenv('MPK_HOME')
        if home:
            home = os.path.expanduser(os.path.expandvars(home))
            if os.path.isdir(home):
                self.system['home'] = home
        self.system['conf'] = os.path.join(self.home, u'settings.json')
        self.load_configuration_file(self.system['conf'])
        
    def load_configuration_file(self, path):
        if path and os.path.isfile(path):
            try:
                content = open(path, 'r')
            except IOError, e:
                self.log.warning(u'Failed to load configuration file %s', path)
                self.log.debug(u'Exception raised: %s', unicode(e))
            else:
                extention = os.path.splitext(path)[1]
                try:
                    if extention == u'.py':
                        node = eval(content.read())
                    elif extention == u'.json':
                        node = json.load(content)
                    self.log.debug(u'Configuration dictionary loaded from %s', path)
                except SyntaxError, e:
                    self.log.warning(u'Syntax error in configuration file %s', path)
                    self.log.debug(u'Exception raised: %s', unicode(e))
                else:
                    if isinstance(node, dict):
                        self.load_configuration_node(node)
                    else:
                        self.log.warning(u'Configuration file %s is not a valid dictionary', path)
                        
    def load_interactive(self, ontology):
        self.ontology = ontology
        
        # Load conf file from command line argument
        if 'configuration path' in self.ontology:
            self.ontology['configuration path'] = os.path.expanduser(os.path.expandvars(self.ontology['configuration path']))
            self.load_configuration_file(self.ontology['configuration path'])
            
        # Override some value from command line
        for e in ('domain', 'host', 'language'):
            if e in self.ontology:
                self.system[e] = self.ontology[e]
        self.ontology['host'] = self.host
        self._load_dynamic_rules()
        
    def load_configuration_node(self, node):
        def check(node): return "enable" not in node or node["enable"]
            
        if node:
            if 'system' in node:
                for k,e in node['system'].iteritems():
                    self.system[k] = e
                    
            if 'archetype' in node:
                for k,e in node['archetype'].iteritems():
                    if check(e):
                        e['key'] = k
                        self.archetype[k] = e
                        
            if 'enumeration' in node:
                for k,e in node['enumeration'].iteritems():
                    if check(e):
                        e['key'] = k
                        self.enumeration[k] = Enumeration(self, e)
                        
            if 'namespace' in node:
                for k,e in node['namespace'].iteritems():
                    e['key'] = k
                    self.namespace[k] = PrototypeSpace(self, e)
                    
            if 'rule' in node:
                for k,e in node['rule'].iteritems():
                    if check(e):
                        e['key'] = k
                        self.rule[k] = Rule(self, e)
                        
            if 'service' in node:
                for k,e in node['service'].iteritems():
                    if check(e):
                        e['name'] = k
                        self.service[k] = e
                        
            if 'table' in node:
                for k,e in node['table'].iteritems():
                    if check(e):
                        e['name'] = k
                        self.table[k] = e
                        
            if 'expression' in node:
                for e in node['expression']:
                    if check(e):
                        # flags defaults to zero
                        if 'flags' not in e: e['flags'] = 0
                        self.expression[e['name']] = re.compile(e['definition'], e['flags'])
                        
            if 'constant' in node:
                for k,e in node['constant'].iteritems():
                    self.constant[k] = e
                    
            if 'command' in node:
                for e in node['command']:
                    if check(e):
                        self.command[e['name']] = e
                        self.which(e)
                        
            if 'preset' in node:
                for k,e in node['preset'].iteritems():
                    if check(e):
                        e['name'] = k
                        self.preset[k] = e
                        
            if 'repository' in node:
                for k,e in node['repository'].iteritems():
                    if check(e):
                        e['host'] = k
                        self.repository[k] = Repository(self, e)
                        
            if 'subtitle filter' in node:
                for k,e in node['subtitle filter'].iteritems():
                    if check(e):
                        e['name'] = k
                        self.subtitle_filter[k] = e
                        
            if 'interface' in node:
                for k,e in node['interface'].iteritems():
                    if check(e):
                        e['key'] = k
                        self.interface[k] = e
                        
    def _load_dynamic_rules(self):
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
                
    def detect_encoding(self, content):
        # This will not survive a multi threaded environment
        self.universal_detector.reset()
        for line in content:
            self.universal_detector.feed(line)
            if self.universal_detector.done:
                break
        self.universal_detector.close()
        return self.universal_detector.result
        
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
                    
    def encode_json(self, node):
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
        if 'routing' not in self.node:
            self.node['routing'] = []
        if 'default' not in self.node:
            self.node['default'] = []
        if 'mapping' not in self.node:
            self.node['mapping'] = []
            
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
        def check(node): return "enable" not in node or node["enable"]
        # Load path mappings
        self._mapping = {}
        for mapping in self.node['mapping']:
            if check(mapping):
                self.log.debug(u'Expanding path %s', mapping['path'])
                mapping['real'] = os.path.realpath(os.path.expanduser(os.path.expandvars(mapping['path'])))
                for alt in mapping['alternate']:
                    self.log.debug(u'Expanding path %s', alt)
                    alternate = os.path.realpath(os.path.expanduser(os.path.expandvars(alt)))
                    if alternate not in self._mapping:
                        self._mapping[alternate] = mapping['real']
                    else:
                        self.log.warning(u'Path %s on %s already mapped to %s', alternate, self.host, self._mapping[alternate])
                        
        # Load the volume enumeration
        for key, volume in self.node['volume']['element'].iteritems():
            if check(volume):
                self.log.debug(u'Expanding path %s', volume['path'])
                volume['real'] = os.path.realpath(os.path.expanduser(os.path.expandvars(volume['path'])))
        self._volume = Enumeration(self.env, self.node['volume'])
        
        # Load routing rules
        routing = self.env.rule['rule.system.default.routing']
        for branch in self.node['volume.default']:
            if 'host' not in branch['requires']:
                branch['requires'].append('host')
            branch['equal']['host'] = self.host
            routing.add_branch(branch)
            
        default = self.env.rule['rule.task.default.preset']
        for branch in self.node['preset.default']:
            if 'host' not in branch['requires']:
                branch['requires'].append('host')
            branch['equal']['host'] = self.host
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
        
    def rebuild_index(self, collection, definition):
        if collection is not None and collection in self.env.table:
            if 'name' in definition:
                table = self.database[collection]
                if 'unique' not in definition: definition['unique'] = False
                if 'dropDups' not in definition: definition['dropDups'] = False
                
                existing = table.index_information()
                
                if definition['name'] in existing:
                    self.log.info(u'Dropping index %s on collection %s', definition['name'], collection)
                    table.drop_index(definition['name'])
                    
                self.log.info(u'Rebuilding index %s on collection %s', definition['name'], collection)
                table.create_index(
                    definition['key'],
                    name=definition['name'],
                    unique=definition['unique'],
                    dropDups=definition['dropDups']
                )
            else:
                self.log.error(u'Refusing to handle unnamed index for collection %s', collection)
        else:
            self.log.error(u'Unknown collection %s', collection)
            

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
            if 'type' in argument['parameter']:
                # eval the type
                argument['parameter']['type'] = eval(argument['parameter']['type'])
                
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
        

