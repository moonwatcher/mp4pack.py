# -*- coding: utf-8 -*-

import re
from ontology import Ontology 

class Caption(object):
    def __init__(self, env):
        self.env = env
        self.slides = []
    
    
    @classmethod
    def from_node(cls, env, node):
        o = cls(env)
        for i in node:
            o.add(Slide.from_node(i))
        return o
    
    
    @property
    def valid(self):
        return self.size > 0
    
    
    @property
    def size(self):
        return len(self.slides)
    
    
    @property
    def node(self):
        node = []
        for slide in self.slides:
            node.append(slide.node)
        return node
    
    
    def add(self, slide):
        if slide and slide.valid:
            self.slides.append(slide)
    
    
    def sort(self):
        self.slides.sort(key=lambda x: x.begin.millisecond)
    
    
    def normalize(self):
        self.sort()
        self.slides = [slide for slide in self.slides if slide.valid]
        for index, slide in enumerate(self.slides):
            slide.index = index + 1
    
    
    def filter(self, name):
        if name in self.env.caption_filter_cache:
            f = self.env.caption_filter_cache[name]
            for slide in self.slides:
                f.filter(slide)
    
    
    def shift(self, offset):
        for slide in self.slide:
            slide.shift(offset)
    
    
    def scale(self, factor):
        for slide in self.slides:
            slide.scale(factor)
    
    
    def encode(self):
        content = None
        if self.valid:
            content = [u'']
            for slide in self.slides:
                slide.encode(content)
        return content
    


class Menu(object):
    def __init__(self, env):
        self.env = env
        self.chapters = []
    
    
    @classmethod
    def from_node(cls, env, node):
        o = cls(env)
        for i in node:
            o.add(Chapter.from_node(i))
        return o
    
    
    @property
    def valid(self):
        return self.size > 1
    
    
    @property
    def size(self):
        return len(self.chapters)
    
    
    @property
    def node(self):
        node = []
        for chapter in self.chapters:
            node.append(chapter.node)
        return node
    
    
    def add(self, chapter):
        if chapter and chapter.valid:
            self.chapters.append(chapter)
    
    
    def normalize(self):
        self.sort()
        self.chapters = [c for c in self.chapters if c.valid]
        for index, chapter in enumerate(self.chapters):
            chapter.index = index + 1
    
    
    def sort(self):
        self.chapters.sort(key=lambda x: x.time.millisecond)
    
    
    def shift(self, offset):
        for chapter in self.chapters:
            chapter.shift(offset)
    
    
    def scale(self, factor):
        for chapter in self.chapters:
            chapter.scale(factor)
    
    
    def encode(self, format):
        content = None
        if self.valid:
            content = []
            for chapter in self.chapters:
                chapter.encode(content, format)
        return content
    


class Chapter(object):
    def __init__(self):
        self.index = None
        self.time = Timestamp(Timestamp.CHAPTER)
        self._name = None
        self.language = None
    
    
    @classmethod
    def from_raw(cls, timecode, name, format):
        o = cls()
        codec = Chapter.format[format]
        if timecode and name:
            
            # Decode timecode
            match = codec['timecode decode'].search(timecode)
            if match:
                frag = match.groupdict()
                o.time.timecode = o.time.codec['encode'].format(
                    int(frag['hour']),
                    int(frag['minute']),
                    int(frag['second']),
                    int(frag['millisecond'])
                )
                
            # Decode name
            if codec['name decode']:
                match = codec['name decode'].search(name)
                if match:
                    frag = match.groupdict()
                    o.name = frag['name'].replace('&quot;', '"')
                    #if 'lang' in frag and frag['lang']:
                    #    lang = self.env.find_language(frag['lang'])
                    #    if lang:
                    #        self.language = lang['iso3t']
            else:
                o.name = name
        return o
    
    
    @classmethod
    def from_node(cls, node):
        o = cls()
        o.index = node['index']
        o.time.millisecond = node['time']
        o.name = node['name']
        return o
    
    
    @property
    def valid(self):
        return self.time is not None and self.time.millisecond > 0
    
    
    @property
    def name(self):
        if self._name is None:
            self._name = Chapter.default_name_format.format(self.index)
        return self._name
    
    
    @property
    def node(self):
        return {
            'index':self.index,
            'time':self.time.millisecond,
            'name':self.name,
        }
    
    
    @name.setter
    def name(self, value):
        match = Chapter.junk_name.search(value)
        if match is None:
            self._name = value.strip('"').strip("'").strip()
        else:
            self._name = None
    
    
    def shift(self, offset):
        self.time.shift(offset)
    
    
    def scale(self, factor):
        self.time.scale(factor)
    
    
    def encode(self, content, format):
        codec = Chapter.format[format]
        content.append(codec['timecode encode'].format(self.index, self.time.timecode))
        content.append(codec['name encode'].format(self.index, self.name))
    
    
    def __unicode__(self):
        return u'{0}. {1}:{2}'.format(self.index, self.time.timecode, self.name)
    
    
    default_name_format = u'Chapter {0}'
    junk_name = re.compile(ur'^(?:[0-9]{,2}:[0-9]{,2}:[0-9]{,2}[\.,][0-9]+|[0-9]+|chapter[\s0-9]+)$', re.UNICODE)
    
    OGG = 1
    MEDIAINFO = 2
    format = {
        1:{
            'timecode encode':u'CHAPTER{0:02d}={1}',
            'timecode decode':re.compile(ur'CHAPTER(?P<index>[0-9]{,2})=(?P<hour>[0-9]{,2}):(?P<minute>[0-9]{,2}):(?P<second>[0-9]{,2})\.(?P<millisecond>[0-9]+)', re.UNICODE),
            'name encode':u'CHAPTER{0:02d}NAME={1}',
            'name decode':re.compile(ur'CHAPTER(?P<index>[0-9]{,2})NAME=(?P<name>.*)', re.UNICODE),
        },
        2:{
            'timecode encode':None,
            'timecode decode':re.compile(ur'_(?P<hour>[0-9]{,2})_(?P<minute>[0-9]{,2})_(?P<second>[0-9]{,2})\.(?P<millisecond>[0-9]+)', re.UNICODE),
            'name encode':None,
            'name decode':re.compile(ur'(?:(?P<lang>[a-z]{2}):)?(?P<name>.*)', re.UNICODE),
        }
    }


class Slide(object):
    def __init__(self):
        self.index = None
        self.begin = Timestamp(Timestamp.SRT)
        self.end = Timestamp(Timestamp.SRT)
        self.content = []
    
    
    @classmethod
    def from_node(cls, node):
        slide = cls()
        slide.index = node['index']
        slide.begin.millisecond = node['begin']
        slide.end.millisecond = node['end']
        slide.content = node['content']
        return slide
    
    
    @property
    def valid(self):
        return self.begin.millisecond > 0 and self.end.millisecond > 0 and \
        self.begin.millisecond < self.end.millisecond and self.content
    
    
    @property
    def node(self):
        return {
            'index':self.index,
            'begin':self.begin.millisecond,
            'end':self.end.millisecond,
            'content':self.content,
        }
    
    
    @property
    def duration(self):
        return self.end.millisecond - self.begin.millisecond
    
    
    def clear(self):
        self.content = []
    
    
    def add(self, line):
        if line:
            line = line.strip()
            if line:
                self.content.append(line)
    
    
    def shift(self, offset):
        self.begin.shift(offset)
        self.end.shift(offset)
    
    
    def scale(self, factor):
        self.begin.scale(factor)
        self.end.scale(factor)
    
    
    def encode(self, content):
        content.append(unicode(self.index))
        content.append(u'{0} --> {1}'.format(self.begin.timecode, self.end.timecode))
        for line in self.content:
            content.append(line)
        content.append(u'')
    


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
    

