# -*- coding: utf-8 -*-

import os
import re
import logging
import hashlib
import chardet
import copy
import textwrap

from config import repository_config
from config import db_config

from db import TagManager

# Container super Class

class Container(object):
    def __init__(self, file_path):
        self.logger = logging.getLogger('mp4pack.container')
        self.meta = None
        self.related = None
        self.file_path = file_path
        self.file_info = file_util.decode_path_info(self.file_path)
        if self.valid():
            self.related = file_util.related(self.file_path)
            self.load_meta()
        else:
            self.logger.warning(u'Unknown file name schema ' + self.file_path)
    
    
    def valid(self):
        return self.file_info != None
    
    
    def load(self):
        pass
    
    
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
                self.meta = {'Media Kind':repository_config['Media Kind'][self.file_info['Media Kind']]['name']}
                
                if 'name' in record:
                    self.meta['Name'] = record['name']
                if 'overview' in record:
                    self.meta['Long Description'] = record['overview']
                if 'content_rating' in record:
                    self.meta['Rating'] = record['content_rating']
                if 'released' in record:
                    self.meta['Release Date'] = record['released'].strftime('%Y-%m-%d')
                if 'tagline' in record:
                    self.meta['Description'] = record['tagline']
                elif 'overview' in record:
                    s = sentence_end.split(record['overview'])
                    if len(s) > 0: self.meta['Description'] = s[0].strip() + '.'
                    
                self._load_cast(record)
                self._load_genre(record)
                result = True
        return result
    
    
    def _load_tvshow_meta(self):
        result = False
        if self.is_tvshow():
            show, episode = tag_manager.find_episode(self.file_info['show_small_name'], self.file_info['TV Season'], self.file_info['TV Episode #'])
            if show != None and episode != None:
                self.meta = {'Media Kind':repository_config['Media Kind'][self.file_info['Media Kind']]['name']}
                
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
                    s = sentence_end.split(episode['overview'])
                    if len(s) > 0: self.meta['Description'] = s[0].strip() + '.'
                if 'released' in episode:
                    self.meta['Release Date'] = episode['released'].strftime('%Y-%m-%d')
                    
                self._load_cast(episode)
                result = True
        return result
    
    
    
    
    def info(self, options):
        return self.__str__()
    
    
    def copy(self, options):
        info = file_util.copy_file_info(self.file_info, options)
        dest_path = file_util.canonic_path(info, self.meta)
        if file_util.check_and_varify(dest_path, options.overwrite):
            command = ['rsync', self.file_path, dest_path]
            message = u'Copy ' + self.file_path + u' --> ' + dest_path
            file_util.execute_command(command, message, options.debug)
            file_util.clean_if_not_exist(dest_path)
            if options.md5:
                self.compare_checksum(dest_path)
        
    
    
    def rename(self, options):
        dest_path = os.path.join(os.path.dirname(self.file_path), self.canonic_name())
        if self.file_path == dest_path:
            self.logger.debug('No renaming needed for ' + dest_path)
        else:
            if file_util.check_path(dest_path, False):
                file_util.varify_directory(dest_path)
                command = ['mv', self.file_path, dest_path]
                message = 'Rename ' + self.file_path + ' --> ' + dest_path
                file_util.execute_command(command, message, options.debug)
                file_util.clean_if_not_exist(dest_path)
            else:
                self.logger.warning('Not renaming, destination exists ' + dest_path)
    
    
    def tag(self, options):
        return
    
    
    def art(self, options):
        return
    
    
    def optimize(self, options):
        return
    
    
    
    
    def extract(self, options):
        return
    
    
    def transcode(self, options):
        return
    
    
    def pack(self, options):
        return
    
    
    def update(self, options):
        return
    
    
    
    def compare_checksum(self, path):
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
        return self.file_info != None and set(('Media Kind', 'imdb_id')).issubset(set(self.file_info.keys())) and self.file_info['Media Kind'] == 'movie'
    
    
    def is_tvshow(self):
        return self.file_info != None and set(('Media Kind', 'show_small_name', 'TV Season', 'TV Episode #')).issubset(set(self.file_info.keys())) and self.file_info['Media Kind'] == 'tvshow'
    
    
    def easy_name(self):
        return file_util.easy_name(self.file_info, self.meta)
    
    
    def canonic_name(self):
        return file_util.canonic_name(self.file_info, self.meta)
    
    
    def canonic_path(self):
        return file_util.canonic_path(self.file_info, self.meta)
    
    
    def print_meta(self):
        result = None
        if self.meta != None:
            result = (u'\n'.join([format_key_value(key, self.meta[key]) for key in sorted(set(self.meta))]))
        return result
    
    
    def print_related(self):
        result = None
        if self.related != None:
            result = (u'\n'.join([format_value(key) for key in sorted(set(self.related))]))
        return result
    
    
    def print_file_info(self):
        result = None
        if self.file_info != None:
            result = (u'\n'.join([format_key_value(key, self.file_info[key]) for key in sorted(set(self.file_info))]))
        return result
    
    
    def __str__(self):
        result = None
        result = format_info_title(self.file_path)
        if self.related != None and len(self.related) > 0:
            result = u'\n'.join((result, format_info_subtitle(u'related'), self.print_related()))
        if self.file_info != None and len(self.file_info) > 0:
            result = u'\n'.join((result, format_info_subtitle(u'from path'), self.print_file_info()))
        if self.meta != None and len(self.meta) > 0:
            result = u'\n'.join((result, format_info_subtitle(u'metadata'), self.print_meta()))
        return result
    
    


class AVContainer(Container):
    def __init__(self, file_path):
        self.logger = logging.getLogger('mp4pack.av')
        Container.__init__(self, file_path)
        if self.valid():
            self.tracks = list()
            self.chapter_markers = list()
            self.tags = dict()
            self.load()
        
    
    
    def set_tag(self, name, value):
        self.tags[name] = value
    
    
    def add_track(self, track):
        if track != None:
            if 'type' in track and 'codec' in track:
                if track['type'] == 'video':
                    if 'pixel width' in track and 'pixel height' in track:
                        track['sar'] = float(track['pixel width']) / float(track['pixel height'])
                if track['type'] == 'audio':
                    track['kind'] = file_util.detect_audio_codec_kind(track['codec'])
                elif track['type'] == 'subtitles':
                    track['kind'] = file_util.detect_subtitle_codec_kind(track['codec'])
                
            self.tracks.append(track)
    
    
    def add_chapter_marker(self, chapter_marker):
        if chapter_marker != None:
            self.chapter_markers.append(chapter_marker)
    
    
    def playback_height(self):
        result = 0
        if len(self.tracks) > 0:
            for t in self.tracks:
                if t['type'] == 'video' and 'sar' in t:
                    if t['sar'] >= ar_16_9:
                        result = t['pixel width'] / t['sar']
                    else:
                        result = t['pixel height']
        return result
    
    
    
    def extract(self, options):
        Container.extract(self, options)
        if options.extract in ('all', 'txt'):
            if len(self.chapter_markers) > 0:
                info = file_util.copy_file_info(self.file_info, options)
                info['kind'] = 'txt'
                dest_path = file_util.canonic_path(info, self.meta)
                
                if file_util.check_and_varify(dest_path, options.overwrite):
                    c = Chapter(dest_path)
                    for cm in self.chapter_markers:
                        c.add_chapter_marker(cm)
                    
                    self.logger.debug('Extracting chapter markers from ' + self.file_path + ' into ' + dest_path)
                    c.write(dest_path)
                    file_util.clean_if_not_exist(dest_path)
        return
    
    
    def pack(self, options):
        Container.pack(self, options)
        info = file_util.copy_file_info(self.file_info, options)
        if options.pack in ('all', 'mkv'):
            info['kind'] = 'mkv'
            dest_path = file_util.canonic_path(info, self.meta)
            if dest_path != None:
                selected_related = file_util.related_by_profile(self.related, info['profile'], info['kind'])
                selected_tracks = file_util.tracks_by_profile(self.tracks, info['profile'], info['kind'])
                command = None
                if file_util.check_and_varify(dest_path, options.overwrite):
                    command = ['mkvmerge', '--output', dest_path, '--no-chapters', '--no-attachments', '--no-subtitles', self.file_path]
                    for t in selected_related:
                        t_info = self.related[t]
                        if t_info['kind'] == 'srt':
                            command.append('--sub-charset')
                            command.append('0:UTF-8')
                            command.append('--language')
                            command.append('0:' + t_info['language'])
                            command.append(t)
                        if t_info['kind'] == 'txt' and t_info['profile'] == 'chapter':
                            command.append('--chapter-language')
                            command.append('eng')
                            command.append('--chapter-charset')
                            command.append('UTF-8')
                            command.append('--chapters')
                            command.append(t)
                            
                    audio_tracks = list()
                    video_tracks = list()
                    for t in selected_tracks:
                        if 'name' in t:
                            command.append('--track-name')
                            command.append(t['number'] + ':' + t['name'])
                        if 'language' in t:
                            command.append('--language')
                            command.append(t['number'] + ':' + t['language'])
                        if t['type'] == 'audio':
                            audio_tracks.append(t['number'])
                        
                        elif t['type'] == 'video':
                            video_tracks.append(t['number'])
                    
                    command.append('--audio-tracks')
                    command.append(','.join(audio_tracks))
                    command.append('--video-tracks')
                    command.append(','.join(video_tracks))
                    
                    self.logger.debug('related files chosen: ' + selected_related.__str__())
                    self.logger.debug('tracks chosen: ' + selected_tracks.__str__())
                    
                    message = 'Pack ' +  self.file_path + ' --> ' + dest_path
                    file_util.execute_command(command, message, options.debug)
                    file_util.clean_if_not_exist(dest_path)
                    
        return
    
    
    def transcode(self, options):
        Container.transcode(self, options)
        info = file_util.copy_file_info(self.file_info, options)
        if options.transcode in ('mkv', 'm4v'):
            info['kind'] = options.transcode
            info = file_util.set_default_info(info)
            dest_path = file_util.canonic_path(info, self.meta)
            if dest_path != None:
                command = None
                if file_util.check_and_varify(dest_path, options.overwrite):
                    command = ['HandbrakeCLI']
                    transcode_config = repository_config['Kind'][info['kind']]['Profile'][info['profile']]['transcode']
                    if 'flags' in transcode_config:
                        for v in transcode_config['flags']:
                            command.append(v)
                            
                    if 'options' in transcode_config:
                        for (k,v) in transcode_config['options'].iteritems():
                            command.append(k)
                            command.append(str(v))
                            
                    found_audio = False
                    audio_options = {'--audio':[]}
                    for s in transcode_config['audio']:
                        for t in self.tracks:
                            for c in s:
                                if all((k in t and t[k] == v) for k,v in c['from'].iteritems()):
                                    found_audio = True
                                    audio_options['--audio'].append(t['number'])
                                    for (k,v) in c['to'].iteritems():
                                        if k not in audio_options: audio_options[k] = []
                                        audio_options[k].append(str(v))
                                        
                        if found_audio:
                            break
                            
                    if found_audio:
                        for (k,v) in audio_options.iteritems():
                            if len(v) > 0:
                                command.append(k)
                                command.append(','.join(v))
                                
                    command.append('--input')
                    command.append(self.file_path)
                    command.append('--output')
                    command.append(dest_path)
                    
                    message = 'Transcode ' +  self.file_path + ' --> ' + dest_path
                    file_util.execute_command(command, message, options.debug)
                    file_util.clean_if_not_exist(dest_path)
        return
    
    
    
    def print_chapter_markers(self):
        return (u'\n'.join([format_value(chapter_marker) for chapter_marker in self.chapter_markers]))
    
    
    def print_tags(self):
        return (u'\n'.join([format_key_value(key, self.tags[key]) for key in sorted(set(self.tags))]))
    
    
    def print_tracks(self):
        return (u'\n'.join([format_value(format_track(track)) for track in self.tracks]))
    
    
    def __str__(self):
        result = Container.__str__(self)
        if len(self.tracks) > 0:
            result = u'\n'.join((result, format_info_subtitle(u'tracks'), self.print_tracks()))
        if len(self.tags) > 0:
            result = u'\n'.join((result, format_info_subtitle(u'tags'), self.print_tags()))
        if len(self.chapter_markers) > 0:
            result = u'\n'.join((result, format_info_subtitle(u'chapter markers'), self.print_chapter_markers()))
        return result
    
    


class ChapterMarker(object):
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
            self.name = name.strip('"').strip("'").strip()
        else:
            self.name = None
    
    
    def set_language(self, language):
        if language != None:
            self.language = language
        else:
            self.language = None
    
    
    def encode(self, line_buffer, index):
        start_time_string = miliseconds_to_time(self.start_time, '.')
        cm = u'CHAPTER' + str(index).zfill(2)
        line_buffer.append(cm + u'=' + unicode(start_time_string, 'utf-8'))
        line_buffer.append(cm + u'NAME=' + self.name)
    
    
    def __str__(self):
        return '{0} : {1}'.format(miliseconds_to_time(self.start_time), self.name)
    



# Matroska Class
class Matroska(AVContainer):
    def __init__(self, file_path):
        self.logger = logging.getLogger('mp4pack.matroska')
        AVContainer.__init__(self, file_path)
    
    
    def _line_depth(self, mkvinfo_line):
        return mkvinfo_line_start_re.search(mkvinfo_line).start(0)
    
    
    def _parse_track(self, index, mkvinfo_report, track_nest_depth):
        track = dict()
        while (self._line_depth(mkvinfo_report[index]) > track_nest_depth):
            match = mkvinfo_track_number_re.search(mkvinfo_report[index])
            if match != None:
                track['number'] = int(match.group(1))
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
                track['frame rate'] = float(match.group(1))
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
                track['pixel width'] = int(match.group(1))
                index += 1
                continue
            match = mkvinfo_video_pixel_height_re.search(mkvinfo_report[index])
            if match != None:
                track['pixel height'] = int(match.group(1))
                index += 1
                continue
            match = mkvinfo_audio_sampling_frequency_re.search(mkvinfo_report[index])
            if match != None:
                track['sampling frequency'] = int(match.group(1))
                index += 1
                continue
                
            index += 1
        
        if 'type' in track and track['type'] == 'audio':
            if 'frame rate' in track: del track['frame rate']
        return index, track
    
    
    def _parse_chapter_marker(self, index, mkvinfo_report, track_nest_depth):
        chapter_marker = ChapterMarker()
        while (self._line_depth(mkvinfo_report[index]) > track_nest_depth):
            match = mkvinfo_chapter_start_re.search(mkvinfo_report[index])
            if match != None:
                chapter_marker.set_start_time(match.group(1))
                index += 1
                continue
            match = mkvinfo_chapter_string_re.search(mkvinfo_report[index])
            if match != None:
                chapter_marker.set_name(match.group(1))
                index += 1
                continue
            match = mkvinfo_chapter_language_re.search(mkvinfo_report[index])
            if match != None:
                chapter_marker.set_language(match.group(1))
                index += 1
                continue
                
            index += 1
            
        return index, chapter_marker
    
    
    def load(self):
        AVContainer.load(self)
        command = ['mkvinfo', self.file_path]
        output, error = file_util.execute_command(command, None)
        mkvinfo_report = unicode(output, 'utf-8').split('\n')
        length = len(mkvinfo_report)
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
                        index, chapter_marker = self._parse_chapter_marker(index + 1, mkvinfo_report, self._line_depth(mkvinfo_report[index]))
                        self.add_chapter_marker(chapter_marker)
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
    
    
    def extract(self, options):
        AVContainer.extract(self, options)
        new_media_files = []
        
        if options.extract in ('all', 'srt', 'ass'):
            command = ['mkvextract', 'tracks', self.file_path ]
            info = file_util.copy_file_info(self.file_info, options)
            selected = list()
            kinds = list()
            if options.extract == 'all':
                kinds.append('srt')
                kinds.append('ass')
            else:
                kinds.append(options.extract)
            
            for k in kinds:
                info['kind'] = k
                info = file_util.set_default_info(info)
                selected += file_util.tracks_by_profile(self.tracks, info['profile'], k)
                
            for t in selected:
                info['kind'] = t['kind']
                info['language'] = t['language']
                dest_path = file_util.canonic_path(info, self.meta)
                if file_util.check_and_varify(dest_path, options.overwrite):
                    new_media_files.append(dest_path)
                    command.append(str(t['number']) + ':' + dest_path)
            
            if len(new_media_files) > 0:
                message = 'Extract tracks from ' + self.file_path
                file_util.execute_command(command, message, options.debug)
                
            for f in new_media_files:
                file_util.clean_if_not_exist(f)
        
        return new_media_files
    
    
    def transcode(self, options):
        AVContainer.transcode(self, options)
        if options.transcode == 'srt':
            o = copy.deepcopy(options)
            o.transcode = None
            o.extract = 'all'
            new_media_files = self.extract(o)
            o.extract = None
            o.transcode = 'srt'
            o.profile = 'clean'
            for f in new_media_files:
                if os.path.exists(f):
                    s = Subtitle(f)
                    s.transcode(o)
    
    



# Mpeg4 Class
class Mpeg4(AVContainer):
    def __init__(self, file_path):
        self.logger = logging.getLogger('mp4pack.mp4')
        AVContainer.__init__(self, file_path)
    
    
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
            track['number'] = int(match.group(1))
            track['codec'] = match.group(2)
            track['duration'] = float(match.group(3))
            track['bit rate'] = int(match.group(4))
            track['pixel width'] = int(match.group(5))
            track['pixel height'] = int(match.group(6))
            track['frame rate'] = float(match.group(7))
        else:
            match = mp4info_audio_track_re.search(mp4info_report_line)
            if match != None:
                track = { 'type':'audio' }
                track['number'] = int(match.group(1))
                track['codec'] = match.group(2)
                track['duration'] = float(match.group(3))
                track['bit rate'] = int(match.group(4))
                track['sampling frequency'] = int(match.group(5))
                
        return track
    
    
    def _parse_chapter_marker(self, mp4chaps_report_line):
        chapter_marker = None
        match = mp4chaps_chapter_re.search(mp4chaps_report_line)
        if match != None:
            chapter_start_time = match.group(2)
            chapter_name = match.group(3)
            chapter_marker = ChapterMarker(chapter_start_time, chapter_name)
        return chapter_marker
    
    
    def load(self):
        AVContainer.load(self)
        command = ['mp4info', self.file_path]
        output, error = file_util.execute_command(command, None)
        mp4info_report = unicode(output, 'utf-8').split('\n')
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
            
        command = ['mp4chaps', '-l', self.file_path]
        output, error = file_util.execute_command(command, None)
        mp4chaps_report = unicode(output, 'utf-8').split('\n')
        length = int(len(mp4chaps_report))
        index = 0
        while index < length:
            chapter_marker = self._parse_chapter_marker(mp4chaps_report[index])
            if chapter_marker != None:
                self.add_chapter_marker(chapter_marker)
            index += 1
    
    
    def tag(self, options):
        AVContainer.tag(self, options)
        command = self.encode_subler_tag_command()
        if command != None:
            message = 'Tag ' + self.file_path
            file_util.execute_command(command, message, options.debug)
        else:
            self.logger.info('No tags need update on ' + self.file_path)
    
    
    def optimize(self, options):
        AVContainer.optimize(self, options)
        command = ['mp4file', '--optimize', self.file_path]
        message = 'Optimize ' + self.file_path
        file_util.execute_command(command, message, options.debug)
    
    
    def update(self, options):
        AVContainer.update(self, options)
        if options.update == 'srt':
            info = file_util.copy_file_info(self.file_info, options)
            info['kind'] = 'srt'
            info = file_util.set_default_info(info)
            if 'profile' in info and 'update' in repository_config['Kind']['srt']['Profile'][info['profile']]:
                update_section = repository_config['Kind']['srt']['Profile'][info['profile']]['update']
                
                message = 'Remove existing subtitle tracks in ' + self.file_path
                command = ['SublerCLI', '-r', self.file_path]
                file_util.execute_command(command, message, options.debug)
                
                selected = {}
                for (p,i) in self.related.iteritems():
                    for c in update_section['related']:
                        if all((k in i and i[k] == v) for k,v in c['from'].iteritems()):
                            selected[p] = i
                            break
                            
                for (p,i) in selected.iteritems():
                    for c in update_section['related']:
                        if all((k in i and i[k] == v) for k,v in c['from'].iteritems()):
                            message = 'Add subtitles ' + p + ' --> ' + self.file_path
                            command = [
                                'SublerCLI', '-i', self.file_path, 
                                '-s', p, 
                                '-l', repository_config['Language'][i['language']], 
                                '-n', c['to']['Name'], 
                                '-a', str(int(round(self.playback_height() * c['to']['height'])))
                            ]
                            file_util.execute_command(command, message, options.debug)
                
                if 'smart' in update_section:
                    smart_section = update_section['smart']
                    found = False
                    for code in smart_section['order']:
                        for (p,i) in selected.iteritems():
                            if i['language'] == code:
                                message = 'Add smart ' + repository_config['Language'][code] + ' subtitles ' + p + ' --> ' + self.file_path
                                command = [
                                    'SublerCLI', '-i', self.file_path, 
                                    '-s', p, 
                                    '-l', repository_config['Language'][smart_section['language']], 
                                    '-n', smart_section['Name'], 
                                    '-a', str(int(round(self.playback_height() * smart_section['height'])))
                                ]
                                file_util.execute_command(command, message, options.debug)
                                found = True
                                break
                        if found: break
    
    
    def encode_subler_tag_command(self):
        result = None
        update = dict()
        if self.meta != None:
            for t in self.meta:
                if not(t in self.tags and self.tags[t] == self.meta[t]):
                    update[t] = self.meta[t]
                    
        elif self.file_info != None:
            if self.is_movie():
                if 'Name' in self.file_info and self.file_info['Name'] != self.tags['Name']:
                    update['Name'] = self.file_info['Name']
                
            elif self.is_tvshow():
                if not('TV Season' in self.tags and self.file_info['TV Season'] == self.tags['TV Season']):
                    update['TV Season'] = self.file_info['TV Season']
                if not('TV Episode #' in self.tags and self.file_info['TV Episode #'] == self.tags['TV Episode #']):
                    update['TV Episode #'] = self.file_info['TV Episode #']
                if 'Name' in self.file_info and not('Name' in self.tags and self.file_info['Name'] == self.tags['Name']):
                    update['Name'] = self.file_info['Name']
        
        if len(update) > 0:
            result = (''.join(['{%s:%s}' % (t, format_for_subler_tag(update[t])) for t in sorted(set(update))]))
        return result
    
    



# Text File
class Text(Container):
    def __init__(self, file_path):
        self.logger = logging.getLogger('mp4pack.text')
        Container.__init__(self, file_path)
    
    
    def read(self):
        lines = None
        try:
            reader = open(self.file_path, 'r')
            lines = reader.readlines()
            reader.close()
            encoding = chardet.detect(''.join(lines))
            self.logger.debug(encoding['encoding'] + ' encoding detected for ' + self.file_path)
            for index in range(len(lines)):
                #lines[index] = unicode(lines[index].strip().decode(encoding['encoding']))
                lines[index] = unicode(lines[index].strip(), encoding['encoding'])
        except IOError as error:
            self.logger.error(error.__str__())
            lines = None
        return lines
    
    
    def decode(self):
        pass
    
    
    def write(self, path):
        lines = self.encode()
        if lines != None and len(lines) > 0:
            try:
                writer = open(path, 'w')
                for line in lines:
                    if line == u'\n':
                        writer.write(line)
                    else:
                        writer.write(line.encode('utf-8'))
                        writer.write(u'\n')
                writer.close()
            except IOError as error:
                self.logger.error(error.__str__())
    
    
    def encode(self):
        return None
    
    
    def transcode(self, options):
        Container.transcode(self, options)
        self.decode()
        info = file_util.copy_file_info(self.file_info, options)
        info['kind'] = options.transcode
        info = file_util.set_default_info(info)
        dest_path = file_util.canonic_path(info, self.meta)
        if file_util.check_and_varify(dest_path, options.overwrite):
            self.logger.info(u'Transcode ' + self.file_path + u' --> ' + dest_path)
            self.write(dest_path)
            file_util.clean_if_not_exist(dest_path)
    
    



# Subtitle Class
class SubtitleBlock(object):
    def __init__(self):
        self.begin = None
        self.end = None
        self.lines = list()
    
    
    def set_begin_miliseconds(self, value):
        self.begin = value
        
    
    
    def set_end_miliseconds(self, value):
        self.end = value
    
    
    def clear(self):
        self.lines = list()
    
    
    def add_line(self, value):
        if value != None:
            value = value.strip()
            if len(value) > 0:
                self.lines.append(value)
    
    
    def shift(self, offset):
        self.begin += offset
        self.end += offset
    
    
    def scale_rate(self, factor):
        self.begin = int(round(float(self.begin) * float(factor)))
        self.end = int(round(float(self.end) * float(factor)))
    
    
    def is_valid(self):
        return self.begin != None and self.end != None and self.begin < self.end and len(self.lines) > 0
    
    
    def encode(self, line_buffer, index):
        line_buffer.append(unicode(index))
        begin_time = miliseconds_to_time(self.begin, ',')
        end_time = miliseconds_to_time(self.end, ',')
        line_buffer.append(unicode(begin_time) + ' --> ' + unicode(end_time))
        for line in self.lines:
            line_buffer.append(line)
        line_buffer.append(u'\n')
    


class Subtitle(Text):
    def __init__(self, file_path):
        self.logger = logging.getLogger('mp4pack.subtitle')
        Text.__init__(self, file_path)
        if self.valid():
            self.subtitle_blocks = None
    
    
    def decode(self):
        def decode_srt(lines):
            current_block_start = None
            next_block_start = None
            current_block = None
            next_block = None
            last_line = len(lines) - 1
            for index in range(len(lines)):
                # last line
                if index == last_line and current_block_start != None:
                    next_block_start = index + 1
                    
                match = srt_time_line.search(lines[index])
                if match != None and lines[index - 1].strip().isdigit():
                    next_block = SubtitleBlock()
                    next_block.set_begin_miliseconds(timecode_to_miliseconds(match.group(1)))
                    next_block.set_end_miliseconds(timecode_to_miliseconds(match.group(2)))
                    if current_block_start != None:
                        next_block_start = index - 1
                    else:
                        # first block
                        current_block_start = index - 1
                        current_block = next_block
                        next_block = None
                        
                if next_block_start != None:
                    for line in lines[current_block_start + 2:next_block_start]:
                        current_block.add_line(line)
                        
                    if current_block.is_valid():
                        self.subtitle_blocks.append(current_block)
                        
                    current_block_start = next_block_start
                    next_block_start = None
                    
                    current_block = next_block
                    next_block = None
        
        
        def decode_ass(lines):
            index = 0
            formation = None
            for line in lines:
                if line == '[Events]':
                    match = ass_formation_line.search(lines[index + 1])
                    if match != None:
                        formation = match.group(1).strip().replace(' ','').split(',')
                    break
                index += 1
                
            if formation != None:
                start = formation.index('Start')
                stop = formation.index('End')
                text = formation.index('Text')
                for line in lines:
                    match = ass_subline.search(line)
                    if match != None:
                        line = match.group(1).strip().split(',')
                        block = SubtitleBlock()
                        block.set_begin_miliseconds(timecode_to_miliseconds(line[start]))
                        block.set_end_miliseconds(timecode_to_miliseconds(line[stop]))
                        
                        subtitle_text = ','.join(line[text:])
                        subtitle_text = ass_event_command_re.sub('', subtitle_text)
                        subtitle_text = subtitle_text.replace('\n', '\N')
                        subtitle_text = ass_condense_line_breaks.sub('\N', subtitle_text)
                        subtitle_text = subtitle_text.split('\N')
                        for line in subtitle_text:
                            block.add_line(line)
                            
                        if block.is_valid():
                            self.subtitle_blocks.append(block)
        
        
        def decode_sub(lines, frame_rate):
            frame_rate = frame_rate_to_float(frame_rate)
            for line in lines:
                if sub_line_begin.search(line):
                    line = line.split('}',2)
                    subtitle_text = line[2].strip().replace('|', '\N')
                    block = SubtitleBlock()
                    block.set_begin_miliseconds(frame_to_miliseconds(line[0].strip('{'), frame_rate))
                    block.set_end_miliseconds(frame_to_miliseconds(line[1].strip('{'), frame_rate))
                    for line in subtitle_text:
                        block.add_line(line)
                        
                    if block.is_valid():
                        self.subtitle_blocks.append(block)
        
        
        if self.subtitle_blocks == None:
            Text.decode(self)
            self.subtitle_blocks = list()
            lines = self.read()
            if self.file_info['kind'] == 'srt':
                decode_srt(lines)
            elif self.file_info['kind'] in ['ass', 'ssa']:
                decode_ass(lines)
            elif self.file_info['kind'] == 'sub':
                decode_sub(lines, 25)
    
    
    def encode(self):
        result = Text.encode(self)
        self.decode()
        if len(self.subtitle_blocks) > 0:
            result = ['\n']
            index = 0
            for block in self.subtitle_blocks:
                index += 1
                block.encode(result, index)
        return result
    
    
    def transcode(self, options):
        self.decode()
        info = file_util.copy_file_info(self.file_info, options)
        info['kind'] = options.transcode
        info = file_util.set_default_info(info)
        
        p = repository_config['Kind'][info['kind']]['Profile'][info['profile']]
        if 'transcode' in p and 'filter' in p['transcode']:
            self.filter(p['transcode']['filter'])
            self.logger.debug('Filtering ' + self.file_path + ' by ' + p['transcode']['filter'].__str__())
        
        if options.time_shift != None:
            self.shift_times(options.time_shift)
            
        if options.input_rate != None and options.output_rate != None:
            input_frame_rate = frame_rate_to_float(options.input_rate)
            output_frame_rate = frame_rate_to_float(options.output_rate)
            if input_frame_rate != None and output_frame_rate != None:
                factor = input_frame_rate / output_frame_rate
                self.change_framerate(factor)
        
        Text.transcode(self, options)
        
    
    
    def filter(self, sequence_list):
        if len(sequence_list) > 0:
            self.subtitle_blocks = subtitle_filter.filter(self.subtitle_blocks, sequence_list)
    
    
    def shift_times(self, offset):
        for block in self.subtitle_blocks:
            block.shift(offset)
    
    
    def change_framerate(self, factor):
        for block in self.subtitle_blocks:
            block.scale_rate(factor)
    
    



# Chapter Class
class Chapter(Text):
    def __init__(self, file_path):
        self.logger = logging.getLogger('mp4pack.chapter')
        Text.__init__(self, file_path)
        if self.valid():
            self.chapter_markers = None
    
    
    def decode(self):
        if self.chapter_markers == None:
            Text.decode(self)
            lines = self.read()
            if lines != None:
                for index in range(len(lines) - 1):
                    match_timecode = ogg_chapter_timestamp_re.search(lines[index])
                    if match_timecode != None:
                        match_name = ogg_chapter_name_re.search(lines[index + 1])
                        if match_name != None:
                            timecode = match_timecode.group(2)
                            name = match_name.group(2)
                            self.add_chapter_marker(ChapterMarker(timecode, name))
    
    
    def encode(self):
        result = Text.encode(self)
        self.decode()
        if self.chapter_markers != None and len(self.chapter_markers) > 0:
            result = list()
            index = 1
            for chapter_marker in self.chapter_markers:
                chapter_marker.encode(result, index)
                index += 1
        
        return result
    
    
    def add_chapter_marker(self, chapter_marker):
        if chapter_marker != None:
            if self.chapter_markers == None:
                self.chapter_markers = list()
            self.chapter_markers.append(chapter_marker)
    



# Image Class
class Image(Container):
    def __init__(self, file_path):
        self.logger = logging.getLogger('mp4pack.image')
        Container.__init__(self, file_path)
    
    





# Tag Name Resolver Class (Singletone)
class TagNameResolver(object):
    def __init__(self):
        self.canonic_map = dict()
        self.mp4info_map = dict()
        
        for tag in db_config['tag']:
            self.canonic_map[tag[0]] = tag
            if tag[2] != None:
                self.mp4info_map[tag[2]] = tag
    
    
    def canonic_name_from_mp4info(self, name):
        result = None
        if name in self.mp4info_map:
            result = self.mp4info_map[name][0]
        return result
    
    
    def subler_name_from_canonic(self, name):
        result = None
        if name in self.canonic_map:
            result = self.canonic_map[name][1]
        return result
    
    



# Subtitle Filter Class (Singleton)
class SubtitleFilter(object):
    def __init__(self):
        self.logger = logging.getLogger('mp4pack.subtitlefilter')
        self.sequence = {}
    
    
    def find_filter_sequence(self, name):
        result = None
        
        from config import subtitle_config
        if name in self.sequence:
            result = self.sequence[name]
        elif name in subtitle_config:
            config = subtitle_config[name]
            self.logger.debug('Loading ' + name + ' filter sequence')
            if config['action'] == 'drop':
                s = DropFilterSequence(config)
                s.load()
                self.sequence[name] = s
                result = s
                
            elif config['action'] == 'replace':
                s = ReplaceFilterSequence(config)
                s.load()
                self.sequence[name] = s
                result = s
        return result
    
    
    def filter(self, blocks, sequence_list):
        for fn in sequence_list:
            if len(blocks) > 0:
                fs = self.find_filter_sequence(fn)
                if fs != None:
                    next = list()
                    for block in blocks:
                        if block.is_valid() and self.filter_block(block, fs):
                            next.append(block)
                    blocks = next
        return blocks
    
    
    def filter_block(self, block, filter_sequence):
        result = block.is_valid()
        if result:
            result = filter_sequence.filter(block)
        return result
        
    


class FilterSequence(object):
    def __init__(self, config):
        self.logger = logging.getLogger('mp4pack.filtersequence')
        self.config = config
    
    
    def filter(self, block):
        result = False
        if block != None:
            result = block.is_valid()
        return result
    


class DropFilterSequence(FilterSequence):
    def __init__(self, config):
        self.logger = logging.getLogger('mp4pack.dropfiltersequence')
        FilterSequence.__init__(self, config)
        self.expression = list()
    
    
    def load(self):
        o = re.UNICODE
        if 'case' in self.config and self.config['case'] == 'insensitive':
            o = o|re.IGNORECASE
        for e in self.config['expression']:
            self.expression.append(re.compile(e,o))
    
    
    def filter(self, block):
        result = FilterSequence.filter(self, block)
        if result:
            if self.config['scope'] == 'line':
                original = block.lines
                block.clear()
                for line in original:
                    keep = True
                    for e in self.expression:
                        if e.search(line) != None:
                            self.logger.debug('Found match in ' + line)
                            keep = False
                            break
                    if keep:
                        block.add_line(line)
                        
            elif self.config['scope'] == 'block':
                for line in block.lines:
                    for e in self.expression:
                        if e.search(line) != None:
                            block.clear()
                            break
                    if not block.is_valid():
                        break
                        
            result = block.is_valid()
        return result
    


class ReplaceFilterSequence(FilterSequence):
    def __init__(self, config):
        self.logger = logging.getLogger('mp4pack.replacefiltersequence')
        FilterSequence.__init__(self, config)
        self.expression = list()
    
    
    def load(self):
        o = re.UNICODE
        if 'case' in self.config and self.config['case'] == 'insensitive':
            o = o|re.IGNORECASE
            
        if self.config['scope'] == 'block':
            o = o|re.MULTILINE
            
        for e in self.config['expression']:
            self.expression.append([re.compile(e[0], o), e[1]])
    
    
    def filter(self, block):
        result = FilterSequence.filter(self, block)
        if result:
            if self.config['scope'] == 'line':
                for e in self.expression:
                    original = block.lines
                    block.clear()
                    for line in original:
                        block.add_line(e[0].sub(e[1], line))
                    if not block.is_valid():
                        break
                        
            elif self.config['scope'] == 'block':
                all_lines = u'\n'.join(block.lines)
                block.clear()
                for e in self.expression:
                    all_lines = e[0].sub(e[1], all_lines).strip()
                    if not len(all_lines) > 0:
                        break
                for line in all_lines.split(u'\n'):
                    block.add_line(line)
                    
            result = block.is_valid()
        return result
    



# File Utility Class (Singletone)
class FileUtil(object):
    def __init__(self):
        self.logger = logging.getLogger('mp4pack.util')
        kc = repository_config['Kind']
        self.matroska_kinds = [ k for (k,v) in kc.iteritems() if v['container'] == 'matroska' ]
        self.mp4_kinds = [ k for (k,v) in kc.iteritems() if v['container'] == 'mp4' ]
        self.subtitles_kinds = [ k for (k,v) in kc.iteritems() if v['container'] == 'subtitles' ]
        self.chapter_kinds = [ k for (k,v) in kc.iteritems() if v['container'] == 'chapters' ]
        self.image_kinds = [ k for (k,v) in kc.iteritems() if v['container'] == 'image' ]
        
        self.audio_codec_kind = {}
        for k,v in repository_config['Codec']['Audio'].iteritems():
            self.audio_codec_kind[k] = re.compile(v)
        
        self.subtitle_codec_kind = {}
        for k,v in repository_config['Codec']['Subtitle'].iteritems():
            self.subtitle_codec_kind[k] = re.compile(v)
            
        self.file_name_schema_re = {}
        for media_kind in repository_config['Media Kind'].keys():
            self.file_name_schema_re[media_kind] = re.compile(repository_config['Media Kind'][media_kind]['schema'])
    
    
    def decode_path_info(self, file_path):
        # <Volume>/<Media Kind>/<Kind>/<Profile>(/<Show>/<Season>)?(/<Language>)?/(IMDb<IMDB ID> <Name>|<Show> <Code> <Name>).<Extension>
        media_kind = None
        info = None
        if file_path != None:
            for mk, mk_re in self.file_name_schema_re.iteritems():
                match = mk_re.search(os.path.basename(file_path))
                if match != None:
                    media_kind = mk
                    break
            
            if media_kind != None:
                info = {'Media Kind':media_kind}
                
                if media_kind == 'movie':
                    info['imdb_id'] = match.group(1)
                    info['Name'] = match.group(2)
                    info['kind'] = match.group(3)
                    
                elif media_kind == 'tvshow':
                    info['show_small_name'] = match.group(1)
                    info['Code'] = match.group(2)
                    info['TV Season'] = int(match.group(3))
                    info['TV Episode #'] = int(match.group(4))
                    info['Name'] = match.group(5)
                    info['kind'] = match.group(6)
                
                if info['Name'] == None or info['Name'] == '':
                    del info['Name']
                
                prefix = os.path.dirname(file_path)
                if info['kind'] in self.subtitles_kinds:
                    prefix, lang = os.path.split(prefix)
                    if lang in repository_config['Language']:
                        info['language'] = lang
                    
        return info
    
    
    def easy_name(self, info, meta):
        result = None
        if 'Name' in meta:
            result = meta['Name']
        elif 'Name' in info:
            result = info['Name']
        return result
    
    
    def canonic_name(self, info, meta):
        result = None
        valid = False
        
        if 'Media Kind' in info and info['Media Kind'] in repository_config['Media Kind'] and 'kind' in info and info['kind'] in repository_config['Kind']:
            if info['Media Kind'] == 'tvshow':
                if 'show_small_name' in info and 'Code' in info:
                    result = ''.join([info['show_small_name'], ' ', info['Code']])
                    valid = True
            elif info['Media Kind'] == 'movie':
                if 'imdb_id' in info:
                    result = ''.join(['IMDb', info['imdb_id']])
                    valid = True
        if valid:
            easy_name = self.easy_name(info, meta)
            if easy_name != None:
                result = ''.join([result, ' ', easy_name])
            
            result = ''.join([result, '.', info['kind']])
        
        if not valid:
            result = None
        
        return result
    
    
    def canonic_path(self, info, meta):
        result = None
        valid = True
        if ('Media Kind' in info and info['Media Kind'] in repository_config['Media Kind']) and ('kind' in info and info['kind'] in repository_config['Kind']):
            if not 'volume' in info and 'volume' in repository_config['Kind'][info['kind']]['default']:
                info['volume'] = repository_config['Kind'][info['kind']]['default']['volume']
                
            if not 'profile' in info and 'profile' in repository_config['Kind'][info['kind']]['default']:
                info['profile'] = repository_config['Kind'][info['kind']]['default']['profile']
                
            if 'volume' in info and info['volume'] in repository_config['Volume']:
                if 'profile' in info and info['profile'] in repository_config['Kind'][info['kind']]['Profile']:
                    result = os.path.join(repository_config['Volume'][info['volume']], info['Media Kind'], info['kind'], info['profile'])
                
                    if info['Media Kind'] == 'tvshow' and 'show_small_name' in info and 'TV Season' in info:
                        result = os.path.join(result, info['show_small_name'], str(info['TV Season']))
                
                    if info['kind'] in self.subtitles_kinds and 'language' in info and info['language'] in repository_config['Language']:
                            result = os.path.join(result, info['language'])
                else:
                    valid = False
                    if 'profile' in info:
                        self.logger.warning('Invalid profile: ' + info['profile']  + ' for ' + info.__str__())
                    else:
                        self.logger.warning('Unknow profile for ' + info.__str__())
            else:
                valid = False
                if 'volume' in info:
                    self.logger.warning('Invalid volume: ' + info['volume']  + ' for ' + info.__str__())
                else:
                    self.logger.warning('Unknow volume for ' + info.__str__())
        else:
            valid = False
        
        if valid:
            result = os.path.join(result, self.canonic_name(info, meta))
            result = os.path.abspath(result)
        else:
            result = None
        return result
    
    
    def clean_if_not_exist(self, path):
        if not os.path.exists(path):
            try:
                os.removedirs(os.path.dirname(path))
            except OSError:
                pass
    
    
    def clean(self, path):
        try:
            os.remove(path)
            os.removedirs(os.path.dirname(path))
        except OSError:
            pass
    
    
    def related(self, path):
        # <Volume>/<Media Kind>/<Kind>/<Profile>(/<Show>/<Season>)?/(IMDb<IMDB ID> <Name>|<Show> <Code> <Name>).<Extension>
        related = dict()
        info = self.decode_path_info(path)
        meta = {}
        kc = repository_config['Kind']
        vc = repository_config['Volume']
        lc = repository_config['Language']
        
        for v in repository_config['Volume'].keys():
            for k in kc.keys():
                for p in kc[k]['Profile'].keys():
                    if kc[k]['container'] == 'subtitles':
                        for l in lc.keys():
                            i = copy.deepcopy(info)
                            i['volume'] = v
                            i['kind'] = k
                            i['profile'] = p
                            i['language'] = l
                            rp = self.canonic_path(i, meta)
                            if os.path.exists(rp):
                                related[rp] = i
                    else:
                        i = copy.deepcopy(info)
                        i['volume'] = v
                        i['kind'] = k
                        i['profile'] = p
                        rp = self.canonic_path(i, meta)
                        if os.path.exists(rp):
                            related[rp] = i

        return related
    
    
    def related_by_profile(self, related, profile, kind):
        selected = list()
        if profile != None and kind != None and kind in repository_config['Kind'] and profile in repository_config['Kind'][kind]['Profile'] and 'pack' in repository_config['Kind'][kind]['Profile'][profile]:
            for (path,info) in related.iteritems():
                for c in repository_config['Kind'][kind]['Profile'][profile]['pack']['related']:
                    if all((k in info and info[k] == v) for k,v in c.iteritems()):
                        selected.append(path)
                        break
        return selected
    
    
    def tracks_by_profile(self, tracks, profile, kind):
        selected = list()
        if profile != None and kind != None and kind in repository_config['Kind'] and profile in repository_config['Kind'][kind]['Profile'] and 'pack' in repository_config['Kind'][kind]['Profile'][profile]:
            for t in tracks:
                for c in repository_config['Kind'][kind]['Profile'][profile]['pack']['tracks']:
                    if all((k in t and t[k] == v) for k,v in c.iteritems()):
                        selected.append(t)
                        break
        return selected
    
    
    def detect_audio_codec_kind(self, codec):
        result = None
        for k,v in self.audio_codec_kind.iteritems():
            if v.search(codec) != None:
                result = k
                break
        return result
    
    
    def detect_subtitle_codec_kind(self, codec):
        result = None
        for k,v in self.subtitle_codec_kind.iteritems():
            if v.search(codec) != None:
                result = k
                break
        return result
    
    
    def varify_directory(self, path):
        result = False
        try:
            dirname = os.path.dirname(path)
            if not os.path.exists(dirname):
                self.logger.debug('Creating directory ' + dirname)
                os.makedirs(dirname)
                result = True
        except OSError as error:
            self.logger.error(error.__str__())
            result = False
        return result
    
    
    def check_path(self, path, overwrite=False):
        result = True
        if path != None:
            if os.path.exists(path) and not overwrite:
                self.logger.warning('Refusing to overwrite ' + path)
                result = False
        else:
            result = False
        
        return result
    
    
    def check_and_varify(self, path, overwrite=False):
        result = self.check_path(path, overwrite)
        if result:
            self.varify_directory(path)
        return result
    
    
    def execute_command(self, command, message= None, debug=False):
        def encode_command(command):
            cmd = copy.deepcopy(command)
            for index in range(len(cmd)):
                if ' ' in cmd[index]: cmd[index] = "'{0}'".format(cmd[index])
            return ' '.join(cmd)
        
        
        output = None
        error = None
        
        if not debug:
            if command != None:
                self.logger.debug('Execute: ' + encode_command(command))
                if message != None:
                    self.logger.info(message)
                from subprocess import Popen, PIPE
                proc = Popen(command, stdout=PIPE)
                report = proc.communicate()
                
                output = report[0]
                error = report[1]
                
                if error != None and len(error) > 0:
                    self.logger.error(error)
                if output != None and len(output) > 0:
                    #self.logger.debug(output)
                    result = True
        else:
            self.logger.info(message)
            print encode_command(command)
        return output, error
    
    
    def set_default_info(self, info):
        if 'kind' in info:
            if not 'volume' in info and 'volume' in repository_config['Kind'][info['kind']]['default']:
                info['volume'] = repository_config['Kind'][info['kind']]['default']['volume']
                
            if not 'profile' in info and 'profile' in repository_config['Kind'][info['kind']]['default']:
                info['profile'] = repository_config['Kind'][info['kind']]['default']['profile']
        return info
    
    
    def copy_file_info(self, info, options):
        result = None
        if info != None:
            i = copy.deepcopy(info)
            i['volume'] = options.volume
            if i['volume'] == None:
                del i['volume']
        
            i['profile'] = options.profile
            if i['profile'] == None:
                del i['profile']
        return i
    
    



# Service functions
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


def format_for_subler_tag(value):
    if value != None:
        value = value.replace('{','&#123;').replace('}','&#125;').replace(':','&#58;')
    return value



# Generic file loading function
def load_media_file(file_path):
    f = None
    file_type = os.path.splitext(file_path)[1].strip('.')
    if file_type in file_util.mp4_kinds:
        f = Mpeg4(file_path)
    elif file_type in file_util.matroska_kinds:
        f = Matroska(file_path)
    elif file_type in file_util.subtitles_kinds:
        f = Subtitle(file_path)
    elif file_type in file_util.chapter_kinds:
        f = Chapter(file_path)
    elif file_type in file_util.image_kinds:
        f = Image(file_path)
    if f.file_info == None:
        f = None
    return f



# Info format helper functions
def format_info_title(text):
    margin = repository_config['Display']['margin']
    width = repository_config['Display']['wrap']
    indent = repository_config['Display']['indent']
    return u'\n\n\n' + u' '*margin + '[{0:-^{1}}]'.format(text, width + indent)


def format_info_subtitle(text):
    margin = repository_config['Display']['margin']
    indent = repository_config['Display']['indent']
    return u'\n' + u' '*margin + u'[{0:^{1}}]\n'.format(text, indent - 3 - margin)


def format_key_value(key, value):
    margin = repository_config['Display']['margin']
    width = repository_config['Display']['wrap']
    indent = repository_config['Display']['indent']
    
    format_line = u' '*margin + u'{0:-<{1}}: {2}'
    v = unicode(value)
    if len(v) > width:
        lines = textwrap.wrap(value, width)
        space = u'\n' + u' '*indent
        v = space.join(lines)
    return format_line.format(key, indent - 2 - margin,v)


def format_value(value):
    margin = repository_config['Display']['margin']
    return u' '*margin + u'{0}'.format(value)


def format_track(track):
    return u' | '.join([u'{0}: {1}'.format(key, track[key]) for key in sorted(set(track))])



file_util = FileUtil()
tag_manager = TagManager()
tag_name_resolver = TagNameResolver()
subtitle_filter = SubtitleFilter()

ar_16_9 = float(16) / float(9)

full_numeric_time_format = re.compile('([0-9]{,2}):([0-9]{,2}):([0-9]{,2})(?:\.|,)([0-9]+)')
descriptive_time_format = re.compile('(?:([0-9]{,2})h)?(?:([0-9]{,2})m)?(?:([0-9]{,2})s)?(?:([0-9]+))?')
sentence_end = re.compile('[.!?]')

ogg_chapter_timestamp_re = re.compile('CHAPTER([0-9]{,2})=([0-9]{,2}:[0-9]{,2}:[0-9]{,2}\.[0-9]+)')
ogg_chapter_name_re = re.compile('CHAPTER([0-9]{,2})NAME=(.*)', re.UNICODE)

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

mp4info_video_track_re = re.compile('([0-9]+)	video	([^,]+), ([0-9\.]+) secs, ([0-9\.]+) kbps, ([0-9]+)x([0-9]+) @ ([0-9\.]+) fps')
mp4info_h264_video_codec_re = re.compile('H264 ([^@]+)@([0-9\.]+)')
mp4info_audio_track_re = re.compile('([0-9]+)	audio	([^,]+), ([0-9\.]+) secs, ([0-9\.]+) kbps, ([0-9]+) Hz')
mp4info_tag_re = re.compile(' ([^:]+): (.*)$')
mp4chaps_chapter_re  = re.compile('Chapter #([0-9]+) - ([0-9:\.]+) - (.*)$')

srt_time_line = re.compile('^([0-9]{2}:[0-9]{2}:[0-9]{2},[0-9]{3}) --> ([0-9]{2}:[0-9]{2}:[0-9]{2},[0-9]{3})$')
ass_subline = re.compile('^Dialogue\s*:\s*(.*)$')
ass_formation_line = re.compile('^Format\s*:\s*(.*)$')
ass_condense_line_breaks = re.compile(r'(\\N)+')
ass_event_command_re = re.compile(r'\{\\[^\}]+\}')
sub_line_begin = re.compile('^{(\d+)}{(\d+)}')
