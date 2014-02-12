# -*- coding: utf-8 -*-

import re
import logging

from model import Timestamp 

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
        if name in self.env.caption_filter:
            f = self.env.caption_filter[name]
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
    


class CaptionFilter(object):
    def __init__(self, node):
        self.log = logging.getLogger('Caption')
        self.expression = []
        self.action = node['action']
        self.scope = node['scope']
        self.ignorecase = node['ignore case']
        
        option = re.UNICODE
        if self.ignorecase:
            option = option|re.IGNORECASE
        if self.scope == 'slide':
            option = option|re.MULTILINE
            
        for e in node['expression']:
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
        self.log = logging.getLogger('Caption')
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
            if key in self.env.subtitle_filter:
                o = CaptionFilter(self.env.subtitle_filter[key])
                if o.valid:
                    self.log.debug(u'Loaded %s filter pipeline', key)
                    dict.__setitem__(self, key, o)
                else:
                    self.log.error(u'Failed to load %s filter pipeline', key)
                    dict.__setitem__(self, key, None)
            else:
                self.log.error(u'%s subtitle filter is not defined', key)
                dict.__setitem__(self, key, None)
    
    


