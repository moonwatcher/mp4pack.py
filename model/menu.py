# -*- coding: utf-8 -*-

import re
import logging

from model import Timestamp 

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
                    #    lang = self.env.enumeration['language'].parse(frag['lang'])
                    #    if lang: self.language = lang
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

