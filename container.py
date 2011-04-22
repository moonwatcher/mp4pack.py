# -*- coding: utf-8 -*-

import os
import re
import logging
import hashlib
import chardet
import copy
import textwrap
import plistlib

from datetime import datetime
from db import theEntityManager
from subprocess import Popen, PIPE
import xml.etree.cElementTree as ElementTree

from config import theConfiguration as configuration

# Generic file loading function
def make_media_file(file_path):
    f = None
    file_type = os.path.splitext(file_path)[1].strip('.')
    if file_type in configuration.property_map['container']['mp4']['kind']:
        f = Mpeg4(file_path, autoload=False)
    elif file_type in configuration.property_map['container']['matroska']['kind']:
        f = Matroska(file_path, autoload=False)
    elif file_type in configuration.property_map['container']['subtitles']['kind']:
        f = Subtitle(file_path, autoload=False)
    elif file_type in configuration.property_map['container']['chapters']['kind']:
        f = Chapter(file_path, autoload=False)
    elif file_type in configuration.property_map['container']['image']['kind']:
        f = Artwork(file_path, autoload=False)
    elif file_type in configuration.property_map['container']['raw audio']['kind']:
        f = RawAudio(file_path, autoload=False)
    elif file_type in configuration.property_map['container']['avi']['kind']:
        f = Avi(file_path, autoload=False)
        
    return f


# Container super Class
class Container(object):
    def __init__(self, file_path, autoload=True):
        self.logger = logging.getLogger('mp4pack.container')
        self.file_path = file_path
        self.path_info = None
        self.record = None
        self.info = None
        self.meta = None
        
        self.unindexed = []
        self.ghost = []
    
    
    def valid(self):
        return self.path_info is not None and self.info is not None
    
    
    def in_repository(self):
        return theFileUtil.check_if_in_repository(self.path_info)
    
    
    def load(self, refresh=False, download=False):
        result = False
        result = Container.load_path_info(self)
        if result:
            result = self.load_record(refresh, download)
            if result:
                result = self.load_info()
            else:
                self.logger.warning(u'Could not load db record for %s',self.file_path)
        else:
            self.logger.warning(u'Could not undestand file name schema %s',self.file_path)
        if not result:
            Container.unload(self)
        return result
    
    
    def load_path_info(self):
        self.path_info = None
        if self.file_path:
            self.path_info = theFileUtil.decode_path(self.file_path)
        return self.path_info is not None
    
    
    def load_record(self, refresh=False, download=False):
        result = False
        if self.path_info:
            if self.is_movie():
                entity = theEntityManager.find_movie_by_imdb_id(self.path_info['imdb id'], download)
                if entity:
                    self.record = {}
                    self.record['entity'] = entity
                    result = True
                    
            elif self.is_tvshow():
                show, episode = theEntityManager.find_episode(self.path_info['tv show key'], self.path_info['tv season'], self.path_info['tv episode #'], download)
                if show and episode:
                    self.record = {}
                    self.record['entity'] = episode
                    self.record['tv show'] = show
                    result = True
            
            if self.record and 'entity' in self.record:
                if refresh:
                    self.drop_index()
                else:
                    if 'physical' not in self.record['entity'] or not self.record['entity']['physical']:
                        refresh = True
                if refresh:
                    self.refresh_index()
        return result
    
    
    def load_info(self, refresh=False):
        self.info = None
        if self.file_path and self.path_info:
            if self.file_path in self.record['entity']['physical'] and not refresh:
                self.info = self.record['entity']['physical'][self.file_path]['info']
            else:
                self.info = theFileUtil.decode_info(self.file_path)
                if self.in_repository() and self.info:
                    self.record['entity']['physical'][self.file_path] = {}
                    self.record['entity']['physical'][self.file_path]['path info'] = self.path_info
                    self.record['entity']['physical'][self.file_path]['info'] = self.info
                    self.save_record()
                    self.logger.info(u'Refreshed info about %s', self.file_path)
        return self.info is not None
    
    
    def pick_artist(self):
        self.meta['artist'] = None
        if self.is_movie():
            for job in ['directors', 'producers', 'screenwriters', 'codirectors', 'cast']:
                if job in self.meta and self.meta[job]:
                    self.meta['artist'] = self.meta[job][0]
                    break
        elif self.is_tvshow():
            self.meta['artist'] = self.record['tv show']['tvdb_record']['name']
            self.meta['album artist'] = self.record['tv show']['tvdb_record']['name']
            self.meta['sort artist'] = theFileUtil.sort_field(self.record['tv show']['tvdb_record']['name'])
            self.meta['sort album artist'] = theFileUtil.sort_field(self.record['tv show']['tvdb_record']['name'])
            
            # Seems like using on of those as an artist messes up the grouping on iOS
            # Looking at an iTunes file the artist and album artist should have the tv show name
            # for job in ['screenwriters', 'directors', 'producers', 'codirectors', 'cast']:
            #    if job in self.meta and self.meta[job]:
            #        self.meta['artist'] = self.meta[job][0]
            #        break
    
    
    def load_meta(self):
        result = False
        self.meta = None
        if self.is_movie():
            movie = self.record['entity']
            if 'tmdb_record' in movie:
                self.meta = {'media kind':9}
                if 'name' in movie['tmdb_record']:
                    self.meta['name'] = movie['tmdb_record']['name']
                if 'overview' in movie['tmdb_record'] and movie['tmdb_record']['overview'] != 'No overview found.':
                    self.meta['long description'] = FileUtil.whitespace_re.sub(u' ', movie['tmdb_record']['overview']).strip()
                if 'certification' in movie['tmdb_record']:
                    self.meta['rating'] = movie['tmdb_record']['certification']
                if 'released' in movie['tmdb_record']:
                    self.meta['release date'] = datetime.strptime(movie['tmdb_record']['released'], '%Y-%m-%d')
                if 'tagline' in movie['tmdb_record'] and movie['tmdb_record']['tagline']:
                    self.meta['description'] = FileUtil.whitespace_re.sub(u' ', movie['tmdb_record']['tagline']).strip()
                elif 'overview' in movie['tmdb_record'] and movie['tmdb_record']['overview'] != 'No overview found.':
                    s = FileUtil.sentence_end.split(FileUtil.whitespace_re.sub(u' ', movie['tmdb_record']['overview']).strip('\'".,'))
                    if s: self.meta['description'] = s[0].strip('"\' ').strip() + '.'
                self.load_cast(movie['tmdb_record'])
                self.load_genre(movie['tmdb_record'])
                result = True
                
        elif self.is_tvshow():
            show = self.record['tv show']
            episode = self.record['entity']
            if show and 'tvdb_record' in show and episode and 'tvdb_record' in episode:
                self.meta = {'media kind':10}
                
                if 'name' in show['tvdb_record']:
                    self.meta['tv show'] = show['tvdb_record']['name']
                    self.meta['sort tv show'] = theFileUtil.sort_field(show['tvdb_record']['name'])
                if 'name' in show['tvdb_record'] and 'tv_season' in episode['tvdb_record']:
                    album_name = u'{0}, Season {1}'.format(show['tvdb_record']['name'], unicode(episode['tvdb_record']['tv_season']))
                    self.meta['album'] = album_name
                    self.meta['sort album'] = theFileUtil.sort_field(album_name)
                if 'tv_episode' in episode['tvdb_record'] and 'tv_season' in episode['tvdb_record']:
                    self.meta['tv episode id'] = u's{0:02}e{1:02}'.format(episode['tvdb_record']['tv_season'], episode['tvdb_record']['tv_episode'])
                if 'tv_season' in episode['tvdb_record']:
                    self.meta['tv season'] = episode['tvdb_record']['tv_season']
                    self.meta['disk position'] = episode['tvdb_record']['tv_season']
                    self.meta['disk total'] = 0
                    self.meta['disk #'] = u'{0} / {1}'.format(self.meta['disk position'], self.meta['disk total'])
                if 'tv_episode' in episode['tvdb_record']:
                    self.meta['tv episode #'] = episode['tvdb_record']['tv_episode']
                    self.meta['track position'] = episode['tvdb_record']['tv_episode']
                    self.meta['track total'] = 0
                    self.meta['track #'] = u'{0} / {1}'.format(self.meta['track position'], self.meta['track total'])
                if 'name' in episode['tvdb_record']:
                    self.meta['name'] = episode['tvdb_record']['name']
                    self.meta['sort name'] = theFileUtil.sort_field(episode['tvdb_record']['name'])
                    
                if 'certification' in show['tvdb_record']:
                    self.meta['rating'] = show['tvdb_record']['certification']
                if 'tv_network' in show['tvdb_record']:
                    self.meta['tv network'] = show['tvdb_record']['tv_network']
                if 'released' in episode['tvdb_record']:
                    self.meta['release date'] = episode['tvdb_record']['released']
                    
                if 'overview' in episode['tvdb_record']:
                    overview = FileUtil.whitespace_re.sub(u' ', episode['tvdb_record']['overview']).strip()
                    self.meta['long description'] = overview
                    s = FileUtil.sentence_end.split(overview.strip('\'".,'))
                    if s: self.meta['description'] = s[0].strip('"\' ').strip() + '.'
                    
                self.load_genre(show['tvdb_record'])
                self.load_cast(show['tvdb_record'], True, False)
                self.load_cast(episode['tvdb_record'], False, True)
                result = True
        if not result:
            self.meta = None
        else:
            self.pick_artist()
        return result
    
    
    def unload(self):
        if self.unindexed:
            self.drop_index(self.ghost)
            self.refresh_index(self.unindexed)
        self.path_info = None
        self.record = None
        self.info = None
        self.meta = None
    
    
    
    def refresh_index(self, queue=None):
        # <Volume>/<Media Kind>/<Kind>/<Profile>/(<Show>/<Season>/(language/)?<Show> <Code> <Name>|(language/)?IMDb<IMDB ID> <Name>).<Extension>
        if self.record:
            if 'physical' not in self.record['entity']:
                self.record['entity']['physical'] = {}
            
            if queue is None:
                queue = theFileUtil.scan_repository_for_related(self.file_path, self.record['entity'])
            
            if queue:
                discovered = 0
                for path in queue:
                    if path not in self.record['entity']['physical']:
                        related_path_info = theFileUtil.decode_path(path)
                        if theFileUtil.check_if_in_repository(related_path_info):
                            self.logger.debug(u'Indexing %s.', path)
                            self.record['entity']['physical'][path] = {}
                            self.record['entity']['physical'][path]['path info'] = related_path_info
                            self.record['entity']['physical'][path]['info'] = theFileUtil.decode_info(path)
                            discovered += 1
                if discovered:
                    self.save_record()
                    self.logger.debug(u'Indexed %s files related to %s in repository.', discovered, self.file_path)
    
    
    def drop_index(self, queue=None):
        if self.record and 'entity' in self.record and 'physical' in self.record['entity']:
            need_save = False
            if queue:
                for p in queue:
                    if p in self.record['entity']['physical']:
                        self.logger.debug(u'Dropping physical index for %s', p)
                        del self.record['entity']['physical'][p]
                        need_save = True
                if not self.record['entity']['physical']:
                    del self.record['entity']['physical']
                    need_save = True
            else:
                self.logger.debug(u'Dropping all physical index for %s', self.file_path)
                del self.record['entity']['physical']
                need_save = True
            if need_save: self.save_record()
    
    
    def save_record(self):
        if self.is_movie():
            theEntityManager.save_movie(self.record['entity'])
        elif self.is_tvshow():
            theEntityManager.save_tv_episode(self.record['entity'])
    
    
    def queue_for_index(self, path):
        if path not in self.unindexed:
            self.unindexed.append(path)
        if path not in self.ghost:
            self.ghost.append(path)
    
    
    def drop_from_index(self, path):
        if path not in self.ghost:
            self.ghost.append(path)
    
    
    
    
    
    def related(self):
        related = {}
        for k,v in self.record['entity']['physical'].iteritems():
            related[k] = v['path info']
        return related
    
    
    
    
    def info(self, options):
        return unicode(self)
    
    
    def copy(self, options):
        result = None
        path_info = theFileUtil.copy_path_info(self.path_info, options)
        if theFileUtil.complete_path_info_default_values(path_info):
            dest_path = theFileUtil.canonic_path(path_info, self.record['entity'])
            if theFileUtil.varify_if_path_available(dest_path, options.overwrite):
                command = theFileUtil.initialize_command('rsync', self.logger)
                command.extend([self.file_path, dest_path])
                message = u'Copy ' + self.file_path + u' --> ' + dest_path
                theFileUtil.execute(command, message, options.debug, pipeout=True, pipeerr=False, logger=self.logger)
                if theFileUtil.clean_if_not_exist(dest_path):
                    result = dest_path
                    self.queue_for_index(dest_path)
                    if options.md5:
                        self.compare_checksum(dest_path)
        return result
    
    
    def delete(self):
        if self.path_info:
            self.drop_from_index(self.file_path)
            self.logger.debug(u'Delete %s',self.file_path)
            theFileUtil.clean(self.file_path)
    
    
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
                self.drop_from_index(self.file_path)
                self.queue_for_index(dest_path)
            else:
                self.logger.warning(u'Not renaming %s, destination exists: %s', self.file_path, dest_path)
    
    
    def tag(self, options):
        self.load_meta()
    
    
    def optimize(self, options):
        pass
    
    
    def extract(self, options):
        return []
    
    
    def pack(self, options):
        pass
    
    
    def transcode(self, options):
        pass
    
    
    def transform(self, options):
        pass
    
    
    def update(self, options):
        pass
    
    
    
    
    def load_genre(self, record):
        if 'genres' in record and record['genres']:
            genres = [ r for r in record['genres'] if r['type'] == 'genre' ]
            if genres:
                genre = genres[0]
                self.meta['genre'] = genre['name']
                if 'itmf' in genre:
                    self.meta['genre type'] = genre['itmf']
    
    
    def load_cast(self, record, initialize=True, finalize=True):
        if 'cast' in record:
            
            if initialize:
                for i in configuration.property_map['name']['itunemovi']:
                    self.meta[i] = []
                    
            self.meta['directors'].extend([ 
                r['name'] for r in record['cast'] 
                if r['department'] == 'Directing' and r['job'] == 'Director'
            ])
            self.meta['codirectors'].extend([
                r['name'] for r in record['cast'] 
                if r['department'] == 'Directing' and  r['job'] != 'Director'
            ])
            self.meta['producers'].extend([
                r['name'] for r in record['cast'] 
                if r['department'] == 'Production'
            ])
            self.meta['screenwriters'].extend([
                r['name'] for r in record['cast'] 
                if r['department'] == 'Writing'
            ])
            self.meta['cast'].extend([
                r['name'] for r in record['cast'] 
                if r['department'] == 'Actors'
            ])
            
            if finalize:
                for i in configuration.property_map['name']['itunemovi']:
                    if not self.meta[i]:
                        del self.meta[i]
        return
        
    
    
    
    def download_artwork(self, options):
        result = False
        path_info = theFileUtil.copy_path_info(self.path_info, options)
        path_info['kind'] = 'png'
        if theFileUtil.complete_path_info_default_values(path_info):
            selected = []
            lookup = {'kind':'png', 'profile':path_info['profile']}
            for (path, phy) in self.record['entity']['physical'].iteritems():
                if all((k in phy['path info'] and phy['path info'][k] == v) for k,v in lookup.iteritems()):
                    selected.append(path)
                    break
            if not selected:
                artwork = None
                if self.is_movie():
                    artwork = theEntityManager.find_tmdb_movie_poster(self.path_info['imdb id'])
                elif self.is_tvshow():
                    artwork = theEntityManager.find_tvdb_episode_poster(self.path_info['tv show key'], self.path_info['tv season'], self.path_info['tv episode #'])
                if artwork and 'cache' in artwork:
                    path_info['kind'] = artwork['cache']['kind']
                    if 'volume' in path_info: del path_info['volume']
                    image = Artwork(artwork['cache']['path'], False)
                    image.path_info = path_info
                    image.load_record()
                    o = copy.deepcopy(options)
                    o.transcode = 'png'
                    result = image.transcode(o)
                    image.unload()
                    if result:
                        self.load_record()
                        self.logger.debug('Original artwork downloaded to %s', result)
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
        return (
            self.path_info and
            'media kind' in self.path_info and self.path_info['media kind'] == 9 and
            'imdb id' in self.path_info
        )
    
    
    def is_tvshow(self):
        return (
            self.path_info and
            'media kind' in self.path_info and self.path_info['media kind'] == 10 and
            'tv show key' in self.path_info and
            'tv season' in self.path_info and
            'tv episode #' in self.path_info
        )
    
    
    def simple_name(self):
        return theFileUtil.simple_name(self.path_info, self.record['entity'])
    
    
    def canonic_name(self):
        return theFileUtil.canonic_name(self.path_info, self.record['entity'])
    
    
    def canonic_path(self):
        return theFileUtil.canonic_path(self.path_info, self.record['entity'])
    
    
    
    def print_meta(self):
        return theFileUtil.format_display_block(self.meta, configuration.property_map['name']['tag'])
    
    
    def print_related(self):
        result = None
        related = self.related()
        if related:
            result = (u'\n'.join([theFileUtil.format_value(key) for key in sorted(set(related))]))
        return result
    
    
    def print_path_info(self):
        return theFileUtil.format_display_block(self.path_info, configuration.property_map['name']['tag'])
    
    
    def print_file_info(self):
        return theFileUtil.format_display_block(self.info['file'], configuration.property_map['name']['file'])
    
    
    def print_tracks(self):
        return (u'\n\n\n'.join([theFileUtil.format_display_block(track, configuration.property_map['name']['track'][track['type']]) for track in self.info['track']]))
    
    
    def print_tags(self):
        return theFileUtil.format_display_block(self.info['tag'], configuration.property_map['name']['tag'])
    
    
    def print_chapter_markers(self):
        return (u'\n'.join([theFileUtil.format_value(ChapterMarker(marker['time'], marker['name'])) for marker in self.info['menu']]))
    
    
    def __unicode__(self):
        result = None
        result = theFileUtil.format_info_title(self.info['file']['name'])
        
        related = self.related()
        if related:
            result = u'\n'.join((result, theFileUtil.format_info_subtitle(u'related'), self.print_related()))
        
        if self.info['file']:
            result = u'\n'.join((result, theFileUtil.format_info_subtitle(u'file info'), self.print_file_info()))
        if self.path_info:
            result = u'\n'.join((result, theFileUtil.format_info_subtitle(u'path info'), self.print_path_info()))
        
        if self.info['menu']:
            result = u'\n'.join((result, theFileUtil.format_info_subtitle(u'menu'), self.print_chapter_markers()))
        
        if self.info['tag']:
            tag_block = self.print_tags()
            if tag_block:
                result = u'\n'.join((result, theFileUtil.format_info_subtitle(u'tags'), tag_block))
        
        #self.load_meta()
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
    
    
    def load_meta(self):
        Container.load_meta(self)
        #if self.meta:
        #    self.meta['hd video'] = self.hd_video()
        
    
    
    def main_video_track(self):
        result = None
        if self.info['track']:
            for t in self.info['track']:
                if t['type'] == 'video':
                    if (not result and 'stream size') or 'stream size' in t and t['stream size'] > result['stream size']:
                        result = t
        return result
    
    
    def video_width(self):
        result = 0
        v = self.main_video_track()
        if v: result = v['width']
        return result
    
    
    def hd_video(self):
        return self.video_width() > configuration.repository['Default']['hd video min width']
    
    
    def playback_height(self):
        result = 0
        v = self.main_video_track()
        if v:
            if v['display aspect ratio'] >= configuration.repository['Default']['display aspect ratio']:
                result = float(v['width']) / float(configuration.repository['Default']['display aspect ratio'])
            else:
                result = float(v['height'])
        return result
    
    
    def audio_tracks(self):
        return [ t for t in self.info['track'] if 'type' in t and t['type'] == 'audio']
    
    
    def extract(self, options):
        result = Container.extract(self, options)
        if self.info['menu']:
            path_info = theFileUtil.copy_path_info(self.path_info, options)
            path_info['kind'] = 'txt'
            if theFileUtil.complete_path_info_default_values(path_info):
                dest_path = theFileUtil.canonic_path(path_info, self.record['entity'])
                if theFileUtil.varify_if_path_available(dest_path, options.overwrite):
                    c = Chapter(dest_path, False)
                    c.start()
                    for marker in self.info['menu']:
                        c.add_chapter_marker(marker['time'], marker['name'])
                    self.logger.info(u'Extracting chapter markers from %s --> %s', self.file_path, dest_path)
                    c.delete()
                    c.write(dest_path)
                    c.unload()
                    if theFileUtil.clean_if_not_exist(dest_path):
                        result.append(dest_path)
                        self.queue_for_index(dest_path)
        return result
    
    
    def pack(self, options):
        Container.pack(self, options)
        path_info = theFileUtil.copy_path_info(self.path_info, options)
        
        if options.pack in ('m4v'):
            path_info['kind'] = 'm4v'
            if theFileUtil.complete_path_info_default_values(path_info):
                dest_path = theFileUtil.canonic_path(path_info, self.record['entity'])
                if dest_path is not None:
                    pc = configuration.repository['Kind'][path_info['kind']]['Profile'][path_info['profile']]
                    if theFileUtil.varify_if_path_available(dest_path, options.overwrite):
                        command = theFileUtil.initialize_command('subler', self.logger)
                        command.extend([u'-o', dest_path, u'-i', self.file_path])
                        
                        message = u'Pack {0} --> {1}'.format(self.file_path, dest_path)
                        theFileUtil.execute(command, message, options.debug, pipeout=False, pipeerr=False, logger=self.logger)
                        if theFileUtil.clean_if_not_exist(dest_path):
                            self.queue_for_index(dest_path)
                            
        elif options.pack in ('mkv'):
            path_info['kind'] = 'mkv'
            if theFileUtil.complete_path_info_default_values(path_info):
                dest_path = theFileUtil.canonic_path(path_info, self.record['entity'])
                if dest_path is not None:
                    pc = configuration.repository['Kind'][path_info['kind']]['Profile'][path_info['profile']]
                    selected = { 'related':{}, 'track':{} }
                    
                    if 'pack' in pc:
                        # locate related files that need to be muxed in
                        if 'related' in pc['pack']:
                            for (path, phy) in self.record['entity']['physical'].iteritems():
                                for c in pc['pack']['related']:
                                    if all((k in phy['path info'] and phy['path info'][k] == v) for k,v in c.iteritems()):
                                        if phy['path info']['kind'] not in selected['related']:
                                            selected['related'][phy['path info']['kind']] = []
                                        selected['related'][phy['path info']['kind']].append(path)
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
                        
                        if 'name' in self.record['entity']:
                            full_name = name = theFileUtil.full_name(self.path_info, self.record)
                            if full_name:
                                command.append(u'--title')
                                command.append(full_name)
                            
                        for t in selected['track']['video']:
                            #if 'name' in t:
                            #    command.append(u'--track-name')
                            #    command.append(u'{0}:{1}'.format(t['id'], t['name']))
                            if 'language' in t:
                                command.append(u'--language')
                                command.append(u'{0}:{1}'.format(t['id'], theFileUtil.find_language(t['language'])['iso2']))
                                
                        for t in selected['track']['audio']:
                            if 'channels' in t:
                                if t['channels'] < 2: tname = 'Mono'
                                elif t['channels'] > 2: tname = 'Surround'
                                else: tname = 'Stereo'
                                command.append(u'--track-name')
                                command.append(u'{0}:{1}'.format(t['id'], tname))
                            if 'language' in t:
                                command.append(u'--language')
                                command.append(u'{0}:{1}'.format(t['id'], theFileUtil.find_language(t['language'])['iso2']))
                                
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
                                ac3_record = self.record['entity']['physical'][r]
                                lookup = {'codec':'DTS', 'language':ac3_record['path info']['language']}
                                for t in self.info['track']:
                                    if all((k in t and t[k] == v) for k,v in lookup.iteritems()):
                                        if 'delay' in t and t['delay'] != 0:
                                            self.logger.debug(u'Found a matching DTS track with non trivial delay of %d', t['delay'])
                                            command.append(u'--sync')
                                            command.append(u'0:{0}'.format(t['delay']))
                                            break
                                if 'channels' in ac3_record['info']['track'][0]:
                                    channels = ac3_record['info']['track'][0]['channels']
                                    if channels < 2: tname = 'Mono'
                                    elif channels > 2: tname = 'Surround'
                                    else: tname = 'Stereo'
                                    command.append(u'--track-name')
                                    command.append(u'0:{0}'.format(tname))
                                command.append(u'--language')
                                command.append(u'0:{0}'.format(theFileUtil.find_language(ac3_record['path info']['language'])['iso2']))
                                command.append(r)
                        
                        if 'srt' in selected['related']:
                            for r in selected['related']['srt']:
                                path_info = self.record['entity']['physical'][r]['path info']
                                command.append(u'--sub-charset')
                                command.append(u'0:UTF-8')
                                command.append(u'--language')
                                command.append(u'0:{0}'.format(theFileUtil.find_language(path_info['language'])['iso2']))
                                command.append(r)
                        
                        if 'txt' in selected['related']:
                            for r in selected['related']['txt']:
                                path_info = self.record['entity']['physical'][r]['path info']
                                command.append(u'--chapter-language')
                                command.append(u'en')
                                command.append(u'--chapter-charset')
                                command.append(u'UTF-8')
                                command.append(u'--chapters')
                                command.append(r)
                                break
                                
                        message = u'Pack {0} --> {1}'.format(self.file_path, dest_path)
                        theFileUtil.execute(command, message, options.debug, pipeout=False, pipeerr=False, logger=self.logger)
                        if theFileUtil.clean_if_not_exist(dest_path):
                            self.queue_for_index(dest_path)
    
    
    def transcode(self, options):
        result = None
        Container.transcode(self, options)
        path_info = theFileUtil.copy_path_info(self.path_info, options)
        if options.transcode in ('mkv', 'm4v'):
            path_info['kind'] = options.transcode
            if theFileUtil.complete_path_info_default_values(path_info):
                dest_path = theFileUtil.canonic_path(path_info, self.record['entity'])
                if dest_path is not None:
                    command = None
                    if theFileUtil.varify_if_path_available(dest_path, options.overwrite):
                        command = theFileUtil.initialize_command('handbrake', self.logger)
                        tc = configuration.repository['Kind'][path_info['kind']]['Profile'][path_info['profile']]['transcode']
                        
                        if 'flags' in tc:
                            for v in tc['flags']:
                                command.append(v)
                                
                        if 'options' in tc:
                            hb_config = copy.deepcopy(tc['options'])
                            if options.pixel_width: hb_config['--maxWidth'] = options.pixel_width
                            if options.quality: hb_config['--quality'] = options.quality
                            if options.crop: hb_config['--crop'] = options.crop
                            
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
                        if theFileUtil.clean_if_not_exist(dest_path):
                            self.queue_for_index(dest_path)
                            result = dest_path
        return result
    
    
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
        selected = {
            'track':[], 
            'path':{ 'text':[], 'audio':[] },
            'extract':{ 'text':[], 'audio':[] }
        }
        path_info = theFileUtil.copy_path_info(self.path_info, options)
        if 'volume' in path_info: del path_info['volume']
        path_info['profile'] = 'dump'
        for k in ('srt', 'ass', 'dts'):
            if 'volume' in path_info: del path_info['volume']
            path_info['kind'] = k
            if theFileUtil.complete_path_info_default_values(path_info):
                pc = configuration.repository['Kind'][path_info['kind']]['Profile'][path_info['profile']]
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
                if 'volume' in path_info: del path_info['volume']
                path_info['kind'] = t['kind']
                path_info['language'] = t['language']
                if theFileUtil.complete_path_info_default_values(path_info):
                    dest_path = theFileUtil.canonic_path(path_info, self.record['entity'])
                    if dest_path not in selected['path'][t['type']]:
                        if theFileUtil.varify_if_path_available(dest_path, options.overwrite):
                            command.append(u'{0}:{1}'.format(unicode(t['id']), dest_path))
                            selected['path'][t['type']].append(dest_path)
                    else:
                        self.logger.warning('Skipping track %s of type %s because %s is taken', t['id'], t['type'], dest_path)
                            
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
            o.profile = None
            o.extract = None
            for p in selected['extract']['text']:
                s = Subtitle(p)
                o.profile = 'original'
                ts = s.transcode(o)
                o.profile = 'clean'
                ts = s.transcode(o)
                s.delete()
                s.unload()
                if theFileUtil.clean_if_not_exist(ts):
                    result.append(ts)
        
        if selected['extract']['audio']:
            o = copy.deepcopy(options)
            o.transcode = 'ac3'
            o.extract = None
            o.profile = None
            for p in selected['extract']['audio']:
                a = RawAudio(p)
                ta = a.transcode(o)
                a.delete()
                a.unload()
                if theFileUtil.clean_if_not_exist(ta):
                    result.append(ta)
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
                if configuration.property_map['name']['tag'][k]['subler'] 
                and (k not in self.info['tag'] or self.info['tag'][k] != v)
            ]: 
                if k in self.info['tag']:
                    self.logger.debug('Updating tag %s from %s to %s', k, self.info['tag'][k], self.meta[k])
                else:
                    self.logger.debug('Setting tag %s to %s', k, self.meta[k])
                update[k] = self.meta[k]
            
            # check the HD Video flag
            is_hd_video = self.hd_video()
            if is_hd_video and (('hd video' not in self.info['tag']) or ('hd video' in self.info['tag'] and not self.info['tag']['hd video'])):
                update['hd video'] = is_hd_video
            elif not is_hd_video and ('hd video' in self.info['tag'] and self.info['tag']['hd video']):
                update['hd video'] = is_hd_video
                
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
            message = u'Update tags: {0} --> {1}'.format(u', '.join([configuration.property_map['name']['tag'][t]['print'] for t in sorted(set(update.keys()))]), self.file_path)
            command = theFileUtil.initialize_command('subler', self.logger)
            command.extend([u'-o', self.file_path, u'-t', tc])
            theFileUtil.execute(command, message, options.debug, pipeout=True, pipeerr=False, logger=self.logger)
            self.queue_for_index(self.file_path)
            
        else:
            self.logger.info(u'No tags need update in %s', self.file_path)
    
    
    def optimize(self, options):
        AudioVideoContainer.optimize(self, options)
        message = u'Optimize {0}'.format(self.file_path)
        command = theFileUtil.initialize_command('mp4file', self.logger)
        command.extend([u'--optimize', self.file_path])
        theFileUtil.execute(command, message, options.debug, pipeout=True, pipeerr=False, logger=self.logger)
        self.queue_for_index(self.file_path)
        
    
    
    def _update_png(self, options):
        AudioVideoContainer.tag(self, options)
        if options.update == 'png':
            path_info = theFileUtil.copy_path_info(self.path_info, options)
            path_info['kind'] = 'png'
            selected = []
            if theFileUtil.complete_path_info_default_values(path_info):
                if options.download:
                    self.download_artwork(options)
                lookup = {'kind':path_info['kind'], 'profile':path_info['profile']}
                for (path, phy) in self.record['entity']['physical'].iteritems():
                    if all((k in phy['path info'] and phy['path info'][k] == v) for k,v in lookup.iteritems()):
                        selected.append(path)
                        break
            if selected:
                message = u'Update artwork {0} --> {1}'.format(selected[0], self.file_path)
                command = theFileUtil.initialize_command('subler', self.logger)
                command.extend([u'-o', self.file_path, u'-t', u'{{{0}:{1}}}'.format(u'Artwork', selected[0])])
                theFileUtil.execute(command, message, options.debug, pipeout=True, pipeerr=False, logger=self.logger)
                self.queue_for_index(self.file_path)
            else:
                self.logger.warning(u'No artwork available for %s', self.file_path)
    
    
    def _update_jpg(self, options):
        AudioVideoContainer.tag(self, options)
        if options.update == 'jpg':
            path_info = theFileUtil.copy_path_info(self.path_info, options)
            path_info['kind'] = 'jpg'
            selected = []
            if theFileUtil.complete_path_info_default_values(path_info):
                if options.download:
                    self.download_artwork(options)
                lookup = {'kind':path_info['kind'], 'profile':path_info['profile']}
                for (path, phy) in self.record['entity']['physical'].iteritems():
                    if all((k in phy['path info'] and phy['path info'][k] == v) for k,v in lookup.iteritems()):
                        selected.append(path)
                        break
            if selected:
                message = u'Update artwork {0} --> {1}'.format(selected[0], self.file_path)
                command = theFileUtil.initialize_command('subler', self.logger)
                command.extend([u'-o', self.file_path, u'-t', u'{{{0}:{1}}}'.format(u'Artwork', selected[0])])
                theFileUtil.execute(command, message, options.debug, pipeout=True, pipeerr=False, logger=self.logger)
                self.queue_for_index(self.file_path)
            else:
                self.logger.warning(u'No artwork available for %s', self.file_path)
    
    
    def _update_srt(self, options):
        if options.update == 'srt':
            path_info = theFileUtil.copy_path_info(self.path_info, options)
            path_info['kind'] = 'srt'
            if theFileUtil.complete_path_info_default_values(path_info):
                pc = configuration.repository['Kind']['srt']['Profile'][path_info['profile']]
                
                has_changed = False
                if 'profile' in path_info and 'update' in pc:
                    if pc['update']['reset']:
                        message = u'Drop existing subtitle tracks in {0}'.format(self.file_path)
                        command = theFileUtil.initialize_command('subler', self.logger)
                        command.extend([u'-o', self.file_path, u'-r'])
                        theFileUtil.execute(command, message, options.debug, pipeout=True, pipeerr=False, logger=self.logger)
                        has_changed = True
                    
                    if 'related' in pc['update']:
                        selected = {}
                        for (path, phy) in self.record['entity']['physical'].iteritems():
                            for c in pc['update']['related']:
                                if all((k in phy['path info'] and phy['path info'][k] == v) for k,v in c['from'].iteritems()):
                                    selected[path] = phy['path info']
                                    break
                                
                        for (p,i) in selected.iteritems():
                            message = u'Update subtitles {0} --> {1}'.format(p, self.file_path)
                            command = theFileUtil.initialize_command('subler', self.logger)
                            command.extend([
                                u'-o', self.file_path,
                                u'-i', p, 
                                u'-l', configuration.property_map['iso3t']['language'][i['language']]['print'],
                                u'-n', c['to']['Name'], 
                                u'-a', unicode(int(round(self.playback_height() * c['to']['height'])))
                            ])
                            theFileUtil.execute(command, message, options.debug, pipeout=True, pipeerr=False, logger=self.logger)
                            has_changed = True
                            
                        if 'smart' in pc['update']:
                            smart_section = pc['update']['smart']
                            found = False
                            for code in smart_section['order']:
                                for (p,i) in selected.iteritems():
                                    if i['language'] == code:
                                        message = u'Update smart {0} subtitles {1} --> {2}'.format(configuration.property_map['iso3t']['language'][code]['print'], p, self.file_path)
                                        command = theFileUtil.initialize_command('subler', self.logger)
                                        command.extend([
                                            u'-o', self.file_path, 
                                            u'-i', p, 
                                            u'-l', configuration.property_map['iso3t']['language'][smart_section['language']]['print'],
                                            u'-n', smart_section['Name'],
                                            u'-a', unicode(int(round(self.playback_height() * smart_section['height'])))
                                        ])
                                        theFileUtil.execute(command, message, options.debug, pipeout=True, pipeerr=False, logger=self.logger)
                                        found = True
                                        has_changed = True
                                        break
                                if found: break
                    if has_changed:
                        self.queue_for_index(self.file_path)
    
    
    def _update_txt(self, options):
        AudioVideoContainer.tag(self, options)
        if options.update == 'txt':
            path_info = theFileUtil.copy_path_info(self.path_info, options)
            path_info['kind'] = 'txt'
            selected = []
            if theFileUtil.complete_path_info_default_values(path_info):
                pc = configuration.repository['Kind']['txt']['Profile'][path_info['profile']]
                if 'update' in pc:
                    if pc['update']['reset'] and self.info['menu']:
                        message = u'Drop existing chapters in {0}'.format(self.file_path)
                        command = theFileUtil.initialize_command('subler', self.logger)
                        command.extend([u'-o', self.file_path, u'-r', u'-c', u'/dev/null'])
                        theFileUtil.execute(command, message, options.debug, pipeout=True, pipeerr=False, logger=self.logger)
                    if 'related' in pc['update']:
                        lookup = pc['update']['related']
                        for (path, phy) in self.record['entity']['physical'].iteritems():
                            if all((k in phy['path info'] and phy['path info'][k] == v) for k,v in lookup.iteritems()):
                                selected.append(path)
                                break
                                
                        if selected:
                            message = u'Update chapters {0} --> {1}'.format(selected[0], self.file_path)
                            command = theFileUtil.initialize_command('subler', self.logger)
                            command.extend([u'-o', self.file_path, u'-c', selected[0], '-p'])
                            theFileUtil.execute(command, message, options.debug, pipeout=True, pipeerr=False, logger=self.logger)
                            self.queue_for_index(self.file_path)
                        else:
                            self.logger.warning(u'No chapters available for %s', self.file_path)
    
    
    def update(self, options):
        AudioVideoContainer.update(self, options)
        self._update_srt(options)
        self._update_txt(options)
        self._update_png(options)
        self._update_jpg(options)
    
    


# Raw Audio Class
class RawAudio(AudioVideoContainer):
    def __init__(self, file_path, autoload=True):
        AudioVideoContainer.__init__(self, file_path, autoload)
        self.logger = logging.getLogger('mp4pack.rawaudio')
        if autoload:
            self.load()
    
    
    def transcode(self, options):
        result = None
        if options.transcode == 'ac3':
            path_info = theFileUtil.copy_path_info(self.path_info, options)
            path_info['kind'] = options.transcode
            path_info['language'] = self.path_info['language']
            if theFileUtil.complete_path_info_default_values(path_info):
                dest_path = theFileUtil.canonic_path(path_info, self.record['entity'])
                if theFileUtil.varify_if_path_available(dest_path, options.overwrite):
                    track = self.info['track'][0]
                    option = None
                    pc = configuration.repository['Kind'][path_info['kind']]['Profile'][path_info['profile']]
                    if 'transcode' in pc and 'audio' in pc['transcode']:
                        for c in pc['transcode']['audio']:
                            if all((k in track and track[k] == v) for k,v in c['from'].iteritems()):
                                option = c
                                break
                    if option:
                        message = u'Transcode audio {0} --> {1}'.format(self.file_path, dest_path)
                        command = theFileUtil.initialize_command('ffmpeg', self.logger)
                        command.extend([
                            u'-threads',u'{0}'.format(configuration.repository['Default']['threads']),
                            u'-i', self.file_path,
                            u'-acodec', u'ac3',
                            u'-ac', u'{0}'.format(track['channels']),
                            u'-ab', u'{0}k'.format(option['to']['-ab']),
                            dest_path
                        ])
                        theFileUtil.execute(command, message, options.debug, pipeout=True, pipeerr=False, logger=self.logger)
                        if theFileUtil.clean_if_not_exist(dest_path):
                            self.queue_for_index(dest_path)
                            result = dest_path
        return result
    
    


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
        result = None
        Container.transcode(self, options)
        self.decode()
        path_info = theFileUtil.copy_path_info(self.path_info, options)
        path_info['kind'] = options.transcode
        if theFileUtil.complete_path_info_default_values(path_info):
            dest_path = theFileUtil.canonic_path(path_info, self.record['entity'])
            if theFileUtil.varify_if_path_available(dest_path, options.overwrite):
                self.logger.info(u'Transcode %s --> %s', self.file_path, dest_path)
                self.write(dest_path)
                if theFileUtil.clean_if_not_exist(dest_path):
                    self.queue_for_index(dest_path)
                    result = dest_path
        return result
    
    


# Subtitle Class
class Subtitle(Text):
    def __init__(self, file_path, autoload=True):
        Text.__init__(self, file_path, autoload)
        self.logger = logging.getLogger('mp4pack.subtitle')
        self.subtitle_blocks = None
        if autoload:
            self.load()
    
    
    def load_info(self, refresh=False):
        result = Text.load_info(self, refresh)
        if result:
            if not('statistics' in self.info and not refresh):
                result = Subtitle.decode(self)
                if result:
                    statistics = {'Blocks':0, 'Lines':0, 'Sentences':0, 'Words':0, 'Characters':0}
                    statistics['Blocks'] = len(self.subtitle_blocks)
                    for block in self.subtitle_blocks:
                        block.calculate_statistics()
                        for (k,v) in block.statistics.iteritems():
                            statistics[k] += block.statistics[k]
                    self.info['statistics'] = statistics
                    self.save_record()
                    self.logger.info(u'Refreshed statistics for %s', self.file_path)
                else:
                    self.logger.warning('Could not parse subtitle file %s', self.file_path)
        else:
            self.logger.warning('Could not parse text file %s', self.file_path)
        return result
    
    
    def unload(self):
        Text.unload(self)
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
        
        
        result = Text.decode(self)
        if result and self.subtitle_blocks is None:
            lines = self.read()
            if lines:
                self.subtitle_blocks = []
                if self.path_info['kind'] == 'srt':
                    decode_srt(lines)
                elif self.path_info['kind'] in ('ass', 'ssa'):
                    decode_ass(lines)
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
        result = None
        self.decode()
        path_info = theFileUtil.copy_path_info(self.path_info, options)
        path_info['kind'] = options.transcode
        if theFileUtil.complete_path_info_default_values(path_info):
            dest_path = theFileUtil.canonic_path(path_info, self.record['entity'])
            if theFileUtil.varify_if_path_available(dest_path, options.overwrite):
                p = configuration.repository['Kind'][path_info['kind']]['Profile'][path_info['profile']]
                
                # Check if profile dictates filtering
                if 'transcode' in p and 'filter' in p['transcode']:
                    self.filter(p['transcode']['filter'])
                
                # Check if time shift is necessary
                if options.time_shift is not None:
                    self.shift(options.time_shift)
                
                # Check if frame rate conversion is necessary
                input_frame_rate = None
                output_frame_rate = None
                if (options.input_rate is not None and options.output_rate is not None):
                    input_frame_rate = theFileUtil.frame_rate_to_float(options.input_rate)
                    output_frame_rate = theFileUtil.frame_rate_to_float(options.output_rate)
                elif (options.NTSC):
                    input_frame_rate = Subtitle.pal_framerate
                    output_frame_rate = Subtitle.ntsc_framerate
                elif (options.PAL):
                    input_frame_rate = Subtitle.ntsc_framerate
                    output_frame_rate = Subtitle.pal_framerate
                    
                if input_frame_rate is not None and output_frame_rate is not None:
                    factor = input_frame_rate / output_frame_rate
                    self.scale_rate(factor)
                
                self.logger.info(u'Transcode %s --> %s', self.file_path, dest_path)
                self.write(dest_path)
                if theFileUtil.clean_if_not_exist(dest_path):
                    self.queue_for_index(dest_path)
                    result = dest_path
        return result
    
    
    def filter(self, sequence_list):
        if sequence_list:
            self.logger.debug(u'Filtering %s by %s', self.file_path, unicode(sequence_list))
            self.subtitle_blocks = theSubtitleFilter.filter(self.subtitle_blocks, sequence_list)
    
    
    def shift(self, offset):
        self.logger.debug(u'Shifting time codes on %s by %s', self.file_path, unicode(offset))
        block_buffer = self.subtitle_blocks
        self.subtitle_blocks = []
        for block in block_buffer:
            block.shift(offset)
            if block.valid():
                self.subtitle_blocks.append(block)
    
    
    def scale_rate(self, factor):
        self.logger.debug(u'Scaling time codes on %s by %s', self.file_path, unicode(factor))
        for block in self.subtitle_blocks:
            block.scale_rate(factor)
    
    
    def print_subtitle_statistics(self):
        return (u'\n'.join([theFileUtil.format_key_value(key, self.info['statistics'][key]) for key in sorted(set(self.info['statistics']))]))
    
    
    def __unicode__(self):
        result = Text.__unicode__(self)
        result = u'\n'.join((result, theFileUtil.format_info_subtitle(u'subtitle statistics'), self.print_subtitle_statistics()))
        return result
    
    
    srt_time_line = re.compile('^([0-9]{2}:[0-9]{2}:[0-9]{2},[0-9]{3}) --> ([0-9]{2}:[0-9]{2}:[0-9]{2},[0-9]{3})$')
    ass_subline = re.compile('^Dialogue\s*:\s*(.*)$')
    ass_formation_line = re.compile('^Format\s*:\s*(.*)$')
    ass_condense_line_breaks = re.compile(r'(\\N)+')
    ass_event_command_re = re.compile(r'\{\\[^\}]+\}')
    pal_framerate = 25.0
    ntsc_framerate = 23.976


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
        return self.begin and self.begin > 0 and self.end and self.end > 0 and self.begin < self.end and self.lines
    
    
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
    
    
    def load(self, refresh=False, download=False):
        result = Text.load(self, refresh, download)
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
        self.path_info = theFileUtil.decode_path(self.file_path)
    
    
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
        match = ChapterMarker.mediainfo_chapter_name_with_lang_re.search(self.name)
        if match:
            self.name = match.group(2)
        match = ChapterMarker.rubish_chapter_re.search(self.name)
        if match:
            self.name = None
    
    
    def encode(self, line_buffer, index):
        line_buffer.append(ChapterMarker.ogg_chapter_timestamp_format.format(str(index).zfill(2), unicode(theFileUtil.miliseconds_to_time(self.time, '.'), 'utf-8')))
        name = self.name
        if name is None:
            name = ChapterMarker.default_chapter_name_format.format(index)
        line_buffer.append(ChapterMarker.ogg_chapter_name_format.format(str(index).zfill(2), name))
    
    
    def __unicode__(self):
        return u'{0} : {1}'.format(theFileUtil.miliseconds_to_time(self.time), self.name)
    
    ogg_chapter_timestamp_format = u'CHAPTER{0}={1}'
    ogg_chapter_name_format = u'CHAPTER{0}NAME={1}'
    default_chapter_name_format = u'Chapter {0}'
    mediainfo_chapter_name_with_lang_re = re.compile(u'^(?:([a-z]{2,3}):)?(.*)$', re.UNICODE)
    rubish_chapter_re = re.compile('([0-9]{,2}:[0-9]{,2}:[0-9]{,2}[\.,][0-9]+|[0-9]+|chapter[\s0-9]+)')




# Artwork Class
class Artwork(Container):
    def __init__(self, file_path, autoload=True):
        Container.__init__(self, file_path, autoload)
        self.logger = logging.getLogger('mp4pack.image')
        if autoload:
            self.load()
    
    
    def transcode(self, options):
        result = None
        path_info = theFileUtil.copy_path_info(self.path_info, options)
        path_info['kind'] = options.transcode
        if theFileUtil.complete_path_info_default_values(path_info):
            dest_path = theFileUtil.canonic_path(path_info, self.record['entity'])
            if theFileUtil.varify_if_path_available(dest_path, options.overwrite):
                p = configuration.repository['Kind'][path_info['kind']]['Profile'][path_info['profile']]
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
                        if size != rsize:
                            self.logger.debug(u'Resize artwork: %dx%d --> %dx%d', size[0], size[1], rsize[0], rsize[1])
                            image = image.resize(rsize, Image.ANTIALIAS)
                            
                        self.logger.info(u'Transcode %s --> %s', self.file_path, dest_path)
                        image.save(dest_path)
                        
                        if theFileUtil.clean_if_not_exist(dest_path):
                            self.queue_for_index(dest_path)
                            result = dest_path
        return result
    




# Subtitle Filter Class (Singleton)
class SubtitleFilter(object):
    def __init__(self):
        self.logger = logging.getLogger('mp4pack.filter.manager')
        self.sequence = {}
    
    
    def find_filter_sequence(self, name):
        result = None
        if name in self.sequence:
            result = self.sequence[name]
        elif name in configuration.subtitle:
            config = configuration.subtitle[name]
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
    
    
    def convert_mediainfo_value(self, kind, value):
        result = value
        if kind == 'int' or kind == 'enum':
            try:
                result = int(value)
            except ValueError as error:
                # Sometimes mediainfo would report a pair of integers, sparated by a /
                if self.mediainfo_integer_list.match(value):
                    result = min([int(v) for v in value.split('/')])
                    self.logger.warning('Picking minimal value %d from mediainfo list of integers %s', result, value)
                else:
                    self.logger.error('Could not decode Integer: %s', value)
                    result = None
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
            else:
                self.logger.debug('Unknow datetime format for %s', value)
        elif kind == 'bool':
            if self.true_value.search(value) is not None:
                result = True
            else:
                result = False
        return result
    
    
    def parse_mp4info(self, path, info):
        command = theFileUtil.initialize_command('mp4info', self.logger)
        command.append(path)
        proc = Popen(command, stdout=PIPE, stderr=PIPE)
        report = proc.communicate()
        mp4info_report = unicode(report[0], 'utf-8').splitlines()
        for line in mp4info_report:
            match = self.mp4info_tag.search(line)
            if match is not None:
                tag = match.groups()
                if tag[0] in configuration.property_map['mp4info']['tag']:
                    n = configuration.property_map['mp4info']['tag'][tag[0]]
                    info['tag'][n['name']] = tag[1]
    
    
    def decode_info(self, path):
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
                                if t.tag in configuration.property_map['mediainfo']['tag']:
                                    p = configuration.property_map['mediainfo']['tag'][t.tag]
                                    info['tag'][p['name']] = t.text
                                elif t.tag in configuration.property_map['mediainfo']['file']:
                                    p = configuration.property_map['mediainfo']['file'][t.tag]
                                    info['file'][p['name']] = t.text
                        elif track_type in configuration.property_map['mediainfo']['track']:
                            track = {}
                            for t in tn:
                                if t.tag in configuration.property_map['mediainfo']['track'][track_type]:
                                    p = configuration.property_map['mediainfo']['track'][track_type][t.tag]
                                    value = self.convert_mediainfo_value(p['type'], t.text)
                                    track[p['name']] = value
                            if track:
                                track['type'] = track_type
                                if track_type == 'video':
                                     if 'encoder settings' in track and 'encoder' in track and track['encoder'].count('x264'):
                                         track['encoder settings'] = track['encoder settings'].split(' / ')
                                
                                # check to see if language is not set and set it to default
                                if track['type'] in configuration.track_with_language:
                                    if 'language' not in track or track['language'] == 'und':
                                        track['language'] = configuration.options.language
                                
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
                    self.parse_mp4info(path, info)
                
                # Handle Special Atoms
                if 'itunmovi' in info['tag'] and info['tag']['itunmovi']:
                    info['tag']['itunmovi'] = info['tag']['itunmovi'].replace('&quot;', '"')
                    info['tag']['itunmovi'] = self.clean_xml.sub(u'', info['tag']['itunmovi']).strip()
                    plist = plistlib.readPlistFromString(info['tag']['itunmovi'].encode('utf-8'))
                    for k,v in configuration.property_map['plist']['itunemovi'].iteritems():
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
                    if 'genre' not in info['tag']:
                        info['tag']['genre'] = configuration.property_map['code']['gnre'][info['tag']['genre type']]['print']
                    
                    
                # Format info fields
                for k,v in info['tag'].iteritems():
                    value = self.convert_mediainfo_value(configuration.property_map['name']['tag'][k]['type'], v)
                    info['tag'][k] = value
                for k,v in info['file'].iteritems():
                    value = self.convert_mediainfo_value(configuration.property_map['name']['file'][k]['type'], v)
                    info['file'][k] = value
                    
                # Fix description and long description
                if 'description' in info['tag']:
                    info['tag']['description'] = info['tag']['description'].replace('&quot;', '"')
                if 'long description' in info['tag']:
                    info['tag']['long description'] = info['tag']['long description'].replace('&quot;', '"')
        return info
    
    
    
    def decode_path(self, path, extended=True):
        # <Volume>/<Media Kind>/<Kind>/<Profile>/(<Show>/<Season>/(language/)?<Show> <Code> <Name>|(language/)?IMDb<IMDB ID> <Name>).<Extension>
        path_info = {}
        if path:
            basename = os.path.basename(path)
            for mk in configuration.supported_media_kind:
                match = mk['schema'].search(basename)
                if match is not None:
                    path_info = {'media kind':mk['code']}
                    if mk['name'] == 'movie':
                        path_info['imdb id'] = match.group(1)
                        path_info['name'] = match.group(2)
                        path_info['kind'] = match.group(3)
                    elif mk['name'] == 'tvshow':
                        path_info['tv show key'] = match.group(1)
                        path_info['tv episode id'] = match.group(2)
                        path_info['tv season'] = int(match.group(3))
                        path_info['tv episode #'] = int(match.group(4))
                        path_info['name'] = match.group(5)
                        path_info['kind'] = match.group(6)
                    prefix = os.path.dirname(path)
                    if path_info['kind'] in configuration.kind_with_language:
                        prefix, iso = os.path.split(prefix)
                        lang = self.find_language(iso)
                        if lang: path_info['language'] = lang['iso3t']
                    break
                    
            if 'media kind' in path_info and extended:
                # media kind was detected and parsed
                suffix = os.path.realpath(path)
                for k,v in configuration.repository['Volume'].iteritems():
                    if os.path.commonprefix([v['realpath'], suffix]) == v['realpath']:
                        path_info['volume'] = k
                        suffix = os.path.relpath(suffix, v['realpath'])
                        break
                
                if 'volume' in path_info:
                    # Path is in repository
                    fragments = suffix.split('/')
                    if (
                        len(fragments) > 3 and
                        fragments[0] in configuration.property_map['name']['stik'] and path_info['media kind'] == configuration.property_map['name']['stik'][fragments[0]]['code'] and
                        fragments[1] in configuration.repository['Kind'] and path_info['kind'] == fragments[1] and
                        fragments[2] in configuration.repository['Kind'][path_info['kind']]['Profile']
                    ): path_info['profile'] = fragments[2]
                    
        if 'name' in path_info and not path_info['name']:
            del path_info['name']
            
        return path_info
    
    
    def scan_repository_for_related(self, path, entity):
        related = None
        if path:
            path_info = self.decode_path(path)
            related = []
            self.logger.debug(u'Scanning repository for file related to %s.', path)
            for v in configuration.repository['Volume']:
                for k in configuration.repository['Kind']:
                    for p in configuration.repository['Kind'][k]['Profile']:
                        if k in configuration.kind_with_language:
                            for l in configuration.property_map['iso3t']['language']:
                                related_path_info = copy.deepcopy(path_info)
                                related_path_info['volume'] = v
                                related_path_info['kind'] = k
                                related_path_info['profile'] = p
                                related_path_info['language'] = l
                                related_path = theFileUtil.canonic_path(related_path_info, entity)
                                if os.path.exists(related_path):
                                    related.append(related_path)
                        else:
                            related_path_info = copy.deepcopy(path_info)
                            related_path_info['volume'] = v
                            related_path_info['kind'] = k
                            related_path_info['profile'] = p
                            related_path = theFileUtil.canonic_path(related_path_info, entity)
                            if os.path.exists(related_path):
                                related.append(related_path)
        return related
    
    
    
    def check_if_in_repository(self, path_info):
        return path_info and 'volume' in path_info and 'profile' in path_info
    
    
    def complete_path_info_default_values(self, path_info):
        result = True
        if 'kind' in path_info and path_info['kind'] in configuration.repository['Kind'].keys():
            kc = configuration.repository['Kind'][path_info['kind']]
            if 'profile' not in path_info:
                if 'default' in kc and 'profile' in kc['default']:
                    path_info['profile'] = kc['default']['profile']
                else:
                    result = False
                    self.logger.warning(u'Could not assign default profile for %s', unicode(path_info))
                    
            if result and not self.profile_valid_for_kind(path_info['profile'], path_info['kind']):
                result = False
                self.logger.warning(u'Profile %s is invalid for kind %s', path_info['profile'], path_info['kind'])
                
            if result:
                if 'volume' not in path_info:
                    if path_info['profile'] in kc['Profile'] and 'default' in kc['Profile'][path_info['profile']]:
                        dpc = kc['Profile'][path_info['profile']]['default']
                        if path_info['media kind'] in dpc:
                            if 'volume' in dpc[path_info['media kind']]:
                                path_info['volume'] = dpc[path_info['media kind']]['volume']
                if 'volume' not in path_info:
                    result = False
                    self.logger.warning(u'Could not assign default volume for %s', unicode(path_info))
        else:
            result = False
            if 'kind' in path_info:
                self.logger.warning(u'Invalid kind for %s', unicode(path_info))
            else:
                self.logger.warning(u'Unknow kind for %s', unicode(path_info))
                
        return result
    
    
    def copy_path_info(self, path_info, options):
        result = None
        if path_info:
            result = copy.deepcopy(path_info)
            result['volume'] = options.volume
            if result['volume'] is None:
                del result['volume']
                
            result['profile'] = options.profile
            if result['profile'] is None:
                del result['profile']
        return result
    
    
    
    def sort_field(self, value):
        if value:
            match = self.prefix_to_remove_from_sort.search(value)
            if match:
                value = match.group(2).strip()
                if not value:
                    value = None
        return value
    
    
    def simple_name(self, path_info, entity=None):
        result = None
        if entity and 'simple_name' in entity:
            result = entity['simple_name']
        elif 'name' in path_info:
            result = path_info['name']
        if result:
            result = self.characters_to_exclude_from_filename.sub(u'', result)
        return result
    
    
    def full_name(self, path_info, record):
        result = None
        if 'media kind' in path_info:
            if path_info['media kind'] == 10: # TV Show
                result = u''.join([record['tv show']['name'], u' s', u'{0:02d}'.format(record['entity']['tv_season']), u'e', u'{0:02d}'.format(record['entity']['tv_episode']), u' ',record['entity']['name']])
            elif path_info['media kind'] == 9: # Movie
                result = u''.join([u'IMDb', record['entity']['imdb_id'], u' ', record['entity']['name']])
        return result
    
    
    def canonic_name(self, path_info, entity=None):
        result = None
        valid = False
        
        if 'media kind' in path_info and 'kind' in path_info:
            if path_info['media kind'] == 10: # TV Show
                if 'tv show key' in path_info and 'tv episode id' in path_info:
                    result = u''.join([path_info['tv show key'], u' ', path_info['tv episode id']])
                    valid = True
            elif path_info['media kind'] == 9: # Movie
                if 'imdb id' in path_info:
                    result = u''.join([u'IMDb', path_info['imdb id']])
                    valid = True
        if valid:
            name = self.simple_name(path_info, entity)
            if name is not None:
                result = u''.join([result, u' ', name])
            result = u''.join([result, u'.', path_info['kind']])
        else:
            result = None
        
        return result
    
    
    def canonic_path(self, path_info, entity=None):
        result = None
        valid = True
        if 'kind' in path_info and path_info['kind'] in configuration.repository['Kind']:
            if 'volume' in path_info and path_info['volume'] in configuration.repository['Volume']:
                if 'profile' in path_info:
                    if self.profile_valid_for_kind(path_info['profile'], path_info['kind']):
                        result = os.path.join(configuration.repository['Volume'][path_info['volume']]['path'], configuration.property_map['code']['stik'][path_info['media kind']]['name'], path_info['kind'], path_info['profile'])
                        if path_info['media kind'] == 10 and 'tv show key' in path_info and 'tv season' in path_info:
                            result = os.path.join(result, path_info['tv show key'], str(path_info['tv season']))
                        
                        if path_info['kind'] in configuration.kind_with_language:
                            if 'language' in path_info:
                                lang = self.find_language(path_info['language'])
                                if lang:
                                    result = os.path.join(result, lang['iso3t'])
                                else:
                                    valid = False
                                    self.logger.warning(u'Unknown language for %s', unicode(path_info))
                            else:
                                valid = False
                                self.logger.warning(u'Missing language for %s', unicode(path_info))
                    else:
                        valid = False
                        self.logger.warning(u'Invalid profile for %s', unicode(path_info))
                else:
                    valid = False
                    self.logger.warning(u'Unknow profile for %s', unicode(path_info))
            else:
                valid = False
                if 'volume' in path_info:
                    self.logger.warning(u'Invalid volume for %s', unicode(path_info))
                else:
                    self.logger.warning(u'Unknow volume for %s', unicode(path_info))
        else:
            valid = False
            if 'kind' in path_info:
                self.logger.warning(u'Invalid kind for %s', unicode(path_info))
            else:
                self.logger.warning(u'Unknow kind for %s', unicode(path_info))
        
        if valid:
            result = os.path.join(result, self.canonic_name(path_info, entity))
            result = os.path.abspath(result)
        else:
            result = None
        return result
    
    
    def clean_if_not_exist(self, path):
        result = True
        if path:
            if not os.path.exists(path):
                result = False
                try:
                    os.removedirs(os.path.dirname(path))
                except OSError:
                    pass
        else:
            result = False
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
        return profile and kind and kind in configuration.repository['Kind'].keys() and profile in configuration.repository['Kind'][kind]['Profile'].keys()
        
    
    
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
        if command in configuration.repository['Command']:
            c = configuration.repository['Command'][command]
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
    
    
    
    def find_language(self, iso):
        result = None
        if len(iso) == 3:
            if iso in configuration.property_map['iso3t']['language']:
                result = configuration.property_map['iso3t']['language'][iso]
            elif iso in configuration.property_map['iso3b']['language']:
                result = configuration.property_map['iso3b']['language'][iso]
        elif len(iso) == 2 and iso in configuration.property_map['iso2']['language']:
            result = configuration.property_map['iso2']['language'][iso]
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
        m = configuration.property_map['name']['tag'][key]
        if 'subler' in m:
            pkey = m['subler']
            if m['type'] == 'enum':
                pvalue = configuration.property_map['code'][m['atom']][value]['print']
            elif m['type'] in ('string', 'list'):
                if m['type'] == 'list':
                    pvalue = u', '.join(value)
                else:
                    if key == 'language':
                        pvalue = configuration.property_map['iso3t']['language'][value]['print']
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
    
    
    
    def format_display_block(self, block, mapping):
        result = None
        result = [ theFileUtil.format_key_value(k, v, mapping) for k,v in block.iteritems() ]
        result = [ v for v in sorted(set(result)) if v ]
        if result:
            result = u'\n'.join(result)
        else:
            result = None
        return result
    
    
    def format_info_title(self, text):
        return FileUtil.format_info_title_display.format(text)
    
    
    def format_info_subtitle(self, text):
        return FileUtil.format_info_subtitle_display.format(text)
    
    
    def format_byte_as_iec_60027_2(self, value):
        result = None
        if value:
            p = 0
            v = float(value)
            while v > 1024 and p < 4:
                p += 1
                v /= 1024.0
            result = '{0:.2f} {1}'.format(v, FileUtil.binary_iec_60027_2_prefix[p])
        return result
    
    
    def format_bit_as_si(self, value):
        result = None
        if value:
            p = 0
            v = float(value)
            while v > 1000 and p < 4:
                p += 1
                v /= 1000.0
            result = '{0:.2f} {1}'.format(v, FileUtil.decimal_si_prefix[p])
        return result
    
    
    def format_key_value(self, key, value, mapping=None):
        pkey = None
        pvalue = None
        result = None
        if mapping:
            m = mapping[key]
            if not ('display' in m and not m['display']):
                pkey = m['print']
                ptype = m['type']
                if ptype == 'enum':
                    pvalue = configuration.property_map['code'][m['atom']][value]['print']
                    
                elif ptype in ('string', 'list'):
                    if ptype == 'list':
                        pvalue = u', '.join(value)
                    else:
                        if key == 'language':
                            lang = self.find_language(value)
                            pvalue = lang['print']
                        else:
                            pvalue = unicode(value)
                    if len(pvalue) > FileUtil.format_wrap_width:
                        lines = textwrap.wrap(pvalue, FileUtil.format_wrap_width)
                        pvalue = FileUtil.format_indent.join(lines)
                        
                elif ptype == 'float':
                    pvalue = u'{0:.3f}'.format(value)
                    
                elif ptype == 'bool':
                    if value:
                        pvalue = u'yes'
                    else:
                        pvalue = u'no'
                        
                elif ptype == 'int':
                    if 'format' in m:
                        pformat = m['format']
                        if pformat == 'bitrate':
                            pvalue = '{0}/s'.format(self.format_bit_as_si(value))
                        elif pformat == 'millisecond':
                            pvalue = self.miliseconds_to_time(value)
                        elif pformat == 'byte':
                            pvalue = self.format_byte_as_iec_60027_2(value)
                        elif pformat == 'bit':
                            pvalue = '{0} bit'.format(value)
                        elif pformat == 'frequency':
                            pvalue = '{0} Hz'.format(value)
                        elif pformat == 'pixel':
                            pvalue = '{0} px'.format(value)
                        else:
                            pvalue = unicode(value)
                    else:
                        pvalue = unicode(value)
                        
                else:
                    pvalue = value
                
            else:
                pass
        else:
            pkey = key
            pvalue = value
            
        if pvalue:
            result = FileUtil.format_key_value_display.format(pkey, pvalue)
        return result
    
    
    def format_value(self, value):
        return FileUtil.format_value_display.format(value)
    
    
    format_indent = u'\n' + u' '* configuration.repository['Display']['indent']
    format_wrap_width = configuration.repository['Display']['wrap']
    
    format_khz_display = u'{0}kHz'
    format_info_title_display = u'\n\n\n{1}[{{0:-^{0}}}]'.format(configuration.repository['Display']['wrap'] + configuration.repository['Display']['indent'], u' ' * configuration.repository['Display']['margin'])
    format_info_subtitle_display = u'\n{1}[{{0:^{0}}}]\n'.format(configuration.repository['Display']['indent'] - configuration.repository['Display']['margin'] - 3, u' ' * configuration.repository['Display']['margin'])
    format_key_value_display = u'{1}{{0:-<{0}}}: {{1}}'.format(configuration.repository['Display']['indent'] - configuration.repository['Display']['margin'] - 2, u' ' * configuration.repository['Display']['margin'])
    format_value_display = u'{0}{{0}}'.format(u' ' * configuration.repository['Display']['margin'])
    
    full_numeric_time_format = re.compile('([0-9]{,2}):([0-9]{,2}):([0-9]{,2})(?:\.|,)([0-9]+)')
    characters_to_exclude_from_filename = re.compile(ur'[\\\/?<>:*|\'"^\.]')
    escaped_subler_tag_characters = set(('{', '}', ':'))
    binary_iec_60027_2_prefix = {0:'Byte', 1:'KiB', 2:'MiB', 3:'GiB', 4:'TiB'}
    decimal_si_prefix = {0:'bit', 1:'kbit', 2:'Mbit', 3:'Gbit', 4:'Tbit'}
    sentence_end = re.compile(ur'[.!?]')
    whitespace_re = re.compile(ur'\s+', re.UNICODE)
    
    
    mediainfo_integer_list = re.compile('[0-9]+(?:\s*/\s*[0-9]+)+')
    prefix_to_remove_from_sort = re.compile('^(the |a )(.+)$', re.IGNORECASE)
    clean_xml = re.compile(ur'\s+/\s+(?:\t)*', re.UNICODE)
    itunextc_structure = re.compile(ur'([^|]+)\|([^|]+)\|([^|]+)\|([^|]+)?')
    true_value = re.compile(ur'yes|true|1', re.IGNORECASE)
    full_utc_datetime = re.compile(u'(?:UTC )?([0-9]{4})(?:-([0-9]{2})(?:-([0-9]{2})(?: ([0-9]{2}):([0-9]{2}):([0-9]{2}))?)?)?', re.UNICODE)
    mediainfo_chapter_timecode = re.compile(u'_([0-9]{2})_([0-9]{2})_([0-9]{2})\.([0-9]{3})')
    mp4info_tag = re.compile(u' ([^:]+): (.*)$')


# Singleton
theSubtitleFilter = SubtitleFilter()
theFileUtil = FileUtil()



