# -*- coding: utf-8 -*-

import re
import json
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
            hour = None
            minute = None
            second = None
            millisecond = None
            
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
            'decode':re.compile(u'([0-9]{,2}):([0-9]{,2}):([0-9]{,2})(?:[,.])([0-9]+)', re.UNICODE)
        },
        2:{
            'encode':u'{0:02d}:{1:02d}:{2:02d}.{3:03d}',
            'decode':re.compile(u'([0-9]{,2}):([0-9]{,2}):([0-9]{,2})\.([0-9]+)', re.UNICODE)
        },
    }

class ResourceTransform(object):
    def __init__(self, resource):
        self.resource = resource
        self.pivot = {}
    
    
    @property
    def env(self):
        return self.resource.env
    
    
    @property
    def node(self):
        return { u'pivot':[ p.node for p in self.pivot.values() ] }
    
    
    @property
    def space(self):
        return self.resource.asset.resource.values()
    
    
    @property
    def single_pivot(self):
        if len(self.pivot) > 0:
            return self.pivot.values()[0]
        else:
            return None
    
    
    def transform(self, preset, action):
        if action in preset['action']:
            # First use the pivot section to select resources to pivot
            if 'pivot' in preset['action'][action]:
                for branch in preset['action'][action]['pivot']:
                    if 'operator' in branch:
                        operator = getattr(self, branch['operator'], None)
                        if operator:
                            if 'constraint' in branch:
                                operator(branch['constraint'])
                            else:
                                operator()
                                
            # Than use the transform to resolve the pivots on the selected resources
            if 'transform' in preset['action'][action] and self.pivot:
                for template in preset['action'][action]['transform']:
                    for branch in template['branch']:
                        taken = False
                        for pivot in self.pivot.values():
                            if pivot.location.match(branch):
                                taken = pivot.transform(template)
                                if template['mode'] == 'choose':
                                    break
                                    
                        if template['mode'] == 'choose' and taken:
                            break
    
    
    def add(self, resource):
        if resource.uri not in self.pivot:
            self.pivot[resource.uri] = ResourcePivot(resource)
    
    
    def remove(self, resource):
        if resource.uri in self.pivot:
            del self.pivot[resource.uri]
    
    
    def this(self):
        self.add(self.resource)
    
    
    def select(self, constraint):
        for resource in self.space:
            if resource.location.match(constraint):
                self.add(resource)
    
    
    def intersect(self, constraint):
        for k in self.selected.keys():
            if not self.selected[k].location.match(constraint):
                self.remove(self.selected[k])
    
    
    def subtract(self, constraint):
        for k in self.selected.keys():
            if self.selected[k].location.match(constraint):
                self.remove(self.selected[k])
    


class ResourcePivot(object):
    def __init__(self, resource):
        self.resource = resource
        self.location = Ontology.clone(resource.location)
        self.stream = []
    
    
    @property
    def node(self):
        return {
            u'location':self.location,
            u'stream':self.stream,
        }
    
    
    def __unicode__(self):
        return unicode(self.node)
    
    
    @property
    def uri(self):
        return self.resource.uri
    
    
    @property
    def taken(self):
        return len(self.stream) > 0
    
    
    def transform(self, template):
        # apply overrides on the pivot location from the template
        if 'override' in template:
            for k,v in template['override'].iteritems():
                self.location[k] = v
                
        # apply track rules from the template
        if 'track' in template:
            for rule in template['track']:
                for branch in rule['branch']:
                    taken = False
                    for stream in self.resource.stream:
                        if stream.match(branch):
                            taken = True
                            s = Ontology.clone(stream)
                            s['resource path digest'] = self.resource.location['path digest']
                            if 'override' in rule:
                                for k,v in rule['override'].iteritems(): s[k] = v
                            self.stream.append(s)
                            
                            if rule['mode'] == 'choose':
                                break
                                
                    if rule['mode'] == 'choose' and taken:
                        break
        return self.taken
    



