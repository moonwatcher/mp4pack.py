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
            self.logger.warning(u'Unknown file name schema %s',self.file_path)
    
    
    def valid(self):
        return self.file_info is not None
    
    
    def load(self):
        pass
    
    
    def load_meta(self):
        result = False
        self.meta = []
        if self.is_movie():
            result = self._load_movie_meta()
        elif self.is_tvshow():
            result = self._load_tvshow_meta()
            
        if not result:
            self.meta = None
            
        return result
    
    
    def _load_genre(self, record):
        if 'genre' in record.keys() and record['genre']:
            g = record['genre'][0]
            self.meta['Genre'] = g['name']
            if 'itmf_code' in g.keys():
                self.meta['GenreID'] = g['itmf_code']
    
    
    def _load_cast(self, record):
        if 'cast' in record.keys():
            directors = [ r for r in record['cast'] if r['job'] == 'director' ]
            codirectors = [ r for r in record['cast'] if r['job'] == 'director of photography' ]
            producers = [ r for r in record['cast'] if r['job'].count('producer') > 0 ]
            screenwriters = [ r for r in record['cast'] if r['job'] == 'screenplay' or r['job'] == 'author' ]
            actors = [ r for r in record['cast'] if r['job'] == 'actor' ]
            
            artist = None
            if directors:
                if not artist: artist = directors[0]
                self.meta['Director'] = ', '.join([ d['name'] for d in directors ])
                
            if codirectors:
                if not artist: artist = codirectors[0]
                self.meta['Codirector'] = ', '.join([ d['name'] for d in codirectors ])
                
            if producers:
                if not artist: artist = producers[0]
                self.meta['Producers'] = ', '.join([ d['name'] for d in producers ])
                
            if screenwriters:
                if not artist: artist = screenwriters[0]
                self.meta['Screenwriters'] = ', '.join([ d['name'] for d in screenwriters ])
                
            if actors:
                if 'Cast' in self.meta and self.meta['Cast']:
                    self.meta['Cast'] = ', '.join([self.meta['Cast'], ', '.join([ d['name'] for d in actors ])])
                else:
                    self.meta['Cast'] = ', '.join([ d['name'] for d in actors ])
                    
                if not artist: artist = actors[0]
                    
            if artist:
                self.meta['Artist'] = artist['name']
        return
    
    
    def _load_movie_meta(self):
        result = False
        if self.is_movie():
            record = tag_manager.find_movie_by_imdb_id(self.file_info['imdb_id'])
            if record:
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
                    if s: self.meta['Description'] = s[0].strip() + '.'
                    
                self._load_cast(record)
                self._load_genre(record)
                result = True
        return result
    
    
    def _load_tvshow_meta(self):
        result = False
        if self.is_tvshow():
            show, episode = tag_manager.find_episode(self.file_info['show_small_name'], self.file_info['TV Season'], self.file_info['TV Episode #'])
            if show and episode:
                self.meta = {'Media Kind':repository_config['Media Kind'][self.file_info['Media Kind']]['name']}
                
                if 'content_rating' in show:
                    self.meta['Rating'] = show['content_rating']
                if 'network' in show:
                    self.meta['TV Network'] = show['network']
                    
                self._load_genre(show)
                
                if 'cast' in show.keys():
                    actors = [ r for r in show['cast'] if r['job'] == 'actor' ]
                    if actors:
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
                    if s: self.meta['Description'] = s[0].strip() + '.'
                if 'released' in episode:
                    self.meta['Release Date'] = episode['released'].strftime('%Y-%m-%d')
                    
                self._load_cast(episode)
                result = True
        return result
    
    
    
    def info(self, options):
        return self.__unicode__()
    
    
    def copy(self, options):
        info = file_util.copy_file_info(self.file_info, options)
        if file_util.complete_info_default_values(info):
            dest_path = file_util.canonic_path(info, self.meta)
            if file_util.check_and_varify(dest_path, options.overwrite):
                command = [u'rsync', self.file_path, dest_path]
                message = u'Copy ' + self.file_path + u' --> ' + dest_path
                file_util.execute_command(command, message, options.debug)
                file_util.clean_if_not_exist(dest_path)
                if options.md5:
                    self.compare_checksum(dest_path)
        
    
    
    def rename(self, options):
        dest_path = os.path.join(os.path.dirname(self.file_path), self.canonic_name())
        if os.path.exists(dest_path) and os.path.samefile(self.file_path, dest_path):
            self.logger.debug(u'No renaming needed for %s',dest_path)
        else:
            if file_util.check_path(dest_path, False):
                file_util.varify_directory(dest_path)
                command = [u'mv', self.file_path, dest_path]
                message = u'Rename {0} --> {1}'.format(self.file_path, dest_path)
                file_util.execute_command(command, message, options.debug)
                file_util.clean_if_not_exist(dest_path)
            else:
                self.logger.warning(u'Not renaming, destination exists %s | %s', self.file_path, dest_path)
    
    
    def tag(self, options):
        pass
    
    
    def art(self, options):
        pass
    
    
    def optimize(self, options):
        pass
    
    
    
    def extract(self, options):
        return []
    
    
    def transcode(self, options):
        pass
    
    
    def pack(self, options):
        pass
    
    
    def update(self, options):
        pass
    
    
    
    def compare_checksum(self, path):
        result = False
        if os.path.exists(self.file_path) and os.path.exists(path):
            source_md5 = hashlib.md5(file(self.file_path).read()).hexdigest()
            dest_md5 = hashlib.md5(file(path).read()).hexdigest()
            if source_md5 == dest_md5:
                self.logger.info(u'md5 match: %s %s',source_md5, self.canonic_name())
                result = True
            else:
                self.logger.error(u'md5 mismatch: %s is not %s for %s', source_md5, dest_md5, self.canonic_name())
        return result
    
    
    def is_movie(self):
        return self.file_info is not None and set(('Media Kind', 'imdb_id')).issubset(set(self.file_info.keys())) and self.file_info['Media Kind'] == 'movie'
    
    
    def is_tvshow(self):
        return self.file_info is not None and set(('Media Kind', 'show_small_name', 'TV Season', 'TV Episode #')).issubset(set(self.file_info.keys())) and self.file_info['Media Kind'] == 'tvshow'
    
    
    def easy_name(self):
        return file_util.easy_name(self.file_info, self.meta)
    
    
    def canonic_name(self):
        return file_util.canonic_name(self.file_info, self.meta)
    
    
    def canonic_path(self):
        return file_util.canonic_path(self.file_info, self.meta)
    
    
    def print_meta(self):
        result = None
        if self.meta:
            result = (u'\n'.join([format_key_value(key, self.meta[key]) for key in sorted(set(self.meta))]))
        return result
    
    
    def print_related(self):
        result = None
        if self.related:
            result = (u'\n'.join([format_value(key) for key in sorted(set(self.related))]))
        return result
    
    
    def print_file_info(self):
        result = None
        if self.file_info:
            result = (u'\n'.join([format_key_value(key, self.file_info[key]) for key in sorted(set(self.file_info))]))
        return result
    
    
    def __unicode__(self):
        result = None
        result = format_info_title(self.file_path)
        if self.related:
            result = u'\n'.join((result, format_info_subtitle(u'related'), self.print_related()))
        if self.file_info:
            result = u'\n'.join((result, format_info_subtitle(u'from path'), self.print_file_info()))
        if self.meta:
            result = u'\n'.join((result, format_info_subtitle(u'metadata'), self.print_meta()))
        return result
    
    


class AVContainer(Container):
    def __init__(self, file_path):
        self.logger = logging.getLogger('mp4pack.av')
        Container.__init__(self, file_path)
        if self.valid():
            self.tracks = []
            self.chapter_markers = []
            self.tags = {}
            self.load()
        
    
    
    def set_tag(self, name, value):
        self.tags[name] = value
    
    
    def add_track(self, track):
        if track:
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
        if chapter_marker:
            self.chapter_markers.append(chapter_marker)
    
    
    def playback_height(self):
        result = 0
        if self.tracks:
            for t in self.tracks:
                if t['type'] == 'video' and 'sar' in t:
                    if t['sar'] >= ar_16_9:
                        result = t['pixel width'] / t['sar']
                    else:
                        result = t['pixel height']
                    break
        return result
    
    
    
    def extract(self, options):
        result = Container.extract(self, options)
        if self.chapter_markers :
            info = file_util.copy_file_info(self.file_info, options)
            info['kind'] = 'txt'
            if file_util.complete_info_default_values(info):
                dest_path = file_util.canonic_path(info, self.meta)
                if file_util.check_and_varify(dest_path, options.overwrite):
                    c = Chapter(dest_path)
                    for cm in self.chapter_markers:
                        c.add_chapter_marker(cm)
                
                    self.logger.debug(u'Extracting chapter markers from %s to %s', self.file_path, dest_path)
                    c.write(dest_path)
                    if file_util.clean_if_not_exist(dest_path):
                        result.append(dest_path)
        return result
    
    
    def pack(self, options):
        Container.pack(self, options)
        info = file_util.copy_file_info(self.file_info, options)
        if options.pack in ('mkv'):
            info['kind'] = 'mkv'
            if file_util.complete_info_default_values(info):
                dest_path = file_util.canonic_path(info, self.meta)
                if dest_path is not None:
                    pc = repository_config['Kind'][info['kind']]['Profile'][info['profile']]
                    selected_related = []
                    selected_tracks = []
                
                    if 'pack' in pc:
                        if 'related' in pc['pack']:
                            for (path,info) in self.related.iteritems():
                                for c in pc['pack']['related']:
                                    if all((k in info and info[k] == v) for k,v in c.iteritems()):
                                        selected_related.append(path)
                                        break
                        if 'tracks' in pc['pack']:
                            for t in self.tracks:
                                for c in pc['pack']['tracks']:
                                    if all((k in t and t[k] == v) for k,v in c.iteritems()):
                                        selected_tracks.append(t)
                                        break
                                    
                    if file_util.check_and_varify(dest_path, options.overwrite):
                        command = [u'mkvmerge', u'--output', dest_path, u'--no-chapters', u'--no-attachments', u'--no-subtitles', self.file_path]
                        
                        for r in selected_related:
                            rinfo = self.related[r]
                            if rinfo['kind'] == 'srt':
                                command.append(u'--sub-charset')
                                command.append(u'0:UTF-8')
                                command.append(u'--language')
                                command.append(u'0:{0}'.format(rinfo['language']))
                                command.append(r)
                            
                            if rinfo['kind'] == 'txt' and rinfo['profile'] == 'chapter':
                                command.append(u'--chapter-language')
                                command.append(u'eng')
                                command.append(u'--chapter-charset')
                                command.append(u'UTF-8')
                                command.append(u'--chapters')
                                command.append(r)
                            
                        audio_tracks = []
                        video_tracks = []
                        for t in selected_tracks:
                            if 'name' in t:
                                command.append(u'--track-name')
                                command.append(u'{0}:{1}'.format(t['number'], t['name']))
                            
                            if 'language' in t:
                                command.append(u'--language')
                                command.append(u'{0}:{1}'.format(t['number'], t['language']))
                            
                            if t['type'] == 'audio':
                                audio_tracks.append(unicode(t['number']))
                            elif t['type'] == 'video':
                                video_tracks.append(unicode(t['number']))
                    
                        command.append(u'--audio-tracks')
                        command.append(u','.join(audio_tracks))
                        command.append(u'--video-tracks')
                        command.append(u','.join(video_tracks))
                    
                        message = u'Pack {0} --> {1}'.format(self.file_path, dest_path)
                        file_util.execute_command(command, message, options.debug)
                        file_util.clean_if_not_exist(dest_path)
                    
        return
    
    
    def transcode(self, options):
        Container.transcode(self, options)
        info = file_util.copy_file_info(self.file_info, options)
        if options.transcode in ('mkv', 'm4v'):
            info['kind'] = options.transcode
            if file_util.complete_info_default_values(info):
                dest_path = file_util.canonic_path(info, self.meta)
                if dest_path is not None:
                    command = None
                    if file_util.check_and_varify(dest_path, options.overwrite):
                        command = [u'HandbrakeCLI']
                        tc = repository_config['Kind'][info['kind']]['Profile'][info['profile']]['transcode']
                    
                        if 'flags' in tc:
                            for v in tc['flags']:
                                command.append(v)
                            
                        if 'options' in tc:
                            for (k,v) in tc['options'].iteritems():
                                command.append(k)
                                command.append(unicode(v))
                            
                        found_audio = False
                        audio_options = {'--audio':[]}
                        for s in tc['audio']:
                            for t in self.tracks:
                                for c in s:
                                    if all((k in t and t[k] == v) for k,v in c['from'].iteritems()):
                                        found_audio = True
                                        audio_options['--audio'].append(unicode(t['number']))
                                        for (k,v) in c['to'].iteritems():
                                            if k not in audio_options: audio_options[k] = []
                                            audio_options[k].append(unicode(v))
                                        
                            if found_audio:
                                break
                            
                        if found_audio:
                            for (k,v) in audio_options.iteritems():
                                if v:
                                    command.append(k)
                                    command.append(u','.join(v))
                                
                        command.append(u'--input')
                        command.append(self.file_path)
                        command.append(u'--output')
                        command.append(dest_path)
                    
                        message = u'Transcode {0} --> {1}'.format(self.file_path, dest_path)
                        file_util.execute_command(command, message, options.debug)
                        file_util.clean_if_not_exist(dest_path)
        return
    
    
    
    def print_chapter_markers(self):
        return (u'\n'.join([format_value(chapter_marker) for chapter_marker in self.chapter_markers]))
    
    
    def print_tags(self):
        return (u'\n'.join([format_key_value(key, self.tags[key]) for key in sorted(set(self.tags))]))
    
    
    def print_tracks(self):
        return (u'\n'.join([format_value(format_track(track)) for track in self.tracks]))
    
    
    def __unicode__(self):
        result = Container.__unicode__(self)
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
        if start_time is not None:
            self.start_time = timecode_to_miliseconds(start_time)
        else:
            self.start_time = None
    
    
    def set_name(self, name):
        if name is not None:
            self.name = name.strip('"').strip("'").strip()
        else:
            self.name = None
    
    
    def set_language(self, language):
        if language is not None:
            self.language = language
        else:
            self.language = None
    
    
    def encode(self, line_buffer, index):
        start_time_string = unicode(miliseconds_to_time(self.start_time, '.'), 'utf-8')
        line_buffer.append(u'CHAPTER{0}={1}'.format(str(index).zfill(2), start_time_string))
        line_buffer.append(u'CHAPTER{0}NAME={1}'.format(str(index).zfill(2), self.name))
    
    
    def __unicode__(self):
        return u'{0} : {1}'.format(miliseconds_to_time(self.start_time), self.name)
    



# Matroska Class
class Matroska(AVContainer):
    def __init__(self, file_path):
        self.logger = logging.getLogger('mp4pack.matroska')
        AVContainer.__init__(self, file_path)
    
    
    def _line_depth(self, mkvinfo_line):
        return mkvinfo_line_start_re.search(mkvinfo_line).start(0)
    
    
    def _parse_track(self, index, mkvinfo_report, track_nest_depth):
        track = {}
        while (self._line_depth(mkvinfo_report[index]) > track_nest_depth):
            match = mkvinfo_track_number_re.search(mkvinfo_report[index])
            if match is not None:
                track['number'] = int(match.group(1))
                index += 1
                continue
            match = mkvinfo_track_type_re.search(mkvinfo_report[index])
            if match is not None:
                track['type'] = match.group(1)
                index += 1
                continue
            match = mkvinfo_codec_id_re.search(mkvinfo_report[index])
            if match is not None:
                track['codec'] = match.group(1)
                index += 1
                continue
            match = mkvinfo_video_fps_re.search(mkvinfo_report[index])
            if match is not None:
                track['frame rate'] = float(match.group(1))
                index += 1
                continue
            match = mkvinfo_language_re.search(mkvinfo_report[index])
            if match is not None:
                track['language'] = match.group(1)
                index += 1
                continue
            match = mkvinfo_name_re.search(mkvinfo_report[index])
            if match is not None:
                track['name'] = match.group(1)
                index += 1
                continue
            match = mkvinfo_video_pixel_width_re.search(mkvinfo_report[index])
            if match is not None:
                track['pixel width'] = int(match.group(1))
                index += 1
                continue
            match = mkvinfo_video_pixel_height_re.search(mkvinfo_report[index])
            if match is not None:
                track['pixel height'] = int(match.group(1))
                index += 1
                continue
            match = mkvinfo_audio_sampling_frequency_re.search(mkvinfo_report[index])
            if match is not None:
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
            if match is not None:
                chapter_marker.set_start_time(match.group(1))
                index += 1
                continue
            match = mkvinfo_chapter_string_re.search(mkvinfo_report[index])
            if match is not None:
                chapter_marker.set_name(match.group(1))
                index += 1
                continue
            match = mkvinfo_chapter_language_re.search(mkvinfo_report[index])
            if match is not None:
                chapter_marker.set_language(match.group(1))
                index += 1
                continue
                
            index += 1
            
        return index, chapter_marker
    
    
    def load(self):
        AVContainer.load(self)
        command = [u'mkvinfo', self.file_path]
        output, error = file_util.execute_command(command, None)
        mkvinfo_report = unicode(output, 'utf-8').splitlines()
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
                    while mkvinfo_chapter_atom_re.search(mkvinfo_report[index]) is None:
                        index += 1
                else:
                    index += 1
                    
            elif mkvinfo_start_re.search(mkvinfo_report[index]):
                in_mkvinfo_output = True
                index += 1
    
    
    def extract(self, options):
        result = AVContainer.extract(self, options)
        if options.profile is None or file_util.profile_valid_for_kind(options.profile, 'srt'):
            selected_files = []
            selected_tracks = []
            info = file_util.copy_file_info(self.file_info, options)
            if 'volume' in info: del info['volume']
            info['profile'] = 'dump'
            
            for k in ('srt', 'ass'):
                if 'volume' in info: del info['volume']
                info['kind'] = k
                if file_util.complete_info_default_values(info):
                    pc = repository_config['Kind'][info['kind']]['Profile'][info['profile']]
                    if 'extract' in pc and 'tracks' in pc['extract']:
                        for t in self.tracks:
                            for c in pc['extract']['tracks']:
                                if all((k in t and t[k] == v) for k,v in c.iteritems()):
                                    selected_tracks.append(t)
                                    break
                                    
            if selected_tracks:
                command = [u'mkvextract', u'tracks', self.file_path ]
                for t in selected_tracks:
                    if 'volume' in info: del info['volume']
                    info['kind'] = t['kind']
                    info['language'] = t['language']
                    if file_util.complete_info_default_values(info):
                        dest_path = file_util.canonic_path(info, self.meta)
                        if file_util.check_and_varify(dest_path, options.overwrite):
                            selected_files.append(dest_path)
                            command.append(u'{0}:{1}'.format(unicode(t['number']), dest_path))
                        
            if selected_files:
                message = u'Extract {0} tracks from {1}'.format(unicode(len(selected_files)), self.file_path)
                file_util.execute_command(command, message, options.debug)
        
            extracted_files = []
            for f in selected_files:
                if file_util.clean_if_not_exist(f):
                    extracted_files.append(f)
        
            o = copy.deepcopy(options)
            o.transcode = 'srt'
            o.extract = None
        
            for f in extracted_files:
                s = Subtitle(f)
                s.transcode(o)
                result.append(f)
        else:
            self.logger.warning('Skipping subtitle extraction. Profile %s invalid for srt kind.', options.profile)
        return result
    



# Mpeg4 Class
class Mpeg4(AVContainer):
    def __init__(self, file_path):
        self.logger = logging.getLogger('mp4pack.mp4')
        AVContainer.__init__(self, file_path)
    
    
    def _parse_tag(self, line):
        name = None
        value = None
        match = mp4info_tag_re.search(line)
        if match:
            mp4info_tag_name = match.group(1)
            name = tag_name_resolver.canonic_name_from_mp4info(mp4info_tag_name)
            value = match.group(2)
        return name, value
    
    
    def _parse_track(self, line):
        track = None
        match = mp4info_video_track_re.search(line)
        if match:
            track = { 'type':'video' }
            track['number'] = int(match.group(1))
            track['codec'] = match.group(2)
            track['duration'] = float(match.group(3))
            track['bit rate'] = int(match.group(4))
            track['pixel width'] = int(match.group(5))
            track['pixel height'] = int(match.group(6))
            track['frame rate'] = float(match.group(7))
        else:
            match = mp4info_audio_track_re.search(line)
            if match:
                track = { 'type':'audio' }
                track['number'] = int(match.group(1))
                track['codec'] = match.group(2)
                track['duration'] = float(match.group(3))
                track['bit rate'] = int(match.group(4))
                track['sampling frequency'] = int(match.group(5))
                
        return track
    
    
    def _parse_chapter_marker(self, line):
        m = None
        match = mp4chaps_chapter_re.search(line)
        if match:
            start_time = match.group(2)
            name = match.group(3)
            m = ChapterMarker(start_time, name)
        return m
    
    
    def load(self):
        AVContainer.load(self)
        command = [u'mp4info', self.file_path]
        output, error = file_util.execute_command(command, None)
        mp4info_report = unicode(output, 'utf-8').splitlines()
        
        in_tag_section = False
        for idx, line in enumerate(mp4info_report):
            if not in_tag_section:
                track = self._parse_track(line)
                if track:
                    self.add_track(track)
                    continue
                    
            name, value = self._parse_tag(line)
            if name:
                self.set_tag(name, value)
                if not in_tag_section:
                    in_tag_section = True
            
        command = [u'mp4chaps', u'-l', self.file_path]
        output, error = file_util.execute_command(command, None)
        mp4chaps_report = unicode(output, 'utf-8').splitlines()
        for idx, line in enumerate(mp4chaps_report):
            m = self._parse_chapter_marker(line)
            if m: self.add_chapter_marker(m)
    
    
    def tag(self, options):
        AVContainer.tag(self, options)
        tc = self.build_subler_tag_update_string()
        if tc:
            message = u'Tag {0}'.format(self.file_path)
            command = [u'SublerCLI', u'-i', self.file_path, u'-t', tc]
            file_util.execute_command(command, message, options.debug)
        else:
            self.logger.info(u'No tags need update in %s', self.file_path)
    
    
    def optimize(self, options):
        AVContainer.optimize(self, options)
        message = u'Optimize {0}'.format(self.file_path)
        command = [u'mp4file', u'--optimize', self.file_path]
        file_util.execute_command(command, message, options.debug)
    
    
    def update(self, options):
        AVContainer.update(self, options)
        if options.update == 'txt':
            pass
            
        if options.update == 'srt':
            info = file_util.copy_file_info(self.file_info, options)
            info['kind'] = 'srt'
            if file_util.complete_info_default_values(info):
                pc = repository_config['Kind']['srt']['Profile'][info['profile']]
                
                if 'profile' in info and 'update' in pc:
                    message = u'Remove existing subtitle tracks in {0}'.format(self.file_path)
                    command = [u'SublerCLI', u'-r', self.file_path]
                    file_util.execute_command(command, message, options.debug)
                    
                    selected = {}
                    for (p,i) in self.related.iteritems():
                        for c in pc['update']['related']:
                            if all((k in i and i[k] == v) for k,v in c['from'].iteritems()):
                                selected[p] = i
                                break
                            
                    for (p,i) in selected.iteritems():
                        for c in pc['update']['related']:
                            if all((k in i and i[k] == v) for k,v in c['from'].iteritems()):
                                message = u'Add subtitles {0} --> {1}'.format(p, self.file_path)
                                command = [
                                    u'SublerCLI', u'-i', self.file_path, 
                                    u'-s', p, 
                                    u'-l', repository_config['Language'][i['language']], 
                                    u'-n', c['to']['Name'], 
                                    u'-a', unicode(int(round(self.playback_height() * c['to']['height'])))
                                ]
                                file_util.execute_command(command, message, options.debug)
                                
                    if 'smart' in pc['update']:
                        smart_section = pc['update']['smart']
                        found = False
                        for code in smart_section['order']:
                            for (p,i) in selected.iteritems():
                                if i['language'] == code:
                                    message = u'Add smart {0} subtitles {1} --> {2}'.format(repository_config['Language'][code], p, self.file_path)
                                    command = [
                                        u'SublerCLI', u'-i', self.file_path, 
                                        u'-s', p, 
                                        u'-l', repository_config['Language'][smart_section['language']], 
                                        u'-n', smart_section['Name'], 
                                        u'-a', unicode(int(round(self.playback_height() * smart_section['height'])))
                                    ]
                                    file_util.execute_command(command, message, options.debug)
                                    found = True
                                    break
                            if found: break
    
    
    def build_subler_tag_update_string(self):
        result = None
        update = {}
        if self.meta:
            for t in self.meta:
                if not(t in self.tags and self.tags[t] == self.meta[t]):
                    update[t] = self.meta[t]
                    
        elif self.file_info:
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
        
        if update:
            result = (u''.join([u'{{{0}:{1}}}'.format(t, format_for_subler_tag(update[t])) for t in sorted(set(update))]))
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
            content = reader.read()
            reader.close()
        except IOError as error:
            self.logger.error(str(error))
            content = None
        
        if content:
            encoding = chardet.detect(content)
            self.logger.debug(u'%s encoding detected for %s', encoding['encoding'], self.file_path)
            content = unicode(content, encoding['encoding'])
            lines = content.splitlines()
        return lines
    
    
    def decode(self):
        pass
    
    
    def write(self, path):
        lines = self.encode()
        if lines:
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
                self.logger.error(str(error))
    
    
    def encode(self):
        return None
    
    
    def transcode(self, options):
        Container.transcode(self, options)
        self.decode()
        info = file_util.copy_file_info(self.file_info, options)
        info['kind'] = options.transcode
        if file_util.complete_info_default_values(info):
            dest_path = file_util.canonic_path(info, self.meta)
            if file_util.check_and_varify(dest_path, options.overwrite):
                self.logger.info(u'Transcode %s --> %s', self.file_path, dest_path)
                self.write(dest_path)
                file_util.clean_if_not_exist(dest_path)
    
    



# Subtitle Class
class SubtitleBlock(object):
    def __init__(self):
        self.begin = None
        self.end = None
        self.lines = []
    
    
    def set_begin_miliseconds(self, value):
        self.begin = value
        
    
    
    def set_end_miliseconds(self, value):
        self.end = value
    
    
    def clear(self):
        self.lines = []
    
    
    def add_line(self, value):
        if value:
            value = value.strip()
            if value:
                self.lines.append(value)
    
    
    def shift(self, offset):
        self.begin += offset
        self.end += offset
    
    
    def scale_rate(self, factor):
        self.begin = int(round(float(self.begin) * float(factor)))
        self.end = int(round(float(self.end) * float(factor)))
    
    
    def valid(self):
        return self.begin and self.end and self.begin < self.end and self.lines
    
    
    def encode(self, line_buffer, index):
        line_buffer.append(unicode(index))
        begin_time = miliseconds_to_time(self.begin, ',')
        end_time = miliseconds_to_time(self.end, ',')
        line_buffer.append(u'{0} --> {1}'.format(unicode(begin_time), unicode(end_time)))
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
                if index == last_line and current_block_start is not None:
                    next_block_start = index + 1
                    
                match = srt_time_line.search(lines[index])
                if match is not None and lines[index - 1].strip().isdigit():
                    next_block = SubtitleBlock()
                    next_block.set_begin_miliseconds(timecode_to_miliseconds(match.group(1)))
                    next_block.set_end_miliseconds(timecode_to_miliseconds(match.group(2)))
                    if current_block_start is not None:
                        next_block_start = index - 1
                    else:
                        # first block
                        current_block_start = index - 1
                        current_block = next_block
                        next_block = None
                        
                if next_block_start is not None:
                    for line in lines[current_block_start + 2:next_block_start]:
                        current_block.add_line(line)
                        
                    if current_block.valid():
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
                    if match is not None:
                        formation = match.group(1).strip().replace(' ','').split(',')
                    break
                index += 1
                
            if formation is not None:
                start = formation.index('Start')
                stop = formation.index('End')
                text = formation.index('Text')
                for line in lines:
                    match = ass_subline.search(line)
                    if match is not None:
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
                            
                        if block.valid():
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
                        
                    if block.valid():
                        self.subtitle_blocks.append(block)
        
        
        if not self.subtitle_blocks:
            Text.decode(self)
            self.subtitle_blocks = []
            lines = self.read()
            if self.file_info['kind'] == 'srt':
                decode_srt(lines)
            elif self.file_info['kind'] in ('ass', 'ssa'):
                decode_ass(lines)
            #elif self.file_info['kind'] == 'sub':
            #    decode_sub(lines, 25)
    
    
    def encode(self):
        result = Text.encode(self)
        self.decode()
        if self.subtitle_blocks:
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
        if file_util.complete_info_default_values(info):
            p = repository_config['Kind'][info['kind']]['Profile'][info['profile']]
            if 'transcode' in p and 'filter' in p['transcode']:
                self.filter(p['transcode']['filter'])
                self.logger.debug(u'Filtering %s by %s', self.file_path, unicode(p['transcode']['filter']))
                
            if options.time_shift is not None:
                self.shift_times(options.time_shift)
                
            if options.input_rate is not None and options.output_rate is not None:
                input_frame_rate = frame_rate_to_float(options.input_rate)
                output_frame_rate = frame_rate_to_float(options.output_rate)
                if input_frame_rate is not None and output_frame_rate is not None:
                    factor = input_frame_rate / output_frame_rate
                    self.change_framerate(factor)
                    
        Text.transcode(self, options)
    
    
    def filter(self, sequence_list):
        if sequence_list:
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
        if not self.chapter_markers:
            Text.decode(self)
            lines = self.read()
            if lines:
                for index in range(len(lines) - 1):
                    match_timecode = ogg_chapter_timestamp_re.search(lines[index])
                    if match_timecode is not None:
                        match_name = ogg_chapter_name_re.search(lines[index + 1])
                        if match_name is not None:
                            timecode = match_timecode.group(2)
                            name = match_name.group(2)
                            self.add_chapter_marker(ChapterMarker(timecode, name))
    
    
    def encode(self):
        result = Text.encode(self)
        self.decode()
        if self.chapter_markers:
            result = []
            for idx, m in enumerate(self.chapter_markers):
                m.encode(result, idx + 1)
        return result
    
    
    def add_chapter_marker(self, chapter_marker):
        if chapter_marker is not None:
            if not self.chapter_markers:
                self.chapter_markers = []
            self.chapter_markers.append(chapter_marker)
    



# Image Class
class Image(Container):
    def __init__(self, file_path):
        self.logger = logging.getLogger('mp4pack.image')
        Container.__init__(self, file_path)
    
    



# Tag Name Resolver Class (Singletone)
class TagNameResolver(object):
    def __init__(self):
        self.canonic_map = {}
        self.mp4info_map = {}
        
        for tag in db_config['tag']:
            self.canonic_map[tag[0]] = tag
            if tag[2] is not None:
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
            self.logger.debug(u'Loading %s filter sequence', name)
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
            if blocks:
                fs = self.find_filter_sequence(fn)
                if fs:
                    next = []
                    for block in blocks:
                        if block.valid() and self.filter_block(block, fs):
                            next.append(block)
                    blocks = next
        return blocks
    
    
    def filter_block(self, block, filter_sequence):
        result = block.valid()
        if result:
            result = filter_sequence.filter(block)
        return result
        
    


class FilterSequence(object):
    def __init__(self, config):
        self.logger = logging.getLogger('mp4pack.filter')
        self.config = config
    
    
    def filter(self, block):
        result = False
        if block is not None:
            result = block.valid()
        return result
    


class DropFilterSequence(FilterSequence):
    def __init__(self, config):
        self.logger = logging.getLogger('mp4pack.filter.drop')
        FilterSequence.__init__(self, config)
        self.expression = []
    
    
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
                        if e.search(line) is not None:
                            self.logger.debug(u'Found match in %s', line)
                            keep = False
                            break
                    if keep:
                        block.add_line(line)
                        
            elif self.config['scope'] == 'block':
                for line in block.lines:
                    for e in self.expression:
                        if e.search(line) is not None:
                            block.clear()
                            break
                    if not block.valid(): break
                        
            result = block.valid()
        return result
    


class ReplaceFilterSequence(FilterSequence):
    def __init__(self, config):
        self.logger = logging.getLogger('mp4pack.filter.replace')
        FilterSequence.__init__(self, config)
        self.expression = []
    
    
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
                    if not block.valid(): break
                        
            elif self.config['scope'] == 'block':
                all_lines = u'\n'.join(block.lines)
                block.clear()
                for e in self.expression:
                    all_lines = e[0].sub(e[1], all_lines).strip()
                    if not all_lines: break
                for line in all_lines.split(u'\n'):
                    block.add_line(line)
                    
            result = block.valid()
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
        if file_path is not None:
            for mk, mk_re in self.file_name_schema_re.iteritems():
                match = mk_re.search(os.path.basename(file_path))
                if match is not None:
                    media_kind = mk
                    break
            
            if media_kind is not None:
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
                
                if not info['Name']:
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
            if easy_name is not None:
                result = ''.join([result, ' ', easy_name])
            
            result = ''.join([result, '.', info['kind']])
        
        if not valid:
            result = None
        
        return result
    
    
    def canonic_path(self, info, meta):
        result = None
        valid = True
        if 'kind' in info and info['kind'] in repository_config['Kind'].keys():
            if 'volume' in info and info['volume'] in repository_config['Volume']:
                if 'profile' in info:
                    if self.profile_valid_for_kind(info['profile'], info['kind']):
                        result = os.path.join(repository_config['Volume'][info['volume']], info['Media Kind'], info['kind'], info['profile'])
                        if info['Media Kind'] == 'tvshow' and 'show_small_name' in info and 'TV Season' in info:
                            result = os.path.join(result, info['show_small_name'], str(info['TV Season']))
                            
                        if info['kind'] in self.subtitles_kinds and 'language' in info and info['language'] in repository_config['Language']:
                                result = os.path.join(result, info['language'])
                    else:
                        valid = False
                        self.logger.warning(u'Invalid profile for %s', unicode(info))
                else:
                    valid = False
                    self.logger.warning(u'Unknow profile for %s', unicode(info))
            else:
                valid = False
                if 'volume' in info:
                    self.logger.warning(u'Invalid volume for %s', unicode(info))
                else:
                    self.logger.warning(u'Unknow volume for %s', unicode(info))
        else:
            valid = False
            if 'kind' in info:
                self.logger.warning(u'Invalid kind for %s', unicode(info))
            else:
                self.logger.warning(u'Unknow kind for %s', unicode(info))
        
        if valid:
            result = os.path.join(result, self.canonic_name(info, meta))
            result = os.path.abspath(result)
        else:
            result = None
        return result
    
    
    def clean_if_not_exist(self, path):
        result = True
        if not os.path.exists(path):
            result = False
            try:
                os.removedirs(os.path.dirname(path))
            except OSError:
                pass
                
        return result
    
    
    def clean(self, path):
        try:
            os.remove(path)
            os.removedirs(os.path.dirname(path))
        except OSError:
            pass
    
    
    def related(self, path):
        # <Volume>/<Media Kind>/<Kind>/<Profile>(/<Show>/<Season>)?/(IMDb<IMDB ID> <Name>|<Show> <Code> <Name>).<Extension>
        related = {}
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
    
    
    def detect_audio_codec_kind(self, codec):
        result = None
        for k,v in self.audio_codec_kind.iteritems():
            if v.search(codec) is not None:
                result = k
                break
        return result
    
    
    def detect_subtitle_codec_kind(self, codec):
        result = None
        for k,v in self.subtitle_codec_kind.iteritems():
            if v.search(codec) is not None:
                result = k
                break
        return result
    
    
    def varify_directory(self, path):
        result = False
        try:
            dirname = os.path.dirname(path)
            if not os.path.exists(dirname):
                self.logger.debug(u'Creating directory %s', dirname)
                os.makedirs(dirname)
                result = True
        except OSError as error:
            self.logger.error(str(error))
            result = False
        return result
    
    
    def profile_valid_for_kind(self, profile, kind):
        return profile and kind and kind in repository_config['Kind'].keys() and profile in repository_config['Kind'][kind]['Profile'].keys()
            
    
    
    def check_path(self, path, overwrite=False):
        result = True
        if path is not None:
            if os.path.exists(path) and not overwrite:
                self.logger.warning(u'Refusing to overwrite %s', path)
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
            cmd = []
            for e in command:
                if u' ' in e:
                    cmd.append(u'"{0}"'.format(e))
                else:
                    cmd.append(e)
            return u' '.join(cmd)
        
        
        output = None
        error = None
        
        if not debug:
            if command:
                self.logger.debug(u'Execute: %s', encode_command(command))
                if message:
                    self.logger.info(message)
                from subprocess import Popen, PIPE
                proc = Popen(command, stdout=PIPE)
                report = proc.communicate()
                
                output = report[0]
                error = report[1]
                
                if error:
                    self.logger.error(error)
                if output:
                    #self.logger.debug(output)
                    result = True
        else:
            self.logger.info(message)
            print encode_command(command)
        return output, error
    
    
    def complete_info_default_values(self, info):
        result = True
        if 'kind' in info and info['kind'] in repository_config['Kind'].keys():
            kc = repository_config['Kind'][info['kind']]
            if 'profile' not in info:
                if 'default' in kc and 'profile' in kc['default']:
                    info['profile'] = kc['default']['profile']
                else:
                    result = False
                    self.logger.warning(u'Could not assign default profile for %s', unicode(info))
                    
            if result and not self.profile_valid_for_kind(info['profile'], info['kind']):
                result = False
                self.logger.warning(u'Profile %s is invalid for kind %s', info['profile'], info['kind'])
                
            if result:
                if 'volume' not in info:
                    if info['profile'] in kc['Profile'] and 'default' in kc['Profile'][info['profile']]:
                        dpc = kc['Profile'][info['profile']]['default']
                        if info['Media Kind'] in dpc:
                            if 'volume' in dpc[info['Media Kind']]:
                                info['volume'] = dpc[info['Media Kind']]['volume']
                if 'volume' not in info:
                    result = False
                    self.logger.warning(u'Could not assign default volume for %s', unicode(info))
        else:
            result = False
            if 'kind' in info:
                self.logger.warning(u'Invalid kind for %s', unicode(info))
            else:
                self.logger.warning(u'Unknow kind for %s', unicode(info))
        
        return result
    
    
    def copy_file_info(self, info, options):
        result = None
        if info:
            i = copy.deepcopy(info)
            i['volume'] = options.volume
            if i['volume'] is None:
                del i['volume']
        
            i['profile'] = options.profile
            if i['profile'] is None:
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
    if match is not None:
        hours = match.group(1)
        minutes = match.group(2)
        seconds = match.group(3)
        milliseconds = match.group(4)
        valid = True
        
    else:
        match = descriptive_time_format.search(timecode)
        if match is not None:
            if match.group(1) is not None:
                hours = match.group(1)
            if match.group(2) is not None:
                minutes = match.group(2)
            if match.group(3) is not None:
                seconds = match.group(3)
            if match.group(4) is not None:
                milliseconds = match.group(4)
            valid = True
            
    if milliseconds is not None:
        if len(milliseconds) == 2:
            milliseconds = 10 * int(milliseconds)
        elif len(milliseconds) >= 3:
            milliseconds = milliseconds[0:3]
            milliseconds = int(milliseconds)
        else:
            milliseconds = int(milliseconds)
    else:
        milliseconds = 0
        
    if seconds is not None:
        seconds = int(seconds)
    else:
        seconds = 0
        
    if minutes is not None:
        minutes = int(minutes)
    else:
        minutes = 0
        
    if hours is not None:
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


def frame_to_miliseconds(frame, frame_rate):
    return round(float(1000)/float(frame_rate) * float(frame))


def format_for_subler_tag(value):
    if value and isinstance(value, unicode) and escaped_subler_tag_characters.issubset(value):
        value = value.replace(u'{',u'&#123;').replace(u'}',u'&#125;').replace(u':',u'&#58;')
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
    if not f.file_info:
        f = None
    return f



# Info format helper functions
def format_info_title(text):
    margin = repository_config['Display']['margin']
    width = repository_config['Display']['wrap']
    indent = repository_config['Display']['indent']
    return u'\n\n\n{2}[{0:-^{1}}]'.format(text, width + indent, u' '*margin)


def format_info_subtitle(text):
    margin = repository_config['Display']['margin']
    indent = repository_config['Display']['indent']
    return u'\n{2}[{0:^{1}}]\n'.format(text, indent - 3 - margin, u' '*margin)


def format_key_value(key, value):
    margin = repository_config['Display']['margin']
    width = repository_config['Display']['wrap']
    indent = repository_config['Display']['indent']
    
    format_line = u'{3}{0:-<{1}}: {2}'
    v = unicode(value)
    if len(v) > width:
        lines = textwrap.wrap(value, width)
        space = u'\n' + u' '*indent
        v = space.join(lines)
    return format_line.format(key, indent - 2 - margin, v, u' '*margin)


def format_value(value):
    margin = repository_config['Display']['margin']
    return u'{1}{0}'.format(value, u' '*margin)


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
escaped_subler_tag_characters = set(('{', '}', ':'))

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
