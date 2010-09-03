# -*- coding: utf-8 -*-

import os
import re
import logging
import hashlib
from config import repository_config
from db import TagManager

def load_media_file(file_path):
    f = None
    file_type = os.path.splitext(file_path)[1].strip('.')
    
    if file_type in container_type['Mpeg4']:
        f = Mpeg4(file_path)
    elif file_type in container_type['Matroska']:
        f = Matroska(file_path)
    elif file_type in container_type['Subtitle']:
        f = Subtitle(file_path)
    
    return f




# Container super Class

class Container(object):
    def __init__(self, file_path):
        self.logger = logging.getLogger('mp4pack.container')
        self.exists = False
        self.file_path = None
        self.meta = None
        if os.path.isfile(file_path):
            self.exists = True
            self.file_path = os.path.abspath(file_path)
            self.file_info = file_detail_detector.detect(self.file_path)
    
    
    def load(self):
        self.load_meta()
    
    
    def clean(self, path):
        try:
            os.remove(path)
            os.removedirs(os.path.dirname(path))
        except OSError:
            pass
    
    
    def copy(self, volume, profile, overwrite=False, md5=False):
        dest_path = self.canonic_path(volume, profile)
        if os.path.exists(dest_path) and not overwrite:
            self.logger.warning('Not overwriting ' + dest_path)
        else:
            dirname = os.path.dirname(dest_path)
            if not os.path.exists(dirname):
                os.makedirs(dirname)
            
            self.logger.info('Copy ' + self.file_path + ' --> ' + dest_path)
            from subprocess import Popen, PIPE
            proc = Popen(["rsync", self.file_path, dest_path], stdout=PIPE)
            report = proc.communicate()
            
            if report[1] != None and len(report[1]) > 0:
                self.logger.error(report[1])
            if report[0] != None and len(report[0]) > 0:
                self.logger.info(report[0])
            
            if not os.path.exists(dest_path):
                self.clean(dest_path)
            if md5:
                self.check(dest_path)
        
    
    
    def check(self, path):
        result = False
        if os.path.exists(self.file_path) and os.path.exists(path):
            source_md5 = hashlib.md5(file(self.file_path).read()).hexdigest()
            dest_md5 = hashlib.md5(file(path).read()).hexdigest()
            if source_md5 == dest_md5:
                self.logger.info('md5 match: ' + source_md5 + ' ' + self.canonic_name())
                result = True
            else:
                self.logger.error('md5 mismatch: ' + source_md5 + ' ' + dest_md5 + ' ' + self.canonic_name())
        return result
    
    
    def is_movie(self):
        return self.file_info != None and set(('media_kind', 'imdb_id')).issubset(set(self.file_info.keys())) and self.file_info['media_kind'] == 'movie'
    
    
    def is_tvshow(self):
        return self.file_info != None and set(('media_kind', 'show_small_name', 'season_number', 'episode_number')).issubset(set(self.file_info.keys())) and self.file_info['media_kind'] == 'tvshow'
    
    
    def _load_genre(self, record):
        if 'genre' in record.keys():
            if len(record['genre']) > 0:
                g = record['genre'][0]
                self.meta['Genre'] = g['name']
                if 'itmf_code' in g.keys():
                    self.meta['GenreID'] = g['itmf_code']
        return
    
    
    def _load_cast(self, record):
        if 'cast' in record.keys():
            directors = [ r for r in record['cast'] if r['job'] == 'director' ]
            codirectors = [ r for r in record['cast'] if r['job'] == 'director of photography' ]
            producers = [ r for r in record['cast'] if r['job'].count('producer') > 0 ]
            screenwriters = [ r for r in record['cast'] if r['job'] == 'screenplay' or r['job'] == 'author' ]
            actors = [ r for r in record['cast'] if r['job'] == 'actor' ]
            
            artist = None
            if len(directors) > 0:
                if artist == None:
                    artist = directors[0]
                self.meta['Director'] = ', '.join([ d['name'] for d in directors ])
            
            if len(codirectors) > 0:
                if artist == None:
                    artist = codirectors[0]
                self.meta['Codirector'] = ', '.join([ d['name'] for d in codirectors ])
            
            if len(producers) > 0:
                if artist == None:
                    artist = producers[0]
                self.meta['Producers'] = ', '.join([ d['name'] for d in producers ])
            
            if len(screenwriters) > 0:
                if artist == None:
                    artist = screenwriters[0]
                self.meta['Screenwriters'] = ', '.join([ d['name'] for d in screenwriters ])
            
            if len(actors) > 0:
                if 'Cast' in self.meta and self.meta['Cast'] != None:
                    self.meta['Cast'] = ', '.join([self.meta['Cast'], ', '.join([ d['name'] for d in actors ])])
                else:
                    self.meta['Cast'] = ', '.join([ d['name'] for d in actors ])
                    
                if artist == None:
                    artist = actors[0]
                
            if artist != None:
                self.meta['Artist'] = artist['name']
        return
    
    
    def _load_movie_meta(self):
        result = False
        if self.is_movie():
            record = tag_manager.find_movie_by_imdb_id(self.file_info['imdb_id'])
            if record != None:
                self.meta = {'Media Kind':self.file_info['media_kind']}
                
                if 'name' in record:
                    self.meta['Name'] = record['name']
                if 'overview' in record:
                    self.meta['Long Description'] = record['overview']
                if 'content_rating' in record:
                    self.meta['Rating'] = record['content_rating']
                if 'released' in record:
                    self.meta['Release Date'] = record['released'].strftime("%Y-%m-%d")
                if 'tagline' in record:
                    self.meta['Description'] = record['tagline']
                
                self._load_cast(record)
                self._load_genre(record)
                result = True
        return result
    
    
    def _load_tvshow_meta(self):
        result = False
        if self.is_tvshow():
            show, episode = tag_manager.find_episode(self.file_info['show_small_name'], self.file_info['season_number'], self.file_info['episode_number'])
            if show != None and episode != None:
                self.meta = {'Media Kind':self.file_info['media_kind']}
                
                if 'content_rating' in show:
                    self.meta['Rating'] = show['content_rating']
                if 'network' in show:
                    self.meta['TV Network'] = show['network']
                
                self._load_genre(show)
                
                if 'cast' in show.keys():
                    actors = [ r for r in show['cast'] if r['job'] == 'actor' ]
                    if len(actors) > 0:
                        self.meta['Cast'] = ', '.join([ d['name'] for d in actors ])
                
                if 'show' in episode:
                    self.meta['TV Show'] = episode['show']
                    self.meta['Album'] = episode['show']
                if 'season_number' in episode:
                    self.meta['TV Season'] = episode['season_number']
                    self.meta['Disk #'] = episode['season_number']
                if 'episode_number' in episode:
                    self.meta['TV Episode #'] = episode['episode_number']
                    self.meta['Track #'] = episode['episode_number']
                if 'name' in episode:
                    self.meta['Name'] = episode['name']
                if 'overview' in episode:
                    self.meta['Long Description'] = episode['overview']
                    self.meta['Description'] = episode['overview']
                if 'released' in episode:
                    self.meta['Release Date'] = episode['released'].strftime("%Y-%m-%d")
                
                self._load_cast(episode)
                result = True
        return result
    
    
    def load_meta(self):
        result = False
        self.meta = list()
        if self.is_movie():
            result = self._load_movie_meta()
        elif self.is_tvshow():
            result = self._load_tvshow_meta()
        
        if not result:
            self.meta = None
            
        return result
    
    
    def canonic_name(self, info=None):
        result = None
        if info == None:
            info = self.file_info
        if self.is_movie():
            result = ''.join(['IMDb', info['imdb_id'], ' ', info['name'], '.', info['type']])
        elif self.is_tvshow():
            result = ''.join([info['show_small_name'], ' ', info['code'], ' ', info['name'], '.', info['type']])
        return result
    
    
    def canonic_path(self, volume, profile, info=None):
        result = repository_config['volumes'][volume]
        if info == None:
            info = self.file_info
        if self.is_movie():
            result = os.path.join(result, info['media_kind'], info['type'], profile)
        elif self.is_tvshow():
            result = os.path.join(result, info['media_kind'], info['type'], profile, info['show_small_name'], str(info['season_number']))
            
        if info['type'] in container_type['Subtitle']:
            result = os.path.join(result, info['language'])
            
        result = os.path.join(result, self.canonic_name(info))
        return result
    
    
    def print_meta(self):
        result = None
        if self.meta != None:
            result = ('\n'.join(["%s: %s" % (key, self.meta[key]) for key in sorted(set(self.meta))]))
        return result
    
    
    def print_file_info(self):
        result = None
        if self.file_info != None:
            result = ('\n'.join(["%s: %s" % (key, self.file_info[key]) for key in sorted(set(self.file_info))]))
        return result
    
    
    def __str__(self):
        result = None
        if self.exists:
            result = '\n' + self.file_path
            if self.file_info != None and len(self.file_info) > 0:
                result = '\n'.join((result, '\n# Parsed from path: ', self.print_file_info()))
            if self.meta != None and len(self.meta) > 0:
                result = '\n'.join((result, '\n# Meta: ', self.print_meta()))
        else:
            result = '\nfile does not exist'
        return result
    
    


class AVContainer(Container):
    def __init__(self, file_path):
        Container.__init__(self, file_path)
        self.logger = logging.getLogger('mp4pack.avcontainer')
        self.tracks = []
        self.chapters = []
        self.tags = dict()
        self.load()
        
    
    
    def set_tag(self, name, value):
        self.tags[name] = value
    
    
    def add_track(self, track):
        if track != None:
            self.tracks.append(track)
    
    
    def add_chapter(self, chapter):
        if chapter != None:
            self.chapters.append(chapter)
    
    
    def print_chapters(self):
        return ('\n'.join(["%s" % chapter for chapter in self.chapters]))
    
    
    def print_tags(self):
        return ('\n'.join(["%s: %s" % (key, self.tags[key]) for key in sorted(set(self.tags))]))
    
    
    def print_tracks(self):
        return ('\n'.join(["%s" % track for track in self.tracks]))
    
    
    def __str__(self):
        result = Container.__str__(self)
        if self.exists:
            if len(self.tracks) > 0:
                result = '\n'.join((result, '\n# Tracks: ', self.print_tracks()))
            if len(self.tags) > 0:
                result = '\n'.join((result, '\n# Tags: ', self.print_tags()))
            if len(self.chapters) > 0:
                result = '\n'.join((result, '\n# Chapter: ', self.print_chapters()))
        
        return result
    
    


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
    





# Matroska Class

class Matroska(AVContainer):
    def __init__(self, file_path):
        AVContainer.__init__(self, file_path)
        self.logger = logging.getLogger('mp4pack.container.matroska')
    
    
    def _line_depth(self, mkvinfo_line):
        return mkvinfo_line_start_re.search(mkvinfo_line).start(0)
    
    
    def _parse_track(self, index, mkvinfo_report, track_nest_depth):
        track = dict()
        while (self._line_depth(mkvinfo_report[index]) > track_nest_depth):
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
    
    
    def _parse_chapter(self, index, mkvinfo_report, track_nest_depth):
        chapter = Chapter()
        while (self._line_depth(mkvinfo_report[index]) > track_nest_depth):
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
    
    
    def load(self):
        AVContainer.load(self)
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
                        index, track = self._parse_track(index + 1, mkvinfo_report, self._line_depth(mkvinfo_report[index]))
                        self.add_track(track)
                    in_segment_tracks = False
                    
                elif (in_chapters):
                    while mkvinfo_chapter_atom_re.search(mkvinfo_report[index]):
                        index, chapter = self._parse_chapter(index + 1, mkvinfo_report, self._line_depth(mkvinfo_report[index]))
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




# Mpeg4 Class

class Mpeg4(AVContainer):
    def __init__(self, file_path):
        AVContainer.__init__(self, file_path)
        self.logger = logging.getLogger('mp4pack.container.mp4')
    
    
    def _parse_tag(self, mp4info_report_line):
        name = None
        value = None
        match = mp4info_tag_re.search(mp4info_report_line)
        if match != None:
            mp4info_tag_name = match.group(1)
            name = tag_name_resolver.canonic_name_from_mp4info(mp4info_tag_name)
            value = match.group(2)
        return name, value
    
    
    def _parse_track(self, mp4info_report_line):
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
    
    
    def _parse_chapter(self, mp4chaps_report_line):
        chapter = None
        match = mp4chaps_chapter_re.search(mp4chaps_report_line)
        if match != None:
            chapter_start_time = match.group(2)
            chapter_name = match.group(3)
            chapter = Chapter(chapter_start_time, chapter_name)
        return chapter
    
    
    def load(self):
        AVContainer.load(self)
        
        from subprocess import Popen, PIPE
        mp4info_proc = Popen(["mp4info", self.file_path], stdout=PIPE)
        mp4info_report = mp4info_proc.communicate()[0].split('\n')        
        length = int(len(mp4info_report))
        index = 0
        in_tag_section = False
        while index < length:
            if not in_tag_section:
                track = self._parse_track(mp4info_report[index])            
                if track != None:
                    self.add_track(track)
                    index += 1
                    continue
                    
            name, value = self._parse_tag(mp4info_report[index])
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
            chapter = self._parse_chapter(mp4chaps_report[index])
            if chapter != None:
                self.add_chapter(chapter)
            index += 1
    
    


mp4info_video_track_re = re.compile('([0-9]+)	video	([^,]+), ([0-9\.]+) secs, ([0-9\.]+) kbps, ([0-9]+)x([0-9]+) @ ([0-9\.]+) fps')
mp4info_h264_video_codec_re = re.compile('H264 ([^@]+)@([0-9\.]+)')
mp4info_audio_track_re = re.compile('([0-9]+)	audio	([^,]+), ([0-9\.]+) secs, ([0-9\.]+) kbps, ([0-9]+) Hz')
mp4info_tag_re = re.compile(' ([^:]+): (.*)$')
mp4chaps_chapter_re  = re.compile('Chapter #([0-9]+) - ([0-9:\.]+) - (.*)$')




# Subtitle Class

class Subtitle(Container):
    def __init__(self, file_path, input_frame_rate='25', output_frame_rate='25', format=None):
        Container.__init__(self, file_path)
        self.logger = logging.getLogger('mp4pack.container.subtitle')
        self.input_frame_rate = input_frame_rate
        self.output_frame_rate = output_frame_rate
        self.time_begin = []
        self.time_end = []
        self.subtitle_list = []
        #self.load(file_path)
    
    
    def load(self):
        Container.load(self)
        if self.exists:
            file_lines = self.read_subtitle_file()
            self.decode(file_lines)
            if self.input_frame_rate != self.output_frame_rate:
                self.change_framerate()
            self.filter_lines()
        
    
    
    def write(self, output_file=None):
        file_lines = self.encode()
        self.write_subtitle_file(file_lines, output_file)
    
    
    def read_subtitle_file(self):
        file_lines = None
        if self.file_path == None:
            try:
                file_lines = sys.stdin.readlines()
            except:
                sys.stderr.write("Cannot read stdin\n")
        else:
            try:
                file_reader = open(self.file_path, 'r')
            except:
                sys.stderr.write("Cannot open file\n")
            file_lines = file_reader.readlines()
            file_reader.close()
        
        for index in range(len(file_lines)):
            if rmdos.search(file_lines[index]):
                clean_line = rmdos.sub('\n', file_lines[index])
                del file_lines[index]
                file_lines.insert(index, clean_line)
        return file_lines
    
    
    def write_subtitle_file(self, file_lines, output_file=None):
        end = '\n'    
        try:
            if output_file == None:
                for line in file_lines:
                    if line == '\n':
                        sys.stdout.write(end)
                    else:
                        sys.stdout.write(line + end)
            else:
                file_writer = open(output_file, 'w') 
                for line in file_lines:
                    if line == '\n':
                        file_writer.write(end)
                    else:
                        file_writer.write(line + end)
                        
                file_writer.close
        except IOError:
            if output_file == '-':
                sys.stderr.write("Can not write to stdout.\n")
            else:
                sys.stderr.write("Can not write to file " + output_file + ".\n")
    
    
    def encode(self):
        length = int(len(self.subtitle_list))
        index = 0
        file_lines = ['\n']
        while index < length:
            file_lines.append(str(index + 1))
            begin = miliseconds_to_time(self.time_begin[index], ',')
            stop = miliseconds_to_time(self.time_end[index], ',')
            file_lines.append(str(begin) +' --> '+str(stop))
            file_lines.append(str(self.subtitle_list[index]).replace('\N','\n'))
            file_lines.append('\n')
            index = index + 1
        return file_lines
    
    
    def decode(self, file_lines):
        def decode_srt(file_lines):
            indexlist= []
            for index in range(len(file_lines)):
                match = srt_time_line.search(file_lines[index])
                if match != None and str(file_lines[index - 1].strip('\n')).isdigit():
                    indexlist.append(index)
                    begin = timecode_to_miliseconds(match.group(1))
                    end = timecode_to_miliseconds(match.group(2))
                    self.time_begin.append(begin)
                    self.time_end.append(end)
            
            indexlist.append(len(file_lines) + 1)
            
            a = 0
            for index in indexlist[0:-1]:
                a = a + 1
                firstline = index + 1
                lastline = indexlist[a] - 1
                subline = ''.join(file_lines[firstline:lastline])
                while True:
                    if subtitle_noneline.search(subline):
                        subline = subtitle_noneline.sub('',subline)
                    else:
                        break
                self.subtitle_list.append(subline.replace('\n', '\N'))
        
        
        def decode_ass(file_lines):
            index = 0
            for line in file_lines:
                if line == '[Events]\n':
                    formation = file_lines[index + 1].replace(':',',').replace(' ','').strip('\n').split(',')
                    break
                index = index + 1
                
            start = formation.index('Start')
            stop = formation.index('End')
            text = formation.index('Text')
            for line in file_lines:
                if ass_subline.search(line):
                    line = re.sub('\n$','',line).split(',')
                    linepart = line[0].split(':')
                    del line[0]
                    line.insert(0, linepart[0])
                    line.insert(1, ':'.join(linepart[1: len(linepart)]))
                    
                    self.time_begin.append(timecode_to_miliseconds(line[start]))
                    self.time_end.append(timecode_to_miliseconds(line[stop]))
                    
                    subpart = ','.join(line[text:1 + text + (len(line) - len(formation))])
                    subpart = ass_event_command_re.sub('', subpart)
                    self.subtitle_list.append(subpart.replace(r'\n', '\N'))
        
        
        def decode_sub(file_lines, frame_rate):
            frame_rate = frame_rate_to_float(frame_rate)
            for line in file_lines:
                if sub_line_begin.search(line):
                    line = line.split('}',2)
                    self.time_begin.append(frame_to_miliseconds(line[0].strip('{'), frame_rate))
                    self.time_end.append(frame_to_miliseconds(line[1].strip('{'), frame_rate))
                    self.subtitle_list.append(line[2].strip('\n').replace('|', '\N'))
        
        
        if self.file_info['type'] == 'srt':
            decode_srt(file_lines)
        elif self.file_info['type'] == 'sub':
            decode_sub(file_lines, self.input_frame_rate)
        elif self.file_info['type'] in ['ass', 'ssa']:
            decode_ass(file_lines)
    
    
    def remove_duplicate_lines(self):
        dupindex = []
        for index in range(len(self.time_begin[0:-1])):
            if self.time_begin[index] == self.time_begin[index + 1] and self.time_end[index] == self.time_end[index + 1] and self.subtitle_list[index] == self.subtitle_list[index + 1]:
                dupindex.append(index + 1)
        
        dupindex.reverse()
        
        for index in dupindex:
            del self.time_begin[index]
            del self.time_end[index]
            del self.subtitle_list[index]
    
    
    def filter_lines(self):
        removeindex = []
        for index in range(len(self.subtitle_list)):
            if subtitle_line_filter.is_bad_line(self.subtitle_list[index]):
                removeindex.append(index)
            else:
                self.subtitle_list[index] = subtitle_line_filter.clean(self.subtitle_list[index])
                if subtitle_empty_line_re.search(self.subtitle_list[index]) != None:
                    removeindex.append(index)
        
        removeindex.reverse()
        for index in removeindex:
            del self.time_begin[index]
            del self.time_end[index]
            del self.subtitle_list[index]
    
    
    def shift_times(self, offset):
        def move_times_on_list(times, start, stop, offset):
            index = start
            for time in times[start:stop]:
                time = int(time) + int(offset)
                del times[index]
                times.insert(index,time)
                index = index + 1
            return times
        
        begin, stop = parse_limits(offset, len(self.time_begin))
        offset = timecode_to_miliseconds(offset.split(',')[0])
        self.time_begin = move_times_on_list(self.time_begin, begin, stop, offset)
        self.time_end = move_times_on_list(self.time_end, begin, stop, offset)
    
    
    def modify_duration(self, add):
        time = timecode_to_miliseconds(add.split(',')[0])
        begin, end = parse_limits(add, len(self.time_end))
        for index in range(begin, end):
            endtime = self.time_end[index] + int(time) 
            if index + 1 != len(self.time_begin):
                if endtime + 50 > self.time_begin[index + 1]:
                    endtime = self.time_begin[index + 1] - 50
                    
            del self.time_end[index]
            self.time_end.insert(index, endtime)
    
    
    def scale_length(self, factor):
        if str(factor.split(',')[0]).isdigit():
            begin, end = parse_limits(factor, len(self.time_end))
            for index in range(begin, end):
                endtime = int(round(float(self.time_end[index] - self.time_begin[index]) * float(factor.split(',')[0]))) + self.time_begin[index]
                if index + 1 != len(self.time_begin):
                    if endtime + 50 > self.time_begin[index + 1]:
                        endtime = self.time_begin[index + 1] - 50
                del self.time_end[index]
                self.time_end.insert(index, endtime)
        else:
            sys.stderr.write("Scale factor is not a digit! No alternation done.\n")
    
    
    def change_framerate(self):
        def scale(times, scale_frame_rate):
            index = 0
            for time in times:
                time = int(round(float(time) * float(scale_frame_rate)))
                del times[index]
                times.insert(index, time)
                index = index + 1
            return times
        
        
        input_frame_rate = frame_rate_to_float(self.input_frame_rate)
        output_frame_rate = frame_rate_to_float(self.output_frame_rate)
        scale_frame_rate = input_frame_rate/output_frame_rate
        self.time_begin = scale(self.time_begin, scale_frame_rate)
        self.time_end = scale(self.time_end, scale_frame_rate)
    
    


srt_time_line = re.compile("^([0-9]{2}:[0-9]{2}:[0-9]{2},[0-9]{3}) --> ([0-9]{2}:[0-9]{2}:[0-9]{2},[0-9]{3})$")
subtitle_noneline = re.compile("\n$")
subtitle_empty_line_re = re.compile("^\s*$")
ass_subline = re.compile('^Dialog.*')
ass_event_command_re = re.compile(r'\{\\[^\}]+\}')
sub_line_begin = re.compile('^{(\d+)}{(\d+)}')
rmdos = re.compile('\r\n$')




class TagNameResolver(object):
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
    

tag_name_resolver = TagNameResolver()

class SubtitleLineFilter(object):
    def __init__(self):
        self.remove_pattern_list = []
        self.replace_pattern_list = []
        self.replacement_list = []
        
        from config.subfilter import line_remove
        for remove_filter in line_remove:
            self.remove_pattern_list.append(re.compile(remove_filter,re.UNICODE))
            
        from config.subfilter import line_replace
        for replace_filter in line_replace:
            self.replace_pattern_list.append(re.compile(replace_filter[0], re.MULTILINE|re.UNICODE)) 
            self.replacement_list.append(replace_filter[1])
    
    
    def is_bad_line(self, line):
        for index in range(len(self.remove_pattern_list)):
            if self.remove_pattern_list[index].search(line) != None:
                return True
        return False
    
    
    def clean(self, line):
        line = line.replace('\N', '\n')
        for index in range(len(self.replace_pattern_list)):            
            line = self.replace_pattern_list[index].sub(self.replacement_list[index], line)
        line = line.replace('\n', '\N')
        return line
    
    

subtitle_line_filter = SubtitleLineFilter()

class FileDetailDetector(object):
    def __init__(self):
        self.file_name_schema_re = {}
        for media_kind in repository_config['Media Kind'].keys():
            self.file_name_schema_re[media_kind] = re.compile(repository_config['Media Kind'][media_kind]['schema'])
    
    
    def detect(self, file_path):
        media_kind = None
        info = None
        if file_path != None:
            match = None
            for mk, mk_re in self.file_name_schema_re.iteritems():
                match = mk_re.search(os.path.basename(file_path))
                if match != None:
                    media_kind = mk
                    break
            
            if media_kind != None:
                info = {'media_kind':media_kind}
                
                if media_kind == 'movie':
                    info['imdb_id'] = match.group(1)
                    info['name'] = match.group(2)
                    info['type'] = match.group(3)
                    
                elif media_kind == 'tvshow':
                    info['show_small_name'] = match.group(1)
                    info['code'] = match.group(2)
                    info['season_number'] = int(match.group(3))
                    info['episode_number'] = int(match.group(4))
                    info['name'] = match.group(5)
                    info['type'] = match.group(6)
            
            dirname = os.path.dirname(file_path)
            if info['type'] in container_type['Subtitle']:
                lang = os.path.split(dirname)[1]
                if lang in repository_config['language']:
                    info['language'] = lang
                    
        return info
    

file_detail_detector = FileDetailDetector()

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


def frame_rate_to_float(frame_rate):
    frame_rate = str(frame_rate).split('/',1)
    if len(frame_rate) == 2 and str(frame_rate[0]).isdigit() and str(frame_rate[1]).isdigit():
        frame_rate = float(frame_rate[0])/float(frame_rate[1])
    elif str(frame_rate[0].replace('.', '',1)).isdigit():
        frame_rate = float(frame_rate[0])
    else:
        frame_rate = None
    return frame_rate


def parse_limits(limits, length):
    begin = 0
    stop = length
    limits = str(limits).split(',')
    if len(limits) >= 2:
        if str(limits[1]).isdigit():
            begin = int(limits[1]) - 1
            if len(limits) >= 3 and str(limits[2]).isdigit():
                stop = int(limits[2])
                
    if begin < 0:
        begin = 0
    elif begin > length:
        begin = length
        
    if stop > length:
        stop = length
        
    if stop < begin and begin < length:
        stop = begin
        
    return begin, stop


def frame_to_miliseconds(frame, frame_rate):
    return round(float(1000)/float(frame_rate) * float(frame))


tag_manager = TagManager()
container_type = { 'Subtitle':['srt', 'ass', 'sub', 'ssa'], 'Mpeg4':['mp4', 'm4v', 'm4a', 'm4b'], 'Matroska':['mkv'] }
full_numeric_time_format = re.compile('([0-9]{,2}):([0-9]{,2}):([0-9]{,2})(?:\.|,)([0-9]+)')
descriptive_time_format = re.compile('(?:([0-9]{,2})h)?(?:([0-9]{,2})m)?(?:([0-9]{,2})s)?(?:([0-9]+))?')
