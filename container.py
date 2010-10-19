# -*- coding: utf-8 -*-

import os
import re
import logging
import hashlib
import chardet
import copy
import textwrap

from config import repository_config
from db import theEntityManager


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
    elif file_type in theFileUtil.container['timecode']['kind']:
        f = Timecode(file_path, autoload=False)
        
    return f


# Container super Class
class Container(object):
    def __init__(self, file_path, autoload=True):
        self.logger = logging.getLogger('mp4pack.container')
        self.file_path = file_path
        self.path_info = None
        self.file_info = None
        self.related = None
        self.meta = None
    
    
    def valid(self):
        return self.path_info is not None
    
    
    def load(self):
        result = False
        Container.load_path_info(self)
        if self.path_info is not None:
            result = True
            self.load_file_info()
            self.load_related()
            self.load_meta()
        else:
            self.logger.warning(u'Could not undestand file name schema %s',self.file_path)
            Container.unload(self)
            
        return result
    
    
    def unload(self):
        self.path_info = None
        self.file_info = None
        self.related = None
        self.meta = None
    
    
    def load_path_info(self):
        # <Volume>/<Media Kind>/<Kind>/<Profile>(/<Show>/<Season>)?(/<Language>)?/(IMDb<IMDB ID> <Name>|<Show> <Code> <Name>).<Extension>
        self.path_info = None
        if self.file_path:
            for mk,v in repository_config['Media Kind'].iteritems():
                match = v['detect'].search(os.path.basename(self.file_path))
                if match is not None:
                    self.path_info = {'Media Kind':mk}
                    if mk == 'movie':
                        self.path_info['imdb_id'] = match.group(1)
                        self.path_info['Name'] = match.group(2)
                        self.path_info['kind'] = match.group(3)
                        
                    elif mk == 'tvshow':
                        self.path_info['show_small_name'] = match.group(1)
                        self.path_info['Code'] = match.group(2)
                        self.path_info['TV Season'] = int(match.group(3))
                        self.path_info['TV Episode #'] = int(match.group(4))
                        self.path_info['Name'] = match.group(5)
                        self.path_info['kind'] = match.group(6)
                        
                    if not self.path_info['Name']:
                        del self.path_info['Name']
                        
                    prefix = os.path.dirname(self.file_path)
                    if self.path_info['kind'] in theFileUtil.kind_with_language:
                        prefix, lang = os.path.split(prefix)
                        if lang in repository_config['Language']:
                            self.path_info['language'] = lang
    
    
    def load_file_info(self):
        if os.path.exists(self.file_path):
            self.file_info = {}
            self.file_info['Length'] = int(os.path.getsize(self.file_path))
            self.file_info['Size'] = theFileUtil.bytes_to_human_readable(self.file_info['Length'])
    
    
    def load_related(self):
        # <Volume>/<Media Kind>/<Kind>/<Profile>(/<Show>/<Season>)?/(IMDb<IMDB ID> <Name>|<Show> <Code> <Name>).<Extension>
        self.related = {}
        kc = repository_config['Kind']
        vc = repository_config['Volume']
        lc = repository_config['Language']
        
        for v in repository_config['Volume'].keys():
            for k in kc.keys():
                for p in kc[k]['Profile'].keys():
                    if kc[k]['container'] in ('subtitles', 'raw audio', 'timecode'):
                        for l in lc.keys():
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
            record = theEntityManager.find_movie_by_imdb_id(self.path_info['imdb_id'])
            if record:
                self.meta = {'Media Kind':repository_config['Media Kind'][self.path_info['Media Kind']]['name']}
                
                if 'name' in record:
                    self.meta['Name'] = record['name']
                if 'overview' in record:
                    self.meta['Long Description'] = FileUtil.whitespace_re.sub(u' ', record['overview']).strip()
                if 'content_rating' in record:
                    self.meta['Rating'] = record['content_rating']
                if 'released' in record:
                    self.meta['Release Date'] = record['released'].strftime('%Y-%m-%d')
                if 'tagline' in record:
                    self.meta['Description'] = FileUtil.whitespace_re.sub(u' ', record['tagline']).strip()
                elif 'overview' in record:
                    s = FileUtil.sentence_end.split(FileUtil.whitespace_re.sub(u' ', record['overview']).strip('\'".,'))
                    if s: self.meta['Description'] = s[0].strip('"\' ').strip() + '.'
                    
                self.load_cast(record)
                self.load_genre(record)
                result = True
                
        elif self.is_tvshow():
            show, episode = theEntityManager.find_episode(self.path_info['show_small_name'], self.path_info['TV Season'], self.path_info['TV Episode #'])
            if show and episode:
                self.meta = {'Media Kind':repository_config['Media Kind'][self.path_info['Media Kind']]['name']}
                
                if 'content_rating' in show:
                    self.meta['Rating'] = show['content_rating']
                if 'network' in show:
                    self.meta['TV Network'] = show['network']
                    
                self.load_genre(show)
                
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
                    overview = FileUtil.whitespace_re.sub(u' ', episode['overview']).strip()
                    self.meta['Long Description'] = overview
                    s = FileUtil.sentence_end.split(overview.strip('\'".,'))
                    if s: self.meta['Description'] = s[0].strip('"\' ').strip() + '.'
                if 'released' in episode:
                    self.meta['Release Date'] = episode['released'].strftime('%Y-%m-%d')
                    
                self.load_cast(episode)
                result = True
                
        if not result:
            self.meta = None
            
        return result
    
    
    def load_media_info(self):
        mediainfo = {'General':{}, 'Audio':[], 'Video':[], 'Text':[], 'Menu':{}}
        command = theFileUtil.initialize_command('mediainfo', self.logger)
        command.extend(['--Language=raw', '-f', self.file_path])
        output, error = theFileUtil.execute(command, None)
        mediainfo_report = unicode(output, 'utf-8').splitlines()
    
    
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
            self.meta['Genre'] = g['name']
            if 'itmf_code' in g.keys():
                self.meta['GenreID'] = g['itmf_code']
                
    
    
    def load_cast(self, record):
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
                artwork = theEntityManager.find_tmdb_movie_poster(self.path_info['imdb_id'])
            elif self.is_tvshow():
                artwork = theEntityManager.find_tvdb_episode_poster(self.path_info['show_small_name'], self.path_info['TV Season'], self.path_info['TV Episode #'])
                
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
        return self.path_info is not None and set(('Media Kind', 'imdb_id')).issubset(set(self.path_info.keys())) and self.path_info['Media Kind'] == 'movie'
    
    
    def is_tvshow(self):
        return self.path_info is not None and set(('Media Kind', 'show_small_name', 'TV Season', 'TV Episode #')).issubset(set(self.path_info.keys())) and self.path_info['Media Kind'] == 'tvshow'
    
    
    def easy_name(self):
        return theFileUtil.easy_name(self.path_info, self.meta)
    
    
    def canonic_name(self):
        return theFileUtil.canonic_name(self.path_info, self.meta)
    
    
    def canonic_path(self):
        return theFileUtil.canonic_path(self.path_info, self.meta)
    
    
    
    def print_meta(self):
        result = None
        if self.meta:
            result = (u'\n'.join([theFileUtil.format_key_value(key, self.meta[key]) for key in sorted(set(self.meta))]))
        return result
    
    
    def print_related(self):
        result = None
        if self.related:
            result = (u'\n'.join([theFileUtil.format_value(key) for key in sorted(set(self.related))]))
        return result
    
    
    def print_path_info(self):
        result = None
        if self.path_info:
            result = (u'\n'.join([theFileUtil.format_key_value(key, self.path_info[key]) for key in sorted(set(self.path_info))]))
        return result
    
    
    def print_file_info(self):
        result = None
        if self.file_info:
            result = (u'\n'.join([theFileUtil.format_key_value(key, self.file_info[key]) for key in sorted(set(self.file_info))]))
        return result
    
    
    def __unicode__(self):
        result = None
        result = theFileUtil.format_info_title(self.file_path)
        if self.related:
            result = u'\n'.join((result, theFileUtil.format_info_subtitle(u'related'), self.print_related()))
        if self.path_info:
            result = u'\n'.join((result, theFileUtil.format_info_subtitle(u'path info'), self.print_path_info()))
        if self.file_info:
            result = u'\n'.join((result, theFileUtil.format_info_subtitle(u'file info'), self.print_file_info()))
        if self.meta:
            result = u'\n'.join((result, theFileUtil.format_info_subtitle(u'metadata'), self.print_meta()))
        return result
    
    
    mediainfo_general_block = re.compile('^General$')
    mediainfo_video_block = re.compile('^Video(?: #([0-9]+))?$')
    mediainfo_audio_block = re.compile('^Audio(?: #([0-9]+))?$')
    mediainfo_text_block = re.compile('^Text(?: #([0-9]+))?$')
    mediainfo_menu_block = re.compile('^Menu$')


class AudioVideoContainer(Container):
    def __init__(self, file_path, autoload=True):
        Container.__init__(self, file_path, autoload)
        self.logger = logging.getLogger('mp4pack.av')
        self.tracks = None
        self.chapter_markers = None
        self.tags = None
    
    
    def valid(self):
        return Container.valid(self) and self.tracks is not None
    
    
    def load(self):
        result = Container.load(self)
        if result:
            self.tracks = []
            self.chapter_markers = []
            self.tags = {}
        else:
            AudioVideoContainer.unload(self)
        return result
    
    
    def unload(self):
        Container.unload(self)
        self.tracks = None
        self.chapter_markers = None
        self.tags = None
    
    
    
    def set_tag(self, name, value):
        self.tags[name] = value
    
    
    def add_track(self, track):
        if track:
            if 'type' in track:
                if track['type'] in repository_config['Codec']:
                    if 'codec' in track:
                        for k,v in repository_config['Codec'][track['type']].iteritems():
                            if v['detect'].search(track['codec']) is not None:
                                track['kind'] = k
                                break
                                
                if track['type'] in theFileUtil.stream_type_with_language:
                    if 'language' not in track or track['language'] == 'und':
                        track['language'] = repository_config['Options'].language
                        
                if track['type'] == 'video':
                    if 'pixel width' in track and 'pixel height' in track:
                        track['sar'] = float(track['pixel width']) / float(track['pixel height'])
            self.tracks.append(track)
    
    
    def add_chapter_marker(self, chapter_marker):
        if chapter_marker:
            self.chapter_markers.append(chapter_marker)
    
    
    def video_width(self):
        result = 0
        if self.tracks:
            for t in self.tracks:
                if t['type'] == 'video' and 'pixel width' in t:
                    result = t['pixel width']
                    break
        return result
    
    
    def playback_height(self):
        result = 0
        if self.tracks:
            for t in self.tracks:
                if t['type'] == 'video' and 'sar' in t:
                    if t['sar'] >= repository_config['Default']['display aspect ratio']:
                        result = t['pixel width'] / t['sar']
                    else:
                        result = t['pixel height']
                    break
        return result
    
    
    def audio_tracks(self):
        return [ t for t in self.tracks if 'type' in t and t['type'] == 'audio']
    
    
    def extract(self, options):
        result = Container.extract(self, options)
        if self.chapter_markers :
            info = theFileUtil.copy_path_info(self.path_info, options)
            info['kind'] = 'txt'
            if theFileUtil.complete_info_default_values(info):
                dest_path = theFileUtil.canonic_path(info, self.meta)
                if theFileUtil.varify_if_path_available(dest_path, options.overwrite):
                    c = Chapter(dest_path, False)
                    c.start()
                    for cm in self.chapter_markers:
                        c.add_chapter_marker(cm)
                        
                    self.logger.info(u'Extracting chapter markers from %s to %s', self.file_path, dest_path)
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
                    selected = {
                        'related':{},
                        'track':{},
                        'tc for ac3':{}
                    }
                    
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
                            for t in self.tracks:
                                for c in pc['pack']['tracks']:
                                    if all((k in t and t[k] == v) for k,v in c.iteritems()):
                                        if t['type'] not in selected['track']:
                                            selected['track'][t['type']] = []
                                        selected['track'][t['type']].append(t)
                                        break
                    
                    # match a timecode for to each related ac3 file
                    if 'ac3' in selected['related']:
                        for r in selected['related']['ac3']:
                            ac3_info = self.related[r]
                            tc_path = None
                            for tc in selected['related']['tc']:
                                tc_info = copy.deepcopy(self.related[tc])
                                del tc_info['kind']
                                if all((k in ac3_info and ac3_info[k] == v) for k,v in tc_info.iteritems()):
                                    tc_path = tc
                            selected['tc for ac3'][r] = tc_path
                    
                    self.logger.debug(selected)
                    
                    if theFileUtil.varify_if_path_available(dest_path, options.overwrite):
                        command = theFileUtil.initialize_command('mkvmerge', self.logger)
                        command.extend([u'--output', dest_path, u'--no-chapters', u'--no-attachments', u'--no-subtitles'])
                        
                        for t in selected['track']['audio'] + selected['track']['video']:
                            if 'name' in t:
                                command.append(u'--track-name')
                                command.append(u'{0}:{1}'.format(t['number'], t['name']))
                            
                            if 'language' in t:
                                command.append(u'--language')
                                command.append(u'{0}:{1}'.format(t['number'], t['language']))
                                
                        command.append(u'--audio-tracks')
                        command.append(u','.join([ unicode(k['number']) for k in selected['track']['audio'] ]))
                        command.append(u'--video-tracks')
                        command.append(u','.join([ unicode(k['number']) for k in selected['track']['video'] ]))
                        command.append(self.file_path)
                        
                        if 'ac3' in selected['related']:
                            for r in selected['related']['ac3']:
                                i = self.related[r]
                                if r in selected['tc for ac3']:
                                    tc = Timecode(selected['tc for ac3'][r])
                                    delay = tc.timecodes[0]
                                    if delay != 0:
                                        command.append(u'--sync')
                                        command.append(u'0:{0}'.format(delay))
                                
                                command.append(u'--language')
                                command.append(u'0:{0}'.format(i['language']))
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
    
    
    
    def print_chapter_markers(self):
        return (u'\n'.join([theFileUtil.format_value(chapter_marker) for chapter_marker in self.chapter_markers]))
    
    
    def print_tags(self):
        return (u'\n'.join([theFileUtil.format_key_value(key, self.tags[key]) for key in sorted(set(self.tags))]))
    
    
    def print_tracks(self):
        return (u'\n'.join([theFileUtil.format_value(theFileUtil.format_track(track)) for track in self.tracks]))
    
    
    def __unicode__(self):
        result = Container.__unicode__(self)
        if len(self.tracks) > 0:
            result = u'\n'.join((result, theFileUtil.format_info_subtitle(u'tracks'), self.print_tracks()))
        if len(self.tags) > 0:
            result = u'\n'.join((result, theFileUtil.format_info_subtitle(u'tags'), self.print_tags()))
        if len(self.chapter_markers) > 0:
            result = u'\n'.join((result, theFileUtil.format_info_subtitle(u'chapter markers'), self.print_chapter_markers()))
        return result
    
    


# Matroska Class
class Matroska(AudioVideoContainer):
    def __init__(self, file_path, autoload=True):
        AudioVideoContainer.__init__(self, file_path, autoload)
        self.logger = logging.getLogger('mp4pack.matroska')
        if autoload:
            self.load()
    
    
    def load(self):
        result = AudioVideoContainer.load(self)
        if result:
            command = theFileUtil.initialize_command('mkvinfo', self.logger)
            command.append(self.file_path)
            output, error = theFileUtil.execute(command, None)
            mkvinfo_report = unicode(output, 'utf-8').splitlines()
            if mkvinfo_report and Matroska.mkvinfo_not_embl_re.search(mkvinfo_report[0]) == None:
                length = len(mkvinfo_report)
                index = 0
                in_mkvinfo_output = False
                in_segment_tracks = False
                in_chapters = False
                while index < length:
                    if in_mkvinfo_output:
                        if (in_segment_tracks):
                            while Matroska.mkvinfo_a_track_re.search(mkvinfo_report[index]):
                                index, track = self._parse_track(index + 1, mkvinfo_report, self._line_depth(mkvinfo_report[index]))
                                self.add_track(track)
                            in_segment_tracks = False
                            
                        elif (in_chapters):
                            while Matroska.mkvinfo_chapter_atom_re.search(mkvinfo_report[index]):
                                index, chapter_marker = self._parse_chapter_marker(index + 1, mkvinfo_report, self._line_depth(mkvinfo_report[index]))
                                self.add_chapter_marker(chapter_marker)
                            in_chapters = False
                            
                        elif Matroska.mkvinfo_segment_tracks_re.search(mkvinfo_report[index]):
                            in_segment_tracks = True
                            index += 1
                            
                        elif Matroska.mkvinfo_chapters_re.search(mkvinfo_report[index]):
                            in_chapters = True
                            while Matroska.mkvinfo_chapter_atom_re.search(mkvinfo_report[index]) is None:
                                index += 1
                        else:
                            index += 1
                            
                    elif Matroska.mkvinfo_start_re.search(mkvinfo_report[index]):
                        in_mkvinfo_output = True
                        index += 1
                        
                if not self.tracks:
                    result = False
            else:
                result = False
        
        if not result:
            self.logger.warning('Could not load matroska file %s', self.file_path)
            Matroska.unload(self)
            
        return result
    
    
    
    def _line_depth(self, mkvinfo_line):
        return Matroska.mkvinfo_line_start_re.search(mkvinfo_line).start(0)
    
    
    def _parse_track(self, index, mkvinfo_report, track_nest_depth):
        track = {}
        while (self._line_depth(mkvinfo_report[index]) > track_nest_depth):
            match = Matroska.mkvinfo_track_number_re.search(mkvinfo_report[index])
            if match is not None:
                track['number'] = int(match.group(1))
                index += 1
                continue
            match = Matroska.mkvinfo_track_type_re.search(mkvinfo_report[index])
            if match is not None:
                track['type'] = match.group(1)
                index += 1
                continue
            match = Matroska.mkvinfo_codec_id_re.search(mkvinfo_report[index])
            if match is not None:
                track['codec'] = match.group(1)
                index += 1
                continue
            match = Matroska.mkvinfo_video_fps_re.search(mkvinfo_report[index])
            if match is not None:
                track['frame rate'] = float(match.group(1))
                index += 1
                continue
            match = Matroska.mkvinfo_language_re.search(mkvinfo_report[index])
            if match is not None:
                track['language'] = match.group(1)
                index += 1
                continue
            match = Matroska.mkvinfo_name_re.search(mkvinfo_report[index])
            if match is not None:
                track['name'] = match.group(1)
                index += 1
                continue
            match = Matroska.mkvinfo_video_pixel_width_re.search(mkvinfo_report[index])
            if match is not None:
                track['pixel width'] = int(match.group(1))
                index += 1
                continue
            match = Matroska.mkvinfo_video_pixel_height_re.search(mkvinfo_report[index])
            if match is not None:
                track['pixel height'] = int(match.group(1))
                index += 1
                continue
            match = Matroska.mkvinfo_audio_sampling_frequency_re.search(mkvinfo_report[index])
            if match is not None:
                track['sampling frequency'] = int(match.group(1))
                index += 1
                continue
            match = Matroska.mkvinfo_audio_channels_re.search(mkvinfo_report[index])
            if match is not None:
                track['channels'] = int(match.group(1))
                index += 1
                continue
            
            index += 1
        
        if 'type' in track and track['type'] == 'audio':
            if 'frame rate' in track: del track['frame rate']
        return index, track
    
    
    def _parse_chapter_marker(self, index, mkvinfo_report, track_nest_depth):
        chapter_marker = ChapterMarker()
        while (self._line_depth(mkvinfo_report[index]) > track_nest_depth):
            match = Matroska.mkvinfo_chapter_start_re.search(mkvinfo_report[index])
            if match is not None:
                chapter_marker.set_start_time(match.group(1))
                index += 1
                continue
            match = Matroska.mkvinfo_chapter_string_re.search(mkvinfo_report[index])
            if match is not None:
                chapter_marker.set_name(match.group(1))
                index += 1
                continue
            match = Matroska.mkvinfo_chapter_language_re.search(mkvinfo_report[index])
            if match is not None:
                chapter_marker.set_language(match.group(1))
                index += 1
                continue
                
            index += 1
            
        return index, chapter_marker
    
    
    def extract(self, options):
        result = AudioVideoContainer.extract(self, options)
        if options.profile is None or theFileUtil.profile_valid_for_kind(options.profile, 'srt'):
            selected = {
                'track':[], 
                'path':{
                    'subtitles':[], 
                    'audio':[],
                    'timecode':[]
                },
                'extract':{
                    'subtitles':[], 
                    'audio':[],
                    'timecode':[]
                }
                
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
                        for t in self.tracks:
                            for c in pc['extract']['tracks']:
                                if all((k in t and t[k] == v) for k,v in c.iteritems()):
                                    selected['track'].append(t)
                                    break
                                    
            if selected['track']:
                command = theFileUtil.initialize_command('mkvextract', self.logger)
                command.extend([u'tracks', self.file_path ])
                
                tc_command = theFileUtil.initialize_command('mkvextract', self.logger)
                tc_command.extend([u'timecodes_v2', self.file_path ])
                
                
                for t in selected['track']:
                    if 'volume' in info: del info['volume']
                    info['kind'] = t['kind']
                    info['language'] = t['language']
                    if theFileUtil.complete_info_default_values(info):
                        dest_path = theFileUtil.canonic_path(info, self.meta)
                        if theFileUtil.varify_if_path_available(dest_path, options.overwrite):
                            if t['kind'] == 'dts':
                                tc_info = theFileUtil.copy_path_info(info, options)
                                tc_info['kind'] = 'tc'
                                if theFileUtil.complete_info_default_values(tc_info):
                                    tc_dest_path = theFileUtil.canonic_path(tc_info, self.meta)
                                    if theFileUtil.varify_if_path_available(tc_dest_path, options.overwrite):
                                        tc_command.append(u'{0}:{1}'.format(unicode(t['number']), tc_dest_path))
                                        selected['path']['timecode'].append(tc_dest_path)
                                        
                                        command.append(u'{0}:{1}'.format(unicode(t['number']), dest_path))
                                        selected['path'][t['type']].append(dest_path)
                            else:
                                command.append(u'{0}:{1}'.format(unicode(t['number']), dest_path))
                                selected['path'][t['type']].append(dest_path)
                                
            if selected['path']['subtitles'] or selected['path']['audio']:
                message = u'Extract {0} subtitle and {1} audio tracks from {2}'.format(
                    unicode(len(selected['path']['subtitles'])), 
                    unicode(len(selected['path']['audio'])), 
                    self.file_path
                )
                theFileUtil.execute(command, message, options.debug, pipeout=False, pipeerr=False, logger=self.logger)
                
                message = u'Extract timecodes for {0} audio tracks from {1}'.format(
                    unicode(len(selected['path']['audio'])), 
                    self.file_path
                )
                theFileUtil.execute(tc_command, message, options.debug, pipeout=False, pipeerr=False, logger=self.logger)
                
            for k in selected['path'].keys():
                for p in selected['path'][k]:
                    if theFileUtil.clean_if_not_exist(p):
                        selected['extract'][k].append(p)
            
            if selected['extract']['subtitles']:
                o = copy.deepcopy(options)
                o.transcode = 'srt'
                o.extract = None
                for p in selected['extract']['subtitles']:
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
            
            if selected['extract']['timecode']:
                o = copy.deepcopy(options)
                o.transcode = 'tc'
                o.extract = None
                o.profile = None
                o.overwrite = True
                for p in selected['extract']['timecode']:
                    t = Timecode(p)
                    t.transcode(o)
                    result.append(p)
                    
        else:
            self.logger.warning('Skipping subtitle extraction. Profile %s invalid for srt kind.', options.profile)
        return result
    
    
    mkvinfo_not_embl_re = re.compile('No EBML head found')
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
    mkvinfo_audio_channels_re = re.compile('\+ Channels: ([0-9]+)')
    mkvinfo_video_pixel_width_re = re.compile('\+ Pixel width: ([0-9]+)')
    mkvinfo_video_pixel_height_re = re.compile('\+ Pixel height: ([0-9]+)')
    mkvinfo_chapters_re = re.compile('\+ Chapters')
    mkvinfo_chapter_atom_re = re.compile('\+ ChapterAtom')
    mkvinfo_chapter_start_re = re.compile('\+ ChapterTimeStart: ([0-9\.:]+)')
    mkvinfo_chapter_string_re = re.compile('\+ ChapterString: (.*)')
    mkvinfo_chapter_language_re = re.compile('\+ ChapterLanguage: ([a-z]+)')
    mkvinfo_line_start_re = re.compile('\+')


# Mpeg4 Class
class Mpeg4(AudioVideoContainer):
    def __init__(self, file_path, autoload=True):
        AudioVideoContainer.__init__(self, file_path, autoload)
        self.logger = logging.getLogger('mp4pack.mp4')
        if autoload:
            self.load()
    
    
    def load(self):
        result = AudioVideoContainer.load(self)
        if result:
            command = theFileUtil.initialize_command('mp4info', self.logger)
            command.append(self.file_path)
            output, error = theFileUtil.execute(command, None)
            mp4info_report = unicode(output, 'utf-8').splitlines()
            if not error or Mpeg4.mp4info_not_mp4.search(error) is None:
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
                    
                command = theFileUtil.initialize_command('mp4chaps', self.logger)
                command.extend([u'-l', self.file_path])
                output, error = theFileUtil.execute(command, None)
                mp4chaps_report = unicode(output, 'utf-8').splitlines()
                for idx, line in enumerate(mp4chaps_report):
                    m = self._parse_chapter_marker(line)
                    if m: self.add_chapter_marker(m)
                
                if not self.tracks:
                    result = False
            else:
                result = False
        
        if not result:
            self.logger.warning('Could not load mp4 file %s', self.file_path)
            Mpeg4.unload(self)
        
        return result
    
    
    def _parse_tag(self, line):
        name = None
        value = None
        match = Mpeg4.mp4info_tag_re.search(line)
        if match:
            mp4info_tag_name = match.group(1)
            name = theFileUtil.canonic_tag_name_from_mp4info(mp4info_tag_name)
            value = match.group(2)
        return name, value
    
    
    def _parse_track(self, line):
        track = None
        match = Mpeg4.mp4info_video_track_re.search(line)
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
            match = Mpeg4.mp4info_audio_track_re.search(line)
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
        match = Mpeg4.mp4chaps_chapter_re.search(line)
        if match:
            start_time = match.group(2)
            name = match.group(3)
            m = ChapterMarker(start_time, name)
        return m
    
    
    
    def tag(self, options):
        AudioVideoContainer.tag(self, options)
        tc = None
        update = {}
        width = self.video_width()
        if width > repository_config['Default']['hd video min width']:
            update['HD Video'] = 'yes'
        else:
            update['HD Video'] = 'no'
            
        if self.meta:
            for k in [k for (k,v) in self.meta.iteritems() if k not in self.tags or self.tags[k] != v]:
                update[k] = self.meta[k]
                    
        elif self.path_info:
            if self.is_movie():
                if 'Name' in self.path_info and self.path_info['Name'] != self.tags['Name']:
                    update['Name'] = self.path_info['Name']
                
            elif self.is_tvshow():
                if not('TV Season' in self.tags and self.path_info['TV Season'] == self.tags['TV Season']):
                    update['TV Season'] = self.path_info['TV Season']
                if not('TV Episode #' in self.tags and self.path_info['TV Episode #'] == self.tags['TV Episode #']):
                    update['TV Episode #'] = self.path_info['TV Episode #']
                if 'Name' in self.path_info and not('Name' in self.tags and self.path_info['Name'] == self.tags['Name']):
                    update['Name'] = self.path_info['Name']
        if update:
            tc = u''.join([u'{{{0}:{1}}}'.format(theFileUtil.subler_tag_name_from_canonic(t), theFileUtil.escape_for_subler_tag(update[t])) for t in sorted(set(update))])
            message = u'Tag {0} {1}'.format(self.file_path, u','.join(sorted(set(update.keys()))))
            self.logger.info(u'Update %s --> %s', u', '.join(sorted(set(update.keys()))), self.file_path)
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
                                    u'-l', repository_config['Language'][i['language']],
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
                                    message = u'Update smart {0} subtitles {1} --> {2}'.format(repository_config['Language'][code], p, self.file_path)
                                    command = theFileUtil.initialize_command('subler', self.logger)
                                    command.extend([
                                        u'-i', self.file_path, 
                                        u'-s', p, 
                                        u'-l', repository_config['Language'][smart_section['language']],
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
    
    
    mp4info_not_mp4 = re.compile('mp4info: can\'t open')
    mp4info_video_track_re = re.compile('([0-9]+)	video	([^,]+), ([0-9\.]+) secs, ([0-9\.]+) kbps, ([0-9]+)x([0-9]+) @ ([0-9\.]+) fps')
    mp4info_h264_video_codec_re = re.compile('H264 ([^@]+)@([0-9\.]+)')
    mp4info_audio_track_re = re.compile('([0-9]+)	audio	([^,]+), ([0-9\.]+) secs, ([0-9\.]+) kbps, ([0-9]+) Hz')
    mp4info_tag_re = re.compile(' ([^:]+): (.*)$')
    mp4chaps_chapter_re  = re.compile('Chapter #([0-9]+) - ([0-9:\.]+) - (.*)$')


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
            self.file_info['Encoding'] = encoding['encoding']
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
    
    


# Audiocode Class
class Timecode(Text):
    def __init__(self, file_path, autoload=True):
        Text.__init__(self, file_path, autoload)
        self.logger = logging.getLogger('mp4pack.audiocode')
        self.timecodes = None
        self.scope = 2
        if autoload:
            self.load()
    
    
    def valid(self):
        return Text.valid(self) and self.timecodes is not None
    
    
    def load(self):
        result = Text.load(self)
        if result:
            self.timecodes = []
            result = Timecode.decode(self)
        if not result:
            self.logger.warning('Could not parse timecode file %s', self.file_path)
            Timecode.unload(self)
        return result
    
    
    def unload(self):
        Text.unload(self)
        self.timecodes = None
    
    
    def decode(self):
        result = Text.decode(self)
        self.timecodes= []
        if result:
            lines = self.read()
            for line in lines:
                if Timecode.timecode_line_re.search(line) is not None:
                    self.timecodes.append(int(line.strip()))
            if not self.timecodes:
                result = False
        return result
    
    
    def read(self):
        lines = None
        if os.path.exists(self.file_path):
            try:
                reader = open(self.file_path, 'r')
                scope = self.scope
                lines = []
                for line in reader:
                    lines.append(line)
                    scope -= 1
                    if not scope > 0:
                        break
                reader.close()
            except IOError as error:
                self.logger.error(str(error))
        return lines
    
    
    def encode(self):
        timecode_strings = []
        for tc in self.timecodes:
            timecode_strings.append(unicode(tc))
        return timecode_strings
    
    
    timecode_line_re = re.compile('^[0-9]+$')


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
                            timecode = match_timecode.group(2)
                            name = match_name.group(2)
                            self.add_chapter_marker(ChapterMarker(timecode, name))
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
    
    
    def add_chapter_marker(self, chapter_marker):
        if chapter_marker is not None:
            self.chapter_markers.append(chapter_marker)
    
    
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
    def __init__(self, start_time=None, name=None, language=None):
        self.set_start_time(start_time)
        self.set_name(name)
        self.set_language(language)
    
    
    def set_start_time(self, start_time):
        if start_time is not None:
            self.start_time = theFileUtil.timecode_to_miliseconds(start_time)
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
        start_time_string = unicode(theFileUtil.miliseconds_to_time(self.start_time, '.'), 'utf-8')
        line_buffer.append(u'CHAPTER{0}={1}'.format(str(index).zfill(2), start_time_string))
        line_buffer.append(u'CHAPTER{0}NAME={1}'.format(str(index).zfill(2), self.name))
    
    
    def __unicode__(self):
        return u'{0} : {1}'.format(theFileUtil.miliseconds_to_time(self.start_time), self.name)
    


# Artwork Class
class Artwork(Container):
    def __init__(self, file_path, autoload=True):
        Container.__init__(self, file_path, autoload)
        self.logger = logging.getLogger('mp4pack.image')
        if autoload:
            self.load()
    
    
    def load(self):
        result = Container.load(self)
        if result:
            image = None
            from PIL import Image
            try:
                image = Image.open(self.file_path)
            except IOError:
                result = False
            if result:
                self.file_info['Pixel Width'] = image.size[0]
                self.file_info['Pixel Height'] = image.size[1]
                self.file_info['Format'] = image.format
        if not result:
            self.logger.warning('Could not parse artwork file %s', self.file_path)
            Artwork.unload(self)
        return result
    
    
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
                            self.logger.debug(u'Found match in %s', line)
                            keep = False
                            break
                    if keep:
                        block.add_line(line)
                        
            elif self.config['scope'] == 'block':
                keep = True
                for line in block.lines:
                    for e in self.expression:
                        if e.search(line) is not None:
                            self.logger.debug(u'Found match in %s', line)
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
                            self.logger.debug(u'Replaced "%s" with "%s"', line, filtered_line)
                    if not block.valid(): break
                        
            elif self.config['scope'] == 'block':
                all_lines = u'\n'.join(block.lines)
                block.clear()
                for e in self.expression:
                    filtered_lines = e[0].sub(e[1], all_lines).strip()
                    if all_lines != filtered_lines:
                        self.logger.debug(u'Replaced "%s" with "%s"', all_lines, filtered_lines)
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
        self.kind_with_language = self.container['subtitles']['kind'] + self.container['raw audio']['kind'] + self.container['timecode']['kind']
        
        # Tag naming map
        tc = repository_config['Tag']
        self.canonic_tag_map = {}
        self.mp4info_tag_map = {}
        for tag in tc:
            self.canonic_tag_map[tag[0]] = tag
            if tag[2] is not None:
                self.mp4info_tag_map[tag[2]] = tag
        
    
    
    def canonic_tag_name_from_mp4info(self, name):
        result = None
        if name in self.mp4info_tag_map:
            result = self.mp4info_tag_map[name][0]
        return result
    
    
    def subler_tag_name_from_canonic(self, name):
        result = None
        if name in self.canonic_tag_map:
            result = self.canonic_tag_map[name][1]
        return result
    
    
    def easy_name(self, info, meta):
        result = None
        if meta and 'Name' in meta:
            result = meta['Name']
        elif 'Name' in info:
            result = info['Name']
        if result:
            result = FileUtil.illegal_characters_for_filename.sub(u'', result)
        return result
    
    
    def canonic_name(self, info, meta):
        result = None
        valid = False
        
        if 'Media Kind' in info and info['Media Kind'] in repository_config['Media Kind'] and 'kind' in info and info['kind'] in repository_config['Kind']:
            if info['Media Kind'] == 'tvshow':
                if 'show_small_name' in info and 'Code' in info:
                    result = u''.join([info['show_small_name'], u' ', info['Code']])
                    valid = True
            elif info['Media Kind'] == 'movie':
                if 'imdb_id' in info:
                    result = u''.join([u'IMDb', info['imdb_id']])
                    valid = True
        if valid:
            easy_name = self.easy_name(info, meta)
            if easy_name is not None:
                result = u''.join([result, u' ', easy_name])
            
            result = u''.join([result, u'.', info['kind']])
        
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
                        
                        if info['kind'] in self.kind_with_language:
                            if 'language' in info and info['language'] in repository_config['Language']:
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
    
    
    def escape_for_subler_tag(self, value):
        if value and isinstance(value, unicode) and FileUtil.escaped_subler_tag_characters.issubset(value):
            value = value.replace(u'{',u'&#123;').replace(u'}',u'&#125;').replace(u':',u'&#58;')
        return value
    
    
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
    
    
    def format_key_value(self, key, value):
        value = unicode(value)
        if len(value) > FileUtil.format_wrap_width:
            lines = textwrap.wrap(value, FileUtil.format_wrap_width)
            value = FileUtil.format_indent.join(lines)
        return FileUtil.format_key_value_display.format(key, value)
    
    
    def format_value(self, value):
        return FileUtil.format_value_display.format(value)
    
    
    def format_track(self, track):
        t = {}
        for (k,v) in track.iteritems():
            if k == 'sampling frequency':
                t[k] = FileUtil.format_khz_display.format(int(int(v) / 1000))
            elif isinstance(v, float):
                t[k] = '{0:.2f}'.format(v)
            else:
                t[k] = v
        return u' | '.join([u'{0}: {1}'.format(key, t[key]) for key in sorted(set(t))])
    
    
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


# Singleton
theSubtitleFilter = SubtitleFilter()
theFileUtil = FileUtil()



