# -*- coding: utf-8 -*-

import os
import re
import logging
import hashlib
import chardet
import copy
import textwrap
import plistlib
import xml.sax.saxutils

from datetime import datetime
from config import repository_config
from config import media_property
from db import theEntityManager
from subprocess import Popen, PIPE
import xml.etree.cElementTree as ElementTree

# Generic file loading function
def make_media_file(file_path):
    f = None
    file_type = os.path.splitext(file_path)[1].strip('.')
    if file_type in theFileUtil.container['mp4']['kind']:
        f = Mpeg4(file_path, autoload=False)
    elif file_type in theFileUtil.container['matroska']['kind']:
        f = Matroska(file_path, autoload=False)
    elif file_type in theFileUtil.container['subtitles']['kind']:
        f = Subtitle(file_path, autoload=False)
    elif file_type in theFileUtil.container['chapters']['kind']:
        f = Chapter(file_path, autoload=False)
    elif file_type in theFileUtil.container['image']['kind']:
        f = Artwork(file_path, autoload=False)
    elif file_type in theFileUtil.container['raw audio']['kind']:
        f = RawAudio(file_path, autoload=False)
    elif file_type in theFileUtil.container['avi']['kind']:
        f = Avi(file_path, autoload=False)
        
    return f


# Container super Class
class Container(object):
    def __init__(self, file_path, autoload=True):
        self.logger = logging.getLogger('mp4pack.container')
        self.file_path = file_path
        self.path_info = None
        self.info = None
        self.related = None
        self.meta = None
    
    
    def valid(self):
        return self.path_info is not None and self.info is not None
    
    
    def load(self):
        result = False
        Container.load_path_info(self)
        if self.path_info is not None:
            result = True
            self.load_info()
            self.load_related()
            self.load_meta()
        else:
            self.logger.warning(u'Could not undestand file name schema %s',self.file_path)
            Container.unload(self)
            
        return result
    
    
    def unload(self):
        self.path_info = None
        self.info = None
        self.related = None
        self.meta = None
    
    
    def load_info(self):
        self.info = None
        if self.file_path:
            self.info = theFileUtil.load_info(self.file_path)
    
    
    def load_path_info(self):
        # <Volume>/<Media Kind>/<Kind>/<Profile>(/<Show>/<Season>)?(/<Language>)?/(IMDb<IMDB ID> <Name>|<Show> <Code> <Name>).<Extension>
        self.path_info = None
        if self.file_path:
            for mk in media_property['stik']:
                if 'schema' in mk:
                    match = mk['schema'].search(os.path.basename(self.file_path))
                    if match is not None:
                        self.path_info = {'media kind':mk['code']}
                        if mk['name'] == 'movie':
                            self.path_info['imdb id'] = match.group(1)
                            self.path_info['name'] = match.group(2)
                            self.path_info['kind'] = match.group(3)
                        
                        elif mk['name'] == 'tvshow':
                            self.path_info['tv show key'] = match.group(1)
                            self.path_info['tv episode id'] = match.group(2)
                            self.path_info['tv season'] = int(match.group(3))
                            self.path_info['tv episode #'] = int(match.group(4))
                            self.path_info['name'] = match.group(5)
                            self.path_info['kind'] = match.group(6)
                        
                        if not self.path_info['name']:
                            del self.path_info['name']
                        
                        prefix = os.path.dirname(self.file_path)
                        if self.path_info['kind'] in theFileUtil.kind_with_language:
                            prefix, lang = os.path.split(prefix)
                            if lang in theFileUtil.property_map['iso3t']['language']:
                                self.path_info['language'] = lang
    
    
    def load_related(self):
        # <Volume>/<Media Kind>/<Kind>/<Profile>(/<Show>/<Season>)?/(IMDb<IMDB ID> <Name>|<Show> <Code> <Name>).<Extension>
        self.related = {}
        for v in repository_config['Volume']:
            for k in repository_config['Kind']:
                for p in repository_config['Kind'][k]['Profile']:
                    if repository_config['Kind'][k]['container'] in ('subtitles', 'raw audio'):
                        for l in theFileUtil.property_map['iso3t']['language']:
                            i = copy.deepcopy(self.path_info)
                            i['volume'] = v
                            i['kind'] = k
                            i['profile'] = p
                            i['language'] = l
                            rp = theFileUtil.canonic_path(i, self.meta)
                            if os.path.exists(rp):
                                self.related[rp] = i
                    else:
                        i = copy.deepcopy(self.path_info)
                        i['volume'] = v
                        i['kind'] = k
                        i['profile'] = p
                        rp = theFileUtil.canonic_path(i, self.meta)
                        if os.path.exists(rp):
                            self.related[rp] = i
    
    
    def load_meta(self):
        result = False
        self.meta = None
        if self.is_movie():
            record = theEntityManager.find_movie_by_imdb_id(self.path_info['imdb id'])
            if record:
                self.meta = {'media kind':9}
                
                if 'name' in record:
                    self.meta['name'] = record['name']
                if 'overview' in record:
                    self.meta['long description'] = FileUtil.whitespace_re.sub(u' ', record['overview']).strip()
                if 'content_rating' in record:
                    self.meta['rating'] = record['content_rating']
                if 'released' in record:
                    self.meta['release date'] = record['released']
                if 'tagline' in record:
                    self.meta['description'] = FileUtil.whitespace_re.sub(u' ', record['tagline']).strip()
                elif 'overview' in record:
                    s = FileUtil.sentence_end.split(FileUtil.whitespace_re.sub(u' ', record['overview']).strip('\'".,'))
                    if s: self.meta['description'] = s[0].strip('"\' ').strip() + '.'
                    
                self.load_cast(record)
                self.load_genre(record)
                result = True
                
        elif self.is_tvshow():
            show, episode = theEntityManager.find_episode(self.path_info['tv show key'], self.path_info['tv season'], self.path_info['tv episode #'])
            if show and episode:
                self.meta = {'media kind':10}
                
                if 'content_rating' in show:
                    self.meta['rating'] = show['content_rating']
                if 'network' in show:
                    self.meta['tv network'] = show['network']
                    
                self.load_genre(show)
                self.load_cast(show, True, False)
                if 'show' in episode:
                    self.meta['tv show'] = episode['show']
                    self.meta['album'] = episode['show']
                if 'season_number' in episode:
                    self.meta['tv season'] = episode['season_number']
                    self.meta['disk position'] = episode['season_number']
                    self.meta['disk total'] = 0
                if 'episode_number' in episode:
                    self.meta['tv episode #'] = episode['episode_number']
                    self.meta['track position'] = episode['episode_number']
                    self.meta['track total'] = 0
                if 'name' in episode:
                    self.meta['name'] = episode['name']
                if 'overview' in episode:
                    overview = FileUtil.whitespace_re.sub(u' ', episode['overview']).strip()
                    self.meta['long description'] = overview
                    s = FileUtil.sentence_end.split(overview.strip('\'".,'))
                    if s: self.meta['description'] = s[0].strip('"\' ').strip() + '.'
                if 'released' in episode:
                    self.meta['release date'] = episode['released']
                    
                self.meta['track #'] = u'{0} / {1}'.format(self.meta['track position'], self.meta['track total'])
                self.meta['disk #'] = u'{0} / {1}'.format(self.meta['disk position'], self.meta['disk total'])
                
                self.load_cast(episode, False, True)
                result = True
                
        if not result:
            self.meta = None
        else:
            self.pick_artist()
        return result
    
    
    def info(self, options):
        return unicode(self)
    
    
    def copy(self, options):
        result = None
        info = theFileUtil.copy_path_info(self.path_info, options)
        if theFileUtil.complete_info_default_values(info):
            dest_path = theFileUtil.canonic_path(info, self.meta)
            if theFileUtil.varify_if_path_available(dest_path, options.overwrite):
                command = theFileUtil.initialize_command('rsync', self.logger)
                command.extend([self.file_path, dest_path])
                message = u'Copy ' + self.file_path + u' --> ' + dest_path
                theFileUtil.execute(command, message, options.debug, pipeout=True, pipeerr=False, logger=self.logger)
                if theFileUtil.clean_if_not_exist(dest_path):
                    result = dest_path
                    if options.md5:
                        self.compare_checksum(dest_path)
        return result
    
    
    def rename(self, options):
        dest_path = os.path.join(os.path.dirname(self.file_path), self.canonic_name())
        if os.path.exists(dest_path) and os.path.samefile(self.file_path, dest_path):
            self.logger.debug(u'No renaming needed for %s',dest_path)
        else:
            if theFileUtil.check_if_path_available(dest_path, False):
                theFileUtil.varify_directory(dest_path)
                command = theFileUtil.initialize_command('mv', self.logger)
                command.extend([self.file_path, dest_path])
                message = u'Rename {0} --> {1}'.format(self.file_path, dest_path)
                theFileUtil.execute(command, message, options.debug, pipeout=True, pipeerr=False, logger=self.logger)
                theFileUtil.clean_if_not_exist(dest_path)
            else:
                self.logger.warning(u'Not renaming %s, destination exists: %s', self.file_path, dest_path)
    
    
    def tag(self, options):
        pass
    
    
    def optimize(self, options):
        pass
    
    
    
    def extract(self, options):
        return []
    
    
    def pack(self, options):
        pass
    
    
    def transcode(self, options):
        pass
    
    
    def update(self, options):
        pass
    
    
    
    def load_genre(self, record):
        if 'genre' in record.keys() and record['genre']:
            g = record['genre'][0]
            self.meta['genre'] = g['name']
            if 'code' in g:
                self.meta['genre type'] = g['code']
                
    
    
    def load_cast(self, record, initialize=True, finalize=True):
        if 'cast' in record:
            
            if initialize:
                for i in theFileUtil.property_map['name']['itunemovi']:
                    self.meta[i] = []
                    
            self.meta['directors'].extend([ r['name'] for r in record['cast'] if r['job'] == 'director' ])
            self.meta['codirectors'].extend([ r['name'] for r in record['cast'] if r['job'] == 'director of photography' ])
            self.meta['producers'].extend([ r['name'] for r in record['cast'] if r['job'].count('producer') > 0 ])
            self.meta['screenwriters'].extend([ r['name'] for r in record['cast'] if r['job'] == 'screenplay' or r['job'] == 'author' ])
            self.meta['cast'].extend([ r['name'] for r in record['cast'] if r['job'] == 'actor' ])
            
            if finalize:
                for i in theFileUtil.property_map['name']['itunemovi']:
                    if not self.meta[i]:
                        del self.meta[i]
        return
        
    
    
    def pick_artist(self):
        self.meta['artist'] = None
        if self.is_movie():
            for job in ('directors', 'producers', 'screenwriters', 'codirectors', 'cast'):
                if job in self.meta and self.meta[job]:
                    self.meta['artist'] = self.meta[job][0]
                    break
        elif self.is_tvshow():
            for job in ('screenwriters', 'directors', 'producers', 'codirectors', 'cast'):
                if job in self.meta and self.meta[job]:
                    self.meta['artist'] = self.meta[job][0]
                    break
    
    
    def download_artwork(self, options):
        result = False
        
        selected = []
        lookup = {'kind':'jpg', 'profile':'normal'}
        for (path,info) in self.related.iteritems():
            if all((k in info and info[k] == v) for k,v in lookup.iteritems()):
                selected.append(path)
                break
        if not selected:
            info = theFileUtil.copy_path_info(self.path_info, options)
            if self.is_movie():
                artwork = theEntityManager.find_tmdb_movie_poster(self.path_info['imdb id'])
            elif self.is_tvshow():
                artwork = theEntityManager.find_tvdb_episode_poster(self.path_info['tv show key'], self.path_info['tv season'], self.path_info['tv episode #'])
                
            if artwork:
                info = theFileUtil.copy_path_info(self.path_info, options)
                info['kind'] = artwork['kind']
                if 'volume' in info: del info['volume']
                if theFileUtil.complete_info_default_values(info):
                    p = Artwork(artwork['local'], False)
                    p.path_info = info
                    p.load_meta()
                    o = copy.deepcopy(options)
                    o.profile = 'download'
                    result = p.copy(o)
                    
                    if result:
                        self.logger.debug('Original artwork downloaded to %s', result)
                        p = Artwork(result)
                        o = copy.deepcopy(options)
                        o.transcode = 'jpg'
                        p.transcode(o)
        return result
    
    
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
        return self.path_info is not None and set(('media kind', 'imdb id')).issubset(set(self.path_info.keys())) and self.path_info['media kind'] == 9
    
    
    def is_tvshow(self):
        return self.path_info is not None and set(('media kind', 'tv show key', 'tv season', 'tv episode #')).issubset(set(self.path_info.keys())) and self.path_info['media kind'] == 10
    
    
    def easy_name(self):
        return theFileUtil.easy_name(self.path_info, self.meta)
    
    
    def canonic_name(self):
        return theFileUtil.canonic_name(self.path_info, self.meta)
    
    
    def canonic_path(self):
        return theFileUtil.canonic_path(self.path_info, self.meta)
    
    
    
    def print_meta(self):
        result = None
        if self.meta:
            result = (u'\n'.join([theFileUtil.format_key_value(key, self.meta[key], theFileUtil.property_map['name']['tag']) for key in sorted(set(self.meta))]))
        return result
    
    
    def print_related(self):
        result = None
        if self.related:
            result = (u'\n'.join([theFileUtil.format_value(key) for key in sorted(set(self.related))]))
        return result
    
    
    def print_path_info(self):
        result = None
        if self.path_info:
            result = (u'\n'.join([theFileUtil.format_key_value(key, self.path_info[key], theFileUtil.property_map['name']['tag']) for key in sorted(set(self.path_info))]))
        return result
    
    
    def print_file_info(self):
         return (u'\n'.join([theFileUtil.format_key_value(t, self.info['file'][t], theFileUtil.property_map['name']['file']) for t in sorted(set(self.info['file']))]))
    
    
    def print_tracks(self):
        return (u'\n\n\n'.join([theFileUtil.format_track(track) for track in self.info['track']]))
    
    
    def print_tags(self):
        return (u'\n'.join([theFileUtil.format_key_value(t, self.info['tag'][t], theFileUtil.property_map['name']['tag']) for t in sorted(set(self.info['tag']))]))
    
    
    def print_chapter_markers(self):
        return (u'\n'.join([theFileUtil.format_value(ChapterMarker(marker['time'], marker['name'])) for marker in self.info['menu']]))
    
    
    def __unicode__(self):
        result = None
        result = theFileUtil.format_info_title(self.file_path)
        if self.related:
            result = u'\n'.join((result, theFileUtil.format_info_subtitle(u'related'), self.print_related()))
        if self.related:
            result = u'\n'.join((result, theFileUtil.format_info_subtitle(u'file'), self.print_file_info()))
        if self.path_info:
            result = u'\n'.join((result, theFileUtil.format_info_subtitle(u'path info'), self.print_path_info()))
        
        if self.info['menu']:
            result = u'\n'.join((result, theFileUtil.format_info_subtitle(u'chapter markers'), self.print_chapter_markers()))
        
        if self.info['tag']:
            result = u'\n'.join((result, theFileUtil.format_info_subtitle(u'tags'), self.print_tags()))
        if self.meta:
            result = u'\n'.join((result, theFileUtil.format_info_subtitle(u'metadata'), self.print_meta()))
        
        if self.info['track']:
            result = u'\n'.join((result, theFileUtil.format_info_subtitle(u'tracks'), self.print_tracks()))
        return result
    
    


class AudioVideoContainer(Container):
    def __init__(self, file_path, autoload=True):
        Container.__init__(self, file_path, autoload)
        self.logger = logging.getLogger('mp4pack.av')
    
    
    def valid(self):
        return Container.valid(self) and self.info['track']
    
    
    def load(self):
        result = Container.load(self)
        if result and self.meta:
            self.meta['hd video'] = self.hd_video()
        return result
    
    
    def main_video_track(self):
        result = None
        if self.info['track']:
            for t in self.info['track']:
                if t['type'] == 'video':
                    if not result or t['bit rate'] > result['bit rate']:
                        result = t
        return result
    
    
    def video_width(self):
        result = 0
        v = self.main_video_track()
        if v: result = v['width']
        return result
    
    
    def hd_video(self):
        return self.video_width() > repository_config['Default']['hd video min width']
    
    
    def playback_height(self):
        result = 0
        v = self.main_video_track()
        if v:
            if v['display aspect ratio'] >= repository_config['Default']['display aspect ratio']:
                result = v['width'] / v['display aspect ratio']
            else:
                result = v['height']
            
        return result
    
    
    def audio_tracks(self):
        return [ t for t in self.info['track'] if 'type' in t and t['type'] == 'audio']
    
    
    def extract(self, options):
        result = Container.extract(self, options)
        if self.info['menu']:
            info = theFileUtil.copy_path_info(self.path_info, options)
            info['kind'] = 'txt'
            if theFileUtil.complete_info_default_values(info):
                dest_path = theFileUtil.canonic_path(info, self.meta)
                if theFileUtil.varify_if_path_available(dest_path, options.overwrite):
                    c = Chapter(dest_path, False)
                    c.start()
                    for marker in self.info['menu']:
                        c.add_chapter_marker(marker['time'], marker['name'])
                        
                    self.logger.info(u'Extracting chapter markers from %s --> %s', self.file_path, dest_path)
                    c.write(dest_path)
                    if theFileUtil.clean_if_not_exist(dest_path):
                        result.append(dest_path)
        return result
    
    
    def pack(self, options):
        Container.pack(self, options)
        info = theFileUtil.copy_path_info(self.path_info, options)
        if options.pack in ('mkv'):
            info['kind'] = 'mkv'
            if theFileUtil.complete_info_default_values(info):
                dest_path = theFileUtil.canonic_path(info, self.meta)
                if dest_path is not None:
                    pc = repository_config['Kind'][info['kind']]['Profile'][info['profile']]
                    selected = { 'related':{}, 'track':{} }
                    
                    if 'pack' in pc:
                        # locate related files that need to be muxed in
                        if 'related' in pc['pack']:
                            for (path,info) in self.related.iteritems():
                                for c in pc['pack']['related']:
                                    if all((k in info and info[k] == v) for k,v in c.iteritems()):
                                        if info['kind'] not in selected['related']:
                                            selected['related'][info['kind']] = []
                                        selected['related'][info['kind']].append(path)
                                        break
                        #locate related tracks that need to be muxed in
                        if 'tracks' in pc['pack']:
                            for t in self.info['track']:
                                for c in pc['pack']['tracks']:
                                    if all((k in t and t[k] == v) for k,v in c.iteritems()):
                                        if t['type'] not in selected['track']:
                                            selected['track'][t['type']] = []
                                        selected['track'][t['type']].append(t)
                                        break
                                        
                    self.logger.debug(selected)
                    
                    if theFileUtil.varify_if_path_available(dest_path, options.overwrite):
                        command = theFileUtil.initialize_command('mkvmerge', self.logger)
                        command.extend([u'--output', dest_path, u'--no-global-tags', u'--no-track-tags', u'--no-chapters', u'--no-attachments', u'--no-subtitles'])
                        
                        if 'name' in self.meta and self.meta['name']:
                            command.append(u'--title')
                            command.append(self.meta['name'])
                            
                        for t in selected['track']['video']:
                            if 'name' in t:
                                command.append(u'--track-name')
                                command.append(u'{0}:{1}'.format(t['id'], t['name']))
                            if 'language' in t:
                                command.append(u'--language')
                                command.append(u'{0}:{1}'.format(t['id'], t['language']))
                                
                        for t in selected['track']['audio']:
                            if 'channels' in t:
                                if t['channels'] < 2: tname = 'Mono'
                                elif t['channels'] > 2: tname = 'Surround'
                                else: tname = 'Stereo'
                                command.append(u'--track-name')
                                command.append(u'{0}:{1}'.format(t['id'], tname))
                            if 'language' in t:
                                command.append(u'--language')
                                command.append(u'{0}:{1}'.format(t['id'], t['language']))
                                
                        command.append(u'--audio-tracks')
                        command.append(u','.join([ unicode(k['id']) for k in selected['track']['audio'] ]))
                        command.append(u'--video-tracks')
                        command.append(u','.join([ unicode(k['id']) for k in selected['track']['video'] ]))
                        command.append(self.file_path)
                        
                        if 'ac3' in selected['related']:
                            for r in selected['related']['ac3']:
                                # try to locate the DTS sound track from which the AC-3 track was transcoded
                                # if a match is found duplicate the delay
                                # checking exact duration ir sample cound migth be more accurate
                                lookup = {'codec':'DTS', 'language':self.related[r]['language']}
                                for t in self.info['track']:
                                    if all((k in t and t[k] == v) for k,v in lookup.iteritems()):
                                        if 'delay' in t and t['delay'] != 0:
                                            self.logger.debug(u'Found a matching DTS track with non trivial delay of %d', t['delay'])
                                            command.append(u'--sync')
                                            command.append(u'0:{0}'.format(t['delay']))
                                            break
                                            
                                command.append(u'--language')
                                command.append(u'0:{0}'.format(self.related[r]['language']))
                                command.append(r)
                        
                        if 'srt' in selected['related']:
                            for r in selected['related']['srt']:
                                i = self.related[r]
                                command.append(u'--sub-charset')
                                command.append(u'0:UTF-8')
                                command.append(u'--language')
                                command.append(u'0:{0}'.format(i['language']))
                                command.append(r)
                        
                        if 'txt' in selected['related']:
                            for r in selected['related']['txt']:
                                i = self.related[r]
                                command.append(u'--chapter-language')
                                command.append(u'eng')
                                command.append(u'--chapter-charset')
                                command.append(u'UTF-8')
                                command.append(u'--chapters')
                                command.append(r)
                                
                        message = u'Pack {0} --> {1}'.format(self.file_path, dest_path)
                        theFileUtil.execute(command, message, options.debug, pipeout=False, pipeerr=False, logger=self.logger)
                        theFileUtil.clean_if_not_exist(dest_path)
    
    
    def transcode(self, options):
        Container.transcode(self, options)
        info = theFileUtil.copy_path_info(self.path_info, options)
        if options.transcode in ('mkv', 'm4v'):
            info['kind'] = options.transcode
            if theFileUtil.complete_info_default_values(info):
                dest_path = theFileUtil.canonic_path(info, self.meta)
                if dest_path is not None:
                    command = None
                    if theFileUtil.varify_if_path_available(dest_path, options.overwrite):
                        command = theFileUtil.initialize_command('handbrake', self.logger)
                        tc = repository_config['Kind'][info['kind']]['Profile'][info['profile']]['transcode']
                        
                        if 'flags' in tc:
                            for v in tc['flags']:
                                command.append(v)
                                
                        if 'options' in tc:
                            hb_config = copy.deepcopy(tc['options'])
                            if options.pixel_width: hb_config['--maxWidth'] = options.pixel_width
                            if options.quality: hb_config['--quality'] = options.quality
                            
                            for (k,v) in hb_config.iteritems():
                                command.append(k)
                                command.append(unicode(v))
                                
                        found_audio = False
                        audio_options = {'--audio':[]}
                        for s in tc['audio']:
                            for idx, t in enumerate(self.audio_tracks()):
                                for c in s:
                                    if all((k in t and t[k] == v) for k,v in c['from'].iteritems()):
                                        found_audio = True
                                        audio_options['--audio'].append(unicode(idx + 1))
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
                        command.extend([u'--input', self.file_path, u'--output', dest_path])
                        message = u'Transcode {0} --> {1}'.format(self.file_path, dest_path)
                        theFileUtil.execute(command, message, options.debug, pipeout=False, pipeerr=False, logger=self.logger)
                        theFileUtil.clean_if_not_exist(dest_path)
        return
    
    
    def __unicode__(self):
        return Container.__unicode__(self)
    
    


# Matroska Class
class Avi(AudioVideoContainer):
    def __init__(self, file_path, autoload=True):
        AudioVideoContainer.__init__(self, file_path, autoload)
        self.logger = logging.getLogger('mp4pack.avi')
        if autoload:
            self.load()
    


# Matroska Class
class Matroska(AudioVideoContainer):
    def __init__(self, file_path, autoload=True):
        AudioVideoContainer.__init__(self, file_path, autoload)
        self.logger = logging.getLogger('mp4pack.matroska')
        if autoload:
            self.load()
    
    
    def extract(self, options):
        result = AudioVideoContainer.extract(self, options)
        if options.profile is None or theFileUtil.profile_valid_for_kind(options.profile, 'srt'):
            selected = {
                'track':[], 
                'path':{ 'text':[], 'audio':[] },
                'extract':{ 'text':[], 'audio':[] }
            }
            info = theFileUtil.copy_path_info(self.path_info, options)
            if 'volume' in info: del info['volume']
            info['profile'] = 'dump'
            for k in ('srt', 'ass', 'dts'):
                if 'volume' in info: del info['volume']
                info['kind'] = k
                if theFileUtil.complete_info_default_values(info):
                    pc = repository_config['Kind'][info['kind']]['Profile'][info['profile']]
                    if 'extract' in pc and 'tracks' in pc['extract']:
                        for t in self.info['track']:
                            for c in pc['extract']['tracks']:
                                if all((k in t and t[k] == v) for k,v in c.iteritems()):
                                    t['kind'] = k
                                    selected['track'].append(t)
                                    break
                                    
            if selected['track']:
                command = theFileUtil.initialize_command('mkvextract', self.logger)
                command.extend([u'tracks', self.file_path ])
                for t in selected['track']:
                    if 'volume' in info: del info['volume']
                    info['kind'] = t['kind']
                    info['language'] = t['language']
                    if theFileUtil.complete_info_default_values(info):
                        dest_path = theFileUtil.canonic_path(info, self.meta)
                        if theFileUtil.varify_if_path_available(dest_path, options.overwrite):
                            command.append(u'{0}:{1}'.format(unicode(t['id']), dest_path))
                            selected['path'][t['type']].append(dest_path)
                                
            if selected['path']['text'] or selected['path']['audio']:
                message = u'Extract {0} subtitle and {1} audio tracks from {2}'.format(
                    unicode(len(selected['path']['text'])), 
                    unicode(len(selected['path']['audio'])), 
                    self.file_path
                )
                theFileUtil.execute(command, message, options.debug, pipeout=False, pipeerr=False, logger=self.logger)
                
            for k in selected['path']:
                for p in selected['path'][k]:
                    if theFileUtil.clean_if_not_exist(p):
                        selected['extract'][k].append(p)
            
            if selected['extract']['text']:
                o = copy.deepcopy(options)
                o.transcode = 'srt'
                o.extract = None
                for p in selected['extract']['text']:
                    s = Subtitle(p)
                    s.transcode(o)
                    result.append(p)
            
            if selected['extract']['audio']:
                o = copy.deepcopy(options)
                o.transcode = 'ac3'
                o.extract = None
                o.profile = None
                for p in selected['extract']['audio']:
                    a = RawAudio(p)
                    a.transcode(o)
                    result.append(p)
        else:
            self.logger.warning('Skipping subtitle extraction. Profile %s invalid for srt kind.', options.profile)
        return result
    
    


# Mpeg4 Class
class Mpeg4(AudioVideoContainer):
    def __init__(self, file_path, autoload=True):
        AudioVideoContainer.__init__(self, file_path, autoload)
        self.logger = logging.getLogger('mp4pack.mp4')
        if autoload:
            self.load()
    
    
    def tag(self, options):
        AudioVideoContainer.tag(self, options)
        tc = None
        update = {}
        if self.meta:
            for k in [ 
                k for k,v in self.meta.iteritems()
                if theFileUtil.property_map['name']['tag'][k]['subler'] 
                and (k not in self.info['tag'] or self.info['tag'][k] != v)
            ]: update[k] = self.meta[k]
                    
        elif self.path_info:
            if self.is_movie():
                if 'name' in self.path_info and self.path_info['name'] != self.info['tag']['name']:
                    update['name'] = self.path_info['name']
                
            elif self.is_tvshow():
                if not('tv season' in self.info['tag'] and self.path_info['tv season'] == self.info['tag']['tv season']):
                    update['tv season'] = self.path_info['tv season']
                if not('tv episode #' in self.info['tag'] and self.path_info['tv episode #'] == self.info['tag']['tv episode #']):
                    update['tv episode #'] = self.path_info['tv episode #']
                if 'name' in self.path_info and not('name' in self.info['tag'] and self.path_info['name'] == self.info['tag']['name']):
                    update['name'] = self.path_info['name']
        if update:
            tc = u''.join([theFileUtil.format_key_value_for_subler(t, update[t]) for t in sorted(set(update))])
            message = u'Update tags: {0} --> {1}'.format(u', '.join([theFileUtil.property_map['name']['tag'][t]['print'] for t in sorted(set(update.keys()))]), self.file_path)
            command = theFileUtil.initialize_command('subler', self.logger)
            command.extend([u'-i', self.file_path, u'-t', tc])
            theFileUtil.execute(command, message, options.debug, pipeout=True, pipeerr=False, logger=self.logger)
        else:
            self.logger.info(u'No tags need update in %s', self.file_path)
    
    
    def optimize(self, options):
        AudioVideoContainer.optimize(self, options)
        message = u'Optimize {0}'.format(self.file_path)
        command = theFileUtil.initialize_command('mp4file', self.logger)
        command.extend([u'--optimize', self.file_path])
        theFileUtil.execute(command, message, options.debug, pipeout=True, pipeerr=False, logger=self.logger)
    
    
    
    def _update_jpg(self, options):
        AudioVideoContainer.tag(self, options)
        if options.update == 'jpg':
            info = theFileUtil.copy_path_info(self.path_info, options)
            info['kind'] = 'jpg'
            selected = []
            if theFileUtil.complete_info_default_values(info):
                if info['profile'] == 'normal':
                    if self.download_artwork(options):
                        self.logger.debug(u'Reloading related artwork for %s', self.file_path)
                        self.load_related()
                lookup = {'kind':info['kind'], 'profile':info['profile']}
                for (path,info) in self.related.iteritems():
                    if all((k in info and info[k] == v) for k,v in lookup.iteritems()):
                        selected.append(path)
                        break
                
            if selected:
                message = u'Update artwork {0} --> {1}'.format(selected[0], self.file_path)
                command = theFileUtil.initialize_command('subler', self.logger)
                command.extend([u'-i', self.file_path, u'-t', u'{{{0}:{1}}}'.format(u'Artwork', selected[0])])
                theFileUtil.execute(command, message, options.debug, pipeout=True, pipeerr=False, logger=self.logger)
            else:
                self.logger.warning(u'No artwork available for %s', self.file_path)
    
    
    def _update_srt(self, options):
        if options.update == 'srt':
            info = theFileUtil.copy_path_info(self.path_info, options)
            info['kind'] = 'srt'
            if theFileUtil.complete_info_default_values(info):
                pc = repository_config['Kind']['srt']['Profile'][info['profile']]
                
                if 'profile' in info and 'update' in pc:
                    message = u'Drop existing subtitle tracks in {0}'.format(self.file_path)
                    command = theFileUtil.initialize_command('subler', self.logger)
                    command.extend([u'-i', self.file_path, u'-r'])
                    theFileUtil.execute(command, message, options.debug, pipeout=True, pipeerr=False, logger=self.logger)
                    
                    selected = {}
                    for (p,i) in self.related.iteritems():
                        for c in pc['update']['related']:
                            if all((k in i and i[k] == v) for k,v in c['from'].iteritems()):
                                selected[p] = i
                                break
                            
                    for (p,i) in selected.iteritems():
                        for c in pc['update']['related']:
                            if all((k in i and i[k] == v) for k,v in c['from'].iteritems()):
                                message = u'Update subtitles {0} --> {1}'.format(p, self.file_path)
                                command = theFileUtil.initialize_command('subler', self.logger)
                                command.extend([
                                    u'-i', self.file_path,
                                    u'-s', p, 
                                    u'-l', theFileUtil.property_map['iso3t']['language'][i['language']]['print'],
                                    u'-n', c['to']['Name'], 
                                    u'-a', unicode(int(round(self.playback_height() * c['to']['height'])))
                                ])
                                theFileUtil.execute(command, message, options.debug, pipeout=True, pipeerr=False, logger=self.logger)
                                
                    if 'smart' in pc['update']:
                        smart_section = pc['update']['smart']
                        found = False
                        for code in smart_section['order']:
                            for (p,i) in selected.iteritems():
                                if i['language'] == code:
                                    message = u'Update smart {0} subtitles {1} --> {2}'.format(theFileUtil.property_map['iso3t']['language'][code]['print'], p, self.file_path)
                                    command = theFileUtil.initialize_command('subler', self.logger)
                                    command.extend([
                                        u'-i', self.file_path, 
                                        u'-s', p, 
                                        u'-l', theFileUtil.property_map['iso3t']['language'][smart_section['language']]['print'],
                                        u'-n', smart_section['Name'], 
                                        u'-a', unicode(int(round(self.playback_height() * smart_section['height'])))
                                    ])
                                    theFileUtil.execute(command, message, options.debug, pipeout=True, pipeerr=False, logger=self.logger)
                                    found = True
                                    break
                            if found: break
    
    
    def _update_txt(self, options):
        AudioVideoContainer.tag(self, options)
        if options.update == 'txt':
            info = theFileUtil.copy_path_info(self.path_info, options)
            info['kind'] = 'txt'
            selected = []
            if theFileUtil.complete_info_default_values(info):
                lookup = {'kind':info['kind'], 'profile':info['profile']}
                for (path,info) in self.related.iteritems():
                    if all((k in info and info[k] == v) for k,v in lookup.iteritems()):
                        selected.append(path)
                        break
                
            if selected:
                message = u'Update chapters {0} --> {1}'.format(selected[0], self.file_path)
                command = theFileUtil.initialize_command('subler', self.logger)
                command.extend([u'-i', self.file_path, u'-c', selected[0], '-p'])
                theFileUtil.execute(command, message, options.debug, pipeout=True, pipeerr=False, logger=self.logger)
            else:
                self.logger.warning(u'No chapters available for %s', self.file_path)
    
    
    def update(self, options):
        AudioVideoContainer.update(self, options)
        self._update_srt(options)
        self._update_txt(options)
        self._update_jpg(options)
    
    


# Raw Audio Class
class RawAudio(AudioVideoContainer):
    def __init__(self, file_path, autoload=True):
        AudioVideoContainer.__init__(self, file_path, autoload)
        self.logger = logging.getLogger('mp4pack.rawaudio')
        if autoload:
            self.load()
    
    
    def transcode(self, options):
        if options.transcode == 'ac3':
            info = theFileUtil.copy_path_info(self.path_info, options)
            info['kind'] = options.transcode
            info['language'] = self.path_info['language']
            if theFileUtil.complete_info_default_values(info):
                dest_path = theFileUtil.canonic_path(info, self.meta)
                if theFileUtil.varify_if_path_available(dest_path, options.overwrite):
                    if self.path_info['kind'] == 'dts':
                        tp = repository_config['Kind'][info['kind']]['Profile'][info['profile']]['transcode']
                        
                        dcadec_command = theFileUtil.initialize_command('dcadec', self.logger)
                        for (k,v) in tp['dcadec'].iteritems():
                            dcadec_command.append(k)
                            dcadec_command.append(v)
                        dcadec_command.append(self.file_path)
                        
                        aften_command = theFileUtil.initialize_command('aften', self.logger)
                        aften_command.append('-')
                        for (k,v) in tp['aften'].iteritems():
                            aften_command.append(k)
                            aften_command.append(v)
                        aften_command.append(dest_path)
                        
                        self.logger.info(u'Transcode %s --> %s',self.file_path, dest_path)
                        from subprocess import Popen, PIPE
                        dcadec_proc = Popen(dcadec_command, stdout=PIPE)
                        aften_proc = Popen(aften_command, stdin=dcadec_proc.stdout, stdout=PIPE)
                        report = aften_proc.communicate()
                        
                        theFileUtil.clean_if_not_exist(dest_path)
    
    


# Text File
class Text(Container):
    def __init__(self, file_path, autoload=True):
        Container.__init__(self, file_path, autoload)
        self.logger = logging.getLogger('mp4pack.text')
    
    
    def read(self):
        lines = None
        content = None
        if os.path.exists(self.file_path):
            try:
                reader = open(self.file_path, 'r')
                content = reader.read()
                reader.close()
            except IOError as error:
                self.logger.error(str(error))
                content = None
        
        if content:
            encoding = chardet.detect(content)
            self.info['file']['encoding'] = encoding['encoding']
            self.logger.debug(u'%s encoding detected for %s', encoding['encoding'], self.file_path)
            content = unicode(content, encoding['encoding'], errors='ignore')
            lines = content.splitlines()
        return lines
    
    
    def decode(self):
        return True
    
    
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
        info = theFileUtil.copy_path_info(self.path_info, options)
        info['kind'] = options.transcode
        if theFileUtil.complete_info_default_values(info):
            dest_path = theFileUtil.canonic_path(info, self.meta)
            if theFileUtil.varify_if_path_available(dest_path, options.overwrite):
                self.logger.info(u'Transcode %s --> %s', self.file_path, dest_path)
                self.write(dest_path)
                theFileUtil.clean_if_not_exist(dest_path)
    
    


# Subtitle Class
class Subtitle(Text):
    def __init__(self, file_path, autoload=True):
        Text.__init__(self, file_path, autoload)
        self.logger = logging.getLogger('mp4pack.subtitle')
        self.subtitle_blocks = None
        self.statistics = None
        if autoload:
            self.load()
    
    
    def valid(self):
        return Text.valid(self) and self.subtitle_blocks is not None
    
    
    def load(self):
        result = Text.load(self)
        if result:
            self.subtitle_blocks = []
            self.statistics = {}
            result = Subtitle.decode(self)
        else:
            self.logger.warning('Could not parse text file %s', self.file_path)
        if not result:
            self.logger.warning('Could not parse subtitle file %s', self.file_path)
            Subtitle.unload(self)
        return result
    
    
    def unload(self):
        Text.unload(self)
        self.subtitle_blocks = None
        self.statistics = None
    
    
    
    def calculate_statistics(self):
        self.statistics = {'Blocks':0, 'Lines':0, 'Sentences':0, 'Words':0, 'Characters':0}
        self.statistics['Blocks'] = len(self.subtitle_blocks)
        
        for block in self.subtitle_blocks:
            block.calculate_statistics()
            for (k,v) in block.statistics.iteritems():
                self.statistics[k] += block.statistics[k]
    
    
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
                    
                match = Subtitle.srt_time_line.search(lines[index])
                if match is not None and lines[index - 1].strip().isdigit():
                    next_block = SubtitleBlock()
                    next_block.set_begin_miliseconds(theFileUtil.timecode_to_miliseconds(match.group(1)))
                    next_block.set_end_miliseconds(theFileUtil.timecode_to_miliseconds(match.group(2)))
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
                    match = Subtitle.ass_formation_line.search(lines[index + 1])
                    if match is not None:
                        formation = match.group(1).strip().replace(' ','').split(',')
                    break
                index += 1
                
            if formation is not None:
                start = formation.index('Start')
                stop = formation.index('End')
                text = formation.index('Text')
                for line in lines:
                    match = Subtitle.ass_subline.search(line)
                    if match is not None:
                        line = match.group(1).strip().split(',')
                        block = SubtitleBlock()
                        block.set_begin_miliseconds(theFileUtil.timecode_to_miliseconds(line[start]))
                        block.set_end_miliseconds(theFileUtil.timecode_to_miliseconds(line[stop]))
                        
                        subtitle_text = ','.join(line[text:])
                        subtitle_text = Subtitle.ass_event_command_re.sub('', subtitle_text)
                        subtitle_text = subtitle_text.replace('\n', '\N')
                        subtitle_text = Subtitle.ass_condense_line_breaks.sub('\N', subtitle_text)
                        subtitle_text = subtitle_text.split('\N')
                        for line in subtitle_text:
                            block.add_line(line)
                            
                        if block.valid():
                            self.subtitle_blocks.append(block)
        
        
        def decode_sub(lines, frame_rate):
            frame_rate = theFileUtil.frame_rate_to_float(frame_rate)
            for line in lines:
                if Subtitle.sub_line_begin.search(line):
                    line = line.split('}',2)
                    subtitle_text = line[2].strip().replace('|', '\N')
                    block = SubtitleBlock()
                    block.set_begin_miliseconds(theFileUtil.frame_to_miliseconds(line[0].strip('{'), frame_rate))
                    block.set_end_miliseconds(theFileUtil.frame_to_miliseconds(line[1].strip('{'), frame_rate))
                    for line in subtitle_text:
                        block.add_line(line)
                        
                    if block.valid():
                        self.subtitle_blocks.append(block)
        
        
        result = Text.decode(self)
        if result:
            lines = self.read()
            if lines:
                self.subtitle_blocks = []
                self.statistics = []
                if self.path_info['kind'] == 'srt':
                    decode_srt(lines)
                elif self.path_info['kind'] in ('ass', 'ssa'):
                    decode_ass(lines)
                #elif self.path_info['kind'] == 'sub':
                #    decode_sub(lines, 25)
            
            if not self.subtitle_blocks:
                result = False
        return result
    
    
    def encode(self):
        result = Text.encode(self)
        if self.subtitle_blocks:
            result = [u'\n']
            for idx, block in enumerate(self.subtitle_blocks):
                block.encode(result, idx + 1)
        return result
    
    
    def transcode(self, options):
        self.decode()
        info = theFileUtil.copy_path_info(self.path_info, options)
        info['kind'] = options.transcode
        if theFileUtil.complete_info_default_values(info):
            dest_path = theFileUtil.canonic_path(info, self.meta)
            if theFileUtil.varify_if_path_available(dest_path, options.overwrite):
                p = repository_config['Kind'][info['kind']]['Profile'][info['profile']]
                if 'transcode' in p and 'filter' in p['transcode']:
                    self.filter(p['transcode']['filter'])
                
                if options.time_shift is not None:
                    self.shift(options.time_shift)
                
                if options.input_rate is not None and options.output_rate is not None:
                    input_frame_rate = theFileUtil.frame_rate_to_float(options.input_rate)
                    output_frame_rate = theFileUtil.frame_rate_to_float(options.output_rate)
                    if input_frame_rate is not None and output_frame_rate is not None:
                        factor = input_frame_rate / output_frame_rate
                        self.scale_rate(factor)
                
                self.logger.info(u'Transcode %s --> %s', self.file_path, dest_path)
                self.write(dest_path)
                theFileUtil.clean_if_not_exist(dest_path)    
    
    
    def filter(self, sequence_list):
        if sequence_list:
            self.logger.debug(u'Filtering %s by %s', self.file_path, unicode(sequence_list))
            self.subtitle_blocks = theSubtitleFilter.filter(self.subtitle_blocks, sequence_list)
    
    
    def shift(self, offset):
        self.logger.debug(u'Shifting time codes on %s by %s', self.file_path, unicode(offset))
        for block in self.subtitle_blocks:
            block.shift(offset)
    
    
    def scale_rate(self, factor):
        self.logger.debug(u'Scaling time codes on %s by %s', self.file_path, unicode(factor))
        for block in self.subtitle_blocks:
            block.scale_rate(factor)
    
    
    def print_subtitle_statistics(self):
        self.calculate_statistics()
        return (u'\n'.join([theFileUtil.format_key_value(key, self.statistics[key]) for key in sorted(set(self.statistics))]))
    
    
    def __unicode__(self):
        result = Text.__unicode__(self)
        if self.subtitle_blocks:
            result = u'\n'.join((result, theFileUtil.format_info_subtitle(u'subtitle statistics'), self.print_subtitle_statistics()))
        return result
    
    
    srt_time_line = re.compile('^([0-9]{2}:[0-9]{2}:[0-9]{2},[0-9]{3}) --> ([0-9]{2}:[0-9]{2}:[0-9]{2},[0-9]{3})$')
    ass_subline = re.compile('^Dialogue\s*:\s*(.*)$')
    ass_formation_line = re.compile('^Format\s*:\s*(.*)$')
    ass_condense_line_breaks = re.compile(r'(\\N)+')
    ass_event_command_re = re.compile(r'\{\\[^\}]+\}')
    sub_line_begin = re.compile('^{(\d+)}{(\d+)}')


class SubtitleBlock(object):
    def __init__(self):
        self.begin = None
        self.end = None
        self.lines = []
        self.statistics = None
    
    
    def calculate_statistics(self):
        self.statistics = {'Lines':len(self.lines), 'Sentences':0, 'Words':0, 'Characters':0}
        all_lines = u'\n'.join(self.lines)
        self.statistics['Words'] = len([w for w in FileUtil.whitespace_re.split(all_lines) if w])
        self.statistics['Sentences'] = len([s for s in FileUtil.sentence_end.split(all_lines) if s])
        self.statistics['Characters'] = len(all_lines)
    
    
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
        begin_time = theFileUtil.miliseconds_to_time(self.begin, ',')
        end_time = theFileUtil.miliseconds_to_time(self.end, ',')
        line_buffer.append(u'{0} --> {1}'.format(unicode(begin_time), unicode(end_time)))
        for line in self.lines:
            line_buffer.append(line)
        line_buffer.append(u'\n')
    




# Chapter Class
class Chapter(Text):
    def __init__(self, file_path, autoload=True):
        Text.__init__(self, file_path, autoload)
        self.logger = logging.getLogger('mp4pack.chapter')
        self.chapter_markers = None
        if autoload:
            self.load()
    
    
    def valid(self):
        return Text.valid(self) and self.chapter_markers
    
    
    def load(self):
        result = Text.load(self)
        if result:
            self.chapter_markers = []
            result = Chapter.decode(self)
        if not result:
            self.logger.warning('Could not parse chapter file %s', self.file_path)
            Chapter.unload(self)
        return result
    
    
    def unload(self):
        Text.unload(self)
        self.chapter_markers = None
    
    
    def start(self):
        self.chapter_markers = []
    
    
    def decode(self):
        result = Text.decode(self)
        if result:
            lines = self.read()
            if lines:
                self.chapter_markers = []
                for index in range(len(lines) - 1):
                    match_timecode = Chapter.ogg_chapter_timestamp_re.search(lines[index])
                    if match_timecode is not None:
                        match_name = Chapter.ogg_chapter_name_re.search(lines[index + 1])
                        if match_name is not None:
                            time = match_timecode.group(2)
                            name = match_name.group(2)
                            if time and name:
                                time = theFileUtil.timecode_to_miliseconds(time)
                                name = name.strip('"').strip("'").strip()
                                self.add_chapter_marker(time, name)
            if not self.chapter_markers:
                result = False
        return result
    
    
    def encode(self):
        result = Text.encode(self)
        self.decode()
        if self.chapter_markers:
            result = []
            for idx, m in enumerate(self.chapter_markers):
                m.encode(result, idx + 1)
        return result
    
    
    def add_chapter_marker(self, time, name):
        if time and name:
            self.chapter_markers.append(ChapterMarker(time, name))
    
    
    def print_chapter_markers(self):
        return (u'\n'.join([theFileUtil.format_value(chapter_marker) for chapter_marker in self.chapter_markers]))
    
    
    def __unicode__(self):
        result = Text.__unicode__(self)
        if len(self.chapter_markers) > 0:
            result = u'\n'.join((result, theFileUtil.format_info_subtitle(u'chapter markers'), self.print_chapter_markers()))
        return result
    
    
    ogg_chapter_timestamp_re = re.compile('CHAPTER([0-9]{,2})=([0-9]{,2}:[0-9]{,2}:[0-9]{,2}\.[0-9]+)')
    ogg_chapter_name_re = re.compile('CHAPTER([0-9]{,2})NAME=(.*)', re.UNICODE)


class ChapterMarker(object):
    def __init__(self, time=None, name=None):
        self.time = time
        self.name = name
    
    
    def encode(self, line_buffer, index):
        line_buffer.append(u'CHAPTER{0}={1}'.format(str(index).zfill(2), unicode(theFileUtil.miliseconds_to_time(self.time, '.'), 'utf-8')))
        line_buffer.append(u'CHAPTER{0}NAME={1}'.format(str(index).zfill(2), self.name))
    
    
    def __unicode__(self):
        return u'{0} : {1}'.format(theFileUtil.miliseconds_to_time(self.time), self.name)
    




# Artwork Class
class Artwork(Container):
    def __init__(self, file_path, autoload=True):
        Container.__init__(self, file_path, autoload)
        self.logger = logging.getLogger('mp4pack.image')
        if autoload:
            self.load()
    
    
    def transcode(self, options):
        info = theFileUtil.copy_path_info(self.path_info, options)
        info['kind'] = options.transcode
        if theFileUtil.complete_info_default_values(info):
            dest_path = theFileUtil.canonic_path(info, self.meta)
            if theFileUtil.varify_if_path_available(dest_path, options.overwrite):
                p = repository_config['Kind'][info['kind']]['Profile'][info['profile']]
                if 'transcode' in p:
                    if 'size' in p['transcode']:
                        from PIL import Image
                        image = Image.open(self.file_path)
                        size = image.size
                        resize = True
                        factor = 1.0
                        if 'constraint' in p['transcode'] and p['transcode']['constraint'] == 'max':
                            max_side = max(size)
                            if max_side > p['transcode']['size']:
                                factor = float(p['transcode']['size']) / float(max_side)
                            else:
                                resize = False
                                self.logger.debug(u'Not resizing. Artwork is %dx%d and profile max dimension is %d', size[0], size[1], p['transcode']['size'])
                        else:
                            min_side = min(size)
                            if min_side > p['transcode']['size']:
                                factor = float(p['transcode']['size']) / float(min_side)
                            else:
                                resize = False
                                self.logger.debug(u'Not resizing. Artwork is %dx%d and profile min dimension is %d', size[0], size[1], p['transcode']['size'])
                        
                        rsize = (int(round(size[0] * factor)), int(round(size[1] * factor)))
                        if size == rsize:
                            self.copy(options)
                        else:
                            self.logger.debug(u'Resize artwork: %dx%d --> %dx%d', size[0], size[1], rsize[0], rsize[1])
                            image = image.resize(rsize, Image.ANTIALIAS)
                            self.logger.info(u'Transcode %s --> %s', self.file_path, dest_path)
                            image.save(dest_path)
    




# Subtitle Filter Class (Singleton)
class SubtitleFilter(object):
    def __init__(self):
        self.logger = logging.getLogger('mp4pack.filter.manager')
        self.sequence = {}
    
    
    def find_filter_sequence(self, name):
        result = None
        
        from config import subtitle_config
        if name in self.sequence:
            result = self.sequence[name]
        elif name in subtitle_config:
            config = subtitle_config[name]
            self.logger.info(u'Loading %s filter sequence', name)
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
        FilterSequence.__init__(self, config)
        self.logger = logging.getLogger('mp4pack.filter.drop')
        self.expression = []
    
    
    def load(self):
        o = re.UNICODE
        if 'case' in self.config and self.config['case'] == 'insensitive':
            o = o|re.IGNORECASE
        for e in self.config['expression']:
            try:
                exp = re.compile(e,o)
            except:
                self.logger.warning('Failed to load filter %s', e)
                exp = None
            
            if exp:
                self.expression.append(exp)
    
    
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
                            self.logger.debug(u'Drop %s', line)
                            keep = False
                            break
                    if keep:
                        block.add_line(line)
                        
            elif self.config['scope'] == 'block':
                keep = True
                for line in block.lines:
                    for e in self.expression:
                        if e.search(line) is not None:
                            self.logger.debug(u'Drop %s', line)
                            keep = False
                            break
                    if not keep:
                        block.clear()
                        break
                        
            result = block.valid()
        return result
    


class ReplaceFilterSequence(FilterSequence):
    def __init__(self, config):
        FilterSequence.__init__(self, config)
        self.logger = logging.getLogger('mp4pack.filter.replace')
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
                        filtered_line = e[0].sub(e[1], line)
                        block.add_line(filtered_line)
                        if line != filtered_line:
                            self.logger.debug(u'Replaced "%s" --> "%s"', line, filtered_line)
                    if not block.valid(): break
                        
            elif self.config['scope'] == 'block':
                all_lines = u'\n'.join(block.lines)
                block.clear()
                for e in self.expression:
                    filtered_lines = e[0].sub(e[1], all_lines).strip()
                    if all_lines != filtered_lines:
                        self.logger.debug(u'Replaced "%s" --> "%s"', all_lines, filtered_lines)
                    if not filtered_lines: 
                        break
                if filtered_lines:
                    for line in all_lines.split(u'\n'):
                        block.add_line(line)
                    
            result = block.valid()
        return result
    




# File Utility Class (Singletone)
class FileUtil(object):
    def __init__(self):
        self.logger = logging.getLogger('mp4pack.util')
        
        # Container / Kind map
        kc = repository_config['Kind']
        self.container = {}
        for c in tuple(set([ v['container'] for k,v in repository_config['Kind'].iteritems() ])):
            self.container[c] = {'kind':[ k for (k,v) in repository_config['Kind'].iteritems() if v['container'] == c ]}
        
        self.stream_type_with_language = ('audio', 'subtitles', 'video')
        self.kind_with_language = self.container['subtitles']['kind'] + self.container['raw audio']['kind']
        
        self.property_map = {}
        for key in ('name', 'mediainfo', 'mp4info'):
            if key not in self.property_map:
                self.property_map[key] = {}
            for block in ('file', 'tag'):
                if block not in self.property_map[key]:
                    self.property_map[key][block] = {}
                for p in media_property[block]:
                    if key in p and p[key] is not None:
                        self.property_map[key][block][p[key]] = p
            
            self.property_map[key]['track'] = {}
            for block in ('audio', 'video', 'text', 'image'):
                if block not in self.property_map[key]['track']:
                    self.property_map[key]['track'][block] = {}
                for p in media_property['track']['common']:
                    if key in p and p[key] is not None:
                        self.property_map[key]['track'][block][p[key]] = p
                    
                for p in media_property['track'][block]:
                    if key in p and p[key] is not None:
                        self.property_map[key]['track'][block][p[key]] = p
        
        for key in ('name', 'plist'):
            if key not in self.property_map:
                self.property_map[key] = {}
            self.property_map[key]['itunemovi'] = {}
            for p in media_property['itunemovi']:
                self.property_map[key]['itunemovi'][p[key]] = p
        
        for key in ('name', 'code'):
            if key not in self.property_map:
                self.property_map[key] = {}
            for block in ('stik', 'sfID', 'rtng', 'akID', 'gnre'):
                if block not in self.property_map[key]:
                    self.property_map[key][block] = {}
                for p in media_property[block]:
                    self.property_map[key][block][p[key]] = p
        
        for key in ('name', 'iso3t', 'iso3b', 'iso2'):
            if key not in self.property_map:
                self.property_map[key] = {}
            self.property_map[key]['language'] = {}
            for p in media_property['language']:
                if key in p:
                    self.property_map[key]['language'][p[key]] = p
    
    
    def convert_mediainfo_value(self, kind, value):
        result = value
        if kind == 'int' or kind == 'enum':
            result = int(value)
        elif kind == 'float':
            result = float(value)
        elif kind == 'date':
            match = self.full_utc_datetime.search(value)
            if match:
                tm = []
                for idx,p in enumerate(match.groups()):
                    if p is None:
                        if idx > 2: tm.append(0)
                        else: tm.append(1)
                    else: tm.append(int(p))
                result = datetime(tm[0], tm[1], tm[2], tm[3], tm[4], tm[5])
        elif kind == 'bool':
            if self.true_value.search(value) is not None:
                result = True
            else:
                result = False
        return result
    
    
    def load_mp4info(self, path, info):
        command = theFileUtil.initialize_command('mp4info', self.logger)
        command.append(path)
        proc = Popen(command, stdout=PIPE, stderr=PIPE)
        report = proc.communicate()
        mp4info_report = unicode(report[0], 'utf-8').splitlines()
        for line in mp4info_report:
            match = self.mp4info_tag.search(line)
            if match is not None:
                tag = match.groups()
                if tag[0] in self.property_map['mp4info']['tag']:
                    n = self.property_map['mp4info']['tag'][tag[0]]
                    info['tag'][n['name']] = tag[1]
    
    
    def load_info(self, path):
        info = None
        command = theFileUtil.initialize_command('mediainfo', self.logger)
        command.extend([u'--Language=raw', u'--Output=XML', u'-f', path])
        proc_mediainfo = Popen(command, stdout=PIPE, stderr=PIPE)
        proc_grep = Popen([u'grep', u'-v', u'Cover_Data'], stdin=proc_mediainfo.stdout, stdout=PIPE)
        report = proc_grep.communicate()
        element = ElementTree.fromstring(report[0])
        file_nodes = element.findall(u'File')
        if file_nodes:
            track_nodes = file_nodes[0].findall(u'track')
            if track_nodes:
                info = {'file':{}, 'tag':{}, 'track':[], 'menu':[]}
                for tn in track_nodes:
                    if 'type' in tn.attrib:
                        track_type = tn.attrib['type'].lower()
                        if track_type == 'general':
                            for t in tn:
                                if t.tag in self.property_map['mediainfo']['tag']:
                                    p = self.property_map['mediainfo']['tag'][t.tag]
                                    info['tag'][p['name']] = xml.sax.saxutils.unescape(t.text, {u'&quot;':u'"'})
                                elif t.tag in self.property_map['mediainfo']['file']:
                                    p = self.property_map['mediainfo']['file'][t.tag]
                                    info['file'][p['name']] = t.text
                        elif track_type in self.property_map['mediainfo']['track']:
                            track = {}
                            for t in tn:
                                if t.tag in self.property_map['mediainfo']['track'][track_type]:
                                    p = self.property_map['mediainfo']['track'][track_type][t.tag]
                                    value = self.convert_mediainfo_value(p['type'], t.text)
                                    track[p['name']] = value
                            if track:
                                track['type'] = track_type
                                # check to see if language is not set and set it to default
                                #if track['type'] in theFileUtil.stream_type_with_language:
                                #    if 'language' not in track or track['language'] == 'und':
                                #        track['language'] = repository_config['Options'].language
                                
                                info['track'].append(track)
                        elif track_type == 'menu':
                            for t in tn:
                                match = self.mediainfo_chapter_timecode.search(t.tag)
                                if match != None:
                                    c = {}
                                    tc = match.groups()
                                    c['time'] = (int(tc[0]) * 3600 + int(tc[1]) * 60 + int(tc[2])) * 1000 + int(tc[3])
                                    c['name'] = t.text
                                    info['menu'].append(c)
                
                # Add tag info from mp4info
                if 'format' in info['file'] and info['file']['format'] == 'MPEG-4':
                    self.load_mp4info(path, info)
                
                # Handle Special Atoms
                if 'itunmovi' in info['tag']:
                    info['tag']['itunmovi'] = xml.sax.saxutils.unescape(self.clean_xml.sub(u'', info['tag']['itunmovi']), {u'&quot;':u'"'}).strip()
                    if info['tag']['itunmovi']:
                        plist = plistlib.readPlistFromString(info['tag']['itunmovi'].encode('utf-8'))
                        for k,v in self.property_map['plist']['itunemovi'].iteritems():
                            if k in plist:
                                l = [ unicode(n['name']) for n in plist[k]]
                                if l: info['tag'][v['name']] = l
                if 'itunextc' in info['tag']:
                    match = self.itunextc_structure.search(info['tag']['itunextc'])
                    if match is not None:
                        info['tag']['rating standard'] = match.group(1)
                        info['tag']['rating'] = match.group(2)
                        info['tag']['rating score'] = match.group(3)
                        info['tag']['rating annotation'] = match.group(4)
                if 'track position' in info['tag']:
                    info['tag']['track #'] = u'{0} / {1}'.format(info['tag']['track position'], info['tag']['track total'])
                if 'disk position' in info['tag']:
                    info['tag']['disk #'] = u'{0} / {1}'.format(info['tag']['disk position'], info['tag']['disk total'])
                if 'cover' in info['tag']:
                    info['tag']['cover'] = info['tag']['cover'].count('Yes')
                if 'genre type' in info['tag']:
                    info['tag']['genre type'] = int(info['tag']['genre type'].split(u',')[0])
                # Format info fields
                for k,v in info['tag'].iteritems():
                    value = self.convert_mediainfo_value(self.property_map['name']['tag'][k]['type'], v)
                    info['tag'][k] = value
                for k,v in info['file'].iteritems():
                    value = self.convert_mediainfo_value(self.property_map['name']['file'][k]['type'], v)
                    info['file'][k] = value
        return info
    
    
    
    
    
    def easy_name(self, info, meta):
        result = None
        if meta and 'name' in meta:
            result = meta['name']
        elif 'name' in info:
            result = info['name']
        if result:
            result = self.illegal_characters_for_filename.sub(u'', result)
        return result
    
    
    def canonic_name(self, info, meta):
        result = None
        valid = False
        
        if 'media kind' in info and 'kind' in info:
            if info['media kind'] == 10: # TV Show
                if 'tv show key' in info and 'tv episode id' in info:
                    result = u''.join([info['tv show key'], u' ', info['tv episode id']])
                    valid = True
            elif info['media kind'] == 9: # Movie
                if 'imdb id' in info:
                    result = u''.join([u'IMDb', info['imdb id']])
                    valid = True
        if valid:
            name = self.easy_name(info, meta)
            if name is not None:
                result = u''.join([result, u' ', name])
            result = u''.join([result, u'.', info['kind']])
        else:
            result = None
        
        return result
    
    
    def canonic_path(self, info, meta):
        result = None
        valid = True
        if 'kind' in info and info['kind'] in repository_config['Kind']:
            if 'volume' in info and info['volume'] in repository_config['Volume']:
                if 'profile' in info:
                    if self.profile_valid_for_kind(info['profile'], info['kind']):
                        result = os.path.join(repository_config['Volume'][info['volume']], self.property_map['code']['stik'][info['media kind']]['name'], info['kind'], info['profile'])
                        if info['media kind'] == 10 and 'tv show key' in info and 'tv season' in info:
                            result = os.path.join(result, info['tv show key'], str(info['tv season']))
                        
                        if info['kind'] in self.kind_with_language:
                            if 'language' in info and info['language'] in self.property_map['iso3t']['language']:
                                result = os.path.join(result, info['language'])
                            else:
                                valid = False
                                self.logger.warning(u'Unknown language for %s', unicode(info))
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
        
    
    
    def check_if_path_available(self, path, overwrite=False):
        result = True
        if path is not None:
            if os.path.exists(path) and not overwrite:
                self.logger.warning(u'Refusing to overwrite %s', path)
                result = False
        else:
            result = False
        
        return result
    
    
    def varify_if_path_available(self, path, overwrite=False):
        result = self.check_if_path_available(path, overwrite)
        if result:
            self.varify_directory(path)
        return result
    
    
    def initialize_command(self, command, logger):
        result = None
        if command in repository_config['Command']:
            c = repository_config['Command'][command]
            if 'path' in c:
                result = [c['path'],]
            else:
                logger.warning(u'Command %s could not be located. Is it installed?', c['binary'])
        return result
    
    
    def execute(self, command, message=None, debug=False, pipeout=True, pipeerr=True, logger=None):
        def encode_command(command):
            cmd = []
            for e in command:
                if u' ' in e:
                    cmd.append(u'"{0}"'.format(e))
                else:
                    cmd.append(e)
            return u' '.join(cmd)
        
        report = None
        if command:
            if not debug:
                if logger == None:
                    logger = self.logger
                
                logger.debug(u'Execute: %s', encode_command(command))
                if message:
                    logger.info(message)
                
                from subprocess import Popen, PIPE
                if pipeout and pipeerr:
                    proc = Popen(command, stdout=PIPE, stderr=PIPE)
                elif pipeout and not pipeerr:
                    proc = Popen(command, stdout=PIPE)
                elif not pipeout and pipeerr:
                    proc = Popen(command, stderr=PIPE)
                elif not pipeout and not pipeerr:
                    proc = Popen(command)
                
                report = proc.communicate()
            else:
                logger.info(message)
                print encode_command(command)
        return report
    
    
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
                        if info['media kind'] in dpc:
                            if 'volume' in dpc[info['media kind']]:
                                info['volume'] = dpc[info['media kind']]['volume']
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
    
    
    def copy_path_info(self, info, options):
        result = None
        if info:
            result = copy.deepcopy(info)
            result['volume'] = options.volume
            if result['volume'] is None:
                del result['volume']
        
            result['profile'] = options.profile
            if result['profile'] is None:
                del result['profile']
        return result
    
    
    def timecode_to_miliseconds(self, timecode):
        result = None
        hours = 0
        minutes = 0
        seconds = 0
        milliseconds = 0
        
        match = FileUtil.full_numeric_time_format.search(timecode)
        if match is not None:
            hours = match.group(1)
            minutes = match.group(2)
            seconds = match.group(3)
            milliseconds = match.group(4)
            
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
    
    
    def miliseconds_to_time(self, miliseconds, millisecond_sep='.'):
        hours = int(miliseconds) / int(3600000)
        hours_modulo = int(miliseconds) % int(3600000)
        minutes = int(hours_modulo) / int(60000)
        minutes_modulo = int(hours_modulo) % int(60000)
        seconds = int(minutes_modulo) / int(1000)
        seconds_modulo = int(minutes_modulo) % int(1000)
        milliseconds = int(seconds_modulo)
        return '{0:02d}:{1:02d}:{2:02d}{3}{4:03d}'.format(hours, minutes, seconds, millisecond_sep, milliseconds)
    
    
    def format_key_value_for_subler(self, key, value):
        m = self.property_map['name']['tag'][key]
        if 'subler' in m:
            pkey = m['subler']
            if m['type'] == 'enum':
                pvalue = self.property_map['code'][m['atom']][value]['print']
            elif m['type'] in ('string', 'list'):
                if m['type'] == 'list':
                    pvalue = u', '.join(value)
                else:
                    if key == 'language':
                        pvalue = self.property_map['iso3t']['language'][value]['print']
                    else:
                        pvalue = unicode(value)
                pvalue = pvalue.replace(u'{',u'&#123;').replace(u'}',u'&#125;').replace(u':',u'&#58;')
            elif m['type'] == 'bool':
                if value: pvalue = u'yes'
                else: pvalue = u'no'
            elif m['type'] == 'date':
                pvalue = value.strftime('%Y-%m-%d %H:%M:%S')
            elif m['type'] == 'int':
                pvalue = unicode(value)
            else:
                pvalue = value
                
        return u'{{{0}:{1}}}'.format(pkey, pvalue)
    
    
    def bytes_to_human_readable(self, value):
        result = None
        if value:
            p = 0
            v = float(value)
            while v > 1024 and p < 4:
                p += 1
                v /= 1024.0
                
            result = '{0:.2f} {1}'.format(v, FileUtil.iec_byte_power_name[p])
        return result
    
    
    def frame_rate_to_float(self, frame_rate):
        frame_rate = str(frame_rate).split('/',1)
        if len(frame_rate) == 2 and str(frame_rate[0]).isdigit() and str(frame_rate[1]).isdigit():
            frame_rate = float(frame_rate[0])/float(frame_rate[1])
        elif str(frame_rate[0].replace('.', '',1)).isdigit():
            frame_rate = float(frame_rate[0])
        else:
            frame_rate = None
        return frame_rate
    
    
    def frame_to_miliseconds(self, frame, frame_rate):
        return round(float(1000)/float(frame_rate) * float(frame))
    
    
    
    
    def format_info_title(self, text):
        return FileUtil.format_info_title_display.format(text)
    
    
    def format_info_subtitle(self, text):
        return FileUtil.format_info_subtitle_display.format(text)
    
    
    def format_key_value(self, key, value, mapping=None):
        if mapping:
            m = mapping[key]
            pkey = m['print']
            if m['type'] == 'enum':
                pvalue = self.property_map['code'][m['atom']][value]['print']
                
            elif m['type'] in ('string', 'list'):
                if m['type'] == 'list': pvalue = u', '.join(value)
                else:
                    if key == 'language':
                        pvalue = self.property_map['iso3t']['language'][value]['print']
                    else:
                        pvalue = unicode(value)
                if len(pvalue) > FileUtil.format_wrap_width:
                    lines = textwrap.wrap(pvalue, FileUtil.format_wrap_width)
                    pvalue = FileUtil.format_indent.join(lines)
                    
            elif m['type'] == 'float':
                pvalue = u'{0:.3f}'.format(value)
                
            elif m['type'] == 'bool':
                if value: pvalue = u'yes'
                else: pvalue = u'no'
                
            else:
                pvalue = value
        else:
            pkey = key
            pvalue = value
        return FileUtil.format_key_value_display.format(pkey, pvalue)
    
    
    def format_value(self, value):
        return FileUtil.format_value_display.format(value)
    
    
    def format_track(self, track):
        return (u'\n'.join([theFileUtil.format_key_value(p, track[p], self.property_map['name']['track'][track['type']]) for p in sorted(set(track))]))
    
    
    format_indent = u'\n' + u' '* repository_config['Display']['indent']
    format_wrap_width = repository_config['Display']['wrap']
    
    format_khz_display = u'{0}kHz'
    format_info_title_display = u'\n\n\n{1}[{{0:-^{0}}}]'.format(repository_config['Display']['wrap'] + repository_config['Display']['indent'], u' ' * repository_config['Display']['margin'])
    format_info_subtitle_display = u'\n{1}[{{0:^{0}}}]\n'.format(repository_config['Display']['indent'] - repository_config['Display']['margin'] - 3, u' ' * repository_config['Display']['margin'])
    format_key_value_display = u'{1}{{0:-<{0}}}: {{1}}'.format(repository_config['Display']['indent'] - repository_config['Display']['margin'] - 2, u' ' * repository_config['Display']['margin'])
    format_value_display = u'{0}{{0}}'.format(u' ' * repository_config['Display']['margin'])
    
    full_numeric_time_format = re.compile('([0-9]{,2}):([0-9]{,2}):([0-9]{,2})(?:\.|,)([0-9]+)')
    illegal_characters_for_filename = re.compile(ur'[\\\/?<>:*|^\.]')
    escaped_subler_tag_characters = set(('{', '}', ':'))
    iec_byte_power_name = {0:'Byte', 1:'KiB', 2:'MiB', 3:'GiB', 4:'TiB'}
    sentence_end = re.compile(ur'[.!?]')
    whitespace_re = re.compile(ur'\s+', re.UNICODE)
    
    
    clean_xml = re.compile(ur'\s+/\s+(?:\t)*', re.UNICODE)
    itunextc_structure = re.compile(ur'([^|]+)\|([^|]+)\|([^|]+)\|([^|]+)?')
    true_value = re.compile(ur'yes|true|1', re.IGNORECASE)
    full_utc_datetime = re.compile(u'(?:UTC )?([0-9]{4})(?:-([0-9]{2})(?:-([0-9]{2})(?: ([0-9]{2}):([0-9]{2}):([0-9]{2}))?)?)?', re.UNICODE)
    mediainfo_chapter_timecode = re.compile(u'_([0-9]{2})_([0-9]{2})_([0-9]{2})\.([0-9]{3})')
    mp4info_tag = re.compile(u' ([^:]+): (.*)$')


# Singleton
theSubtitleFilter = SubtitleFilter()
theFileUtil = FileUtil()



