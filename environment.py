# -*- coding: utf-8 -*-

import os
import re
import logging
import copy
import unicodedata
import urlparse
from subprocess import Popen, PIPE
from datetime import timedelta

import config
from ontology import Ontology
from asset import AssetCache
from db import EntityManager

from model import Timestamp

class Environment(object):
    def __init__(self):
        self.log = logging.getLogger('environment')
        
        from config.runtime import runtime as runtime_config
        self.runtime = runtime_config
        
        self.configuration = None
        self.ontology = None
        self.em = None
        self.caption_filter_cache = CaptionFilterCache(self)
        self.universal_detector = None
        
        self.lookup = {
            'model':{},
            'volume':{},
        }
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
        }
        
        self.load()
    
    
    def __unicode__(self):
        return unicode(u'{}:{}'.format(self.domain, self.host))
    
    
    # Properties
    @property
    def verbosity(self):
        return self.runtime['log level'][self.ontology['verbosity']]
    
    
    @property
    def system(self):
        return self.state['system']
    
    
    @property
    def prototype(self):
        return self.state['prototype']
    
    
    @property
    def model(self):
        return self.state['model']
    
    
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
    def format(self):
        return self.state['format']
    
    
    @property
    def repository(self):
        return self.state['repository']
    
    
    @property
    def volume(self):
        return self.state['volume']
    
    
    @property
    def expression(self):
        return self.state['expression']
    
    
    @property
    def service(self):
        return self.runtime['service']
    
    
    @property
    def profile(self):
        return self.state['profile']
    
    
    @property
    def kind(self):
        return self.state['kind']
    
    
    @property
    def kind_with_language(self):
        return self.runtime['kind with language']
    
    
    # Loading...
    def load(self):
        
        # start from the base user conf
        from config.base import base as base_config
        self.configuration = copy.deepcopy(base_config)
        self.load_system(self.configuration['system'])
        
        # Override the default home folder from env if specified
        env_home = os.getenv('MPK_HOME')
        if env_home and os.path.exists(env_home):
            self.system['home'] = env_home
            
        if self.home:
            self.load_external_config(os.path.join(self.home, 'mpk.conf'))
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
        self._load_default_host_rule()
        self._load_default_language_rule()
        self._load_volume_location_rule()
        self._load_cache_location_rule()
        self._load_container_rule()
        self.configuration['playback']['aspect ratio'] = float(float(self.configuration['playback']['width'])/float(self.configuration['playback']['height']))
        
        o = Ontology(self, self.repository[self.host]['mongodb'])
        self.em = EntityManager(self, o)
    
    
    def load_external_config(self, path):
        if path and os.path.exists(path):
            path = os.path.abspath(path)
            try:
                external = eval(open(path).read())
                self.log.debug('Load external config file %s', path)
                self.configuration = dict(self.configuration.items() + external.items())
            except IOError as ioerr:
                self.log.warning('Failed to load config file %s', path)
                self.log.debug(ioerr)
    
    
    def load_system(self, config):
        for k,v in config.iteritems():
            self.system[k] = v
    
    
    def load_expressions(self, config):
        for expression in config:
            if 'flags' in expression and expression['flags']:
                self.expression[expression['name']] = re.compile(expression['definition'], expression['flags'])
            else:
                self.expression[expression['name']] = re.compile(expression['definition'])
    
    
    def load_commands(self, config):
        for command in config:
            self.command[command['name']] = command
            if command['binary']:
                # check the command exists and get an absolute path for it
                c = ['which', command['binary']]
                proc = Popen(c, stdout=PIPE, stderr=PIPE)
                report = proc.communicate()
                if report[0]:
                    command['path'] = report[0].splitlines()[0]
        self.available['command'] = set([i['name'] for i in self.command.values() if 'path' in i])
    
    
    def load_actions(self, config):
        for action in config:
            self.action[action['name']] = action
            action['active'] = True
            if 'depend' in action:
                action['depend'] = set(action['depend'])
                if not action['depend'].issubset(self.available['command']):
                    action['active'] = False
                    self.log.debug(u'Action %s has unsatisfied dependencies: %s', 
                        action['name'], 
                        u', '.join(list(action['depend'] - self.available['command']))
                    )
        self.available['action'] = set([i['name'] for i in self.action.values() if i['active']])
    
    
    def load_info(self, config):
        # Load a default report profile
        report = {
            'file':sorted(set([ v['name'] for v in config['file'] if 'name' in v])),
            'tag':sorted(set([ v['name'] for v in config['tag'] if 'name' in v])),
            'track':{},
        }
        common = [ v['name'] for v in config['track']['common'] if 'name' in v]
        for t in ('audio', 'video', 'text', 'image'):
            prop = common + [ v['name'] for v in config['track'][t] if 'name' in v]
            report['track'][t] = sorted(set(prop))
        self.report['default'] = report
    
    
    def load_model(self, config):
        for node_name, node_value in config.iteritems():
            node_value['name'] = node_name
            space = Enumeration(self, node_value)
            self.model[node_name] = space
            space.load()
    
    
    def load_service(self, config):
        for k,v in config:
            v['name'] = k
            self.service[k] = v
    
    
    def load_prototype(self, config):
        for block_name, block_value in config.iteritems():
            self.prototype[block_name] = {}
            for node_name, node_value in block_value.iteritems():
                node_value['name'] = node_name
                space = PrototypeSpace(self, node_value)
                self.prototype[block_name][node_name] = space
                space.load()
    
    
    def load_reports(self, config):
        for k,v in config.iteritems():
            self.report[k] = v
    
    
    def load_profiles(self, config):
        for name, profile in config.iteritems():
            profile['name'] = name
            for action in ('tag', 'rename', 'extract', 'pack', 'update', 'transcode'):
                if action not in profile:
                    profile[action] = self.profile['default'][action]
            self.profile[name] = profile
    
    
    def load_kinds(self, config):
        for kind_name, kind in config.iteritems():
            kind['name'] = kind_name
            self.kind[kind_name] = kind
    
    
    def load_rules(self, config):
        for rule in config: self._load_rule(rule)
    
    
    def load_repositories(self, config):
        for name, repository in config.iteritems():
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
        if 'rule' not in self.lookup:
            self.lookup['rule'] = {'name':{}, 'provide':{}, }
            
        if rule['name'] not in self.lookup['rule']['name']:
            self.lookup['rule']['name'][rule['name']] = rule
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
                if provide not in self.lookup['rule']['provide']:
                    self.lookup['rule']['provide'][provide] = []
                self.lookup['rule']['provide'][provide].append(rule)
        else:
            self.log.warning('Refusing to redefine rule %s.')
    
    
    def _load_default_host_rule(self):
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
    
    
    def _load_volume_location_rule(self):
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
    
    
    def _load_cache_location_rule(self):
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
        
    
    
    def _load_container_rule(self):
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
    
    
    def _load_default_language_rule(self):
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
        
    
    
    def load_format(self, config):
        self.format['wrap width'] = config['wrap']
        self.format['indent width'] = config['indent']
        self.format['margin width'] = config['margin']
        
        self.format['indent'] = u'\n' + u' ' * self.format['indent width']
        self.format['info title display'] = u'\n\n\n{1}[{{0:-^{0}}}]'.format(
            self.format['wrap width'] + self.format['indent width'],
            u' ' * self.format['margin width']
        )
        self.format['info subtitle display'] = u'\n{1}[{{0:^{0}}}]\n'.format(
            self.format['indent width'] - self.format['margin width'] - 3,
            u' ' * self.format['margin width']
        )
        self.format['key value display'] = u'{1}{{0:-<{0}}}: {{1}}'.format(
            self.format['indent width'] - self.format['margin width'] - 2,
            u' ' * self.format['margin width']
        )
        self.format['value display'] = u'{0}{{0}}'.format(u' ' * self.format['margin width'])
    
    
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
                        if self.env.model['language'].find(iso):
                            result['language'] = iso
                             
                    if prefix:
                        if result['media kind'] == 'tvshow':
                            prefix = os.path.dirname(prefix)
                            if prefix: prefix = os.path.dirname(prefix)
                            
                    if prefix:
                        profile = os.path.basename(prefix)
                        if profile: result['profile'] = profile
                        
            return result
    
    
    # Path manipulation
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
    
    
    def scan_for_related(self, properties):
        result = None
        if properties:
            result = []
            self.log.debug(u'Scanning repository for file related to %s', properties)
            for v in self.repository['volume'].values():
                if v['scan']:
                    for p in self.profile.values():
                        for k in p['kind']:
                            if k in self.kind_with_language:
                                for l in self.model['language'].element.keys():
                                    related = copy.deepcopy(properties)
                                    related['volume'] = v['name']
                                    related['kind'] = k
                                    related['profile'] = p['name']
                                    related['language'] = l
                                    related_path = self.encode_canonic_path(related)
                                    if os.path.exists(related_path):
                                        result.append(related)
                                        self.log.debug('Discovered %s', related_path)
                            else:
                                related = copy.deepcopy(properties)
                                related['volume'] = v['name']
                                related['kind'] = k
                                related['profile'] = p['name']
                                related_path = self.encode_canonic_path(related)
                                if os.path.exists(related_path):
                                    result.append(related)
                                    self.log.debug('Discovered %s', related_path)
        return result
    
    
    def canonic_path_for(self, path):
        result = path
        real_path = os.path.realpath(os.path.abspath(path))
        for vol_path, vol in self.lookup['volume'].iteritems():
            if os.path.commonprefix([vol_path, real_path]) == vol_path:
                result = real_path.replace(vol_path, vol['path'])
                break
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
    
    
    def is_path_exists(self, path):
        if path is not None and os.path.exists(path): return True
        else: return False
    
    
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
    
    
    # Command execution
    def initialize_command(self, command, log):
        result = None
        if command in self.available['command']:
            c = self.command[command]
            result = [ c['path'], ]
        else:
            log.warning(u'Command %s is unavailable', c['name'])
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
    
    
    def remove_accents(self, value):
        result = None
        if value:
            nkfd_form = unicodedata.normalize('NFKD', value)
            result = self.runtime['empty string'].join([c for c in nkfd_form if not unicodedata.combining(c)])
        return result
    
    
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
    
    
    def encode_subler_key_value(self, key, value):
        m = self.configuration.lookup['name']['tag'][key]
        if 'subler' in m:
            pkey = m['subler']
            if m['type'] == 'enum':
                pvalue = self.configuration.lookup['code'][m['atom']][value]['print']
            elif m['type'] in ('string', 'list', 'dict'):
                if m['type'] == 'list':
                    pvalue = u', '.join(value)
                elif m['type'] == 'dict':
                    pvalue = u', '.join(['{0}:{1}'.format(k,v) for k,v in value.iteritems()])
                else:
                    if key == 'language':
                        pvalue = self.configuration.lookup['iso3t']['language'][value]['print']
                    else:
                        pvalue = unicode(value)
                pvalue = pvalue.replace(u'{',u'&#123;').replace(u'}',u'&#125;').replace(u':',u'&#58;')
                
            elif m['type'] == 'bool':
                if value: pvalue = u'yes'
                else: pvalue = u'no'
            elif m['type'] == 'date':
                pvalue = value.strftime('%Y-%m-%d %H:%M:%S')
            elif m['type'] == 'int':
                pvalue = unicode(value)
            else:
                pvalue = value
                
        return u'{{{0}:{1}}}'.format(pkey, pvalue)
    
    
    
    
    


# Caption filter
class CaptionFilter(object):
    def __init__(self, config):
        self.log = logging.getLogger('Filter pipeline')
        self.expression = []
        self.action = config['action']
        self.scope = config['scope']
        self.ignorecase = config['ignore case']
        
        option = re.UNICODE
        if self.ignorecase:
            option = option|re.IGNORECASE
        if self.scope == 'slide':
            option = option|re.MULTILINE
            
        for e in config['expression']:
            try:
                if self.action == 'replace':
                    self.expression.append((re.compile(e[0], option), e[1]))
                elif self.action == 'drop':
                    self.expression.append(re.compile(e,option))
            except:
                self.log.warning(u'Failed to load expression %s', e)
    
    
    @property
    def valid(self):
        return len(self.expression) > 0
    
    
    def filter(self, slide):
        result = slide is not None and slide.valid
        if result:
            if self.action == 'replace':
                if self.scope == 'line':
                    for e in self.expression:
                        original = slide.content
                        slide.clear()
                        for line in original:
                            filtered = e[0].sub(e[1], line)
                            slide.add(filtered)
                            
                            # This should be commented out in production
                            if line != filtered:
                                self.log.debug(u'Replaced "%s" --> "%s"', line, filtered)
                                
                        if not slide.valid:
                            break
                            
                elif self.scope == 'slide':
                    content = u'\n'.join(slide.lines)
                    slide.clear()
                    for e in self.expression:
                        filtered = e[0].sub(e[1], content)
                        
                         # This should be commented out in production
                        if content != filtered:
                            self.log.debug(u'Replaced "%s" --> "%s"', content, filtered)
                            
                        content = filtered.strip()
                        if not content:
                            break
                    if content:
                        for line in content.split(u'\n'):
                            slide.append(line)
                            
            elif self.action == 'drop':
                if self.scope == 'line':
                    original = slide.content
                    slide.clear()
                    for line in original:
                        keep = True
                        for e in self.expression:
                            if e.search(line) is not None:
                                self.log.debug(u'Drop %s', line)
                                keep = False
                                break
                        if keep:
                            slide.add(line)
                            
                elif self.scope == 'slide':
                    keep = True
                    for line in slide.content:
                        for e in self.expression:
                            if e.search(line) is not None:
                                self.log.debug(u'Drop \n%s', u'\n'.join(slide.content))
                                keep = False
                                break
                        if not keep:
                            slide.clear()
                            break
            result = slide.valid
        return result
    


class CaptionFilterCache(dict):
    def __init__(self, env, *args, **kw):
        dict.__init__(self, *args, **kw)
        self.log = logging.getLogger('Subtitle Filter Cache')
        self.env = env
    
    
    def __contains__(self, key):
        self.resolve(key)
        return dict.__getitem__(self, key) is not None
    
    
    def __delitem__(self, key):
        if dict.__contains__(self, key):
            dict.__delitem__(self, key)
    
    
    def __missing__(self, key):
        self.resolve(key)
        return dict.__getitem__(self, key)
    
    
    def resolve(self, key):
        if not dict.__contains__(self, key):
            if key in self.env.configuration['subtitles']['filters']:
                o = CaptionFilter(self.env.configuration['subtitles']['filters'][key])
                if o.valid:
                    self.log.debug(u'Loaded %s filter pipeline', key)
                    dict.__setitem__(self, key, o)
                else:
                    self.log.error(u'Failed to load %s filter pipeline', key)
                    dict.__setitem__(self, key, None)
            else:
                self.log.error(u'%s subtitle filter is not defined', key)
                dict.__setitem__(self, key, None)
    
    


# Generic Space / Element model
class Space(object):
    def __init__(self, env, node):
        self.log = logging.getLogger('Space')
        self.env = env
        self.node = node
        self.element = None
        self._synonym = None
        
        if 'default' not in self.node:
            self.node['default'] = {}
            
        if 'enabled' not in self.default:
            self.default['enabled'] = True
    
    
    @property
    def key(self):
        return self.node['name']
    
    
    @property
    def synonym(self):
        if self._synonym is None:
            self._synonym = {}
            for synonym in self.node['synonym']:
                for e in self.element.values():
                    if e.node[synonym] is not None and \
                    e.node[synonym] not in self._synonym:
                        self._synonym[e[synonym]] = e
        return self._synonym
    
    
    @property
    def default(self):
        return self.node['default']
    
    
    def find(self, key):
        if key is not None and key in self.element:
            return self.element[key]
        else: return None
    
    
    def get(self, key):
        element = self.search(key)
        if element is not None: return element.name
        else: return None
    
    
    def search(self, value):
        if value is not None and value in self.synonym:
            return self.synonym[value]
        else: return None
    
    
    def parse(self, value):
        element = self.search(value)
        if element is not None: return element.key
        else: return None
    
    


class Element(object):
    def __init__(self, space, node):
        self.log = logging.getLogger('Element')
        self.space = space
        self.node = node
        
        if self.node is not None and \
        'key' in self.node and \
        'name' in self.node:
            # Load defaults
            for field in self.default:
                if field not in self.node:
                    self.node[field] = self.default[field]
    
    
    @property
    def env(self):
        return self.space.env
    
    
    @property
    def default(self):
        return self.space.default
    
    
    @property
    def enabled(self):
        return self.node is not None and self.node['enabled']
    
    
    @property
    def key(self):
        return self.node['key']
    
    
    @property
    def name(self):
        return self.node['name']
    


# Prototype model
class PrototypeSpace(Space):
    def __init__(self, env, node):
        Space.__init__(self, env, node)
    
    
    def load(self):
        for e in self.node['element']:
            prototype = Prototype(self, e)
            if prototype.enabled:
                self.element[prototype.key] = prototype
    


class Prototype(Element):
    def __init__(self, space, node):
        Element.__init__(self, space, node)
        c = lambda x: x
        f = lambda x: x
        
        # Don't bother loading the cast function if not enabled
        if self.enabled:
            if self.node['type']  == unicode:
                c = self._cast_unicode
                f = self._format_unicode
            elif self.node['type'] == int:
                c = self._cast_number
                f = self._format_int
            elif self.node['type'] == float:
                c = self._cast_number
                f = self._format_float
            elif self.node['type'] == 'date':
                c = self._cast_date
                f = self._format_date
            elif self.node['type'] == bool:
                c = self._cast_boolean
                f = self._format_boolean
            elif self.node['type'] == 'enum':
                c = self._cast_enum
                f = self._format_enum
                
            if not self.node['plural']:
                self._cast = c
                self._format = f
            else:
                if self.node['plural'] == 'list':
                    self._format = lambda x: self._format_list(x, f)
                    self._cast = lambda x: self._cast_list(x, c)
                elif self.node['plural'] == 'dict':
                    self._format = lambda x: self._format_dict(x, f)
                    self._cast = lambda x: self._cast_dict(x, c)
                    
            if not self.node['auto cast']:
                self._cast = lambda x: x
    
    
    def cast(self, value):
        if value is not None:
            return self._cast(value)
        else:
            return None
    
    
    def format(self, value):
        if value is not None:
            return self._format(value)
        else:
            return None
    
    
    
    def _wrap(self, value):
        result = value
        if len(value) > self.env.format['wrap width']:
            lines = textwrap.wrap(value, self.env.format['wrap width'])
            result = self.env.format['indent'].join(lines)
        return result
    
    
    def _format_byte_as_iec_60027_2(self, value):
        p = 0
        v = float(value)
        while v > 1024.0 and p < 4:
            p += 1
            v /= 1024.0
        return u'{0:.2f} {1}'.format(v, self.env.model['binary iec 60027 2'].get(p))
    
    
    def _format_bit_as_si(self, value):
        p = 0
        v = float(value)
        while v > 1000.0 and p < 4:
            p += 1
            v /= 1000.0
        return u'{0:.2f} {1}'.format(v, self.env.model['decimal si'].get(p))
    
    
    def _format_timecode(self, value):
        t = Timestamp(Timestamp.SRT)
        t.millisecond = value
        return t.timecode
    
    
    def _format_enum(self, key):
        return self.env.model[self.node['enumeration']].get(key)
    
    
    def _format_float(self, value):
        return u'{0:.3f}'.format(value)
    
    
    def _format_int(self, value):
        result = unicode(value)
        if 'format' in self.node:
            if self.node['format'] == 'bitrate':
                result = u'{0}/s'.format(self._format_bit_as_si(value))
                
            elif self.node['format'] == 'millisecond':
                result =  self._format_timecode(value)
                
            elif self.node['format'] == 'byte':
                result = self._format_byte_as_iec_60027_2(value)
                
            elif self.node['format'] == 'bit':
                result = u'{0} bit'.format(value)
                
            elif self.node['format'] == 'frequency':
                result = u'{0} Hz'.format(value)
                
            elif self.node['format'] == 'pixel':
                result = u'{0} px'.format(value)
                
        return result
    
    
    def _format_boolean(self, value):
        if value is True: return u'yes'
        else: return u'no'
    
    
    def _format_date(self, value):
        return unicode(value)
    
    
    def _format_list(self, value, formatter):
        if value:
            return u', '.join([ formatter(v) for v in value ])
        else:
            return None
    
    
    def _format_dict(self, value, formatter):
        if value:
            return u', '.join([ u'{0}:{1}'.format(k,formatter(v)) for k,v in value.iteritems() ])
        else:
            return None
    
    
    def _format_unicode(self, value):
        return value
    
    
    def _cast_enum(self, value):
        return self.env.model[self.node['enumeration']].parse(value)
    
    
    def _cast_number(self, value):
        result = None
        try:
            result = self.node['type'](value)
        except ValueError as error:
            self.log.error(u'Failed to decode: %s as %s', value, unicode(self.node['type']))
        return result
    
    
    def _cast_unicode(self, value):
        result = unicode(value.strip())
        if not result:
            result = None
        if result and self.node['unescape xml']:
            result = result.replace(u'&quot;', u'"')
        return result
    
    
    def _cast_date(self, value):
        # Datetime conversion, must have at least a Year, Month and Day. 
        # If Year is present but Month and Day are missing they are set to 1
        
        result = None
        match = self.env.expression['full utc datetime'].search(value)
        if match:
            parsed = dict([(k, int(v)) for k,v in match.groupdict().iteritems() if k != u'tzinfo' and v is not None])
            if u'month' not in parsed:
                parsed[u'month'] = 1
            if u'day' not in parsed:
                parsed[u'day'] = 1
            try:
                result = datetime(**parsed)
            except TypeError, ValueError:
                self.log.debug(u'Failed to decode datetime %s', value)
                result = None
        else:
            self.log.debug(u'Failed to parse datetime %s', value)
            result = None
        return result
    
    
    def _cast_boolean(self, value):
        result = False
        if self.env.expression['true value'].search(value) is not None:
            result = True
        return result
    
    
    def _cast_plist(self, value):
        # Clean and parse plist into a dictionary
        result = value.replace(u'&quot;', u'"')
        result = self.env.expression['clean xml'].sub(u'', result).strip()
        result = plistlib.readPlistFromString(result.encode('utf-8'))
        return result
    
    
    def _cast_list(self, value, caster):
        result = None
        if 'plural format' in self.node:
            literals = None
            if self.node['plural format'] == 'mediainfo value list':
                if self.env.expression['mediainfo value list'].match(value):
                    literals = value.split(u'/')
                else:
                    self.log.error(u'Could not parse list %s', value)
            if literals:
                result = [ caster(l) for l in literals ]
        if result:
            result = [ v for v in result if v is not None ]
        if not result:
            result = None
        return result
    
    
    def _cast_dict(self, value, caster):
        result = None
        if 'plural format' in self.node:
            if self.node['plural format'] == 'mediainfo key value list':
                if self.env.expression['mediainfo value list'].match(value):
                    literals = value.split(u'/')
                    result = {}
                    for literal in literals:
                        pair = literal.split(u'=')
                        if len(pair) == 2:
                            result[pair[0].strip()] = caster(pair[1])
                else:
                    self.log.error(u'Could not parse dictionary %s', value)
                    result = None
        if not result:
            result = None
        return result
    


# Enumeration model
class Enumeration(Space):
    def __init__(self, env, node):
        Space.__init__(self, env, node)
    
    
    def load(self):
        for e in self.node['element']:
            element = Element(self, e)
            if element.enabled:
                self.element[element.key] = element
    

