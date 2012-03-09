#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import plistlib
import logging
from ontology import Ontology
from subprocess import Popen, PIPE
import xml.etree.cElementTree as ElementTree
from datetime import datetime

from model import Timestamp, Chapter, Slide, Caption, Menu

class Crawler(object):
    def __init__(self, ontology):
        self.log = logging.getLogger('crawler')
        self.ontology = ontology
        self.tag = Ontology.clone(ontology)
        self.track = []
        
        self.load()
    
    
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
        node = {
            'ontology':self.ontology.node,
            'tag':self.tag.node,
            'track':[],
        }
        
        for track in self.track:
            node['track'].append(track.node)
            
        return node
    
    
    # Loading...
    def load(self):
        self._load_mediainfo()
        
        self._fix_cover()
        
        # Find the main video stream and add playback dimensions accordingly
        self._exapnd_playback_dimensions()
        
        if self.ontology['format'] == u'AC-3' or self.ontology['format'] == u'DTS':
            for index,track in enumerate(self.track):
                track['track id'] = index
                
        if self.ontology['format'] == u'MPEG-4':
            
            # Add tag info from mp4info for MPEG-4
            self._load_mp4info()
            
            # Expand lists from the itunmovi plist atom
            self._expand_itunmovi()
            
            # If gnre is present and ©gen isn't 
            # set ©gen to the print value of the enumerated gnre
            # Confusing isn't it?
            self._fix_genre()
            
        if self.ontology['kind'] == 'chpl':
            self._load_ogg_chapters()
            
        elif self.ontology['kind'] == 'srt':
            self._load_srt()
            
        elif self.ontology['kind'] == 'ass':
            self._load_ass()
    
    
    def _load_mediainfo(self):
        if self.valid:
            command = self.env.initialize_command('mediainfo', self.log)
            if command:
                command.extend([u'--Language=raw', u'--Output=XML', u'-f', self.ontology['path']])
                proc_mediainfo = Popen(command, stdout=PIPE, stderr=PIPE)
                proc_grep = Popen([u'grep', u'-v', u'Cover_Data'], stdin=proc_mediainfo.stdout, stdout=PIPE)
                report = proc_grep.communicate()
                element = ElementTree.fromstring(report[0])
                if element is not None:
                    menu = None
                    file_nodes = element.findall(u'File')
                    if file_nodes:
                        track_nodes = file_nodes[0].findall(u'track')
                        if track_nodes:
                            for track_node in track_nodes:
                                if 'type' in track_node.attrib:
                                    track_type = unicode(track_node.attrib['type'].lower())
                                    if track_type == 'general':
                                        for i in track_node:
                                            self._set_concept(self.ontology, self.env.prototype['crawl']['file'], 'mediainfo', i.tag, i.text)
                                            self._set_concept(self.tag, self.env.prototype['crawl']['tag'], 'mediainfo', i.tag, i.text)
                                            
                                    elif track_type in self.env.prototype['track']:
                                        track = Ontology(self.env)
                                        track['type'] = track_type
                                        for i in track_node:
                                            self._set_concept(track, self.env.prototype['track'][track_type], 'mediainfo', i.tag, i.text)
                                        self._add_track(track)
                                        
                                    elif track_type == 'menu':
                                        menu = Menu(self.env)
                                        for i in track_node:
                                            menu.add(Chapter.from_raw(i.tag, i.text, Chapter.MEDIAINFO))
                                            
                    if menu is not None:
                        menu_track = [ t for t in self.track if t['format'] == u'Apple text' ]
                        if menu_track:
                            menu_track = menu_track[0]
                        else:
                            menu_track = Ontology(self.env)
                            menu_track['type'] = u'text'
                            menu_track['codec'] = u'chpl'
                            self._add_track(menu_track)
                            
                        menu.normalize()
                        if menu.valid:
                            menu_track['content'] = menu.node
                            
                # Release resources held by the element, we no longer need it
                element.clear()
    
    
    def _load_mp4info(self):
        command = self.env.initialize_command('mp4info', self.log)
        if command:
            command.append(self.ontology['path'])
            proc = Popen(command, stdout=PIPE, stderr=PIPE)
            report = proc.communicate()
            mp4info_report = unicode(report[0], 'utf-8').splitlines()
            for line in mp4info_report:
                match = self.env.expression['mp4info tag'].search(line)
                if match is not None:
                    tag = match.groups()
                    self._set_concept(self.tag, self.env.prototype['crawl']['tag'], 'mp4info', tag[0], tag[1])
    
    
    def _load_ogg_chapters(self):
        content = self._read()
        if content:
            content = content.splitlines()
            menu = Menu(self.env)
            for index in range(len(content) - 1):
                menu.add(Chapter.from_raw(content[index], content[index + 1], Chapter.OGG))
                
            menu.normalize()
            if menu.valid:
                track = Ontology(self.env)
                track['content'] = menu.node
                track['type'] = 'text'
                track['codec'] = 'chpl'
                track['language'] = self.ontology['language']
                self._add_track(track)
    
    
    def _load_srt(self):
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
                track = Ontology(self.env)
                track['content'] = caption.node
                track['track id'] = 0
                track['position'] = 0
                track['type'] = 'text'
                track['codec'] = 'srt'
                track['language'] = self.ontology['language']
                self._add_track(track)
    
    
    def _load_ass(self, lines):
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
                track = Ontology(self.env)
                track['content'] = caption.node
                track['track id'] = 0
                track['position'] = 0
                track['type'] = 'text'
                track['codec'] = 'ass'
                track['language'] = self.ontology['language']
                self._add_track(track)
    
    
    def _add_track(self, track):
        result = True
        
        result = result and self._expand_track_codec(track)
        #result = result and track['format'] != u'Apple text'
        result = result and self._expand_channel_configuration(track)
        result = result and self._reset_undefined_language(track)
        
        if result:
            self.track.append(track)
    
    
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
        if 'encoding' not in self.ontology:
            result = self.env.detect_encoding(content.splitlines())
            self.log.debug(u'%s encoding detected for %s with confidence %s', result['encoding'], unicode(self), result['confidence'])
            self.ontology['encoding'] = result['encoding']
    
    
    def _set_concept(self, ontology, space, index, key, value):
        prototype = space.find(index, key)
        if prototype:
            ontology[prototype.name] = prototype.cast(value)
    
    
    def _expand_itunmovi(self):
        if 'itunmovi' in self.tag:
            for k,v in self.tag['itunmovi'].iteritems():
                element = self.env.model['itunemovi'].find('plist', k)
                if element:
                    items = [ i['name'].strip() for i in v ]
                    items = [ unicode(i) for i in items if i ]
                    if items:
                        self.tag[element.key] = items
    
    
    def _fix_genre(self):
        # If gnre is present and ©gen isn't 
        # set ©gen to the print value of the enumerated gnre
        # Confusing isn't it?
        if 'genre type' in self.tag:
            self.tag['genre type'] = int(self.tag['genre type'].split(u',')[0])
            if 'genre' not in self.tag:
                element = self.env.model['gnre'].find('name', self.tag['genre type'])
                if element:
                    self.tag['genre'] = element.node['print']
    
    
    def _fix_cover(self):
        if 'cover' in self.tag:
            self.tag['cover'] = self.tag['cover'].count('Yes')
    
    
    def _reset_undefined_language(self, track):
        if track['language'] == 'und':
            del track['language']
        return True
    
    
    def _expand_channel_configuration(self, track):
        # Set the channels count as the minimum of all configurations
        if 'channel configuration' in track:
            track['channels'] = min(track['channel configuration'])
        return True
    
    
    def _expand_track_codec(self, track):
        if 'format' in track:
            if track['type'] == 'text':
                if track['format'] == 'Timed text':
                    track['codec'] = u'tx3g'
                elif track['format'] == 'Apple text':
                    track['codec'] = u'chpl'
                elif track['format'] == 'UTF-8':
                    track['codec'] = u'srt'
                elif track['format'] == 'ASS':
                    track['codec'] = u'ass'
                elif track['format'] == 'PGS':
                    track['codec'] = u'pgs'
                elif track['format'] == 'RLE':
                    track['codec'] = u'rle'
                    
            elif track['type'] == 'audio':
                if track['format'] == 'AC-3':
                    track['codec'] = u'ac3'
                elif track['format'] == 'MPEG Audio':
                    track['codec'] = u'mp3'
                elif track['format'] == 'DTS':
                    track['codec'] = u'dts'
                elif track['format'] == 'AAC':
                    track['codec'] = u'aac'
                elif track['format'] == 'PCM':
                    track['codec'] = u'pcm'
                    
            elif track['type'] == 'video':
                if track['format'] == 'AVC':
                    track['codec'] = u'h.264'
                elif track['format'] == 'MPEG-4 Visual':
                    track['codec'] = u'h.263'
                elif track['format'] == 'H.263':
                    track['codec'] = u'h.263'
                elif track['format'] == 'MPEG Video':
                    track['codec'] = u'h.262'
                elif track['format'] == 'JPEG':
                    track['codec'] = u'jpeg'
                    
            elif track['type'] == 'image':
                if track['format'] == 'LZ77':
                    track['codec'] = u'png'
                elif track['format'] == 'JPEG':
                    track['codec'] = u'jpg'
                    
        return True
    
    
    def _exapnd_playback_dimensions(self):
        # Find the main video stream and add playback dimensions accordingly
        main = None
        for t in self.track:
            if t['type'] == 'video' and (main is None or t['stream size'] > main['stream size']):
                main = t
        if main:
            self.tag['width'] = float(main['width'])
            if main['display aspect ratio'] >= self.env.configuration['playback']['aspect ratio']:
                self.tag['height'] = self.tag['width'] / self.env.configuration['playback']['aspect ratio']
            else:
                self.tag['height'] = float(main['height'])
    

