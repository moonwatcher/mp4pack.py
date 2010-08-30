# -*- coding: utf-8 -*-

import re
import logging

import container

class MatroskaFile(container.ContainerFile):
    def __init__(self, file_path=None):
        container.ContainerFile.__init__(self, file_path)
        self.logger = logging.getLogger('mp4pack.container.matroska')
        
    
    
    def load(self, file_path):
        container.ContainerFile.load(self, file_path)
        
        from subprocess import Popen, PIPE
        mkvinfo_proc = Popen(["mkvinfo", self.file_path], stdout=PIPE)
        mkvinfo_report = mkvinfo_proc.communicate()[0].split('\n')        
        length = int(len(mkvinfo_report))
        index = 0
        in_mkvinfo_output = False
        in_segment_tracks = False
        in_chapters = False
        
        while index < length:
            if in_mkvinfo_output:            
                if (in_segment_tracks):
                    while mkvinfo_a_track_re.search(mkvinfo_report[index]):
                        index, track = _parse_track(index + 1, mkvinfo_report, _line_depth(mkvinfo_report[index]))
                        self.add_track(track)
                    in_segment_tracks = False
                
                elif (in_chapters):
                    while mkvinfo_chapter_atom_re.search(mkvinfo_report[index]):
                        index, chapter = _parse_chapter(index + 1, mkvinfo_report, _line_depth(mkvinfo_report[index]))
                        self.add_chapter(chapter)
                    in_chapters = False
                
                elif mkvinfo_segment_tracks_re.search(mkvinfo_report[index]):
                    in_segment_tracks = True
                    index += 1
                
                elif mkvinfo_chapters_re.search(mkvinfo_report[index]):
                    in_chapters = True
                    while mkvinfo_chapter_atom_re.search(mkvinfo_report[index]) == None:
                        index += 1
                else:
                    index += 1
            
            elif mkvinfo_start_re.search(mkvinfo_report[index]):
                in_mkvinfo_output = True
                index += 1
    


def is_matroska_file(file_path):
    import os
    extension = os.path.splitext(file_path)[1]
    return matroska_file_type_re.search(extension) != None



def _line_depth(mkvinfo_line):
    return mkvinfo_line_start_re.search(mkvinfo_line).start(0)


def _parse_track(index, mkvinfo_report, track_nest_depth):
    track = dict()
    while (_line_depth(mkvinfo_report[index]) > track_nest_depth):
        match = mkvinfo_track_number_re.search(mkvinfo_report[index])
        if match != None:
            track['number'] = match.group(1)
            index += 1
            continue
        match = mkvinfo_track_type_re.search(mkvinfo_report[index])
        if match != None:
            track['type'] = match.group(1)
            index += 1
            continue
        match = mkvinfo_codec_id_re.search(mkvinfo_report[index])
        if match != None:
            track['codec'] = match.group(1)
            index += 1
            continue
        match = mkvinfo_video_fps_re.search(mkvinfo_report[index])
        if match != None:
            track['frame_rate'] = match.group(1)
            index += 1
            continue
        match = mkvinfo_language_re.search(mkvinfo_report[index])
        if match != None:
            track['language'] = match.group(1)
            index += 1
            continue
        match = mkvinfo_name_re.search(mkvinfo_report[index])
        if match != None:
            track['name'] = match.group(1)
            index += 1
            continue
        match = mkvinfo_video_pixel_width_re.search(mkvinfo_report[index])
        if match != None:
            track['pixel_width'] = match.group(1)
            index += 1
            continue
        match = mkvinfo_video_pixel_height_re.search(mkvinfo_report[index])
        if match != None:
            track['pixel_height'] = match.group(1)
            index += 1
            continue
        match = mkvinfo_audio_sampling_frequency_re.search(mkvinfo_report[index])
        if match != None:
            track['sampling_frequency'] = match.group(1)
            index += 1
            continue
            
        index += 1
        
    return index, track


def _parse_chapter(index, mkvinfo_report, track_nest_depth):
    chapter = container.Chapter()
    while (_line_depth(mkvinfo_report[index]) > track_nest_depth):
        match = mkvinfo_chapter_start_re.search(mkvinfo_report[index])
        if match != None:
            chapter.set_start_time(match.group(1))
            index += 1
            continue
        match = mkvinfo_chapter_string_re.search(mkvinfo_report[index])
        if match != None:
            chapter.set_name(match.group(1))
            index += 1
            continue
        match = mkvinfo_chapter_language_re.search(mkvinfo_report[index])
        if match != None:
            chapter.set_language(match.group(1))
            index += 1
            continue
            
        index += 1
        
    return index, chapter


matroska_file_type_re = re.compile('\.mkv')
mkvinfo_start_re = re.compile('\+ EBML head')
mkvinfo_segment_tracks_re = re.compile('\+ Segment tracks')
mkvinfo_a_track_re = re.compile('\+ A track')
mkvinfo_track_number_re = re.compile('\+ Track number: ([0-9]+)')
mkvinfo_track_type_re = re.compile('\+ Track type: (.*)')
mkvinfo_codec_id_re = re.compile('\+ Codec ID: (.*)')
mkvinfo_language_re = re.compile('\+ Language: ([a-z]+)')
mkvinfo_name_re = re.compile('\+ Name: (.*)')
mkvinfo_video_fps_re = re.compile('\+ Default duration: .*ms \((.*) fps for a video track\)')
mkvinfo_audio_sampling_frequency_re = re.compile('\+ Sampling frequency: ([0-9]+)')
mkvinfo_video_pixel_width_re = re.compile('\+ Pixel width: ([0-9]+)')
mkvinfo_video_pixel_height_re = re.compile('\+ Pixel height: ([0-9]+)')
mkvinfo_chapters_re = re.compile('\+ Chapters')
mkvinfo_chapter_atom_re = re.compile('\+ ChapterAtom')
mkvinfo_chapter_start_re = re.compile('\+ ChapterTimeStart: ([0-9\.:]+)')
mkvinfo_chapter_string_re = re.compile('\+ ChapterString: (.*)')
mkvinfo_chapter_language_re = re.compile('\+ ChapterLanguage: ([a-z]+)')
mkvinfo_line_start_re = re.compile('\+')
