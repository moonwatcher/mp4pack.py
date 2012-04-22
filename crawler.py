#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import logging
from datetime import datetime
from subprocess import Popen, PIPE
import xml.etree.cElementTree as ElementTree

from ontology import Ontology
from model.menu import Chapter, Menu
from model.caption import Caption, Slide

class Crawler(object):
    def __init__(self, ontology):
        self.log = logging.getLogger('crawler')
        self.ontology = ontology
        self.meta = None
        self.stream = None
        
        self._stream = None
        self._menu = None
        self.reload()
    
    
    def __unicode__(self):
        return unicode(self.ontology['resource id'])
    
    
    @property
    def env(self):
        return self.ontology.env
    
    
    @property
    def valid(self):
        return self.ontology is not None and \
        'path' in self.ontology and \
        os.path.exists(self.ontology['path'])
    
    
    @property
    def node(self):
        return {
            'location':self.ontology.node,
            'meta':self.meta.node,
            'stream':[ o.node for o in self.stream ],
        }
    
    
    def reload(self):
        if self.valid:
            self.meta = None
            self.stream = None
            self._stream = []
            self._menu = []
            
            self._load_mediainfo()
            self._load_ogg_chapters()
            self._load_srt()
            self._load_ass()
            self._normalize()
    
    
    
    def _load_mediainfo(self):
        # Propagate self._stream and self._menu from mediainfo
        command = self.env.initialize_command('mediainfo', self.log)
        if command:
            command.extend([u'--Language=raw', u'--Output=XML', u'-f', self.ontology['path']])
            proc_mediainfo = Popen(command, stdout=PIPE, stderr=PIPE)
            proc_grep = Popen([u'grep', u'-v', u'Cover_Data'], stdin=proc_mediainfo.stdout, stdout=PIPE)
            report = proc_grep.communicate()
            element = ElementTree.fromstring(report[0])
            if element is not None:
                menu = None
                for node in element.findall(u'File/track'):
                    if 'type' in node.attrib:
                        mtype = self.env.enumeration['mediainfo stream type'].search(node.attrib['type'])
                        if mtype is not None:
                            if mtype.node['namespace']:
                                o = Ontology(self.env, mtype.node['namespace'])
                                for item in list(node):
                                    o.decode(item.tag, item.text)
                                self._stream.append(o)
                            elif mtype.key == 'menu':
                                m = Menu(self.env)
                                for item in list(node):
                                    m.add(Chapter.from_raw(item.tag, item.text, Chapter.MEDIAINFO))
                                self._add_menu(m)
                                
            # Release resources held by the element, we no longer need it
            element.clear()
    
    
    def _add_menu(self, menu):
        if menu is not None:
            menu.normalize()
            if menu.valid: self._menu.append(menu)
    
    
    def _load_ogg_chapters(self):
        if self.ontology['kind'] == 'chpl':
            content = self._read()
            if content:
                content = content.splitlines()
                m = Menu(self.env)
                for index in range(len(content) - 1):
                    m.add(Chapter.from_raw(content[index], content[index + 1], Chapter.OGG))
                self._add_menu(m)
    
    
    def _load_srt(self):
        if self.ontology['kind'] == 'srt':
            content = self._read()
            if content:
                caption = Caption(self.env)
                content = content.splitlines()
                current_slide_pointer = None
                next_slide_pointer = None
                current = None
                next = None
                last_line = len(content) - 1
                for index in range(len(content)):
                    if index == last_line and current_slide_pointer is not None:
                        # This is the last line
                        next_slide_pointer = index + 1
                    
                    match = self.env.expression['srt time line'].search(content[index])
                    if match is not None and content[index - 1].strip().isdigit():
                        next = Slide()
                        next.begin.timecode = match.group(1)
                        next.end.timecode = match.group(2)
                        if current_slide_pointer is not None:
                            next_slide_pointer = index - 1
                        else:
                            # first block
                            current_slide_pointer = index - 1
                            current = next
                            next = None
                        
                    if next_slide_pointer is not None:
                        for line in content[current_slide_pointer + 2:next_slide_pointer]:
                            current.add(line)
                        caption.add(current)
                        current_slide_pointer = next_slide_pointer
                        next_slide_pointer = None
                        current = next
                        next = None
                    
                caption.normalize()
                if caption.valid:
                    mtype = self.env.enumeration['mediainfo stream type'].find('text')
                    o = Ontology(self.env, mtype.node['namespace'])
                    o['stream type'] = u'text'
                    o['format'] = u'UTF-8'
                    o['language'] = self.ontology['language']
                    o['content'] = caption.node
                    self._stream.append(o)
    
    
    def _load_ass(self, lines):
        if self.ontology['kind'] == 'ass':
            content = self._read()
            if content:
                caption = Caption(self.env)
                content = content.splitlines()
                index = 0
                formation = None
                for line in content:
                    if line == u'[Events]':
                        match = self.env.expression['ass formation line'].search(lines[index + 1])
                        if match is not None:
                            formation = match.group(1).strip().replace(u' ',u'').split(u',')
                        break
                    index += 1
                
                if formation is not None:
                    start = formation.index('Start')
                    stop = formation.index('End')
                    text = formation.index('Text')
                    for line in lines:
                        match = self.env.expression['ass subtitle line'].search(line)
                        if match is not None:
                            line = match.group(1).strip().split(',')
                            slide = Slide(self)
                            slide.begin.timecode = line[start]
                            slide.end.timecode = line[stop]
                            subtitle_text = u','.join(line[text:])
                            subtitle_text = self.env.expression['ass event command'].sub(u'', subtitle_text)
                            subtitle_text = subtitle_text.replace(u'\n', ur'\N')
                            subtitle_text = self.env.expression['ass condense line breaks'].sub(ur'\N', subtitle_text)
                            subtitle_text = subtitle_text.split(ur'\N')
                            for line in subtitle_text:
                                slide.add(line)
                            caption.add(slide)
                        
                caption.normalize()
                if caption.valid:
                    mtype = self.env.enumeration['mediainfo stream type'].find('text')
                    o = Ontology(self.env, mtype.node['namespace'])
                    o['stream type'] = u'text'
                    o['format'] = u'ASS'
                    o['language'] = self.ontology['language']
                    o['content'] = caption.node
                    self._stream.append(o)
    
    
    def _normalize(self):
        if self.meta is None:
            self.stream = []
            normal = {
                'meta':[ o for o in self._stream if o['stream type'] == u'general' ],
                'image':[ o for o in self._stream if o['stream type'] == u'image' ],
                'audio':[],
                'video':[],
                'caption':[],
                'menu':[],
                'preview':[],
            }
            
            # There should always be exactly one info stream
            if normal['meta']:
                self.meta = normal['meta'][0]
                self._fix(self.meta)
            else:
                self.meta = Ontology(self.env, self.env.enumeration['mediainfo stream type'].find('general').node['namespace'])
            del normal['meta']
            
            # Choose the minimum channel count for every audio stream
            for o in [ o for o in self._stream if o['stream type'] == u'audio' ]:
                normal['audio'].append(o)
                if 'channel count' in o:
                    o['channels'] = min(o['channel count'])
                    
            # If the text stream format is 'Apple text' it is a chapter track in mp4,
            # otherwise its a caption stream
            for o in [ o for o in self._stream if o['stream type'] == u'text' ]:
                if o['format'] == u'Apple text':
                    normal['menu'].append(o)
                else:
                    normal['caption'].append(o)
                    
            # Break the video streams into normal video and chapter preview images
            # by relative portion of the stream and locate the primary
            primary = None
            for o in [ o for o in self._stream if o['stream type'] == u'video' ]:
                if o['format'] == u'JPEG' and o['stream portion'] < 0.01:
                    normal['preview'].append(o)
                else:
                    normal['video'].append(o)
                    if primary is None or o['stream portion'] > primary['stream portion']:
                        primary = o
                        
            # If a primary video stream is found set the dimensions on the info node
            if primary:
                primary['primary'] = True
                self.meta['width'] = float(primary['width'])
                if primary['display aspect ratio'] >= self.env.constant['playback aspect ration']:
                    self.meta['height'] = self.meta['width'] / self.env.constant['playback aspect ration']
                else:
                    self.meta['height'] = float(primary['height'])
                    
            # There should only be one menu stream with one menu in it or none at all
            if self._menu:
                if normal['menu']: o = normal['menu'][0]
                else:
                    o = Ontology(self.env, self.env.enumeration['mediainfo stream type'].find('text').node['namespace'])
                    o['stream type'] = u'text'
                o['content'] = self._menu[0].node
                normal['menu'] = [o]
            else: normal['menu'] = []
            
            # Finally, assign the stream kind by the aggregation
            # and append to self.stream
            for k,v in normal.iteritems():
                for o in v:
                    o['stream kind'] = k
                    self.stream.append(o)
                    
            # Clean up
            self._stream = None
            self._menu = None
    
    
    def _read(self):
        content = None
        if self.valid:
            if os.path.exists(self.ontology['path']):
                try:
                    reader = open(self.ontology['path'], 'r')
                    content = reader.read()
                    reader.close()
                except IOError as error:
                    self.log.error(str(error))
                    
            if content:
                self._detect_encoding(content)
                content = unicode(content, self.ontology['encoding'], errors='ignore')
        return content
    
    
    def _detect_encoding(self, content):
        if 'character encoding' not in self.meta:
            result = self.env.detect_encoding(content.splitlines())
            self.log.debug(u'%s encoding detected for %s with confidence %s', result['encoding'], unicode(self), result['confidence'])
            self.meta['character encoding'] = result['character encoding']
    
    
    def _fix(self, ontology):
        if ontology:
            
            # try to decode the genre as an enumerated genre type
            if 'genre' in ontology:
                element = self.env.enumeration['genre'].search(ontology['genre'])
                if element:
                    ontology['genre'] = element.name
                    ontology['genre type'] = element.key
                    
            # count cover pieces
            if 'cover' in ontology:
                ontology['cover'] = ontology['cover'].count('Yes')
                
            # expand the itunmovi plist
            if 'itunmovi' in ontology:
                for k,v in ontology['itunmovi'].iteritems():
                    key = self.env.enumeration['itunmovi'].parse(k)
                    if key:
                        items = [ i['name'].strip() for i in v ]
                        items = [ unicode(i) for i in items if i ]
                        if items:
                            ontology[key] = items
    

