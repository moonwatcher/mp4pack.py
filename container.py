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
from subprocess import Popen, PIPE
import xml.etree.cElementTree as ElementTree


class ContainerFactory(object):
    def __init__(self, entity_manager):
        self.logger = logging.getLogger('Container Factory')
        self.entity_manager = entity_manager
        self.configuration = entity_manager.configuration
        self.util = FileUtil(self)
        self.subtitle_filter = SubtitleFilter(self)
    
    
    def create_media_file(self, path):
        mf= None
        kind = os.path.splitext(path)[1].strip('.')
        if kind in self.configuration.lookup['container']['mp4']['kind']:
            mf = Mpeg4(self, path, autoload=False)
        elif kind in self.configuration.lookup['container']['matroska']['kind']:
            mf = Matroska(self, path, autoload=False)
        elif kind in self.configuration.lookup['container']['subtitles']['kind']:
            mf = Subtitle(self, path, autoload=False)
        elif kind in self.configuration.lookup['container']['chapters']['kind']:
            mf = Chapter(self, path, autoload=False)
        elif kind in self.configuration.lookup['container']['image']['kind']:
            mf = Artwork(self, path, autoload=False)
        elif kind in self.configuration.lookup['container']['raw audio']['kind']:
            mf = RawAudio(self, path, autoload=False)
        elif kind in self.configuration.lookup['container']['avi']['kind']:
            mf = Avi(self, path, autoload=False)
            
        return mf
    
    
    def clean(self, options):
        total = 0
        
        # Cleanup orphan physical references in movies
        saved_movie = 0
        movie_ids = self.entity_manager.list_all_movie_imdbs()
        for movie_id in movie_ids:
            if 'imdb_id' in movie_id:
                need_save = False
                movie = self.entity_manager.find_movie_by_imdb_id(movie_id['imdb_id'])
                if movie and 'physical' in movie:
                    phy = copy.deepcopy(movie['physical'].keys())
                    for uri in phy:
                        path = self.configuration.canonic_path_from_uri(uri)
                        if path is None or not os.path.exists(path):
                            self.logger.debug(u'Dropping physical index for orphan %s', uri)
                            del movie['physical'][uri]
                            need_save = True
                    if not movie['physical']:
                        del movie['physical']
                        need_save = True
                    if need_save:
                        self.entity_manager.save_movie(movie)
                        saved_movie += 1
        total += saved_movie
        self.logger.info(u'Removed orphans from %d movies', saved_movie)
        
        # Cleanup orphan physical references in episodes
        saved_episode = 0
        episode_ids = self.entity_manager.list_all_tv_show_episode_ids()
        for episode_id in episode_ids:
            if '_id' in episode_id:
                need_save = False
                episode = self.entity_manager.find_episode_by_id(episode_id['_id'])
                if episode and 'physical' in episode:
                    phy = copy.deepcopy(episode['physical'].keys())
                    for uri in phy:
                        path = self.configuration.canonic_path_from_uri(uri)
                        if path is None or not os.path.exists(path):
                            self.logger.info(u'Dropping physical index for orphan %s', uri)
                            del episode['physical'][uri]
                            need_save = True
                    if not episode['physical']:
                        del episode['physical']
                        need_save = True
                    if need_save:
                        self.entity_manager.save_tv_episode(episode)
                        saved_episode += 1
        total += saved_episode
        self.logger.info(u'Removed orphans from %d tv episodes', saved_episode)
        
        self.logger.info(u'Removed orphans from a total of %d files', saved_episode)
    



# Container super class
class Container(object):
    def __init__(self, factory, file_path, autoload=True):
        self.logger = logging.getLogger('Container')
        self.factory = factory
        self.file_path = file_path
        self.uri = self.factory.configuration.uri_from_canonic_path(file_path)
        self.path_info = None
        self.record = None
        self.info = None
        self.meta = None
        
        self.unindexed = []
        self.ghost = []
        
        # Processing time
        self.processing = {'start':None, 'finish':None, 'duration':None, 'processed':False}
    
    
    def valid(self):
        return self.path_info is not None and self.info is not None
    
    
    def in_repository(self):
        return self.factory.util.check_if_in_repository(self.path_info)
    
    
    def load(self, refresh=False, download=False):
        
        # Start process tracking
        self.processing['start'] = datetime.utcnow()
        
        result = False
        result = Container.load_path_info(self)
        if result:
            result = self.load_record(refresh, download)
            if result:
                result = self.load_info()
                if not result:
                    self.logger.warning(u'Could not load info for %s',self.file_path)
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
            self.path_info = self.factory.configuration.decode_path(self.file_path)
        return self.path_info is not None
    
    
    def load_record(self, refresh=False, download=False):
        result = False
        if self.path_info:
            if self.is_movie():
                entity = self.factory.entity_manager.find_movie_by_imdb_id(self.path_info['imdb id'], download)
                if entity:
                    self.record = {}
                    self.record['entity'] = entity
                    result = True
                    
            elif self.is_tvshow():
                show, episode = self.factory.entity_manager.find_episode(self.path_info['tv show key'], self.path_info['tv season'], self.path_info['tv episode #'], download)
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
            if self.uri and self.uri in self.record['entity']['physical'] and not refresh:
                self.info = self.record['entity']['physical'][self.uri]['info']
            else:
                self.info = self.factory.util.decode_info(self.file_path)
                if self.uri and self.info:
                    self.record['entity']['physical'][self.uri] = {}
                    self.record['entity']['physical'][self.uri]['path info'] = self.path_info
                    self.record['entity']['physical'][self.uri]['info'] = self.info
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
            self.meta['sort artist'] = self.factory.util.sort_field(self.record['tv show']['tvdb_record']['name'])
            self.meta['sort album artist'] = self.factory.util.sort_field(self.record['tv show']['tvdb_record']['name'])
            
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
                if 'released' in movie['tmdb_record'] and movie['tmdb_record']['released']:
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
                    self.meta['sort tv show'] = self.factory.util.sort_field(show['tvdb_record']['name'])
                if 'name' in show['tvdb_record'] and 'tv_season' in episode['tvdb_record']:
                    album_name = u'{0}, Season {1}'.format(show['tvdb_record']['name'], unicode(episode['tvdb_record']['tv_season']))
                    self.meta['album'] = album_name
                    self.meta['sort album'] = self.factory.util.sort_field(album_name)
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
                    self.meta['sort name'] = self.factory.util.sort_field(episode['tvdb_record']['name'])
                    
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
        
        # Finish process tracking
        self.processing['finish'] = datetime.utcnow()
        self.processing['duration'] = self.processing['finish'] - self.processing['start']
    
    
    def refresh_index(self, queue=None):
        if self.record:
            if 'physical' not in self.record['entity']:
                self.record['entity']['physical'] = {}
            
            if queue is None:
                queue = self.factory.configuration.scan_repository_for_related(self.file_path, self.record['entity'])
            
            if queue:
                discovered = 0
                for path in queue:
                    if path not in self.record['entity']['physical']:
                        related_path_info = self.factory.configuration.decode_path(path)
                        if self.factory.util.check_if_in_repository(related_path_info):
                            uri = self.factory.configuration.uri_from_canonic_path(path)
                            if uri:
                                self.logger.debug(u'Indexing %s.', uri)
                                self.record['entity']['physical'][uri] = {}
                                self.record['entity']['physical'][uri]['uri'] = uri
                                self.record['entity']['physical'][uri]['path info'] = related_path_info
                                self.record['entity']['physical'][uri]['info'] = self.factory.util.decode_info(path)
                                discovered += 1
                if discovered:
                    self.save_record()
                    self.logger.debug(u'Indexed %s files related to %s in repository.', discovered, self.file_path)
    
    
    def drop_index(self, queue=None):
        if self.record and 'entity' in self.record and 'physical' in self.record['entity']:
            need_save = False
            if queue:
                for path in queue:
                    uri = self.factory.configuration.uri_from_canonic_path(path)
                    if uri in self.record['entity']['physical']:
                        self.logger.debug(u'Dropping physical index for %s', uri)
                        del self.record['entity']['physical'][uri]
                        need_save = True
                if not self.record['entity']['physical']:
                    del self.record['entity']['physical']
                    need_save = True
            else:
                self.logger.debug(u'Dropping all related physical index for %s', self.file_path)
                del self.record['entity']['physical']
                need_save = True
            if need_save: self.save_record()
    
    
    def save_record(self):
        if self.is_movie():
            self.factory.entity_manager.save_movie(self.record['entity'])
        elif self.is_tvshow():
            self.factory.entity_manager.save_tv_episode(self.record['entity'])
    
    
    def queue_for_index(self, path):
        if path not in self.unindexed:
            self.unindexed.append(path)
        if path not in self.ghost:
            self.ghost.append(path)
    
    
    def drop_from_index(self, path):
        if path not in self.ghost:
            self.ghost.append(path)
    
    
    def clean(self, options):
        for uri in self.record['entity']['physical'].keys():
            path = self.factory.configuration.canonic_path_from_uri(uri)
            if not os.path.exists(path):
                self.logger.info(u'Found orphan %s', uri)
                self.drop_from_index(path)
    
    
    def related(self):
        related = {}
        for k,v in self.record['entity']['physical'].iteritems():
            related[k] = v['path info']
        return related
    
    
    
    def mark_as_processed(self):
        self.processing['processed'] = True
    
    
    def processed(self):
        return self.processing['processed']
    
    
    def processing_duration(self):
        result = None
        if self.processing['duration']:
            result = abs(self.processing['duration'])
        return result
    
    
    
    def report_info(self, options):
        self.mark_as_processed()
        return unicode(self)
    
    
    def copy(self, options):
        self.mark_as_processed()
        result = None
        path_info = self.factory.configuration.resolve_path_info(self.path_info, {'volume':options.volume, 'profile':options.profile})
        if path_info:
            dest_path = self.factory.configuration.encode_path(path_info, self.record['entity'])
            if self.factory.util.varify_if_path_available(dest_path, options.overwrite):
                command = self.factory.util.initialize_command('rsync', self.logger)
                if command:
                    command.extend([self.file_path, dest_path])
                    message = u'Copy ' + self.file_path + u' --> ' + dest_path
                    self.factory.util.execute(command, message, options.debug, pipeout=True, pipeerr=False, logger=self.logger)
                    if self.factory.util.clean_if_not_exist(dest_path):
                        result = dest_path
                        self.queue_for_index(dest_path)
                        if options.md5:
                            self.compare_checksum(dest_path)
        return result
    
    
    def delete(self):
        self.mark_as_processed()
        if self.path_info:
            self.drop_from_index(self.file_path)
            self.logger.debug(u'Delete %s',self.file_path)
            self.factory.util.clean(self.file_path)
    
    
    def rename(self, options):
        self.mark_as_processed()
        dest_path = os.path.join(os.path.dirname(self.file_path), self.canonic_file_name())
        if os.path.exists(dest_path) and os.path.samefile(self.file_path, dest_path):
            self.logger.debug(u'No renaming needed for %s',dest_path)
        else:
            if self.factory.util.check_if_path_available(dest_path, False):
                self.factory.util.varify_directory(dest_path)
                command = self.factory.util.initialize_command('mv', self.logger)
                if command:
                    command.extend([self.file_path, dest_path])
                    message = u'Rename {0} --> {1}'.format(self.file_path, dest_path)
                    self.factory.util.execute(command, message, options.debug, pipeout=True, pipeerr=False, logger=self.logger)
                    self.drop_from_index(self.file_path)
                    self.queue_for_index(dest_path)
            else:
                self.logger.warning(u'Not renaming %s, destination exists: %s', self.file_path, dest_path)
    
    
    def tag(self, options):
        self.mark_as_processed()
        self.load_meta()
    
    
    def optimize(self, options):
        self.mark_as_processed()
    
    
    def extract(self, options):
        self.mark_as_processed()
        return []
    
    
    def pack(self, options):
        self.mark_as_processed()
    
    
    def transcode(self, options):
        self.mark_as_processed()
    
    
    def update(self, options):
        self.mark_as_processed()
    
    
    
    
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
                for i in self.factory.configuration.lookup['name']['itunemovi']:
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
                for i in self.factory.configuration.lookup['name']['itunemovi']:
                    if not self.meta[i]:
                        del self.meta[i]
        return
        
    
    
    
    def download_artwork(self, options):
        result = False
        path_info = self.factory.configuration.resolve_path_info(
            self.path_info, 
            {'volume':options.volume, 'profile':options.profile, 'kind':'png'}
        )
        if path_info:
            selected = []
            lookup = {'kind':'png', 'profile':path_info['profile']}
            for (path, phy) in self.record['entity']['physical'].iteritems():
                if all((k in phy['path info'] and phy['path info'][k] == v) for k,v in lookup.iteritems()):
                    selected.append(path)
                    break
            if not selected or options.sync:
                artwork = None
                if self.is_movie():
                    artwork = self.factory.entity_manager.find_tmdb_movie_poster(self.path_info['imdb id'])
                elif self.is_tvshow():
                    artwork = self.factory.entity_manager.find_tvdb_episode_poster(self.path_info['tv show key'], self.path_info['tv season'], self.path_info['tv episode #'])
                if artwork and 'cache' in artwork:
                    path_info['kind'] = artwork['cache']['kind']
                    if 'volume' in path_info: del path_info['volume']
                    image = Artwork(self.factory, artwork['cache']['path'], False)
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
                self.logger.info(u'md5 match: %s %s',source_md5, self.canonic_file_name())
                result = True
            else:
                self.logger.error(u'md5 mismatch: %s is not %s for %s', source_md5, dest_md5, self.canonic_file_name())
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
    
    
    def canonic_file_name(self):
        return self.factory.configuration.encode_file_name(self.path_info, self.record['entity'])
    
    
    def canonic_path(self):
        return self.factory.configuration.encode_path(self.path_info, self.record['entity'])
    
    
    
    def print_meta(self):
        return self.factory.util.format_display_block(self.meta, self.factory.configuration.lookup['name']['tag'])
    
    
    def print_related(self):
        result = None
        related = self.related()
        if related:
            result = (u'\n'.join([self.factory.util.format_value(key) for key in sorted(set(related))]))
        return result
    
    
    def print_path_info(self):
        return self.factory.util.format_display_block(self.path_info, self.factory.configuration.lookup['name']['tag'])
    
    
    def print_file_info(self):
        return self.factory.util.format_display_block(self.info['file'], self.factory.configuration.lookup['name']['file'])
    
    
    def print_tracks(self):
        return (u'\n\n\n'.join([self.factory.util.format_display_block(track, self.factory.configuration.lookup['name']['track'][track['type']]) for track in self.info['track']]))
    
    
    def print_tags(self):
        return self.factory.util.format_display_block(self.info['tag'], self.factory.configuration.lookup['name']['tag'])
    
    
    def print_chapter_markers(self):
        return (u'\n'.join([self.factory.util.format_value(ChapterMarker(self, marker['time'], marker['name'])) for marker in self.info['menu']]))
    
    
    def __unicode__(self):
        result = None
        result = self.factory.util.format_info_title(self.info['file']['name'])
        
        related = self.related()
        if related:
            result = u'\n'.join((result, self.factory.util.format_info_subtitle(u'related'), self.print_related()))
        
        if self.info['file']:
            result = u'\n'.join((result, self.factory.util.format_info_subtitle(u'file info'), self.print_file_info()))
        if self.path_info:
            result = u'\n'.join((result, self.factory.util.format_info_subtitle(u'path info'), self.print_path_info()))
        
        if self.info['menu']:
            result = u'\n'.join((result, self.factory.util.format_info_subtitle(u'menu'), self.print_chapter_markers()))
        
        if self.info['tag']:
            tag_block = self.print_tags()
            if tag_block:
                result = u'\n'.join((result, self.factory.util.format_info_subtitle(u'tags'), tag_block))
        
        #self.load_meta()
        if self.meta:
            result = u'\n'.join((result, self.factory.util.format_info_subtitle(u'metadata'), self.print_meta()))
        
        if self.info['track']:
            result = u'\n'.join((result, self.factory.util.format_info_subtitle(u'tracks'), self.print_tracks()))
        return result
    
    


# Audio / Video Container super class
class AudioVideoContainer(Container):
    def __init__(self, factory, file_path, autoload=True):
        Container.__init__(self, factory, file_path, autoload)
        self.logger = logging.getLogger('A/V Container')
    
    
    def valid(self):
        result = Container.valid(self)
        if result and not('track' in self.info and self.info['track']):
            self.logger.warning(u'Failed to decode track information for %s',self.file_path)
            result = False
        return result
    
    
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
        return self.video_width() > self.factory.configuration.user_config['hd threshold']
    
    
    def playback_height(self):
        result = 0
        v = self.main_video_track()
        if v:
            if v['display aspect ratio'] >= self.factory.configuration.user_config['playback']['aspect ratio']:
                result = float(v['width']) / float(self.factory.configuration.user_config['playback']['aspect ratio'])
            else:
                result = float(v['height'])
        return result
    
    
    def audio_tracks(self):
        return [ t for t in self.info['track'] if 'type' in t and t['type'] == 'audio']
    
    
    def extract(self, options):
        result = Container.extract(self, options)
        if self.info['menu']:
            path_info = self.factory.configuration.resolve_path_info(
                self.path_info, 
                {'volume':options.volume, 'profile':options.profile, 'kind':'txt'}
            )
            if path_info:
                dest_path = self.factory.configuration.encode_path(path_info, self.record['entity'])
                if self.factory.util.varify_if_path_available(dest_path, options.overwrite):
                    c = Chapter(self.factory, dest_path, False)
                    c.start()
                    for marker in self.info['menu']:
                        c.add_chapter_marker(marker['time'], marker['name'])
                    self.logger.info(u'Extracting chapter markers from %s --> %s', self.file_path, dest_path)
                    c.delete()
                    c.write(dest_path)
                    c.unload()
                    if self.factory.util.clean_if_not_exist(dest_path):
                        result.append(dest_path)
                        self.queue_for_index(dest_path)
        return result
    
    
    def pack(self, options):
        Container.pack(self, options)
        
        if options.pack in ('m4v', 'mkv'):
            path_info = self.factory.configuration.resolve_path_info(
                self.path_info, 
                {'volume':options.volume, 'profile':options.profile, 'kind':options.pack}
            )
            if path_info:
                dest_path = self.factory.configuration.encode_path(path_info, self.record['entity'])
                if dest_path and self.factory.util.varify_if_path_available(dest_path, options.overwrite):
                    pc = self.factory.configuration.kind[path_info['kind']]['profile'][path_info['profile']]
                    
                    # Packing into m4v with Subler
                    if path_info['kind'] == 'm4v':
                        command = self.factory.util.initialize_command('subler', self.logger)
                        if command:
                            command.extend([u'-o', dest_path, u'-i', self.file_path])
                            
                            message = u'Pack {0} --> {1}'.format(self.file_path, dest_path)
                            self.factory.util.execute(command, message, options.debug, pipeout=False, pipeerr=False, logger=self.logger)
                            if self.factory.util.clean_if_not_exist(dest_path):
                                self.queue_for_index(dest_path)
                                
                    # Packing into Matroska with mkvmerge
                    elif path_info['kind'] == 'mkv':
                        selected = { 'related':{}, 'track':{} }
                        
                        if 'pack' in pc:
                            # locate related files that need to be muxed in
                            if 'related' in pc['pack']:
                                for phy in self.record['entity']['physical'].values():
                                    for c in pc['pack']['related']:
                                        if all((k in phy['path info'] and phy['path info'][k] == v) for k,v in c.iteritems()):
                                            if phy['path info']['kind'] not in selected['related']:
                                                selected['related'][phy['path info']['kind']] = []
                                            path = self.factory.configuration.canonic_path_from_uri(phy['uri'])
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
                                            
                            command = self.factory.util.initialize_command('mkvmerge', self.logger)
                            if command:
                                command.extend([
                                    u'--output', 
                                    dest_path, 
                                    u'--no-global-tags', 
                                    u'--no-track-tags', 
                                    u'--no-chapters', 
                                    u'--no-attachments', 
                                    u'--no-subtitles'
                                ])
                                
                                full_name = None
                                if 'name' in self.record['entity']:
                                    full_name = self.factory.configuration.encode_full_name(self.path_info, self.record)
                                    if full_name:
                                        command.append(u'--title')
                                        command.append(full_name)
                                for t in selected['track']['video']:
                                    if full_name:
                                        command.append(u'--track-name')
                                        command.append(u'{0}:{1}'.format(t['id'], full_name))
                                    if 'language' in t:
                                        command.append(u'--language')
                                        command.append(u'{0}:{1}'.format(t['id'], self.factory.configuration.find_language(t['language'])['iso2']))
                                        
                                for t in selected['track']['audio']:
                                    if 'channels' in t:
                                        if t['channels'] < 2: tname = 'Mono'
                                        elif t['channels'] > 2: tname = 'Surround'
                                        else: tname = 'Stereo'
                                        command.append(u'--track-name')
                                        command.append(u'{0}:{1}'.format(t['id'], tname))
                                    if 'language' in t:
                                        command.append(u'--language')
                                        command.append(u'{0}:{1}'.format(t['id'], self.factory.configuration.find_language(t['language'])['iso2']))
                                        
                                command.append(u'--audio-tracks')
                                command.append(u','.join([ unicode(k['id']) for k in selected['track']['audio'] ]))
                                command.append(u'--video-tracks')
                                command.append(u','.join([ unicode(k['id']) for k in selected['track']['video'] ]))
                                command.append(self.file_path)
                                
                                if 'ac3' in selected['related']:
                                    for r in selected['related']['ac3']:
                                        ac3_path = self.factory.configuration.canonic_path_from_uri(r)
                                        if ac3_path:
                                            # try to locate the DTS sound track from which the AC-3 track was transcoded
                                            # if a match is found duplicate the delay
                                            # checking exact duration or sample cound migth be more accurate
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
                                            command.append(u'0:{0}'.format(self.factory.configuration.find_language(ac3_record['path info']['language'])['iso2']))
                                            command.append(ac3_path)
                                        
                                if 'srt' in selected['related']:
                                    for r in selected['related']['srt']:
                                        srt_path = self.factory.configuration.canonic_path_from_uri(r)
                                        if srt_path:
                                            path_info = self.record['entity']['physical'][r]['path info']
                                            command.append(u'--sub-charset')
                                            command.append(u'0:UTF-8')
                                            command.append(u'--language')
                                            command.append(u'0:{0}'.format(self.factory.configuration.find_language(path_info['language'])['iso2']))
                                            command.append(srt_path)
                                            
                                if 'txt' in selected['related']:
                                    for r in selected['related']['txt']:
                                        txt_path = self.factory.configuration.canonic_path_from_uri(r)
                                        if txt_path:
                                            command.append(u'--chapter-language')
                                            command.append(u'en')
                                            command.append(u'--chapter-charset')
                                            command.append(u'UTF-8')
                                            command.append(u'--chapters')
                                            command.append(txt_path)
                                            break
                                            
                                message = u'Pack {0} --> {1}'.format(self.file_path, dest_path)
                                self.factory.util.execute(command, message, options.debug, pipeout=False, pipeerr=False, logger=self.logger)
                                if self.factory.util.clean_if_not_exist(dest_path):
                                    self.queue_for_index(dest_path)
    
    
    def transcode(self, options):
        Container.transcode(self, options)
        
        result = None
        if options.transcode in ('m4v', 'mkv'):
            path_info = self.factory.configuration.resolve_path_info(
                self.path_info, 
                {'volume':options.volume, 'profile':options.profile, 'kind':options.transcode}
            )
            if path_info:
                dest_path = self.factory.configuration.encode_path(path_info, self.record['entity'])
                if dest_path and self.factory.util.varify_if_path_available(dest_path, options.overwrite):
                    command = self.factory.util.initialize_command('handbrake', self.logger)
                    if command:
                        tc = self.factory.configuration.kind[path_info['kind']]['profile'][path_info['profile']]['transcode']
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
                        self.factory.util.execute(command, message, options.debug, pipeout=False, pipeerr=False, logger=self.logger)
                        if self.factory.util.clean_if_not_exist(dest_path):
                            self.queue_for_index(dest_path)
                            result = dest_path
                            
        return result
    
    
    def __unicode__(self):
        return Container.__unicode__(self)
    


# Text File
class Text(Container):
    def __init__(self, factory, file_path, autoload=True):
        Container.__init__(self, factory, file_path, autoload)
        self.logger = logging.getLogger('Text')
    
    
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
        
        path_info = self.factory.configuration.resolve_path_info(
            self.path_info, 
            {'volume':options.volume, 'profile':options.profile, 'kind':options.transcode}
        )
        if path_info:
            dest_path = self.factory.configuration.encode_path(path_info, self.record['entity'])
            if dest_path and self.factory.util.varify_if_path_available(dest_path, options.overwrite):
                self.logger.info(u'Transcode %s --> %s', self.file_path, dest_path)
                self.write(dest_path)
                if self.factory.util.clean_if_not_exist(dest_path):
                    self.queue_for_index(dest_path)
                    result = dest_path
        return result
    


# Artwork Class
class Artwork(Container):
    def __init__(self, factory, file_path, autoload=True):
        Container.__init__(self, factory, file_path, autoload)
        self.logger = logging.getLogger('Artwork')
        if autoload:
            self.load()
    
    
    def transcode(self, options):
        Container.transcode(self, options)
        
        result = None
        path_info = self.factory.configuration.resolve_path_info(
            self.path_info, 
            {'volume':options.volume, 'profile':options.profile, 'kind':options.transcode}
        )
        if path_info:
            dest_path = self.factory.configuration.encode_path(path_info, self.record['entity'])
            if dest_path and self.factory.util.varify_if_path_available(dest_path, options.overwrite):
                p = self.factory.configuration.kind[path_info['kind']]['profile'][path_info['profile']]
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
                        
                        if self.factory.util.clean_if_not_exist(dest_path):
                            self.queue_for_index(dest_path)
                            result = dest_path
        return result
    


# Avi Class
class Avi(AudioVideoContainer):
    def __init__(self, factory, file_path, autoload=True):
        AudioVideoContainer.__init__(self, factory, file_path, autoload)
        self.logger = logging.getLogger('Avi')
        if autoload:
            self.load()
    


# Matroska Class
class Matroska(AudioVideoContainer):
    def __init__(self, factory, file_path, autoload=True):
        AudioVideoContainer.__init__(self, factory, file_path, autoload)
        self.logger = logging.getLogger('Matroska')
        if autoload:
            self.load()
    
    
    def extract(self, options):
        result = AudioVideoContainer.extract(self, options)
        selected = {
            'track':[], 
            'path':{ 'text':[], 'audio':[] },
            'extract':{ 'text':[], 'audio':[] }
        }
        
        
        path_info = self.factory.configuration.resolve_path_info(
            self.path_info, 
            {'volume':options.volume, 'profile':options.profile}
        )
        if path_info:
            for k in ('srt', 'ass', 'dts'):
                if self.factory.configuration.resolve_path_info(path_info, {'volume':options.volume, 'profile':'dump', 'kind':k}):
                    pc = self.factory.configuration.kind[path_info['kind']]['profile'][path_info['profile']]
                    if 'extract' in pc and 'tracks' in pc['extract']:
                        for t in self.info['track']:
                            for c in pc['extract']['tracks']:
                                if all((k in t and t[k] == v) for k,v in c.iteritems()):
                                    t['kind'] = k
                                    selected['track'].append(t)
                                    break
        if selected['track']:
            command = self.factory.util.initialize_command('mkvextract', self.logger)
            if command:
                command.extend([u'tracks', self.file_path ])
                for t in selected['track']:
                    track_path_info = self.factory.configuration.resolve_path_info(path_info, {
                        'volume':options.volume,
                        'profile':'dump', 
                        'kind':t['kind'], 
                        'language':t['language']
                    })
                    if track_path_info:
                        dest_path = self.factory.configuration.encode_path(track_path_info, self.record['entity'])
                        if dest_path not in selected['path'][t['type']] and self.factory.util.varify_if_path_available(dest_path, options.overwrite):
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
            self.factory.util.execute(command, message, options.debug, pipeout=False, pipeerr=False, logger=self.logger)
            
        for k in selected['path']:
            for p in selected['path'][k]:
                if self.factory.util.clean_if_not_exist(p):
                    selected['extract'][k].append(p)
                    
        if selected['extract']['text']:
            o = copy.deepcopy(options)
            o.transcode = 'srt'
            o.profile = None
            o.extract = None
            for p in selected['extract']['text']:
                s = Subtitle(self.factory, p)
                o.profile = 'original'
                ts = s.transcode(o)
                o.profile = 'clean'
                ts = s.transcode(o)
                s.delete()
                s.unload()
                if self.factory.util.clean_if_not_exist(ts):
                    result.append(ts)
                    
        if selected['extract']['audio']:
            o = copy.deepcopy(options)
            o.transcode = 'ac3'
            o.extract = None
            o.profile = None
            for p in selected['extract']['audio']:
                a = RawAudio(self.factory, p)
                ta = a.transcode(o)
                a.delete()
                a.unload()
                if self.factory.util.clean_if_not_exist(ta):
                    result.append(ta)
        return result
    
    


# Mpeg4 Class
class Mpeg4(AudioVideoContainer):
    def __init__(self, factory, file_path, autoload=True):
        AudioVideoContainer.__init__(self, factory, file_path, autoload)
        self.logger = logging.getLogger('MP4')
        if autoload:
            self.load()
    
    
    def tag(self, options):
        AudioVideoContainer.tag(self, options)
        tc = None
        update = {}
        if self.meta:
            for k in [
                k for k,v in self.meta.iteritems()
                if self.factory.configuration.lookup['name']['tag'][k]['subler'] 
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
            tc = u''.join([self.factory.util.format_key_value_for_subler(t, update[t]) for t in sorted(set(update))])
            message = u'Update tags: {0} --> {1}'.format(u', '.join([self.factory.configuration.lookup['name']['tag'][t]['print'] for t in sorted(set(update.keys()))]), self.file_path)
            command = self.factory.util.initialize_command('subler', self.logger)
            if command:
                command.extend([u'-o', self.file_path, u'-t', tc])
                self.factory.util.execute(command, message, options.debug, pipeout=True, pipeerr=False, logger=self.logger)
                self.queue_for_index(self.file_path)
            
        else:
            self.logger.info(u'No tags need update in %s', self.file_path)
    
    
    def optimize(self, options):
        AudioVideoContainer.optimize(self, options)
        message = u'Optimize {0}'.format(self.file_path)
        command = self.factory.util.initialize_command('subler', self.logger)
        if command:
            command.extend([u'-O', u'-o', self.file_path])
            self.factory.util.execute(command, message, options.debug, pipeout=True, pipeerr=False, logger=self.logger)
            self.queue_for_index(self.file_path)
        
    
    
    def _update_artwork(self, options):
        AudioVideoContainer.tag(self, options)
        if options.update in ('png', 'jpg'):
            path_info = self.factory.configuration.resolve_path_info(self.path_info, {
                'volume':options.volume, 
                'profile':options.profile, 
                'kind':options.update
            })
            if path_info:
                if options.download:
                    self.download_artwork(options)
                    
                selected = []
                lookup = {'kind':path_info['kind'], 'profile':path_info['profile']}
                for phy in self.record['entity']['physical'].values():
                    if all((k in phy['path info'] and phy['path info'][k] == v) for k,v in lookup.iteritems()):
                        path = self.factory.configuration.canonic_path_from_uri(phy['uri'])
                        if path:
                            selected.append(path)
                            break
                            
                if selected:
                    message = u'Update artwork {0} --> {1}'.format(selected[0], self.file_path)
                    command = self.factory.util.initialize_command('subler', self.logger)
                    if command:
                        command.extend([u'-o', self.file_path, u'-t', u'{{{0}:{1}}}'.format(u'Artwork', selected[0])])
                        self.factory.util.execute(command, message, options.debug, pipeout=True, pipeerr=False, logger=self.logger)
                        self.queue_for_index(self.file_path)
                else:
                    self.logger.warning(u'No artwork available for %s', self.file_path)
    
    
    def _update_srt(self, options):
        if options.update in ('srt'):
            path_info = self.factory.configuration.resolve_path_info(self.path_info, {
                'volume':options.volume, 
                'profile':options.profile, 
                'kind':options.update
            })
            if path_info:
                pc = self.factory.configuration.kind['srt']['profile'][path_info['profile']]
                
                has_changed = False
                if 'profile' in path_info and 'update' in pc:
                    if pc['update']['reset']:
                        message = u'Drop existing subtitle tracks in {0}'.format(self.file_path)
                        command = self.factory.util.initialize_command('subler', self.logger)
                        if command:
                            command.extend([u'-o', self.file_path, u'-r'])
                            self.factory.util.execute(command, message, options.debug, pipeout=True, pipeerr=False, logger=self.logger)
                            has_changed = True
                            
                    if 'related' in pc['update']:
                        selected = {}
                        for phy in self.record['entity']['physical'].values():
                            for c in pc['update']['related']:
                                if all((k in phy['path info'] and phy['path info'][k] == v) for k,v in c['from'].iteritems()):
                                    path = self.factory.configuration.canonic_path_from_uri(phy['uri'])
                                    selected[path] = phy['path info']
                                    break
                                
                        for p,i in selected.iteritems():
                            message = u'Update subtitles {0} --> {1}'.format(p, self.file_path)
                            command = self.factory.util.initialize_command('subler', self.logger)
                            if command:
                                command.extend([
                                    u'-o', self.file_path,
                                    u'-i', p, 
                                    u'-l', self.factory.configuration.lookup['iso3t']['language'][i['language']]['print'],
                                    u'-n', c['to']['Name'], 
                                    u'-a', unicode(int(round(self.playback_height() * c['to']['height'])))
                                ])
                                self.factory.util.execute(command, message, options.debug, pipeout=True, pipeerr=False, logger=self.logger)
                                has_changed = True
                                
                        if 'smart' in pc['update']:
                            smart_section = pc['update']['smart']
                            found = False
                            for code in smart_section['order']:
                                for (p,i) in selected.iteritems():
                                    if i['language'] == code:
                                        found = True
                                        message = u'Update smart {0} subtitles {1} --> {2}'.format(self.factory.configuration.lookup['iso3t']['language'][code]['print'], p, self.file_path)
                                        command = self.factory.util.initialize_command('subler', self.logger)
                                        if command:
                                            command.extend([
                                                u'-o', self.file_path, 
                                                u'-i', p, 
                                                u'-l', self.factory.configuration.lookup['iso3t']['language'][smart_section['language']]['print'],
                                                u'-n', smart_section['Name'],
                                                u'-a', unicode(int(round(self.playback_height() * smart_section['height'])))
                                            ])
                                            self.factory.util.execute(command, message, options.debug, pipeout=True, pipeerr=False, logger=self.logger)
                                            has_changed = True
                                        break
                                if found: break
                    if has_changed:
                        self.queue_for_index(self.file_path)
    
    
    def _update_txt(self, options):
        AudioVideoContainer.tag(self, options)
        if options.update in ('txt'):
            path_info = self.factory.configuration.resolve_path_info(self.path_info, {
                'volume':options.volume, 
                'profile':options.profile, 
                'kind':options.update
            })
            if path_info:
                selected = []
                pc = self.factory.configuration.kind['txt']['profile'][path_info['profile']]
                if 'update' in pc:
                    if pc['update']['reset'] and self.info['menu']:
                        message = u'Drop existing chapters in {0}'.format(self.file_path)
                        command = self.factory.util.initialize_command('subler', self.logger)
                        if command:
                            command.extend([u'-o', self.file_path, u'-r', u'-c', u'/dev/null'])
                            self.factory.util.execute(command, message, options.debug, pipeout=True, pipeerr=False, logger=self.logger)
                    if 'related' in pc['update']:
                        lookup = pc['update']['related']
                        for phy in self.record['entity']['physical'].values():
                            if all((k in phy['path info'] and phy['path info'][k] == v) for k,v in lookup.iteritems()):
                                path = self.factory.configuration.canonic_path_from_uri(phy['uri'])
                                selected.append(path)
                                break
                                
                        if selected:
                            message = u'Update chapters {0} --> {1}'.format(selected[0], self.file_path)
                            command = self.factory.util.initialize_command('subler', self.logger)
                            if command:
                                command.extend([u'-o', self.file_path, u'-c', selected[0], '-p'])
                                self.factory.util.execute(command, message, options.debug, pipeout=True, pipeerr=False, logger=self.logger)
                                self.queue_for_index(self.file_path)
                        else:
                            self.logger.warning(u'No chapters available for %s', self.file_path)
    
    
    def update(self, options):
        AudioVideoContainer.update(self, options)
        self._update_srt(options)
        self._update_txt(options)
        self._update_artwork(options)
    
    


# Raw Audio Class
class RawAudio(AudioVideoContainer):
    def __init__(self, factory, file_path, autoload=True):
        AudioVideoContainer.__init__(self, factory, file_path, autoload)
        self.logger = logging.getLogger('Raw Audio')
        if autoload:
            self.load()
    
    
    def transcode(self, options):
        Container.transcode(self, options)
        result = None
        if options.transcode in ('ac3'):
            path_info = self.factory.configuration.resolve_path_info(
                self.path_info, 
                {'volume':options.volume, 'profile':options.profile, 'kind':options.transcode}
            )
            if path_info:
                dest_path = self.factory.configuration.encode_path(path_info, self.record['entity'])
                if dest_path and self.factory.util.varify_if_path_available(dest_path, options.overwrite):
                    command = command = self.factory.util.initialize_command('ffmpeg', self.logger)
                    if command:
                        pc = self.factory.configuration.kind[path_info['kind']]['profile'][path_info['profile']]
                        track = self.info['track'][0]
                        option = None
                        if 'transcode' in pc and 'audio' in pc['transcode']:
                            for c in pc['transcode']['audio']:
                                if all((k in track and track[k] == v) for k,v in c['from'].iteritems()):
                                    option = c
                                    break
                        if option:
                            message = u'Transcode audio {0} --> {1}'.format(self.file_path, dest_path)
                            command.extend([
                                u'-threads',u'{0}'.format(self.factory.configuration.user_config['runtime']['threads']),
                                u'-i', self.file_path,
                                u'-acodec', u'ac3',
                                u'-ac', u'{0}'.format(track['channels']),
                                u'-ab', u'{0}k'.format(option['to']['-ab']),
                                dest_path
                            ])
                            self.factory.util.execute(command, message, options.debug, pipeout=True, pipeerr=False, logger=self.logger)
                            if self.factory.util.clean_if_not_exist(dest_path):
                                self.queue_for_index(dest_path)
                                result = dest_path
        return result
    
    


# Subtitle Class
class Subtitle(Text):
    def __init__(self, factory, file_path, autoload=True):
        Text.__init__(self, factory, file_path, autoload)
        self.logger = logging.getLogger('Subtitle')
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
                    
                    # update the record
                    self.logger.info(u'Refreshed statistics for %s', self.file_path)
                    self.record['entity']['physical'][self.uri]['info']['statistics'] = statistics
                    self.save_record()
                    
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
                    next_block = SubtitleBlock(self)
                    next_block.set_begin_miliseconds(self.factory.util.timecode_to_miliseconds(match.group(1)))
                    next_block.set_end_miliseconds(self.factory.util.timecode_to_miliseconds(match.group(2)))
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
                        block = SubtitleBlock(self)
                        block.set_begin_miliseconds(self.factory.util.timecode_to_miliseconds(line[start]))
                        block.set_end_miliseconds(self.factory.util.timecode_to_miliseconds(line[stop]))
                        
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
        Container.transcode(self, options)
        self.decode()
        result = None
        path_info = self.factory.configuration.resolve_path_info(
            self.path_info, 
            {'volume':options.volume, 'profile':options.profile, 'kind':options.transcode}
        )
        if path_info:
            dest_path = self.factory.configuration.encode_path(path_info, self.record['entity'])
            if dest_path and self.factory.util.varify_if_path_available(dest_path, options.overwrite):
                p = self.factory.configuration.kind[path_info['kind']]['profile'][path_info['profile']]
                
                # Check if profile dictates filtering
                if 'transcode' in p and 'filter' in p['transcode']:
                    # Check filtering by language
                    if path_info['language'] in p['transcode']['filter']:
                        self.logger.debug(u'Apply filters for language %s: %s', path_info['language'], p['transcode']['filter'][path_info['language']])
                        self.filter(p['transcode']['filter'][path_info['language']])
                
                # Check if time shift is necessary
                if options.time_shift is not None:
                    self.shift(options.time_shift)
                
                # Check if frame rate conversion is necessary
                input_frame_rate = None
                output_frame_rate = None
                if (options.input_rate is not None and options.output_rate is not None):
                    input_frame_rate = self.factory.util.frame_rate_to_float(options.input_rate)
                    output_frame_rate = self.factory.util.frame_rate_to_float(options.output_rate)
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
                if self.factory.util.clean_if_not_exist(dest_path):
                    self.queue_for_index(dest_path)
                    result = dest_path
        return result
    
    
    def filter(self, sequence_list):
        if sequence_list:
            self.logger.debug(u'Filtering %s by %s', self.file_path, unicode(sequence_list))
            self.subtitle_blocks = self.factory.subtitle_filter.filter(self.subtitle_blocks, sequence_list)
    
    
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
        return (u'\n'.join([self.factory.util.format_key_value(key, self.info['statistics'][key]) for key in sorted(set(self.info['statistics']))]))
    
    
    def __unicode__(self):
        result = Text.__unicode__(self)
        result = u'\n'.join((result, self.factory.util.format_info_subtitle(u'subtitle statistics'), self.print_subtitle_statistics()))
        return result
    
    
    srt_time_line = re.compile('^([0-9]{2}:[0-9]{2}:[0-9]{2},[0-9]{3}) --> ([0-9]{2}:[0-9]{2}:[0-9]{2},[0-9]{3})$')
    ass_subline = re.compile('^Dialogue\s*:\s*(.*)$')
    ass_formation_line = re.compile('^Format\s*:\s*(.*)$')
    ass_condense_line_breaks = re.compile(r'(\\N)+')
    ass_event_command_re = re.compile(r'\{\\[^\}]+\}')
    pal_framerate = 25.0
    ntsc_framerate = 23.976


# Chapter Class
class Chapter(Text):
    def __init__(self, factory, file_path, autoload=True):
        Text.__init__(self, factory, file_path, autoload)
        self.logger = logging.getLogger('Chapter')
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
        self.path_info = self.factory.configuration.decode_path(self.file_path)
    
    
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
                                time = self.factory.util.timecode_to_miliseconds(time)
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
            self.chapter_markers.append(ChapterMarker(self, time, name))
    
    
    def print_chapter_markers(self):
        return (u'\n'.join([self.factory.util.format_value(chapter_marker) for chapter_marker in self.chapter_markers]))
    
    
    def __unicode__(self):
        result = Text.__unicode__(self)
        if len(self.chapter_markers) > 0:
            result = u'\n'.join((result, self.factory.util.format_info_subtitle(u'chapter markers'), self.print_chapter_markers()))
        return result
    
    
    ogg_chapter_timestamp_re = re.compile('CHAPTER([0-9]{,2})=([0-9]{,2}:[0-9]{,2}:[0-9]{,2}\.[0-9]+)')
    ogg_chapter_name_re = re.compile('CHAPTER([0-9]{,2})NAME=(.*)', re.UNICODE)




class ChapterMarker(object):
    def __init__(self, container, time=None, name=None):
        self.container = container
        self.time = time
        self.name = name
        match = ChapterMarker.mediainfo_chapter_name_with_lang_re.search(self.name)
        if match:
            self.name = match.group(2)
        match = ChapterMarker.rubish_chapter_re.search(self.name)
        if match:
            self.name = None
    
    
    def encode(self, line_buffer, index):
        line_buffer.append(ChapterMarker.ogg_chapter_timestamp_format.format(str(index).zfill(2), unicode(self.container.factory.util.miliseconds_to_time(self.time, '.'), 'utf-8')))
        name = self.name
        if name is None:
            name = ChapterMarker.default_chapter_name_format.format(index)
        line_buffer.append(ChapterMarker.ogg_chapter_name_format.format(str(index).zfill(2), name))
    
    
    def __unicode__(self):
        return u'{0} : {1}'.format(self.container.factory.util.miliseconds_to_time(self.time), self.name)
    
    
    ogg_chapter_timestamp_format = u'CHAPTER{0}={1}'
    ogg_chapter_name_format = u'CHAPTER{0}NAME={1}'
    default_chapter_name_format = u'Chapter {0}'
    mediainfo_chapter_name_with_lang_re = re.compile(u'^(?:([a-z]{2,3}):)?(.*)$', re.UNICODE)
    rubish_chapter_re = re.compile('([0-9]{,2}:[0-9]{,2}:[0-9]{,2}[\.,][0-9]+|[0-9]+|chapter[\s0-9]+)')


class SubtitleBlock(object): 
    def __init__(self, container):
        self.container = container
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
        begin_time = self.container.factory.util.miliseconds_to_time(self.begin, ',')
        end_time = self.container.factory.util.miliseconds_to_time(self.end, ',')
        line_buffer.append(u'{0} --> {1}'.format(unicode(begin_time), unicode(end_time)))
        for line in self.lines:
            line_buffer.append(line)
        line_buffer.append(u'\n')
    


class FilterSequence(object):
    def __init__(self, config):
        self.logger = logging.getLogger('Filter Sequence')
        self.config = config
    
    
    def filter(self, block):
        result = False
        if block is not None:
            result = block.valid()
        return result
    


class DropFilterSequence(FilterSequence):
    def __init__(self, config):
        FilterSequence.__init__(self, config)
        self.logger = logging.getLogger('Drop Filter Sequence')
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
        self.logger = logging.getLogger('Replace Filter Sequence')
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
    



class SubtitleFilter(object):
    def __init__(self, factory):
        self.logger = logging.getLogger('Subtitle Filter')
        self.factory = factory
        self.sequence = {}
    
    
    def find_filter_sequence(self, name):
        result = None
        if name in self.sequence:
            result = self.sequence[name]
        elif name in self.factory.configuration.user_config['subtitles']['filters']:
            config = self.factory.configuration.user_config['subtitles']['filters'][name]
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
    


class FileUtil(object):
    def __init__(self, factory):
        self.logger = logging.getLogger('Util')
        self.factory = factory
    
    
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
        command = self.initialize_command('mp4info', self.logger)
        if command:
            command.append(path)
            proc = Popen(command, stdout=PIPE, stderr=PIPE)
            report = proc.communicate()
            mp4info_report = unicode(report[0], 'utf-8').splitlines()
            for line in mp4info_report:
                match = self.mp4info_tag.search(line)
                if match is not None:
                    tag = match.groups()
                    if tag[0] in self.factory.configuration.lookup['mp4info']['tag']:
                        n = self.factory.configuration.lookup['mp4info']['tag'][tag[0]]
                        info['tag'][n['name']] = tag[1]
    
    
    def decode_info(self, path):
        info = None
        command = self.initialize_command('mediainfo', self.logger)
        if command:
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
                                    if t.tag in self.factory.configuration.lookup['mediainfo']['tag']:
                                        p = self.factory.configuration.lookup['mediainfo']['tag'][t.tag]
                                        info['tag'][p['name']] = t.text
                                    elif t.tag in self.factory.configuration.lookup['mediainfo']['file']:
                                        p = self.factory.configuration.lookup['mediainfo']['file'][t.tag]
                                        info['file'][p['name']] = t.text
                            elif track_type in self.factory.configuration.lookup['mediainfo']['track']:
                                track = {}
                                for t in tn:
                                    if t.tag in self.factory.configuration.lookup['mediainfo']['track'][track_type]:
                                        p = self.factory.configuration.lookup['mediainfo']['track'][track_type][t.tag]
                                        value = self.convert_mediainfo_value(p['type'], t.text)
                                        track[p['name']] = value
                                if track:
                                    track['type'] = track_type
                                    if track_type == 'video':
                                         if 'encoder settings' in track and 'encoder' in track and track['encoder'].count('x264'):
                                             track['encoder settings'] = track['encoder settings'].split(' / ')
                                
                                    # check to see if language is not set and set it to default
                                    if track['type'] in self.factory.configuration.track_with_language:
                                        if 'language' not in track or track['language'] == 'und':
                                            track['language'] = self.factory.configuration.options.language
                                
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
                        for k,v in self.factory.configuration.lookup['plist']['itunemovi'].iteritems():
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
                            info['tag']['genre'] = self.factory.configuration.lookup['code']['gnre'][info['tag']['genre type']]['print']
                    
                    
                    # Format info fields
                    for k,v in info['tag'].iteritems():
                        value = self.convert_mediainfo_value(self.factory.configuration.lookup['name']['tag'][k]['type'], v)
                        info['tag'][k] = value
                    for k,v in info['file'].iteritems():
                        value = self.convert_mediainfo_value(self.factory.configuration.lookup['name']['file'][k]['type'], v)
                        info['file'][k] = value
                    
                    # Fix description and long description
                    if 'description' in info['tag']:
                        info['tag']['description'] = info['tag']['description'].replace('&quot;', '"')
                    if 'long description' in info['tag']:
                        info['tag']['long description'] = info['tag']['long description'].replace('&quot;', '"')
        return info
    
    
    def check_if_in_repository(self, path_info):
        return path_info and 'volume' in path_info and 'profile' in path_info
    
    
    
    
    def sort_field(self, value):
        if value:
            match = self.prefix_to_remove_from_sort.search(value)
            if match:
                value = match.group(2).strip()
                if not value:
                    value = None
        return value
    
    
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
        if command in self.factory.configuration.command:
            c = self.factory.configuration.command[command]
            if 'path' in c and c['path']:
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
        m = self.factory.configuration.lookup['name']['tag'][key]
        if 'subler' in m:
            pkey = m['subler']
            if m['type'] == 'enum':
                pvalue = self.factory.configuration.lookup['code'][m['atom']][value]['print']
            elif m['type'] in ('string', 'list'):
                if m['type'] == 'list':
                    pvalue = u', '.join(value)
                else:
                    if key == 'language':
                        pvalue = self.factory.configuration.lookup['iso3t']['language'][value]['print']
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
        result = [ self.format_key_value(k, v, mapping) for k,v in block.iteritems() ]
        result = [ v for v in sorted(set(result)) if v ]
        if result:
            result = u'\n'.join(result)
        else:
            result = None
        return result
    
    
    def format_info_title(self, text):
        return self.factory.configuration.format['info title display'].format(text)
    
    
    def format_info_subtitle(self, text):
        return self.factory.configuration.format['info subtitle display'].format(text)
    
    
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
                    pvalue = self.factory.configuration.lookup['code'][m['atom']][value]['print']
                    
                elif ptype in ('string', 'list'):
                    if ptype == 'list':
                        pvalue = u', '.join(value)
                    else:
                        if key == 'language':
                            lang = self.factory.configuration.find_language(value)
                            pvalue = lang['print']
                        else:
                            pvalue = unicode(value)
                    if len(pvalue) > self.factory.configuration.format['wrap width']:
                        lines = textwrap.wrap(pvalue, self.factory.configuration.format['wrap width'])
                        pvalue = self.factory.configuration.format['indent'].join(lines)
                        
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
            result = self.factory.configuration.format['key value display'].format(pkey, pvalue)
        return result
    
    
    def format_value(self, value):
        return self.factory.configuration.format['value display'].format(value)
    
    
    format_khz_display = u'{0}kHz'
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


