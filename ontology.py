# -*- coding: utf-8 -*-

import logging
import copy
import re
import unicodedata
import plistlib
import hashlib

from datetime import datetime

class Ontology(dict):
    def __init__(self, env, namespace,  *args, **kw):
        dict.__init__(self, *args, **kw)
        self.log = logging.getLogger('ontology')
        self.env = env
        self.namespace = self.env.namespace[namespace]
        
        # Make sure no empty concepts slipped in...
        for key in dict.keys(self):
            if dict.__getitem__(self, key) is None:
                dict.__delitem__(self, key)
                
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
        return all((k in self and self[k] == v) for k,v in fact.iteritems())
    
    
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
            # so concepts can be assumed to not be None
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
    
    
    def decode(self, synonym, value):
        if synonym and value is not None:
            k,v = self.namespace.decode(synonym, value)
            self.__setitem__(k, v)
    
    
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
                                        if 'digest' in x:
                                            dict.__setitem__(self, x['property'], hashlib.sha1(self[x['digest']]).hexdigest())
                                        if 'reference' in x:
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
                            # This was removing the requirement also removes the dependent atom
                            if 'requires' in branch:
                                for req in branch['requires']:
                                    if req not in self.dependency:
                                        self.dependency[req] = copy.deepcopy(rule.provide)
                                    else:
                                        self.dependency[req] = self.dependency[req].union(rule.provide)
                            break
                            
                    if dict.__contains__(self, key):
                        # self.log.debug(u'Resolved %s', unicode({key:self[key]}))
                        break
    


# Generic Space and Element
class Space(object):
    def __init__(self, env, node):
        self.log = logging.getLogger('Space')
        self.env = env
        self.node = node
        self._element = None
        self._synonym = None
        self._deduction = None
        
        if 'default' not in self.node:
            self.node['default'] = {}
            
        if 'rule' not in self.node:
            self.node['rule'] = []
            
        if 'enabled' not in self.default:
            self.default['enabled'] = True
            
        if 'match' in self.node:
            self.node['pattern'] = re.compile(self.node['match']['expression'], self.node['match']['flags'])
        else:
            self.node['pattern'] = None
    
    
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
    
    
    @property
    def pattern(self):
        return self.node['pattern']
    
    
    def match(self, key):
        return not self.pattern or self.pattern.search(key) is not None
    
    
    def contains(self, key):
        return key is not None and key in self.element
    
    
    def find(self, key):
        if key is not None and key in self.element:
            return self.element[key]
        else: return None
    
    
    def search(self, synonym):
        if synonym is not None and synonym in self.synonym:
            return self.synonym[synonym]
        else: return None
    
    
    def parse(self, synonym):
        element = self.search(synonym)
        if element is not None: return element.key
        else: return None
    
    
    def format(self, key):
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
                for e in self.element.values():
                    if e.node[synonym] is not None and e.node[synonym] not in self._synonym:
                        self._synonym[e.node[synonym]] = e
    


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
    


# Prototype Space and Prototype
class PrototypeSpace(Space):
    def __init__(self, env, node):
        Space.__init__(self, env, node)
        
        if 'simplify' not in self.default:
            self.default['simplify'] = False
    
    
    def _load_element(self):
        self._element = {}
        for k,e in self.node['element'].iteritems():
            if e is None: e = {}
            e['key'] = k
            prototype = Prototype(self, e)
            if prototype.enabled:
                self.element[prototype.key] = prototype
    
    
    def decode(self, synonym, value):
        prototype = self.search(synonym)
        if prototype:
            return (prototype.key, prototype.cast(value))
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
            
        # find the cast and format functions
        c = getattr(self, '_cast_{0}'.format(self.node['type']), None) or (lambda x: x)
        f = getattr(self, '_format_{0}'.format(self.node['type']), None) or (lambda x: x)
        
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
    
    
    @property
    def keyword(self):
        return self.node['keyword']
    
    
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
        return u'{0:.2f} {1}'.format(v, self.env.enumeration['binary iec 60027 2'].get(p))
    
    
    def _format_bit_as_si(self, value):
        p = 0
        v = float(value)
        while v > 1000.0 and p < 4:
            p += 1
            v /= 1000.0
        return u'{0:.2f} {1}'.format(v, self.env.enumeration['decimal si'].get(p))
    
    
    def _format_timecode(self, value):
        t = Timestamp(Timestamp.SRT)
        t.millisecond = value
        return t.timecode
    
    
    def _format_enum(self, value):
        return self.env.enumeration[self.node['enumeration']].format(value)
    
    
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
            return u', '.join([ u'{0}:{1}'.format(k,formatter(v)) for k,v in value.iteritems() ])
        else:
            return None
    
    
    def _format_unicode(self, value):
        return value
    
    
    def _cast_enum(self, value):
        return self.env.enumeration[self.node['enumeration']].parse(value)
    
    
    def _cast_int(self, value):
        result = None
        try:
            result = int(value)
        except ValueError:
            self.log.error(u'Failed to decode: %s as an integer', value)
        return result
    
    
    def _cast_float(self, value):
        result = None
        try:
            result = float(value)
        except ValueError:
            self.log.error(u'Failed to decode: %s as an integer', value)
        return result
    
    
    def _cast_unicode(self, value):
        result = unicode(value.strip())
        if not result:
            result = None
        if result and self.node['unescape xml']:
            result = result.replace(u'&quot;', u'"')
        if self.node['simplify']:
            result = self._simplify(result)
        return result
    
    
    def _cast_date(self, value):
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
                except TypeError, ValueError:
                    self.log.debug(u'Failed to decode datetime %s', value)
            else:
                self.log.debug(u'Failed to parse datetime %s', value)
        return result
    
    
    def _cast_bool(self, value):
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
                    
            elif self.node['plural format'] == 'tvdb list':
                value = self.env.expression['tvdb list separators'].sub(u'|', value)
                value = self.env.expression['space around tvdb list item'].sub(u'|', value)
                value = value.strip().strip(u'|')
                if value:
                    literals = value.split(u'|')
                    
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
    


# Enumeration and Enumerator
class Enumeration(Space):
    def __init__(self, env, node):
        Space.__init__(self, env, node)
    
    
    def _load_element(self):
        self._element = {}
        for k,e in self.node['element'].iteritems():
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
    


# Deduction and Rule
class Deduction(object):
    def __init__(self, env, node):
        self.log = logging.getLogger('deduction')
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
        self.log = logging.getLogger('rule')
        self.env = env
        self.node = node
        
        if 'branch' not in self.node:
            self.node['branch'] = []
            
        for branch in self.branch:
            self._load_branch(branch)
            
    
    
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
        if self._load_branch(branch):
            self.branch.append(branch)
    
    
    def _load_branch(self, branch):
        result = False
        if branch is not None:
            try:
                if 'match' in branch:
                    if 'flags' not in branch['match']:
                        branch['match']['flags'] = re.UNICODE
                    branch['match']['pattern'] = re.compile(branch['match']['expression'], branch['match']['flags'])
                    
                if 'decode' in branch:
                    for c in branch['decode']:
                        if 'flags' not in c:
                            c['flags'] = re.UNICODE
                        c['pattern'] = re.compile(c['expression'], c['flags'])
                result = True
            except Exception, e:
                self.log.error(u'Failed to load banch for rule %s', unicode(self))
                self.log.debug(u'Exception raised: %s', unicode(e))
        return result
    


