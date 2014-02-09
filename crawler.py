# -*- coding: utf-8 -*-

import os
import logging
import base64
from datetime import datetime
from subprocess import Popen, PIPE
import xml.etree.cElementTree as ElementTree

from ontology import Ontology
from model.menu import Chapter, Menu
from model.caption import Caption, Slide

class Crawler(object):
    def __init__(self, ontology):
        self.log = logging.getLogger('Crawler')
        self.ontology = ontology
        self._node = None
        self._execution = None
        self.reload()
        
    def __unicode__(self):
        return unicode(self.ontology['resource uri'])
        
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
        return self._node
        
    def reload(self):
        if self.valid:
            self._node = None
            self._execution = {
                'crawl':{
                    'stream':[],
                    'menu':[],
                }
            }
            
            self._load_mediainfo()
            self._load_ogg_chapters()
            self._load_srt()
            self._load_ass()
            self._normalize()
            self._infer_profile()
            
            self._node = {
                'meta':self._execution['result']['meta'].node,
                'stream':[ o.node for o in self._execution['result']['stream'] ],
            }
            
            # Clean up
            self._execution = None
            
    def _load_mediainfo(self):
        command = self.env.initialize_command('mediainfo', self.log)
        if command:
            command.extend([u'--Language=raw', u'--Output=XML', u'--Full', self.ontology['path']])
            proc_mediainfo = Popen(command, stdout=PIPE, stderr=PIPE)
            proc_grep = Popen([u'grep', u'-v', u'Cover_Data'], stdin=proc_mediainfo.stdout, stdout=PIPE)
            raw_xml = proc_grep.communicate()[0]
            
            # fix mediainfo's violation of xml standards so that ElementTree won't choke on it
            # MediaInfoLib - v0.7.63 seems to be fixed already
            raw_xml = raw_xml.replace('dt:dt="binary.base64"', 'dt="binary.base64"')
            
            # parse the DOM
            element = ElementTree.fromstring(raw_xml)
            if element is not None:
                for node in element.findall(u'File/track'):
                    if 'type' in node.attrib:
                        mtype = self.env.enumeration['mediainfo stream type'].search(node.attrib['type'])
                        if mtype is not None:
                            if mtype.node['namespace']:
                                # initialize an ontology with the correct namespace
                                o = Ontology(self.env, mtype.node['namespace'])
                                
                                # iterate over the properties and populate the ontology
                                for item in list(node):
                                    text = item.text
                                    
                                    # decode base64 encoded element
                                    if 'dt' in item.attrib and item.attrib['dt'] == 'binary.base64':
                                        text = base64.b64decode(text)
                                        
                                    # set the concept on the ontology
                                    o.decode(item.tag, text)
                                    
                                # fix the video encoder settings on video tracks
                                if mtype.key == 'video':
                                    self._fix_mediainfo_encoder_settings(o)
                                    
                                # add the ontology to the stream stack
                                self._execution['crawl']['stream'].append(o)
                                
                            elif mtype.key == 'menu':
                                menu = Menu(self.env)
                                for item in list(node):
                                    menu.add(Chapter.from_raw(item.tag, item.text, Chapter.MEDIAINFO))
                                menu.normalize()
                                if menu.valid:
                                    self._execution['crawl']['menu'].append(menu)
                                    
            # Release resources held by the element, we no longer need it
            element.clear()
            
    def _load_ogg_chapters(self):
        if self.ontology['kind'] == 'chp':
            content = self._read()
            if content:
                content = content.splitlines()
                menu = Menu(self.env)
                for index in range(len(content) - 1):
                    menu.add(Chapter.from_raw(content[index], content[index + 1], Chapter.OGG))
                menu.normalize()
                if menu.valid:
                    self._execution['crawl']['menu'].append(menu)
                    
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
                    self._execution['crawl']['stream'].append(o)
                    
    def _load_ass(self):
        if self.ontology['kind'] == 'ass':
            content = self._read()
            if content:
                caption = Caption(self.env)
                content = content.splitlines()
                index = 0
                formation = None
                for line in content:
                    if line == u'[Events]':
                        match = self.env.expression['ass formation line'].search(content[index + 1])
                        if match is not None:
                            formation = match.group(1).strip().replace(u' ',u'').split(u',')
                        break
                    index += 1
                    
                if formation is not None:
                    start = formation.index('Start')
                    stop = formation.index('End')
                    text = formation.index('Text')
                    for line in content:
                        match = self.env.expression['ass subtitle line'].search(line)
                        if match is not None:
                            line = match.group(1).strip().split(',')
                            slide = Slide()
                            slide.begin.timecode = line[start]
                            slide.end.timecode = line[stop]
                            subtitle_text = u','.join(line[text:])
                            subtitle_text = self.env.expression['ass event command'].sub(self.env.constant['empty string'], subtitle_text)
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
                    self._execution['crawl']['stream'].append(o)
                    
    def _normalize(self):
        self._execution['breakdown'] = {
            'general':[ o for o in self._execution['crawl']['stream'] if o['stream type'] == u'general' ],
            'image':[ o for o in self._execution['crawl']['stream'] if o['stream type'] == u'image' ],
            'audio':[ o for o in self._execution['crawl']['stream'] if o['stream type'] == u'audio' ],
            'video':[ o for o in self._execution['crawl']['stream'] if o['stream type'] == u'video' ],
            'text':[ o for o in self._execution['crawl']['stream'] if o['stream type'] == u'text' ],
        }
        self._execution['normalized'] = {
            'image':[],
            'audio':[],
            'video':[],
            'caption':[],
            'menu':[],
            'preview':[],
        }
        self._execution['result'] = {
            'meta':None,
            'stream':[],
        }
        
        self._execution['normalized']['image'] = self._execution['breakdown']['image']
        
        # There should always be exactly one meta stream
        if self._execution['breakdown']['general']:
            del self._execution['breakdown']['general'][0]['stream type']
            self._execution['result']['meta'] = self._fix_meta(self._execution['breakdown']['general'][0])
            
        # Filter audio streams
        for o in self._execution['breakdown']['audio']:
            # Choose the minimum channel count for every audio stream
            if 'channel count' in o:
                o['channels'] = min(o['channel count'])
            self._execution['normalized']['audio'].append(o)
            
        # If the text stream format is 'Apple text' it is a chapter track in mp4,
        # otherwise its a caption stream
        for o in self._execution['breakdown']['text']:
            if o['format'] == u'Apple text':
                self._execution['normalized']['menu'].append(o)
            else:
                self._execution['normalized']['caption'].append(o)
                
        # Break the video streams into normal video and chapter preview images
        # by relative portion of the stream and locate the primary video stream
        for o in self._execution['breakdown']['video']:
            if o['format'] == u'JPEG' and o['stream portion'] < 0.01:
                self._execution['normalized']['preview'].append(o)
            else:
                self._execution['normalized']['video'].append(o)
                
        # There should only be one menu stream with one menu in it or none at all
        if self._execution['crawl']['menu']:
            if len(self._execution['normalized']['menu']) == 0:
                menu = Ontology(self.env, self.env.enumeration['mediainfo stream type'].find('text').node['namespace'])
            elif len(self._execution['normalized']['menu']) == 1:
                menu = self._execution['normalized']['menu'][0]
            else:
                self.log.warning(u'Multiple menu streams found for %s, ignoring all but the first', unicode(self))
                menu = self._execution['normalized']['menu'][0]
                
            menu['content'] = self._execution['crawl']['menu'][0].node
            self._execution['normalized']['menu'] = [ menu ]
        else:
            self._execution['normalized']['menu'] = []
            
        # clean up the now redundent stacks
        del self._execution['crawl']
        del self._execution['breakdown']
        
        # Finally, assign the stream kind by the aggregation and append to self.stream
        order = {'last':-1, 'missing':[]}
        for stream_kind, streams in self._execution['normalized'].iteritems():
            for stream in streams:
                # remove the mediainfo specific stream type 
                del stream['stream type']
                
                # assign the stream kind
                stream['stream kind'] = stream_kind
                
                # check the if an order is missing and account for the last
                if 'stream order' in stream:
                    order['last'] = max(order['last'], stream['stream order'])
                else:
                    order['missing'].append(stream)
                self._execution['result']['stream'].append(stream)
                
        # fix the streams with missing order
        if order['missing']:
            for stream in order['missing']:
                order['last'] += 1
                stream['stream order'] = order['last']
                
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
                self._detect_text_encoding(content)
                content = unicode(content, self.ontology['encoding'], errors='ignore')
        return content
        
    def _detect_text_encoding(self, content):
        if 'encoding' not in self.ontology:
            result = self.env.detect_encoding(content.splitlines())
            self.log.debug(u'%s encoding detected for %s with confidence %s', result['encoding'], unicode(self), result['confidence'])
            self.ontology['encoding'] = result['encoding']
            
    def _fix_mediainfo_encoder_settings(self, ontology):
        if 'encoder settings string' in ontology:
            if self.env.expression['mediainfo value list'].match(ontology['encoder settings string']):
                literals = ontology['encoder settings string'].split(u'/')
                value = {}
                for literal in literals:
                    pair = literal.split(u'=')
                    if len(pair) == 2:
                        value[pair[0].strip()] = pair[1].strip()
                ontology.decode('Parsed_Encoded_Library_Settings', value)
            else:
                self.log.error(u'Could not parse encoder settings %s', ontology['encoder settings string'])
            del ontology['encoder settings string']
            
    def _fix_meta(self, ontology):
        if ontology is None:
            ontology = Ontology(self.env, self.env.enumeration['mediainfo stream type'].find('general').node['namespace'])
        else:
            # try to decode the genre as an enumerated genre type
            if 'genre name' in ontology:
                element = self.env.enumeration['genre'].search(ontology['genre name'])
                if element:
                    ontology['genre name'] = element.name
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
        return ontology
        
    def _infer_profile(self):
        primary = None
        if self.ontology['essence'] and self.ontology['essence'] in self._execution['normalized']:
            for stream in self._execution['normalized'][self.ontology['essence']]:
                if primary is None or stream['stream portion'] > primary['stream portion']:
                    primary = stream
                    
            if primary:
                primary['primary'] = True
                
                if self.ontology['essence'] == 'video':
                    
                    # set the video profile
                    if 'format profile' in primary:
                        self._execution['result']['meta']['profile'] = primary['format profile'][0]
                    
                    # set dimentions on the meta element
                    self._execution['result']['meta']['width'] = float(primary['width'])
                    
                    if primary['display aspect ratio'] >= self.env.constant['playback aspect ration']:
                        self._execution['result']['meta']['height'] = self._execution['result']['meta']['width'] / self.env.constant['playback aspect ration']
                    else:
                        self._execution['result']['meta']['height'] = float(primary['height'])
                        
                elif self.ontology['essence'] == 'audio':
                    if primary['kind'] in set(('alac', 'flac', 'pcm')):
                        self._execution['result']['meta']['profile'] = 'lossless'
                        
                    elif primary['kind'] in set(('dts', 'ac3')):
                        self._execution['result']['meta']['profile'] = 'surround'
                        
                    elif primary['kind'] in set(('aac', 'mp3', 'ogg')):
                        self._execution['result']['meta']['profile'] = 'lossy'
                        
                elif self.ontology['essence'] == 'caption':
                    pass
                    
                elif self.ontology['essence'] == 'menu':
                    pass
                    
                elif self.ontology['essence'] == 'image':
                    pass
