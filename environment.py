# -*- coding: utf-8 -*-

import os
import re
import logging
import copy
import unicodedata
import urlparse
import plistlib
from subprocess import Popen, PIPE
from datetime import timedelta, datetime

import config

from ontology import Ontology
from model import Timestamp, Enumeration, PrototypeSpace
from model.caption import CaptionFilterCache
from service import Resolver

class Environment(object):
    def __init__(self):
        self.log = logging.getLogger('environment')
        self.runtime = None
        self.configuration = None
        self.ontology = None
        self.caption_filter_cache = None
        self.universal_detector = None
        self.state = {
            'system':{},
            'prototype':{},
            'model':{},
            'available':{},
            'expression':{},
            'command':{},
            'action':{},
            'profile':{},
            'kind':{},
            'report':{},
            'format':{},
            'repository':{},
            'volume':{},
            'rule':{},
        }
        self.lookup = {
            'volume':{},
        }
        self.load()
    
    
    def __unicode__(self):
        return unicode(u'{}:{}'.format(self.domain, self.host))
    
    
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
    
    
    @property
    def prototype(self):
        return self.state['prototype']
    
    
    @property
    def model(self):
        return self.state['model']
    
    
    @property
    def available(self):
        return self.state['available']
    
    
    @property
    def command(self):
        return self.state['command']
    
    
    @property
    def action(self):
        return self.state['action']
    
    
    @property
    def report(self):
        return self.state['report']
    
    
    @property
    def repository(self):
        return self.state['repository']
    
    
    @property
    def volume(self):
        return self.state['volume']
    
    
    @property
    def profile(self):
        return self.state['profile']
    
    
    @property
    def kind(self):
        return self.state['kind']
    
    
    @property
    def rule(self):
        return self.state['rule']
    
    
    @property
    def service(self):
        return self.runtime['service']
    
    
    @property
    def expression(self):
        return self.state['expression']
    
    
    
    # Load environment
    def load(self):
        self.caption_filter_cache = CaptionFilterCache(self)
        
        # Runtime config
        from config.runtime import runtime as runtime_config
        self.runtime = runtime_config
        
        # Base user conf
        from config.base import base as base_config
        self.configuration = copy.deepcopy(base_config)
        self.load_system(self.configuration['system'])
        
        # Override the default home folder from env if specified
        env_home = os.getenv('MPK_HOME')
        if env_home and os.path.exists(env_home):
            self.system['home'] = env_home
            
        if self.home:
            self.load_external_config(os.path.join(self.home, 'dev.conf'))
            self.load_system(self.configuration['system'])
            
        self.profile['default'] = self.runtime['default']['profile']
        self.load_expressions(self.runtime['expression'])
        self.load_commands(self.runtime['command'])
        self.load_actions(self.runtime['action'])
        self.load_service(self.runtime['service'])
        
        from config.model import model as model_config
        self.load_model(model_config)
        
        from config.prototype import prototype as prototype_config
        self.load_prototype(prototype_config)
        self.load_profiles(self.runtime['profile'])
        self.load_kinds(self.runtime['kind'])
        self.load_rules(self.runtime['rule'])
    
    
    def load_interactive(self, arguments):
        self.ontology = arguments
        
        # Load conf file from command line argument
        if 'conf' in self.ontology:
            self.load_external_config(self.ontology['conf'])
            self.load_system(self.configuration['system'])
        
        # Override some value from command line
        for p in ('domain', 'host', 'language'):
            if p in self.ontology:
                self.system[p] = self.ontology[p]
                
        self.load_format(self.configuration['display'])
        self.load_reports(self.configuration['report'])
        self.load_repositories(self.configuration['repository'])
        self._load_dynamic_rules()
        self.configuration['playback']['aspect ratio'] = float (
            float(self.configuration['playback']['width']) / 
            float(self.configuration['playback']['height'])
        )
        self.resolver = Resolver(self)
    
    
    def load_external_config(self, path):
        if path and os.path.exists(path):
            path = os.path.abspath(path)
            try:
                external = eval(open(path).read())
                self.log.debug(u'Load external config file %s', path)
                self.configuration = dict(self.configuration.items() + external.items())
            except IOError as ioerr:
                self.log.warning(u'Failed to load config file %s', path)
                self.log.debug(ioerr)
    
    
    def load_system(self, node):
        for k,v in node.iteritems():
            self.system[k] = v
    
    
    def load_expressions(self, node):
        for expression in node:
            if 'flags' in expression and expression['flags']:
                self.expression[expression['name']] = re.compile(expression['definition'], expression['flags'])
            else:
                self.expression[expression['name']] = re.compile(expression['definition'])
    
    
    def load_commands(self, node):
        for command in node:
            self.command[command['name']] = command
            if command['binary']:
                # check the command exists and get an absolute path for it
                c = ['which', command['binary']]
                proc = Popen(c, stdout=PIPE, stderr=PIPE)
                report = proc.communicate()
                if report[0]:
                    command['path'] = report[0].splitlines()[0]
        self.available['command'] = set([i['name'] for i in self.command.values() if 'path' in i])
    
    
    def load_actions(self, node):
        for action in node:
            self.action[action['name']] = action
            action['active'] = True
            if 'depend' in action:
                action['depend'] = set(action['depend'])
                if not action['depend'].issubset(self.available['command']):
                    action['active'] = False
                    self.log.debug(u'Action %s has unsatisfied dependencies: %s', action['name'], 
                        u', '.join(list(action['depend'] - self.available['command']))
                    )
        self.available['action'] = set([i['name'] for i in self.action.values() if i['active']])
    
    
    def load_info(self, node):
        # Load a default report profile
        report = {
            'file':sorted(set([ v['name'] for v in node['file'] if 'name' in v])),
            'tag':sorted(set([ v['name'] for v in node['tag'] if 'name' in v])),
            'track':{},
        }
        common = [ v['name'] for v in node['track']['common'] if 'name' in v]
        for t in ('audio', 'video', 'text', 'image'):
            prop = common + [ v['name'] for v in node['track'][t] if 'name' in v]
            report['track'][t] = sorted(set(prop))
        self.report['default'] = report
    
    
    def load_model(self, node):
        for node_name, node_value in node.iteritems():
            node_value['name'] = node_name
            space = Enumeration(self, node_value)
            self.model[node_name] = space
            space.load()
    
    
    def load_service(self, node):
        for k,v in node.iteritems():
            v['name'] = k
            self.service[k] = v
    
    
    def load_prototype(self, node):
        for block_name, block_value in node.iteritems():
            self.prototype[block_name] = {}
            for node_name, node_value in block_value.iteritems():
                node_value['name'] = node_name
                space = PrototypeSpace(self, node_value)
                self.prototype[block_name][node_name] = space
                space.load()
    
    
    def load_reports(self, node):
        for k,v in node.iteritems():
            self.report[k] = v
    
    
    def load_profiles(self, node):
        for name, profile in node.iteritems():
            profile['name'] = name
            for action in ('tag', 'rename', 'extract', 'pack', 'update', 'transcode'):
                if action not in profile:
                    profile[action] = self.profile['default'][action]
            self.profile[name] = profile
    
    
    def load_kinds(self, node):
        for kind_name, kind in node.iteritems():
            kind['name'] = kind_name
            self.kind[kind_name] = kind
    
    
    def load_rules(self, node):
        for rule in node: self._load_rule(rule)
    
    
    def load_repositories(self, node):
        for name, repository in node.iteritems():
            self.repository[name] = repository
            repository['name'] = name
            
            if 'rule' in repository:
                self.load_rules(repository['rule'])
                
            if 'volume' in repository:
                for k, volume in repository['volume'].iteritems():
                    volume['name'] = k
                    volume['host'] = repository['name']
                    volume['domain'] = repository['domain']
                    volume['virtual path'] = u'/{0}'.format(volume['name'])
                    self.volume[volume['name']] = volume
                    
                    if 'alias' not in volume: volume['alias'] = []
                    if 'scan' not in volume: volume['scan'] = True
                    if 'index' not in volume: volume['index'] = True
                    
                    # Absolute path defined on a volume always takes precedence
                    # otherwise default to <base>/<volume name>
                    if 'path' not in volume:
                        volume['path'] = os.path.join(repository['base']['path'], volume['name'])
                        
                    # The real path is a singularity for comparing a path to the volume
                    volume['real path'] = os.path.realpath(volume['path'])
                    
                    # Build the alias set for the volume
                    aliases = set()
                    if 'alias' in repository['base']:
                        for alias in repository['base']['alias']:
                            aliases.add(os.path.join(alias, volume['name']))
                    aliases.add(volume['path'])
                    aliases.add(os.path.realpath(volume['path']))
                    for alias in volume['alias']:
                        aliases.add(alias)
                        aliases.add(os.path.realpath(alias))
                    volume['alias'] = tuple(sorted(aliases))
                    
                    for alias in volume['alias']:
                        if alias not in self.lookup['volume']:
                            self.lookup['volume'][alias] = volume
                        else:
                            self.log.error('Alias %s for %s already mapped to volume %s', alias, volume['name'], self.lookup['volume'][alias]['name'])
    
    
    def _load_rule(self, rule):
        for branch in rule['branch']:
            if 'match' in branch:
                flags = re.UNICODE
                if 'flags' in branch['match']: flags |= branch['match']['flags']
                branch['match']['pattern'] = re.compile(branch['match']['expression'], flags)
            if 'decode' in branch:
                flags = re.UNICODE
                if 'flags' in branch['decode']: flags |= branch['decode']['flags']
                for d in branch['decode']: d['pattern'] = re.compile(d['expression'], flags)
                
        for provide in rule['provides']:
            if provide not in self.rule:
                self.rule[provide] = []
            self.rule[provide].append(rule)
    
    
    def _load_dynamic_rules(self):
        # default host
        rule = {
            'name':'default host',
            'provides':set(('host',)),
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
            'provides':set(('language',)),
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
            'provides':set(('volume path', 'domain')),
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
            'provides':set(('cache root',)),
            'branch':[
                {
                    'apply':({'property':'cache root', 'value':self.repository[self.host]['cache']['path']},),
                }
            ],
        }
        self._load_rule(rule)
        
        rule = {
            'name':'container for kind',
            'provides':set(('container',)),
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
            result = Ontology(self)
            result['url'] = url
            
            parsed = urlparse.urlparse(url)
            if parsed.path:
                result['path'] = parsed.path
                
                o = Ontology(self)
                o['file name'] = os.path.basename(parsed.path)
                if 'media kind' in o:
                    result['scheme'] = parsed.scheme or u'file'
                    result['host'] = parsed.hostname or self.host
                    for k,v in o.iteritems():
                        if k != 'file name': result[k] = v
                            
                    if result['host'] in self.repository:
                        if result['scheme'] == 'file':
                            for volume in self.repository[result['host']]['volume'].values():
                                if os.path.commonprefix([volume['path'], parsed.path]) == volume['path']:
                                    result['volume'] = volume['name']
                                    break
                                    
                        elif result['scheme'] == self.runtime['resource scheme']:
                            for volume in self.repository[result['host']]['volume'].values():
                                if os.path.commonprefix([volume['virtual path'], parsed.path]) == volume['virtual path']:
                                    result['volume'] = volume['name']
                                    break
                                    
                    # Deep inference
                    prefix = os.path.dirname(parsed.path)
                    if result['kind'] in self.kind_with_language:
                        prefix, iso = os.path.split(prefix)
                        if self.model['language'].find(iso):
                            result['language'] = iso
                             
                    if prefix:
                        if result['media kind'] == 'tvshow':
                            prefix = os.path.dirname(prefix)
                            if prefix: prefix = os.path.dirname(prefix)
                            
                    if prefix:
                        profile = os.path.basename(prefix)
                        if profile: result['profile'] = profile
                        
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
        result = None
        if command in self.available['command']:
            c = self.command[command]
            result = [ c['path'], ]
        else:
            log.warning(u'Command %s is unavailable', command)
        return result
    
    
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
    
    
    
    # Text processing
    def remove_accents(self, value):
        result = None
        if value:
            nkfd_form = unicodedata.normalize('NFKD', value)
            result = self.runtime['empty string'].join([c for c in nkfd_form if not unicodedata.combining(c)])
        return result
    
    
    def detect_encoding(self, content):
        if self.universal_detector is None:
            from chardet.universaldetector import UniversalDetector
            self.universal_detector = UniversalDetector()
        self.universal_detector.reset()
        for line in content:
            self.universal_detector.feed(line)
            if self.universal_detector.done:
                break
        self.universal_detector.close()
        return self.universal_detector.result
    
    
    def simplify(self, value):
        result = None
        if value:
            v = self.expression['whitespace'].sub(u' ', value).strip()
            if v:
                result = self.expression['characters to exclude from filename'].sub(self.runtime['empty string'], v)
                if not result:
                    result = v
                    result = result.replace(u'?', u'question mark')
                    result = result.replace(u'*', u'asterisk')
                    result = result.replace(u'.', u'period')
                    result = result.replace(u':', u'colon')
                result = self.remove_accents(result)
                result = result.lower()
        return result
    
    
    
    @property
    def format(self):
        return self.state['format']
    
    
    @property
    def kind_with_language(self):
        return self.runtime['kind with language']
    
    
    def load_format(self, node):
        self.format['wrap width'] = node['wrap']
        self.format['indent width'] = node['indent']
        self.format['margin width'] = node['margin']
        
        self.format['indent'] = u'\n' + u' ' * self.format['indent width']
        self.format['info title display'] = u'\n\n\n{1}[{{0:-^{0}}}]'.format (
            self.format['wrap width'] + self.format['indent width'],
            u' ' * self.format['margin width']
        )
        self.format['info subtitle display'] = u'\n{1}[{{0:^{0}}}]\n'.format (
            self.format['indent width'] - self.format['margin width'] - 3,
            u' ' * self.format['margin width']
        )
        self.format['key value display'] = u'{1}{{0:-<{0}}}: {{1}}'.format (
            self.format['indent width'] - self.format['margin width'] - 2,
            u' ' * self.format['margin width']
        )
        self.format['value display'] = u'{0}{{0}}'.format(u' ' * self.format['margin width'])
    

