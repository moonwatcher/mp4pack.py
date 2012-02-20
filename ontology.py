# -*- coding: utf-8 -*-

import logging
import copy

class Ontology(dict):
    def __init__(self, env, *args, **kw):
        dict.__init__(self, *args, **kw)
        
        # Make sure no empty concepts slipped in...
        for key in dict.keys(self):
            if dict.__getitem__(self, key) is None:
                dict.__delitem__(self, key)
                
        self.log = logging.getLogger('ontology')
        self.env = env
        self.kernel = dict(self)
        self.dependency = {}
    
    
    def __unicode__(self):
        return unicode(self.kernel)
    
    
    @classmethod
    def clone(cls, other):
        o = cls(other.env, other.kernel)
        return o
    
    
    @property
    def node(self):
        return self.kernel
    
    
    def match(self, fact):
        return all((k in self and self[k] == v) for k,v in fact.iteritems())
    
    
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
    
    
    def complete(self):
        for key in self.env.lookup['rule']['provide']:
            self[key]
    
    
    def _decode(self, keyword, value):
        if keyword and value is not None and keyword in self.env.lookup['info']['keyword']['tag']:
            prototype = self.env.lookup['info']['keyword']['tag'][keyword]
            if prototype:
                v = value
                if prototype['type'] == int:
                    try:
                        v = int(value)
                    except ValueError as error:
                        self.log.error('Failed to decode integer prototype: %s', unicode({prototype['name']:value}))
                        
                elif prototype['type'] == unicode:
                    v = self.env.simplify(value)
                    
                if v: dict.__setitem__(self, prototype['name'], v)
    
    
    def _resolve(self, key):
        if not dict.__contains__(self, key):
            if key in self.env.lookup['rule']['provide']:
                for rule in self.env.lookup['rule']['provide'][key]:
                    for branch in rule['branch']:
                        taken = True
                        if 'requires' in branch:
                            dependencies = branch['requires'].difference(self)
                            while dependencies:
                                d = dependencies.pop()
                                self._resolve(d)
                                if dict.__contains__(self, d):
                                    dependencies = branch['requires'].difference(self)
                                else: dependencies = None
                            if not branch['requires'].issubset(self):
                                taken = False
                        taken = taken and ('equal' not in branch or all((dict.__contains__(self, k) and dict.__getitem__(self, k) == v) for k,v in branch['equal'].iteritems()))
                        taken = taken and ('match' not in branch or branch['match']['pattern'].match(dict.__getitem__(self, branch['match']['property'])))
                        
                        if taken:
                            if 'apply' in branch:
                                for x in branch['apply']:
                                    if not dict.__contains__(self, x['property']):
                                        if 'format' in x:
                                            dict.__setitem__(self, x['property'], x['format'].format(**self))
                                        elif 'value' in x:
                                            dict.__setitem__(self, x['property'], x['value'])
                                            
                            if 'decode' in branch:
                                for x in branch['decode']:
                                    match = x['pattern'].search(dict.__getitem__(self, x['property']))
                                    if match is not None:
                                        parsed = match.groupdict()
                                        for k,v in parsed.iteritems():
                                            self._decode(k, v)
                                            
                            if 'requires' in branch:
                                for req in branch['requires']:
                                    if req not in self.dependency:
                                        self.dependency[req] = copy.deepcopy(rule['provides'])
                                    else:
                                        self.dependency[req] = self.dependency[req].union(rule['provides'])
                            break
                            
                    if dict.__contains__(self, key):
                        # self.log.debug(u'Resolved %s', unicode({key:self[key]}))
                        break
    

