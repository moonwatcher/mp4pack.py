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
    

