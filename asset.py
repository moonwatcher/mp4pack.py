# -*- coding: utf-8 -*-

import os
import logging
import hashlib
import re

from ontology import Ontology
from model import Timestamp, Chapter, Slide, Caption, Menu, Transform, Query
from crawler import Crawler

class AssetCache(object):
    def __init__(self, env):
        self.log = logging.getLogger('Cache')
        self.env = env
        self.assets = {}
    
    
    @property
    def em(self):
        return self.env.em
    
    
    def find_asset(self, ontology):
        result = None
        if ontology and 'asset id' in ontology:
            if ontology['asset id'] in self.assets:
                result = self.assets[ontology['asset id']]
            else:
                result = Asset(self, ontology)
                if result.valid:
                    result.load()
                    self.assets[ontology['asset id']] = result
                else:
                    result.unload()
                    result = None
        return result
    
    
    def find(self, ontology):
        result = None
        asset = self.find_asset(ontology)
        if asset:
            result = asset.find(ontology)
        return result
    
    
    def clean(self, options):
        pass
    


class Asset(object):
    def __init__(self, cache, ontology):
        self.log = logging.getLogger('asset')
        self.cahce = cache
        self.ontology = ontology
        self.node = None
        self.volatile = False
        self.touched = False
        self.resource = {}
    
    
    def __unicode__(self):
        return unicode(self.ontology['asset id'])
    
    
    @property
    def env(self):
        return self.cahce.env
    
    
    @property
    def em(self):
        return self.cahce.em
    
    
    @property
    def valid(self):
        return self.ontology is not None and 'asset id' in self.ontology
    
    
    @property
    def managed(self):
        return self.valid and self.node is not None
    
    
    @property
    def resources(self):
        self.touch()
        return self.resource.values()
    
    
    def load(self):
        if self.valid:
            self.scan()
            # self.node = self.em.find_asset(self.ontology)
    
    
    def unload(self):
        self.save()
        self.resource.clear()
        self.node = None
        self.volatile = False
    
    
    def flush(self):
        # Reload the node to make sure we have a fresh copy
        self.load()
        
        if self.managed:
            for resource in self.resource.values():
                if resource.orphan:
                    if resource.ontology['uri'] in self.node['entity']['resource']:
                        del self.node['entity']['resource'][resource.ontology['uri']]
                        self.log.debug(u'Dropped record for %s', unicode(resource))
                        self.volatile = True
                        
                elif resource.volatile and resource.indexed:
                    resource.flush()
                    self.node['entity']['resource'][resource.ontology['uri']] = resource.node
                    self.log.debug(u'Flushed record for %s', unicode(resource))
                    self.volatile = True
    
    
    def clean(self):
        # clean orphans from index
        pass
    
    
    def scan(self):
        result = None
        if self.valid:
            o = Ontology.clone(self.ontology)
            del o['path']
            del o['url']
            result = []
            self.log.debug(u'Scanning %s for resources related to %s', self.env.host, unicode(self))
            for volume in self.env.repository[self.env.host]['volume'].values():
                if volume['scan']:
                    o['volume'] = volume['name']
                    for kind in self.env.kind.values():
                        o['kind'] = kind['name']
                        for profile in self.env.profile.values():
                            o['profile'] = profile['name']
                            if kind['name'] not in self.env.kind_with_language:
                                if o['path'] and os.path.exists(o['path']):
                                    self.log.debug(u'Discovered %s', o['path'])
                                    x = self.find(Ontology.clone(o))
                                    # DEBUG
                                    x.load()
                                    
                            else:
                                for language in self.env.model['language'].element.keys():
                                    o['language'] = language
                                    if o['path'] and os.path.exists(o['path']):
                                        self.log.debug(u'Discovered %s', o['path'])
                                        x = self.find(Ontology.clone(o))
                                        # DEBUG
                                        x.load()
                                        
                                    del o['language']
                            del o['profile']
                        del o['kind']
                    del o['volume']
        return result
    
    
    def find(self, ontology):
        result = None
        if 'resource id' in ontology:
            if ontology['resource id'] in self.resource:
                result = self.resource[ontology['resource id']]
            else:
                if 'container' in ontology:
                    if ontology['container'] == 'mp4':
                        result = MP4(self, ontology)
                    elif ontology['container'] == 'matroska':
                        result = Matroska(self, ontology)
                    elif ontology['container'] == 'subtitles':
                        result = Subtitles(self, ontology)
                    elif ontology['container'] == 'chapters':
                        result = TableOfContent(self, ontology)
                    elif ontology['container'] == 'image':
                        result = Artwork(self, ontology)
                    elif ontology['container'] == 'raw audio':
                        result = RawAudio(self, ontology)
                    elif ontology['container'] == 'avi':
                        result = Avi(self, ontology)
                        
                    if result:
                        self.resource[ontology['resource id']] = result
                else:
                    result = None
        return result
    
    
    def save(self):
        self.flush()
        if self.volatile:
            # self.em.save_asset(self.node)
            self.volatile = False
            self.log.debug(u'Saved record for %s', unicode(self))
        
    
    
    def touch(self):
        if not self.touched and self.managed:
            for node in self.node['entity']['resource'].values():
                ontology = Ontology(self.env, node['ontology'])
                self.find(ontology)
            self.touched = True
    
    
    def _lookup_resource_node(self, ontology):
        result = None
        if self.managed and ontology is not None \
        and 'uri' in ontology and ontology['uri'] in self.node['entity']['resource']:
            result = self.node['entity']['resource'][ontology['uri']]
        return result
    


class Resource(object):
    def __init__(self, asset, ontology):
        self.log = logging.getLogger('resource')
        self.asset = asset
        self.ontology = ontology
        self.node = None
        self.volatile = False
        self.orphan = False
        
        self._info = None
        self._track = None
        self._hint = None
    
    
    def __unicode__(self):
        return unicode(self.ontology['resource id'])
    
    
    
    @property
    def env(self):
        return self.asset.env
    
    
    @property
    def em(self):
        return self.asset.em
    
    
    @property
    def cache(self):
        return self.asset.cahce
    
    
    
    @property
    def valid(self):
        return self.ontology is not None and 'resource id' in self.ontology
    
    
    @property
    def indexed(self):
        return 'uri' in self.ontology and \
        self.env.repository[self.ontology['host']]['volume'][self.ontology['volume']]['index']
    
    
    @property
    def local(self):
        return self.ontology['domain'] == self.env.domain
    
    
    @property
    def remote(self):
        return not self.local
    
    
    @property
    def path(self):
        return self.ontology['path']
        #result = None
        #if self.local:
        #    result = self.ontology['path']
        #else:
        #    result = self.ontology['path in cache']
        #return result
    
    
    @property
    def available(self):
        return self.path and os.path.exists(self.path)
    
    
    
    @property
    def info(self):
        if self._info is None:
            if self.valid:
                if self.node and 'tag' in self.node:
                    self._info = Ontology(self.env, self.node['tag'])
                else:
                    self._info = Ontology(self.env)
        return self._info
    
    
    @property
    def track(self):
        if self._track is None:
            if self.valid:
                self._track = []
                if self.node and 'track' in self.node:
                    for track in self.node['track']:
                        self._track.append(Ontology(self.env, track))
        return self._track
    
    
    @property
    def hint(self):
        if self._hint is None:
            if self.valid:
                if self.node and 'hint' in self.node:
                    self._hint = Ontology.from_node(self.env, self.node['hint'])
                else:
                    self._hint = Ontology(self.env)
        return self._hint
    
    
    @hint.setter
    def hint(self, value):
        self._hint = value
        self.volatile = True
    
    
    
    def load(self):
        if self.valid:
            if self.node is None:
                self.node = self.asset._lookup_resource_node(self.ontology)
                
            if self.node is None:
                self.crawl()
    
    
    def crawl(self):
        if self.available:
            crawler = Crawler(self.ontology)
            if crawler.valid:
                self.node = crawler.node
                self.volatile = True
    
    
    def flush(self):
        if self.volatile:
            if self._info is not None:
                self.node['tag'] = self._info.node
                self._info = None
                
            if self._track is not None:
                tracks = []
                for track in self._track:
                    tracks.append(track.node)
                self.node['track'] = tracks
                self._track = None
                
            if self._hint is not None:
                self.node['hint'] = self._hint.node
                self._hint = None
    
    
    def read(self):
        pass
    
    
    def write(self):
        pass
    
    
    
    def fetch(self, job):
        if self.remote and \
        not self.available and \
        self.ontology['path in cache'] and \
        self.env.varify_directory(self.ontology['path in cache']):
            if self.ontology['scheme'] == self.env.runtime['resource scheme']:
                command = self.env.initialize_command('rsync', self.log)
                if command:
                    command.append(u'--partial')
                    command.append(u'--rsh')
                    command.append(u'ssh -p {0}'.format(self.env.repository[self.ontology['host']]['remote']['download port']))
                    command.append(u'{0}:{1}'.format(self.ontology['domain'], self.ontology['file path'].replace(u' ', ur'\ ')))
                    command.append(self.ontology['path in cache'])
                    
                    message = u'Fetch \'{0}\' from {1}'.format(self.ontology['volume relative path'], self.ontology['domain'])
                    self.env.execute(command, message, False, pipeout=True, pipeerr=False, log=self.log)
                    
            else:
                if self.ontology['url']:
                    try:
                        self.log.debug(u'Retrieve %s', self.ontology['url'])
                        filename, headers = urllib.urlretrieve(self.ontology['url'].encode('utf-8'), self.ontology['path in cache'].encode('utf-8'))
                        result = True
                    except IOError:
                        result = False
                        self.env.purge_path(self.ontology['path in cache'])
                        self.log.warning(u'Failed to retrieve %s', self.ontology['url'])
                        
        self.env.purge_if_not_exist(self.ontology['path in cache'])
    
    
    def delete(self, job):
        if self.path:
            self.env.purge_path(self.path)
        self.orphan = True
    
    
    def copy(self, job):
        if 'path' in ontology:
            if self.env.varify_path_is_available(ontology['path'], ontology['overwrite']):
                command = self.env.initialize_command('rsync', self.log)
                if command:
                    command.extend([self.path, ontology['path']])
                    message = u'Copy ' + self.path + u' --> ' + ontology['file path']
                    self.env.execute(command, message, options.debug, pipeout=True, pipeerr=False, log=self.log)
                    if self.env.purge_if_not_exist(ontology['file path']):
                        self.asset.find(ontology)
    
    
    def move(self, job):
        if 'file path' in ontology:
            if os.path.exists(ontology['file path']) and os.path.samefile(self.path, ontology['file path']):
                self.log.debug(u'No move needed for %s', unicode(self))
            else:
                if self.env.varify_path_is_available(ontology['file path'], False):
                    command = self.env.initialize_command('mv', self.log)
                    if command:
                        command.extend([self.path, ontology['file path']])
                        message = u'Rename {0} --> {1}'.format(self.path, ontology['file path'])
                        self.env.execute(command, message, options.debug, pipeout=True, pipeerr=False, log=self.log)
                else:
                    self.log.warning(u'Not renaming %s, destination exists: %s', self.path, ontology['file path'])
    
    
    def compare(self, job):
        result = False
        if os.path.exists(self.path) and os.path.exists(ontology['file path']):
            source_md5 = hashlib.md5(file(self.path).read()).hexdigest()
            dest_md5 = hashlib.md5(file(ontology['file path']).read()).hexdigest()
            if source_md5 == dest_md5:
                self.log.info(u'md5 match: %s %s',source_md5, unicode(self))
                result = True
            else:
                self.log.error(u'md5 mismatch: %s is not %s for %s', source_md5, dest_md5, unicode(self))
        return result
    


class Container(Resource):
    def __init__(self, asset, ontology):
        Resource.__init__(self, asset, ontology)
    
    
    def tag(self, task):
        pass
    
    
    def optimize(self, task):
        pass
    
    
    def extract(self, task):
        pass
    
    
    def pack(self, task):
        pass
    
    
    def transcode(self, task):
        pass
    
    
    def update(self, task):
        pass
    
    
    def report(self, task):
        pass
    


class AudioVideoContainer(Container):
    def __init__(self, asset, ontology):
        Container.__init__(self, asset, ontology)
        self._meta = None
    
    
    @property
    def meta(self):
        if self._meta is None:
            self._meta = Ontology.clone(self.ontology)
            if self._meta['media kind'] == 'movie':
                if 'tmdb_record' in self.node['entity']:
                    movie = self.node['entity']['tmdb_record']
                    
                    if 'name' in movie:
                        self._meta['name'] = movie['name']
                    if 'overview' in movie and movie['overview'] != u'No overview found.':
                        self._meta['long description'] = self.env.expression['whitespace'].sub(u' ', movie['overview']).strip()
                    if 'certification' in movie:
                        self._meta['rating'] = movie['certification']
                    if 'released' in movie and movie['released']:
                        self._meta['release date'] = datetime.strptime(movie['released'], u'%Y-%m-%d')
                    if 'tagline' in movie and movie['tagline']:
                        self._meta['description'] = self.env.expression['whitespace'].sub(u' ', movie['tagline']).strip()
                    elif 'overview' in movie and movie['overview'] != u'No overview found.':
                        s = self.env.expression['sentence end'].split(self.env.expression['whitespace'].sub(u' ', movie['overview']).strip(u'\'".,'))
                        if s: self.meta_['description'] = s[0].strip(u'"\' ').strip() + u'.'
                    self._load_itunemovi_meta(movie)
                    self._load_genre_meta(movie)
                    result = True
                    
            elif self._meta['media kind'] == 'tvshow':
                if show and 'tvdb_record' in show and episode and 'tvdb_record' in episode:
                    show = self.node['tv show']['tvdb_record']
                    episode = self.node['entity']['tvdb_record']
                    if 'name' in show:
                        self._meta['tv show'] = show['name']
                    if 'tv_season' in episode:
                        self._meta['tv season'] = episode['tv_season']
                    if 'tv_episode' in episode:
                        self._meta['tv episode'] = episode['tv_episode']
                    if 'name' in episode:
                        self._meta['name'] = episode['name']
                    if 'certification' in show:
                        self._meta['rating'] = show['certification']
                    if 'tv_network' in show:
                        self._meta['tv network'] = show['tv_network']
                    if 'released' in episode:
                        self._meta['release date'] = episode['released']
                    if 'overview' in episode:
                        overview = self.env.expression['whitespace'].sub(u' ', episode['overview']).strip()
                        self._meta['long description'] = overview
                        s = self.env.expression['sentence end'].split(overview.strip(u'\'".,'))
                        if s: self._meta['description'] = s[0].strip(u'"\' ').strip() + u'.'
                        
                    self._load_genre_meta(show)
                    self._load_itunemovi_meta(show, True, False)
                    self._load_itunemovi_meta(episode, False, True)
        return self._meta
    
    
    @property
    def hd(self):
        return self.info['width'] >= self.env.configuration['hd threshold']
    
    
    
    def extract(self, task): 
        for track in task.transform.single_result.track:
            if track['enabled'] and track['type'] == 'text' and track['codec'] == 'chpl':
                o = Ontology.clone(self.ontology)
                del o['path']
                del o['url']
                o['host'] = task.job.ontology['host']
                o['volume'] = task.job.ontology['volume']
                o['profile'] = task.job.ontology['profile']
                o['language'] = track['language']
                o['kind'] = track['codec']
                product = self.asset.find(o)
                self.env.varify_directory(product.path)
                product.menu = Menu.from_node(self.env, track['content'])
                product.write()
                track['enabled'] = False
                task.product.append(product)
    
    
    def pack(self, task):
        if task.job.ontology['kind'] == 'mkv':
            self._pack_mkv(task)
        elif task.job.ontology['kind'] == 'm4v':
            self._pack_m4v(task)
    
    
    def transcode(self, task):
        product = task.product[0]
        command = self.env.initialize_command('handbrake', self.log)
        if command:
            audio_options = {'--audio':[]}
            
            for track in task.transform.single_result.track:
                if track['type'] == 'video':
                    for flag in track['handbrake flags']:
                        command.append(flag)
                        
                    for k,v in track['handbrake parameters'].iteritems():
                        command.append(k)
                        command.append(unicode(v))
                        
                    x264_config = []
                    for k,v in track['handbrake x264 settings'].iteritems():
                        x264_config.append(u'{0}={1}'.format(k, unicode(v)))
                    x264_config = u':'.join(x264_config)
                    command.append(u'--encopts')
                    command.append(x264_config)
                    
                elif track['type'] == 'audio':
                    audio_options['--audio'].append(unicode(track['position'] + 1))
                    for k,v in track['encoder settings'].iteritems():
                        if k not in audio_options:
                            audio_options[k] = []
                        audio_options[k].append(unicode(v))
                        
            for k,v in audio_options.iteritems():
                command.append(k)
                command.append(u','.join(v))
                
            command.extend([u'--input', self.path, u'--output', product.path])
            message = u'Transcode {0} --> {1}'.format(self.path, product.path)
            self.env.varify_directory(product.path)
            self.env.execute(command, message, task.job.ontology['debug'], pipeout=False, pipeerr=False, log=self.log)
    
    
    
    def _pack_mkv(self, task):
        command = self.env.initialize_command('mkvmerge', self.log)
        if command:
            product = task.product[0]
            
            # Output
            command.append(u'--output')
            command.append(product.path)
            
            for pivot in task.transform.result:
                # Global resource flags
                if 'mkvmerge flags' in pivot.ontology:
                    for flag in pivot.ontology['mkvmerge flags']:
                        command.append(flag)
                        
                if pivot.ontology['kind'] in ('mkv', 'm4v', 'avi'):
                    #command.append(u'--title')
                    #command.append(self.asset.meta['full name'])
                    
                    command.append(u'--audio-tracks')
                    command.append(u','.join([ unicode(track['track id']) for track in pivot.track if track['type'] == 'audio']))
                    command.append(u'--video-tracks')
                    command.append(u','.join([ unicode(track['track id']) for track in pivot.track if track['type'] == 'video']))
                    
                # Iterate the tracks
                for track in pivot.track:
                    if track['codec'] != 'chpl':
                        if 'language' in track:
                            command.append(u'--language')
                            command.append(u'{0}:{1}'.format(track['track id'], self.env.model['language'].find(track['language']).node['ISO 639-1']))
                            
                        if 'name' in track:
                            command.append(u'--track-name')
                            command.append(u'{0}:{1}'.format(track['track id'], track['name']))
                            
                        if 'delay' in pivot.resource.hint:
                            command.append(u'--sync')
                            command.append(u'{0}:{1}'.format(track['track id'], pivot.resource.hint['delay']))
                            
                        if track['codec'] == 'srt':
                            command.append(u'--sub-charset')
                            command.append(u'{0}:{1}'.format(track['track id'], u'UTF-8'))
                            
                    else:
                        command.append(u'--chapter-language')
                        command.append(self.env.model['language'].find(track['language']).node['ISO 639-1'])
                        command.append(u'--chapter-charset')
                        command.append(u'UTF-8')
                        command.append(u'--chapters')
                        
                command.append(pivot.resource.path)
                
            message = u'Pack {0} --> {1}'.format(self.path, product.path)
            self.env.execute(command, message, task.job.ontology['debug'], pipeout=False, pipeerr=False, log=self.log)
    
    
    def _pack_m4v(self, task):
        command = self.env.initialize_command('subler', self.log)
        if command:
            product = task.product[0]
            
            command.extend([u'-o', product.path, u'-i', self.path])
            message = u'Pack {0} --> {1}'.format(unicode(self), unicode(product))
            self.env.execute(command, message, options.debug, pipeout=False, pipeerr=False, log=self.log)
    
    
    def _load_genre_meta(self, record):
        if 'genres' in record and record['genres']:
            genres = [ r for r in record['genres'] if r['type'] == 'genre' ]
            if genres:
                genre = genres[0]
                self._meta['genre'] = genre['name']
                if 'itmf' in genre:
                    self._meta['genre type'] = genre['itmf']
    
    
    def _load_itunemovi_meta(self, record, initialize=True, finalize=True):
        if 'cast' in record:
            if initialize:
                for i in self.env.model['itunmovi'].element.keys():
                    self._meta[i] = []
                    
            self._meta['directors'].extend([ 
                r['name'] for r in record['cast'] 
                if r['department'] == 'Directing' and r['job'] == 'Director'
            ])
            self._meta['codirectors'].extend([
                r['name'] for r in record['cast'] 
                if r['department'] == 'Directing' and  r['job'] != 'Director'
            ])
            self._meta['producers'].extend([
                r['name'] for r in record['cast'] 
                if r['department'] == 'Production'
            ])
            self._meta['screenwriters'].extend([
                r['name'] for r in record['cast'] 
                if r['department'] == 'Writing'
            ])
            self._meta['cast'].extend([
                r['name'] for r in record['cast'] 
                if r['department'] == 'Actors'
            ])
            
            if finalize:
                for i in self.env.model['itunmovi'].element.keys():
                    if not self._meta[i]: del self._meta[i]
    
    


class Text(Container):
    def __init__(self, asset, ontology):
        Container.__init__(self, asset, ontology)
    
    
    def write(self):
        content = self.encode()
        if content:
            try:
                writer = open(self.path, 'w')
                writer.write(content.encode('utf-8'))
                writer.close()
            except IOError as error:
                self.log.error(str(error))
    
    
    def encode(self):
        return None
    


class Artwork(Container):
    def __init__(self, asset, ontology):
        Container.__init__(self, asset, ontology)
    
    
    def transcode(self, task):
        from PIL import Image
        product = task.product[0]
        track = [ t for t in transform.single_result.track if t['type'] == 'image' ]
        if track: track = track[0]
        else: track = None
        if track:
            image = Image.open(source.resource.path)
            factor = None
            if 'max length' in track and max(image.size) > track['max length']:
                factor = float(track['max length']) / float(max(image.size))
                
            elif 'min length' in track and min(image.size) > track['min length']:
                factor = float(track['min length']) / float(min(image.size))
                
            if factor is not None:
                resize = (int(round(image.size[0] * factor)), int(round(image.size[1] * factor)))
                self.log.debug(u'Resize artwork: %dx%d --> %dx%d', image.size[0], image.size[1], resize[0], resize[1])
                image = image.resize(resize, Image.ANTIALIAS)
                
            try:
                image.save(product.path)
            except IOError as err:
                self.log.error(u'Failed to transcode artwork %s', unicode(self))
                self.log.debug(u'Exception raised: %s', err)
    


class Matroska(AudioVideoContainer):
    def __init__(self, asset, ontology):
        AudioVideoContainer.__init__(self, asset, ontology)
    
    
    def extract(self, task):
        AudioVideoContainer.extract(self, task)
        command = self.env.initialize_command('mkvextract', self.log)
        if command:
            command.extend([u'tracks', self.path ])
            
            taken = False
            for track in task.transform.single_result.track:
                if track['enabled']:
                    o = Ontology.clone(self.ontology)
                    del o['path']
                    del o['url']
                    o['host'] = task.job.ontology['host']
                    o['volume'] = task.job.ontology['volume']
                    o['profile'] = task.job.ontology['profile']
                    o['language'] = track['language']
                    o['type'] = track['type']
                    o['kind'] = track['codec']
                    product = self.asset.find(o)
                    self.env.varify_directory(product.path)
                    
                    # Leave a hint about the delay
                    if 'delay' in track:
                        product.hint['delay'] = track['delay']
                        
                    command.append(u'{0}:{1}'.format(unicode(track['track id']), product.path))
                    task.product.append(product)
                    track['enabled'] = False
                    taken = True
                    
            if taken:
                message = u'Extract tracks from {}'.format(unicode(self))
                self.env.execute(command, message, task.job.ontology['debug'], pipeout=False, pipeerr=False, log=self.log)
    


class MP4(AudioVideoContainer):
    def __init__(self, asset, ontology):
        AudioVideoContainer.__init__(self, asset, ontology)
    
    
    def tag(self, task):
        AudioVideoContainer.tag(self, task)
        if self.meta:
            supported = [ k for k in self.meta.keys() if self.env.prototype['crawl']['tag'].find('subler', k) is not None ]
            missing = [ k for k in supported if k not in self.info ]
            outdated = [ k for k in supported if self.info[k] != self.meta[k] ]
            
            if self.hd:
                if 'hd video' not in self.info:
                    missing['hd video'] = True
                elif not self.info['hd video']:
                    outdated['hd video'] = True
            else:
                if 'hd video' not in self.info:
                    missing['hd video'] = False
                elif self.info['hd video']:
                    outdated['hd video'] = False
                    
            for k in outdated:
                self.log.debug('Update tag %s from %s to %s', k, self.info[k], self.meta[k])
                
            for k in missing:
                self.log.debug('Set tag %s to %s', k, self.meta[k])
                
        update = {}
        for k in missing:
            update[k] = self.meta[k]
        for k in outdated:
            update[k] = self.meta[k]
            
        if update:
            q = u''.join([self.env.encode_subler_key_value(k, update[k]) for k in sorted(update)])
            message = u'Update tags: {0} --> {1}'.format(u', '.join([self.env.prototype['crawl']['tag'].find('name', k).node['print'] for k in sorted(update)]), unicode(self))
            command = self.env.initialize_command('subler', self.log)
            if command:
                command.extend([u'-o', self.path, u'-t', q])
                self.env.execute(command, message, task.job.ontology['debug'], pipeout=True, pipeerr=False, log=self.log)
        else:
            self.log.info(u'No tags need update in %s', unicode(self))
    
    
    def optimize(self, task):
        AudioVideoContainer.optimize(self, task)
        message = u'Optimize {0}'.format(self.path)
        command = self.env.initialize_command('subler', self.log)
        if command:
            command.extend([u'-O', u'-o', self.path])
            self.env.execute(command, message, task.job.ontology['debug'], pipeout=True, pipeerr=False, log=self.log)
    
    
    def update(self, task):
        AudioVideoContainer.update(self, task)
        
        if False:
            # Drop subtitles
            message = u'Drop existing subtitle tracks from {0}'.format(self.path)
            command = self.env.initialize_command('subler', self.log)
            if command:
                command.extend([
                    u'-o',
                    self.path,
                    u'-r'
                ])
                self.env.execute(command, message, task.job.ontology['debug'], pipeout=True, pipeerr=False, log=self.log)
                
            # Drop chapters
            message = u'Drop existing chapters in {0}'.format(self.path)
            command = self.env.initialize_command('subler', self.log)
            if command:
                command.extend([
                    u'-o',
                    self.path,
                    u'-r',
                    u'-c',
                    u'/dev/null'
                ])
                self.env.execute(command, message, task.job.ontology['debug'], pipeout=True, pipeerr=False, log=self.log)
                
        for pivot in task.transform.result:
            if pivot.ontology['kind'] == 'srt':
                track = pivot.track[0]
                message = u'Update subtitles {0} --> {1}'.format(pivot.resource.path, self.path)
                command = self.env.initialize_command('subler', self.log)
                if command:
                    command.extend([
                        u'-o', self.path,
                        u'-i', pivot.resource.path,
                        u'-l', self.env.model['language'].find(track['language']).name,
                        u'-n', track['name'],
                        u'-a', unicode(int(round(self.info['height'] * track['height'])))
                    ])
                    self.env.execute(command, message, task.job.ontology['debug'], pipeout=True, pipeerr=False, log=self.log)
                    
            elif pivot.ontology['kind'] == 'png':
                message = u'Update artwork {0} --> {1}'.format(pivot.resource.path, self.path)
                command = self.env.initialize_command('subler', self.log)
                if command:
                    command.extend([
                        u'-o', self.path, 
                        u'-t', 
                        u'{{{0}:{1}}}'.format(u'Artwork', pivot.resource.path)
                    ])
                    self.env.execute(command, message, task.job.ontology['debug'], pipeout=True, pipeerr=False, log=self.log)
                    
            elif pivot.ontology['kind'] == 'chpl':
                message = u'Update chapters {0} --> {1}'.format(pivot.resource.path, self.path)
                command = self.env.initialize_command('subler', self.log)
                if command:
                    command.extend([
                        u'-o', self.path,
                        u'-c',
                        pivot.resource.path,
                        u'-p'
                    ])
                    self.env.execute(command, message, task.job.ontology['debug'], pipeout=True, pipeerr=False, log=self.log)
    


class RawAudio(Container):
    def __init__(self, asset, ontology):
        Container.__init__(self, asset, ontology)
    
    
    def transcode(self, task):
        product = task.product[0]
        track = [ t for t in task.transform.single_result.track if t['type'] == 'audio' ]
        if track: track = track[0]
        else: track = None
        if track:
            
            # Clone the hint ontology
            product.hint = Ontology.clone(self.hint)
            
            command = self.env.initialize_command('ffmpeg', self.log)
            command.append(u'-threads')
            command.append(unicode(self.env.system['threads']))
            command.append(u'-i')
            command.append(self.path)
            
            for k,v in track['ffmpeg parameters'].iteritems():
                command.append(k)
                command.append(unicode(v))
                
            command.append(product.path)
            message = u'Transcode {0} --> {1}'.format(self.path, product.path)
            self.env.varify_directory(product.path)
            self.env.execute(command, message, task.job.ontology['debug'], pipeout=True, pipeerr=False, log=self.log)
    


class Subtitles(Text):
    def __init__(self, asset, ontology):
        Text.__init__(self, asset, ontology)
        self._caption_track = None
        self._caption = None
        
    
    
    @property
    def caption(self):
        if self._caption is None:
            for track in self.track:
                if track['type'] == 'text' and 'content' in track:
                    self._caption_track = track
                    self._caption = Caption.from_node(self.env, track['content'])
                    
            if self._caption is None:
                self._caption = Caption(self.env)
        return self._caption
    
    
    @caption.setter
    def caption(self, value):
        self._caption = value
        self.volatile = True
    
    
    def encode(self):
        result = Text.encode(self)
        if self.valid:
            content = self.caption.encode()
            if content:
                result = u'\n'.join(content)
        return result
    
    
    def transcode(self, task):
        product = task.product[0]
        product.caption = self.caption
        track = [ t for t in task.transform.single_result.track if t['type'] == 'text' ]
        if track: track = track[0]
        else: track = None
        if track:
            
            for name in track['subtitle filters']:
                product.caption.filter(name)
                
            if 'time shift' in task.job.ontology:
                product.caption.shift(task.job.ontology['time shift'])
                
            if 'time scale' in task.job.ontology:
                product.caption.scale(task.job.ontology['time scale'])
                
            product.caption.normalize()
            self.env.varify_directory(product.path)
            product.write()
    


class TableOfContent(Text):
    def __init__(self, asset, ontology):
        Text.__init__(self, asset, ontology)
        self._menu_track = None
        self._menu = None
    
    
    @property
    def menu(self):
        if self._menu is None:
            for track in self.track:
                if track['type'] == 'text' and 'content' in track:
                    self._menu_track = track
                    self._menu = Menu.from_node(self.env, track['content'])
                    
            if self._menu is None:
                self._menu = Menu(self.env)
        return self._menu
    
    
    @menu.setter
    def menu(self, value):
        self._menu = value
        self.volatile = True
    
    
    def encode(self):
        result = Text.encode(self)
        if self.valid:
            content = self.menu.encode(Chapter.OGG)
            if content:
                result = u'\n'.join(content)
        return result
    
    
    def transcode(self, task):
        product = task.product[0]
        product.menu = self.menu
        track = [ t for t in transform.single_result.track if t['type'] == 'text' ]
        if track: track = track[0]
        else: track = None
        if track:
            
            if 'time shift' in task.job.ontology:
                product.menu.shift(task.job.ontology['time shift'])
                
            if 'time scale' in task.job.ontology:
                product.menu.scale(task.job.ontology['time scale'])
                
            product.menu.normalize()
            self.env.varify_directory(product.path)
            product.write()
    

