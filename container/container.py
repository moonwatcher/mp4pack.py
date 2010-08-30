# -*- coding: utf-8 -*-

import os
import re
import logging


class ContainerFile(object):
    
    def __init__(self, file_path=None):
        self.logger = logging.getLogger('mp4pack.container')
        self.file_path = None
        self.file_type = None
        self.exists = False
        self.tracks = []
        self.chapters = []
        self.tags = dict()
        if file_path != None:
            self.load(file_path)
    
    
    def set_tag(self, name, value):
        self.tags[name] = value
    
    
    def add_track(self, track):
        self.tracks.append(track)
    
    
    def add_chapter(self, chapter):
        self.chapters.append(chapter)
    
    
    def load(self, file_path):
        if os.path.isfile(file_path):
            self.exists = True
            self.file_path = os.path.abspath(file_path)
            self.file_type = os.path.splitext(self.file_path)[1]
    
    
    def print_chapters(self):
        return ('\n'.join(["%s" % chapter for chapter in self.chapters]))
    
    
    def print_tags(self):
        return ('\n'.join(["%s: %s" % (key, self.tags[key]) for key in sorted(set(self.tags))]))
    
    
    def print_tracks(self):
        return ('\n'.join(["%s" % track for track in self.tracks]))
    
    
    def __str__(self):
        return '\n\n'.join((self.file_path, self.print_tracks(), self.print_tags(), self.print_chapters()))


class Chapter(object):
    def __init__(self, start_time=None, name=None, language=None):
        self.set_start_time(start_time)
        self.set_name(name)
        self.set_language(language)
    
    
    def set_start_time(self, start_time):
        if start_time != None:
            self.start_time = timecode_to_miliseconds(start_time)
        else:
            self.start_time = None
    
    
    def set_name(self, name):
        if name != None:
            self.name = name.strip('"')
        else:
            self.name = None
    
    
    def set_language(self, language):
        if language != None:
            self.language = language
        else:
            self.language = None
    
    
    def __str__(self):
        return "%s : %s" % (miliseconds_to_time(self.start_time), self.name)
    


class TagMap(object):
    def __init__(self):
        self.canonic_map = dict()
        self.mp4info_map = dict()
        
        from config import tag_name
        
        for tag in tag_name:
            self.canonic_map[tag[0]] = tag
            if tag[2] != None:
                self.mp4info_map[tag[2]] = tag
    
    
    def canonic_name_from_mp4info(self, name):
        result = None
        if name in self.mp4info_map:
            result = self.mp4info_map[name][0]
        return result
    
    




def timecode_to_miliseconds(timecode):
    result = None
    hours = 0
    minutes = 0
    seconds = 0
    milliseconds = 0
    valid = False
    
    match = full_numeric_time_format.search(timecode)
    if match != None:
        hours = match.group(1)
        minutes = match.group(2)
        seconds = match.group(3)
        milliseconds = match.group(4)
        valid = True
        
    else:
        match = descriptive_time_format.search(timecode)
        if match != None:
            if match.group(1) != None:
                hours = match.group(1)
            if match.group(2) != None:
                minutes = match.group(2)
            if match.group(3) != None:
                seconds = match.group(3)
            if match.group(4) != None:
                milliseconds = match.group(4)
            valid = True
            
    if milliseconds != None:
        if len(milliseconds) == 2:
            milliseconds = 10 * int(milliseconds)
        elif len(milliseconds) >= 3:
            milliseconds = milliseconds[0:3]
            milliseconds = int(milliseconds)
        else:
            milliseconds = int(milliseconds)
    else:
        milliseconds = 0
        
    if seconds != None:
        seconds = int(seconds)
    else:
        seconds = 0
        
    if minutes != None:
        minutes = int(minutes)
    else:
        minutes = 0
        
    if hours != None:
        hours = int(hours)
    else:
        hours = 0
        
    result = (hours * 3600 + 60 * minutes + seconds) * 1000 + milliseconds
    
    return result


def miliseconds_to_time(miliseconds, millisecond_sep='.'):
    hours = int(miliseconds) / int(3600*1000)
    hours_modulo = int(miliseconds) % int(3600*1000)
    minutes = int(hours_modulo) / int(60*1000)
    minutes_modulo = int(hours_modulo) % int(60*1000)
    seconds = int(minutes_modulo) / int(1000)
    seconds_modulo = int(minutes_modulo) % int(1000)
    milliseconds = int(seconds_modulo)
    return '%02d:%02d:%02d%s%03d' % (hours, minutes, seconds, millisecond_sep, milliseconds)


tag_map = TagMap()

movie_kind_schema = re.compile('^IMDb(tt[0-9]+) ?(.*)\.([^\.]+)$')
tvshow_episode_kind_schema = re.compile('^(.*) (s([0-9]+)e([0-9]+))(.*)\.([^\.]+)$')

full_numeric_time_format = re.compile('([0-9]{,2}):([0-9]{,2}):([0-9]{,2})(?:\.|,)([0-9]+)')
descriptive_time_format = re.compile('(?:([0-9]{,2})h)?(?:([0-9]{,2})m)?(?:([0-9]{,2})s)?(?:([0-9]+))?')