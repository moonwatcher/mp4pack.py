# -*- coding: utf-8 -*-

import re
import logging

import container

class MP4File(container.ContainerFile):
    def __init__(self, file_path=None):
        container.ContainerFile.__init__(self, file_path)
        self.logger = logging.getLogger('mp4pack.container.mp4')
        
    
    
    def load(self, file_path):
        container.ContainerFile.load(self, file_path)
        
        from subprocess import Popen, PIPE
        mp4info_proc = Popen(["mp4info", self.file_path], stdout=PIPE)
        mp4info_report = mp4info_proc.communicate()[0].split('\n')        
        length = int(len(mp4info_report))
        index = 0
        in_tag_section = False
        while index < length:
            if not in_tag_section:
                track = _parse_track(mp4info_report[index])            
                if track != None:
                    self.add_track(track)
                    index += 1
                    continue
                    
            name, value = _parse_tag(mp4info_report[index])
            if name != None:
                self.set_tag(name, value)
                if not in_tag_section:
                    in_tag_section = True
            index += 1
        
        mp4chaps_proc = Popen(["mp4chaps", "-l", self.file_path], stdout=PIPE)
        mp4chaps_report = mp4chaps_proc.communicate()[0].split('\n')        
        length = int(len(mp4chaps_report))
        index = 0
        while index < length:
            chapter = _parse_chapter(mp4chaps_report[index])
            if chapter != None:
                self.add_chapter(chapter)
            index += 1
    
    


def is_mp4_file(file_path):
    import os
    extension = os.path.splitext(file_path)[1]
    return mp4_file_type_re.search(extension) != None




def _parse_tag(mp4info_report_line):
    name = None
    value = None
    match = mp4info_tag_re.search(mp4info_report_line)
    if match != None:
        mp4info_tag_name = match.group(1)
        name = container.tag_map.canonic_name_from_mp4info(mp4info_tag_name)
        value = match.group(2)
    return name, value


def _parse_track(mp4info_report_line):
    track = None
    match = mp4info_video_track_re.search(mp4info_report_line)
    if match != None:
        track = { 'type':'video' }
        track['number'] = match.group(1)
        track['codec'] = match.group(2)
        track['duration'] = match.group(3)
        track['bit_rate'] = match.group(4)
        track['pixel_width'] = match.group(5)
        track['pixel_height'] = match.group(6)
        track['frame_rate'] = match.group(7)
    else:
        match = mp4info_audio_track_re.search(mp4info_report_line)
        if match != None:
            track = { 'type':'audio' }
            track['number'] = match.group(1)
            track['codec'] = match.group(2)
            track['duration'] = match.group(3)
            track['bit_rate'] = match.group(4)
            track['sampling_frequency'] = match.group(5)
    
    return track


def _parse_chapter(mp4chaps_report_line):
    chapter = None
    match = mp4chaps_chapter_re.search(mp4chaps_report_line)
    if match != None:
        chapter_start_time = match.group(2)
        chapter_name = match.group(3)
        chapter = container.Chapter(chapter_start_time, chapter_name)
    return chapter


mp4_file_type_re = re.compile('\.(mp4|m4v|m4a|m4b)')
mp4info_video_track_re = re.compile('([0-9]+)	video	([^,]+), ([0-9\.]+) secs, ([0-9\.]+) kbps, ([0-9]+)x([0-9]+) @ ([0-9\.]+) fps')
mp4info_h264_video_codec_re = re.compile('H264 ([^@]+)@([0-9\.]+)')
mp4info_audio_track_re = re.compile('([0-9]+)	audio	([^,]+), ([0-9\.]+) secs, ([0-9\.]+) kbps, ([0-9]+) Hz')
mp4info_tag_re = re.compile(' ([^:]+): (.*)$')
mp4chaps_chapter_re  = re.compile('Chapter #([0-9]+) - ([0-9:\.]+) - (.*)$')

