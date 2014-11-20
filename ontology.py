# -*- coding: utf-8 -*-

import logging
import copy
import re
import unicodedata
import plistlib
import hashlib

from datetime import datetime

check = lambda node: 'enable' not in node or node['enable']

class Ontology(dict):
    def __init__(self, env, namespace,  *args, **kw):
        dict.__init__(self, *args, **kw)
        self.log = logging.getLogger('Ontology')
        self.env = env
        self.namespace = self.env.namespace[namespace]
        
        # Make sure no empty concepts slipped in...
        #for key in dict.keys(self):
        #    if dict.__getitem__(self, key) is None:
        #        dict.__delitem__(self, key)
                
        for key in dict.keys(self):
            element = dict.__getitem__(self, key)
            if element is None:
                dict.__delitem__(self, key)
            else:
                prototype = self.namespace.find(key)
                if prototype is not None:
                    if prototype.type == 'embed':
                        if prototype.plural is None:
                            # a reference to an embedded ontology
                            if not isinstance(element, Ontology):
                                dict.__setitem__(self, key, Ontology(self.env, prototype.node['namespace'], element))
                                
                        if prototype.plural == 'list':
                            # a list of references to embedded ontologies
                            for i,e in enumerate(element):
                                if not isinstance(e, Ontology):
                                    element[i] = Ontology(self.env, prototype.node['namespace'], e)
                else:
                    self.log.warning(u'Element %s is missing a Prototype in %s', key, dict.keys(self))
                    
        self.kernel = dict(self)
        self.dependency = {}
        
    def __unicode__(self):
        return unicode(self.kernel)
        
    @classmethod
    def clone(cls, other):
        o = cls(other.env, other.namespace.key, other.kernel)
        return o
        
    @property
    def node(self):
        return self.kernel
        
    def match(self, fact):
        result =  all((k in self and self[k] == v) for k,v in fact.iteritems())
        return result
        
    def project(self, namespace):
        o = Ontology(self.env, namespace)
        for k,v in self.kernel.iteritems():
            if o.namespace.contains(k):
                o[k] = v
        return o
        
    def __setitem__(self, key, value):
        if key is not None:
            # Start by removing the concept to clean any implicit concepts
            # This also has the effect that setting a concept to None will effectively remove the concept,
            # so concepts can be assumed to not be None, but setting one to None removes it
            if dict.__contains__(self, key):
                self.__delitem__(key)
                
            # Concepts set by __setitem__ are considered kernel concepts
            if value is not None:
                # self.log.debug(u'Set kernel concept %s', unicode({key:value}))
                self.kernel[key] = value
                dict.__setitem__(self, key, value)
                
    def __delitem__(self, key):
        # Even if the key is not present
        # We remove it's dependencies
        if key in self.dependency:
            for d in self.dependency[key]:
                if dict.__contains__(self, d):
                    self.__delitem__(d)
            del self.dependency[key]
            
        # Silently ignore del for keys that are not present
        if dict.__contains__(self, key):
            # self.log.debug(u'Removed %s', unicode(key))
            if key in self.kernel:
                del self.kernel[key]
            dict.__delitem__(self, key)
            
    def __contains__(self, key):
        self._resolve(key)
        return dict.__contains__(self, key)
        
    def __missing__(self, key):
        self._resolve(key)
        return self.get(key)
        
    def clear(self):
        self.kernel.clear()
        self.dependency.clear()
        dict.clear(self)
        
    def coalesce(self, source, target):
        k,v = self.namespace.merge(target, self[target], self[source])
        self.__setitem__(k, v)
        
    def merge(self, key, value):
        if key:
            k,v = self.namespace.merge(key, self[key], value)
            self.__setitem__(k, v)
            
    def merge_all(self, mapping):
        for k,v in mapping.iteritems():
            self.merge(k,v)
            
    def decode(self, synonym, value, axis=None):
        if synonym and value is not None:
            k,v = self.namespace.decode(synonym, value, axis)
            self.__setitem__(k, v)
            
    def decode_all(self, mapping, axis=None):
        if not isinstance(mapping, dict):
            self.log.debug(u'Failed to decode %s because the mapping provided is not a dictionary', mapping)
        else:
            for k,v in mapping.iteritems():
                self.decode(k,v, axis)
                
    def _resolve(self, key):
        if not dict.__contains__(self, key):
            if key in self.namespace.deduction.dependency:
                for rule in self.namespace.deduction.dependency[key]:
                    for branch in rule.branch:
                        
                        # Check preconditions are satisfied
                        taken = True
                        if 'requires' in branch:
                            unsatisfied = branch['requires'].difference(self)
                            while unsatisfied:
                                u = unsatisfied.pop()
                                self._resolve(u)
                                if dict.__contains__(self, u):
                                    unsatisfied = branch['requires'].difference(self)
                                else: unsatisfied = None
                            if not branch['requires'].issubset(self):
                                taken = False
                        taken = taken and ('equal' not in branch or all((dict.__contains__(self, k) and dict.__getitem__(self, k) == v) for k,v in branch['equal'].iteritems()))
                        taken = taken and ('match' not in branch or branch['match']['pattern'].match(dict.__getitem__(self, branch['match']['property'])))
                        
                        if taken:
                            if 'apply' in branch:
                                for x in branch['apply']:
                                    if not dict.__contains__(self, x['property']):
                                    
                                        # digest filters
                                        if 'digest' in x and 'algorithm' in x:
                                            if x['algorithm'] == 'sha1':
                                                dict.__setitem__(self, x['property'], hashlib.sha1(self[x['digest']].encode('utf-8')).hexdigest())
                                            elif x['algorithm'] == 'umid':
                                                dict.__setitem__(self, x['property'], Umid(*[self[i] for i in x['digest']]).code)
                                                
                                        if 'reference' in x:
                                            if 'member' in x:
                                                prototype = self.namespace.find(x['property'])
                                                if prototype:
                                                    try:
                                                        dict.__setitem__(self, x['property'], getattr(self[x['reference']], x['member']))
                                                    except AttributeError as e:
                                                        self.log.error(u'Failed to locate member %s for %s: %s', x['member'], x['property'], e)
                                                        
                                            elif 'datetime format' in x:
                                                prototype = self.namespace.find(x['property'])
                                                if prototype:
                                                    dict.__setitem__(self, x['property'], prototype.cast(self[x['reference']].strftime(x['datetime format'])))
                                            else:
                                                dict.__setitem__(self, x['property'], self[x['reference']])
                                                
                                        if 'format' in x:
                                            dict.__setitem__(self, x['property'], x['format'].format(**self))
                                            
                                        elif 'value' in x:
                                            dict.__setitem__(self, x['property'], x['value'])
                                            
                            if 'decode' in branch:
                                for x in branch['decode']:
                                    match = x['pattern'].search(dict.__getitem__(self, x['property']))
                                    if match is not None:
                                        parsed = match.groupdict()
                                        for synonym,raw in parsed.iteritems():
                                            k,v = self.namespace.decode(synonym, raw)
                                            if k is not None and v is not None:
                                                dict.__setitem__(self, k, v)
                                                
                            # Mark all the atom the rule provieds as depending on the requirements
                            # This means removing the requirement also removes the dependent atom
                            if 'requires' in branch:
                                for req in branch['requires']:
                                    if req not in self.dependency:
                                        self.dependency[req] = copy.deepcopy(rule.provide)
                                    else:
                                        self.dependency[req] = self.dependency[req].union(rule.provide)
                            break
                            
    def normalize(self):
        for action in self.namespace.node['normalize']:
            # coalescing several elements into one        
            if action['action'] == 'coalesce':
                target = action['target']
                for source in action['source']:
                    if source in self:
                        self.coalesce(source, target)
                        if not source == target:
                            self.__delitem__(source)
                            
            # complementing embed elements 
            elif action['action'] == 'complement':
                if action['element'] in self:
                    prototype = self.namespace.find(action['element'])
                    if prototype:
                        if prototype.type == 'embed':
                            if prototype.plural:
                                if prototype.plural == 'list':
                                    for e in self[action['element']]:
                                        for k,v in action['extention'].iteritems():
                                            e[k] = v
                            else:
                                for k,v in action['extention'].iteritems():
                                    self[action['element']][k] = v
                                    
        # recursively normalize embedded ontologies
        for key in dict.keys(self):
            element = dict.__getitem__(self, key)
            if element is not None:
                prototype = self.namespace.find(key)
                if prototype is not None:
                    if prototype.type == 'embed':
                        if prototype.plural is None:
                            # a reference to an embedded ontology
                            element.normalize()
                                
                        if prototype.plural == 'list':
                            # a list of references to embedded ontologies
                            for i,e in enumerate(element):
                                e.normalize()                    
                                    


class Space(object):
    def __init__(self, env, node):
        self.log = logging.getLogger('Space')
        self.env = env
        self._element = None
        self._synonym = None
        self._deduction = None
        self.node = {
            'default':{
                'enabled':True,
                'simplify':False,
                'unescape xml':False,
                'auto cast':True,
                'keyword':None,
                'plural':None,
                'atom':None,
                'tmdb':None,
                'rottentomatoes':None,
                'itunes':None,
                'mediainfo':None,
                'subler':None,
                'x264':None,
            },
            'synonym':[],
            'element':{},
            'rule':[],
            'normalize':[],
        }
        self.extend(node)
        
    def __unicode__(self):
        return self.key
        
    def extend(self, node):
        for k,v in node.iteritems():
            if k == 'key':
                self.node['key'] = node['key']
                
            if k in ['default', 'element']:
                if v: self.node[k].update(v)
                
            elif k in ['synonym', 'rule', 'normalize']:
                if v: self.node[k].extend(v)
                
    @property
    def key(self):
        return self.node['key']
        
    @property
    def element(self):
        if self._element is None:
            self._load_element()
        return self._element
        
    @property
    def synonym(self):
        if self._synonym is None:
            self._load_synonym()
        return self._synonym
        
    @property
    def deduction(self):
        if self._deduction is None:
            self._deduction = Deduction(self.env, self.node)
        return self._deduction
        
    @property
    def default(self):
        return self.node['default']
        
    def contains(self, key):
        return key is not None and key in self.element
        
    def find(self, key):
        # returns an element by key
        if key is not None and key in self.element:
            return self.element[key]
        else: return None
        
    def search(self, synonym, axis=None):
        element = None
        # returns an element by synonym
        if synonym is not None and 'synonym' in self.node:
            if axis is None:
                for x in self.node['synonym']:
                    if synonym in self.synonym[x]:
                        element = self.synonym[x][synonym]
                        break
            elif axis in self.node['synonym'] and synonym in self.synonym[axis]:
                element = self.synonym[axis][synonym]
        return element
        
    def parse(self, synonym, axis=None):
        # returns the key by synonym
        element = self.search(synonym, axis)
        if element is not None: return element.key
        else: return None
        
    def format(self, key):
        # returns an element name by key
        element = self.find(key)
        if element is not None: return element.name
        else: return None
        
    def map(self, key, synonym):
        if key is not None and synonym is not None and key in self.element:
            e = self.element[key]
            self.synonym[synonym] = e
            
    def add(self, key, node):
        if key is not None and node is not None:
            self.node['element'][key] = node
            self._element = None
            self._synonym = None
            
    def _load_element(self):
        pass
        
    def _load_synonym(self):
        self._synonym = {}
        if 'synonym' in self.node:
            for synonym in self.node['synonym']:
                self._synonym[synonym] = {}
                for e in self.element.values():
                    if e.node[synonym] is not None:
                        self._synonym[synonym][e.node[synonym]] = e
                        


class Element(object):
    def __init__(self, space, node):
        self.log = logging.getLogger('Element')
        self.space = space
        self.node = node
        
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
        


class PrototypeSpace(Space):
    def __init__(self, env, node):
        Space.__init__(self, env, node)
        
    def _load_element(self):
        self._element = {}
        for k,e in self.node['element'].iteritems():
            if e is None: e = {}
            e['key'] = k
            prototype = Prototype(self, e)
            if prototype.enabled:
                self.element[prototype.key] = prototype
                
    def merge(self, key, first, second):
        prototype = self.find(key)
        if prototype:
            return (prototype.key, prototype.merge(first, second))
        else:
            return (None, None)
            
    def decode(self, synonym, value, axis=None):
        prototype = self.search(synonym, axis)
        if prototype:
            return (prototype.key, prototype.cast(value, axis))
        else:
            return (None, None)
            


class Prototype(Element):
    def __init__(self, space, node):
        Element.__init__(self, space, node)
        
        # if the prototype has an archetype
        # start from the archetype and overlay the prototype
        if self.key in self.env.archetype:
            prototype = copy.deepcopy(self.env.archetype[self.key])
            self.node = dict(prototype.items() + self.node.items())
            
        # apply defaults
        for field in self.default:
            if field not in self.node:
                self.node[field] = self.default[field]
                
        # set a default unicode type
        if 'type' not in self.node:
            self.node['type'] = 'unicode'
            
        # find the cast, format and merge functions
        c = getattr(self, '_cast_{}'.format(self.type), None) or (lambda x,y: x)
        f = getattr(self, '_format_{}'.format(self.type), None) or (lambda x: x)
        m = getattr(self, '_merge_{}'.format(self.type), None) or (lambda x,y: y)
        
        if not self.node['plural']:
            self._cast = c
            self._format = f
            self._merge = m
        else:
            if self.node['plural'] == 'list':
                self._format = lambda x: self._format_list(x, f)
                self._cast = lambda x,y: self._cast_list(x, c, y)
                self._merge = self._merge_list
            elif self.node['plural'] == 'dict':
                self._format = lambda x: self._format_dict(x, f)
                self._cast = lambda x,y: self._cast_dict(x, c, y)
                
        if not self.node['auto cast']:
            self._cast = lambda x,y: x
            
    @property
    def type(self):
        return self.node['type']
        
    @property
    def plural(self):
        return self.node['plural']
        
    @property
    def keyword(self):
        return self.node['keyword']
        
    def cast(self, value, axis=None):
        if value is not None:
            return self._cast(value, axis)
        else:
            return None
            
    def format(self, value):
        if value is not None:
            return self._format(value)
        else:
            return None
            
    def merge(self, first, second):
        result = None
        if first is None:
            if second is not None:
                result = second
        elif second is None:
            result = first
        else:
            result = self._merge(first, second)
        return result
        
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
        return u'{:.2f} {1}'.format(v, self.env.enumeration['binary iec 60027 2'].get(p))
        
    def _format_bit_as_si(self, value):
        p = 0
        v = float(value)
        while v > 1000.0 and p < 4:
            p += 1
            v /= 1000.0
        return u'{:.2f} {1}'.format(v, self.env.enumeration['decimal si'].get(p))
        
    def _format_timecode(self, value):
        t = Timestamp(Timestamp.SRT)
        t.millisecond = value
        return t.timecode
        
    def _format_enum(self, value):
        return self.env.enumeration[self.node['enumeration']].format(value)
        
    def _format_float(self, value):
        return u'{:.3f}'.format(value)
        
    def _format_int(self, value):
        result = unicode(value)
        if 'format' in self.node:
            if self.node['format'] == 'bitrate':
                result = u'{}/s'.format(self._format_bit_as_si(value))
                
            elif self.node['format'] == 'millisecond':
                result =  self._format_timecode(value)
                
            elif self.node['format'] == 'byte':
                result = self._format_byte_as_iec_60027_2(value)
                
            elif self.node['format'] == 'bit':
                result = u'{} bit'.format(value)
                
            elif self.node['format'] == 'frequency':
                result = u'{} Hz'.format(value)
                
            elif self.node['format'] == 'pixel':
                result = u'{} px'.format(value)
                
        return result
        
    def _format_bool(self, value):
        if value is True: return u'yes'
        else: return u'no'
        
    def _format_plist(self, value):
        return unicode(value)
        
    def _format_date(self, value):
        return unicode(value)
        
    def _format_list(self, value, formatter):
        if value:
            return u', '.join([ formatter(v) for v in value ])
        else:
            return None
            
    def _format_dict(self, value, formatter):
        if value:
            return u', '.join([ u'{}:{}'.format(k,formatter(v)) for k,v in value.iteritems() ])
        else:
            return None
            
    def _format_unicode(self, value):
        return value
        
    def _cast_enum(self, value, axis=None):
        return self.env.enumeration[self.node['enumeration']].parse(value)
        
    def _cast_int(self, value, axis=None):
        result = None
        try:
            result = int(value)
        except ValueError:
            self.log.error(u'Failed to decode value %s as integer for %s', value, self.key)
        return result
        
    def _cast_float(self, value, axis=None):
        result = None
        try:
            result = float(value)
        except ValueError:
            self.log.error(u'Failed to decode value %s as float for %s', value, self.key)
        return result
        
    def _cast_unicode(self, value, axis=None):
        result = unicode(value.strip())
        if not result:
            result = None
        if result and self.node['unescape xml']:
            result = result.replace(u'&quot;', u'"')
        if self.node['simplify']:
            result = self._simplify(result)
        return result
        
    def _cast_date(self, value, axis=None):
        result = None
        if 'format' in self.node and self.node['format'] == 'unix time':
            result = self._cast_int(value)
            if result is not None:
                result = datetime.utcfromtimestamp(result)
        else:
            
            # Datetime conversion, must have at least a Year, Month and Day.
            # If Year is present but Month and Day are missing they are set to 1
            match = self.env.expression['full utc datetime'].search(value)
            if match:
                parsed = dict([(k, int(v)) for k,v in match.groupdict().iteritems() if k != u'tzinfo' and v is not None])
                if u'month' not in parsed:
                    parsed[u'month'] = 1
                if u'day' not in parsed:
                    parsed[u'day'] = 1
                try:
                    result = datetime(**parsed)
                except (TypeError, ValueError):
                    self.log.debug(u'Failed to decode value %s as datetime for %s', value, self.key)
            else:
                self.log.debug(u'Failed to parse value %s as datetime for %s', value, self.key)
        return result
        
    def _cast_bool(self, value, axis=None):
        result = False
        if self.env.expression['true value'].search(value) is not None:
            result = True
        return result
        
    def _cast_plist(self, value, axis=None):
        # Clean and parse plist into a dictionary
        result = value
        result = self.env.expression['clean xml'].sub(u'', result).strip()
        try:
            result = plistlib.readPlistFromString(result.encode('utf-8'))
        except Exception:
            self.log.error(u'Failed to parse plist for %s', self.key)
            result = None
            
        return result
        
    def _cast_list(self, value, caster, axis=None):
        result = None
        if 'plural format' in self.node:
            literals = None
            if self.node['plural format'] == 'mediainfo value list':
                if self.env.expression['mediainfo value list'].match(value):
                    literals = value.split(u'/')
                else:
                    self.log.error(u'Failed to parse value %s as list for %s', value, self.key)
                    
            if literals:
                result = [ caster(l, axis) for l in literals ]
        else:
            result = [ caster(v, axis) for v in value ]
            
        # strip None elements
        if result:
            result = [ v for v in result if v is not None ]
            
        if not result:
            result = None
        else:
            if 'single element name' in self.node:
                result = [ { self.node['single element name']:v } for v in result ]
                if 'append to element' in self.node:
                    for i in result:
                        for k,v in self.node['append to element'].iteritems():
                            i[k] = v
        return result
        
    def _cast_dict(self, value, caster, axis=None):
        result = None
        if 'plural format' in self.node:
            if self.node['plural format'] == 'eval':
                try:
                    result = Ontology(self.env, self.node['namespace'], eval(value))
                    # self.log.debug(u'Evaluating dictionary %s %s', result, eval(value))
                except SyntaxError as e:
                    self.log.warning(u'Failed to evaluate dictionary %s', value)
                    self.log.debug(u'Exception raised: %s', unicode(e))
                    result = None
                    
        if not result:
            result = None
        return result
        
    def _cast_embed(self, value, axis=None):
        result = Ontology(self.env, self.node['namespace'])
        result.decode_all(value, axis)
        return result
        
    def _merge_list(self, first, second):
        result = []
        result.extend(first)
        result.extend(second)
        return result
        
    def _remove_accents(self, value):
        result = None
        if value:
            nkfd = unicodedata.normalize('NFKD', value)
            result = self.env.constant['empty string'].join([c for c in nkfd if not unicodedata.combining(c)])
        return result
        
    def _simplify(self, value):
        result = None
        if value:
            v = self.env.expression['whitespace'].sub(self.env.constant['space'], value).strip()
            if v:
                result = self.env.expression['characters to exclude from filename'].sub(self.env.constant['empty string'], v)
                if not result:
                    result = v
                    result = result.replace(u'?', u'question mark')
                    result = result.replace(u'*', u'asterisk')
                    result = result.replace(u'.', u'period')
                    result = result.replace(u':', u'colon')
                result = self._remove_accents(result)
                result = result.lower()
        return result
        


class Enumeration(Space):
    def __init__(self, env, node):
        Space.__init__(self, env, node)
        
    def _load_element(self):
        self._element = {}
        for k,e in self.node['element'].iteritems():
            if check(e):
                if e is None: e = {}
                e['key'] = k
                enumerator = Enumerator(self, e)
                if enumerator.enabled:
                    self.element[enumerator.key] = enumerator
                    


class Enumerator(Element):
    def __init__(self, space, node):
        Element.__init__(self, space, node)
        
        # apply defaults
        for field in self.default:
            if field not in self.node:
                self.node[field] = self.default[field]
                


class Deduction(object):
    def __init__(self, env, node):
        self.log = logging.getLogger('Deduction')
        self.env = env
        self.node = node
        self._rule = None
        self._dependency = None
        
    @property
    def rule(self):
        if self._rule is None:
            self.reload()
        return self._rule
        
    @property
    def dependency(self):
        if self._dependency is None:
            self.reload()
        return self._dependency
        
    def reload(self):
        self._rule = {}
        self._dependency = {}
        for key in self.node['rule']:
            rule = self.env.rule[key]
            self.rule[key] = rule
            for ref in rule.provide:
                if ref not in self.dependency:
                    self.dependency[ref] = []
                self.dependency[ref].append(rule)
                
    def find(self, key):
        if key in self.rule:
            return self.rule[key]
        else:
            return None
            


class Rule(object):
    def __init__(self, env, node):
        self.log = logging.getLogger('Rule')
        self.env = env
        self.node = node
        
        temp = self.node['branch']
        self.node['branch'] = []
        for branch in temp:
            self.add_branch(branch)
            
    def __unicode__(self):
        return self.node['key']
        
    @property
    def valid(self):
        return True
        
    @property
    def provide(self):
        return self.node['provide']
        
    @property
    def branch(self):
        return self.node['branch']
        
    def add_branch(self, branch):
        try:
            if 'match' in branch:
                branch['match']['pattern'] = re.compile(branch['match']['expression'], branch['match']['flags'])
                
            if 'decode' in branch:
                for c in branch['decode']:
                    c['pattern'] = re.compile(c['expression'], c['flags'])
            self.branch.append(branch)
        except Exception as e:
            self.log.error(u'Failed to load banch for rule %s', e['key'])
            self.log.debug(u'Exception raised: %s', unicode(e))
        


class Umid(object):
    def __init__(self, home_id=None, media_kind=None):
        self._home_id = home_id
        self._media_kind = media_kind
        self._code = None
        
    @classmethod
    def decode(cls, code):
        umid = cls()
        umid.code = code
        if umid.code is not None: return umid
        else: return None
        
    @classmethod
    def _checksum(cls, string):
        digits = map(lambda x: int(x,16), string)
        return (sum(digits[::-2]) + sum(map(lambda d: sum(divmod(3*d, 16)), digits[-2::-2]))) % 16
        
    @classmethod
    def _check_digit(cls, string):
        d = Umid._checksum(string + '0')
        if d != 0: d = 16 - d
        return u'{:x}'.format(d)
        
    @classmethod
    def verify(cls, string):
        return string is not None and Umid._checksum(string) == 0
        
    def _parse(self):
        self._media_kind = int(self._code[0:2], 16)
        self._home_id = int(self._code[3:12], 16)
        
    @property
    def media_kind(self):
        if self._media_kind is None and self._code is not None:
            self._parse()
        return self._media_kind
        
    @media_kind.setter
    def media_kind(self, value):
        self._media_kind = value
        self._code = None
        
    @property
    def home_id(self):
        if self._home_id is None and self._code is not None:
            self._parse()
        return self._home_id
        
    @home_id.setter
    def home_id(self, value):
        self._home_id = value
        self._code = None
        
    @property
    def code(self):
        if self._code is None and self._media_kind is not None and self._home_id is not None:
            code = u'{:>02x}{:>010x}'.format(self._media_kind, self._home_id)
            self._code = u'{}{}'.format(code, Umid._check_digit(code))
        return self._code
        
    @code.setter
    def code(self, value):
        self._home_id = None
        self._media_kind = None
        if Umid.verify(value):
            self._code = value
        else:
            self._code = None
            


