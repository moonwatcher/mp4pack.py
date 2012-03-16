# -*- coding: utf-8 -*-

import re
import logging
from datetime import datetime

from ontology import Ontology 

class Timestamp(object):
    def __init__(self, format):
        self._millisecond = 0
        self._timecode = None
        self.codec = Timestamp.format[format]
    
    
    @property
    def millisecond(self):
        if self._millisecond is None and self._timecode is not None:
            hour = 0
            minute = 0
            second = 0
            millisecond = 0
            
            match = self.codec['decode'].search(self._timecode)
            if match is not None:
                hour = match.group(1)
                minute = match.group(2)
                second = match.group(3)
                millisecond = match.group(4)
                
            if millisecond is not None:
                if len(millisecond) == 2:
                    millisecond = 10 * int(millisecond)
                elif len(millisecond) >= 3:
                    millisecond = millisecond[0:3]
                    millisecond = int(millisecond)
                else:
                    millisecond = int(millisecond)
            else:
                millisecond = 0
                
            if second is not None:
                second = int(second)
            else:
                second = 0
                
            if minute is not None:
                minute = int(minute)
            else:
                minute = 0
                
            if hour is not None:
                hour = int(hour)
            else:
                hour = 0
                
            self._millisecond = (hour * 3600 + 60 * minute + second) * 1000 + millisecond
        return self._millisecond
    
    
    @millisecond.setter
    def millisecond(self, value):
        self._millisecond = value
        self._timecode = None
    
    
    @property
    def timecode(self):
        if self._timecode is None and self._millisecond is not None:
            hour = int(self._millisecond) / 3600000
            hour_modulo = int(self._millisecond) % 3600000
            minute = int(hour_modulo) / 60000
            minute_modulo = int(hour_modulo) % 60000
            second = int(minute_modulo) / 1000
            second_modulo = int(minute_modulo) % 1000
            millisecond = int(second_modulo)
            self._timecode = self.codec['encode'].format(hour, minute, second, millisecond)
        return self._timecode
    
    
    @timecode.setter
    def timecode(self, value):
        self._timecode = value
        self._millisecond = None
    
    
    @property
    def node(self):
        return { 'timecode':self.timecode, 'millisecond':self.millisecond }
    
    
    def shift(self, offset):
        self.millisecond += offset
    
    
    def scale(self, factor):
        self.millisecond = int(round(float(self.millisecond) * float(factor)))
    
    
    def __unicode__(self):
        return self.timecode
    
    
    SRT = 1
    CHAPTER = 2
    format = {
        1:{
            'encode':u'{0:02d}:{1:02d}:{2:02d},{3:03d}',
            'decode':re.compile(u'([0-9]{,2}):([0-9]{,2}):([0-9]{,2}),([0-9]+)', re.UNICODE)
        },
        2:{
            'encode':u'{0:02d}:{1:02d}:{2:02d}.{3:03d}',
            'decode':re.compile(u'([0-9]{,2}):([0-9]{,2}):([0-9]{,2})\.([0-9]+)', re.UNICODE)
        },
    }


class Query(object):
    def __init__(self, space):
        self.space = space
        self.resource = {}
    
    
    @property
    def result(self):
        return self.resource.values()
    
    
    def add(self, resource):
        if resource.ontology['resource id'] not in self.resource:
            self.resource[resource.ontology['resource id']] = resource
    
    
    def remove(self, resource):
        if resource.ontology['resource id'] in self.resource:
            del self.resource[resource.ontology['resource id']]
    
    
    def resolve(self, profile):
        if 'query' in profile:
            for branch in profile['query']:
                if 'action' in branch:
                    action = getattr(self, branch['action'], None)
                    if action and 'constraint' in branch:
                        action(branch['constraint'])
    
    
    def select(self, constraint):
        for resource in self.space:
            if resource.ontology.match(constraint):
                self.add(resource)
    
    
    def intersect(self, constraint):
        for k in self.resource.keys():
            if not self.resource[k].ontology.match(constraint):
                self.remove(self.resource[k])
    
    
    def subtract(self, constraint):
        for k in self.resource.keys():
            if self.resource[k].ontology.match(constraint):
                self.remove(self.resource[k])
    


class Pivot(object):
    def __init__(self, resource, rule):
        self.resource = resource
        self.ontology = Ontology.clone(resource.ontology)
        self.track = []
        if 'override' in rule:
            for k,v in rule['override'].iteritems():
                self.ontology[k] = v
    
    
    @property
    def id(self):
        return self.resource.ontology['resource id']
    
    
    @property
    def taken(self):
        return len(self.track) > 0
    
    
    def scan(self, profile):
        for rule in profile:
            for branch in rule['branch']:
                taken = False
                for track in self.resource.track:
                    if track.match(branch):
                        taken = True
                        self._pick_track(track, rule)
                        if rule['mode'] == 'choose':
                            break
                            
                if rule['mode'] == 'choose' and taken:
                    break
                    
        return self.taken
    
    
    def _pick_track(self, track, rule):
        o = Ontology.clone(track)
        if 'override' in rule:
            for k,v in rule['override'].iteritems():
                o[k] = v
        self.track.append(o)
    


class Transform(object):
    def __init__(self):
        self._result = {}
    
    
    @property
    def result(self):
        return self._result.values()
    
    
    @property
    def single_result(self):
        if len(self._result) > 0:
            return self._result.values()[0]
        else:
            return None
    
    
    def resolve(self, space, profile):
        if 'transform' in profile:
            for rule in profile['transform']:
                for branch in rule['branch']:
                    taken = False
                    for resource in space:
                        if resource.ontology.match(branch):
                            taken = True
                            pivot = self._find_pivot(resource, rule)
                            taken = taken and pivot.scan(rule['track'])
                            if rule['mode'] == 'choose':
                                break
                                
                    if rule['mode'] == 'choose' and taken:
                        break
    
    
    def _find_pivot(self, resource, rule):
        pivot = None
        if resource.ontology['resource id'] in self._result:
            pivot = self._result[resource.ontology['resource id']]
            
        else:
            pivot = Pivot(resource, rule)
            self._result[pivot.id] = pivot
        return pivot
    


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
                        self._synonym[e.node[synonym]] = e
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
    


class PrototypeSpace(Space):
    def __init__(self, env, node):
        Space.__init__(self, env, node)
    
    
    def load(self):
        self.element = {}
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
            elif self.node['type'] == 'plist':
                c = self._cast_plist
                f = lambda x: unicode(x)
                
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
    


class Enumeration(Space):
    def __init__(self, env, node):
        Space.__init__(self, env, node)
    
    
    def load(self):
        self.element = {}
        for e in self.node['element']:
            element = Element(self, e)
            if element.enabled:
                self.element[element.key] = element
    

