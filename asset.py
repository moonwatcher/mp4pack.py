# -*- coding: utf-8 -*-

import os
import logging
import hashlib
import re

from ontology import Ontology
from model.menu import Chapter, Menu
from model.caption import Caption
from crawler import Crawler

class AssetCache(object):
    def __init__(self, env):
        self.log = logging.getLogger('cache')
        self.env = env
        self.asset = {}
    
    
    def find_asset(self, location):
        result = None
        if location:
            if 'asset uri' in location and location['asset uri'] in self.asset:
                result = self.asset[location['asset uri']]
            else:
                result = Asset(self, location)
                if result.valid:
                    self.asset[result.uri] = result
                else: result = None
        return result
    
    
    def find(self, location):
        result = None
        if location:
            asset = self.find_asset(location)
            if asset:
                result = asset.find(location)
        return result
    
    
    def clean(self, options):
        pass
    


class Asset(object):
    def __init__(self, cache, location):
        self.log = logging.getLogger('asset')
        self.cache = cache
        self.location = location.project('ns.medium.asset.location')
        self.resource = {}
        self.volatile = False
        self._node = None
        
        if 'asset uri' not in self.location and 'home uri' in self.location:
            home = self.env.resolver.resolve(self.location['home uri'])
            if home is not None:
                self.location['home id'] = home['head']['genealogy']['home id']
            
    
    
    def __unicode__(self):
        return unicode(self.uri)
    
    
    @property
    def env(self):
        return self.cache.env
    
    @property
    def uri(self):
        return self.location['asset uri']
    
    
    @property
    def valid(self):
        return self.uri is not None
    
    
    @property
    def node(self):
        if self._node is None:
            self._node = self.env.resolver.resolve(self.uri)
        return self._node
    
    
    def clean(self):
        # clean orphans from index
        pass
    
    
    def find(self, location):
        result = None
        if location and 'resource uri' in location:
            if location['resource uri'] in self.resource:
                result = self.resource[location['resource uri']]
            else:
                result = Resource.create(self, location)
                if result and result.valid:
                    self.volatile = True
                    self.resource[result.uri] = result
                else: result = None
        return result
    
    
    def commit(self):
        if self.volatile:
            for resource in self.resource.values():
                resource.commit()
                
            self._node = None
            self.resource = {}
            self.env.resolver.remove(self.uri)
            self.volatile = False
    
    def touch(self):
        for ref in self.node['body']['reference'].values():
            location = Ontology(self.env, 'ns.medium.resource.location', ref['genealogy'])
            self.find(location)


    


class Resource(object):
    def __init__(self, asset, location):
        self.log = logging.getLogger('resource')
        self.asset = asset
        self.location = location
        self.volatile = False
        
        self._node = None
        self._meta = None
        self._stream = None
        self._hint = None
    
    
    def __unicode__(self):
        return unicode(self.uri)
    
    
    @classmethod
    def create(cls, asset, location):
        result = None
        if location and 'resource uri' in location:
            kind = location.env.enumeration['kind'].find(location['kind'])
            if kind:
                if kind.node['container'] == 'mp4':
                    result = MP4(asset, location)
                elif kind.node['container'] == 'matroska':
                    result = Matroska(asset, location)
                elif kind.node['container'] == 'subtitles':
                    result = Subtitles(asset, location)
                elif kind.node['container'] == 'chapters':
                    result = TableOfContent(asset, location)
                elif kind.node['container'] == 'image':
                    result = Artwork(asset, location)
                elif kind.node['container'] == 'raw audio':
                    result = RawAudio(asset, location)
                elif kind.node['container'] == 'avi':
                    result = Avi(asset, location)
            else:
                result = cls(asset, location)
        return result
    
    
    @property
    def env(self):
        return self.asset.env
    
    
    @property
    def cache(self):
        return self.asset.cache
    
    @property
    def uri(self):
        return self.location['resource uri']
    
    
    @property
    def valid(self):
        return self.location is not None and \
        'resource uri' in self.location and \
        'home uri' in self.location
    
    
    @property
    def managed(self):
        return self.location['managed']
    
    
    @property
    def indexed(self):
        self.location['host'] in self.env.repository and \
        self.location['volume'] in self.env.repository[self.location['host']]['volume'] and \
        self.env.repository[self.location['host']]['volume'][self.location['volume']]['index']
    
    
    @property
    def local(self):
        return self.location['domain'] == self.env.domain
    
    
    @property
    def remote(self):
        return not self.local
    
    
    @property
    def path(self):
        return self.location['path']
    
    
    @property
    def available(self):
        return self.path and os.path.exists(self.path)
    
    
    @property
    def node(self):
        if self._node is None:
            self._node = self.env.resolver.resolve(self.location['resource uri'], self.location)
        return self._node
    
    
    @property
    def meta(self):
        if self._meta is None:
            if self.node:
                self._meta = Ontology(self.env, 'ns.medium.resource.crawl.meta', self.node['body']['meta'])
        return self._meta
    
    
    @property
    def stream(self):
        if self._stream is None:
            if self.node and 'stream' in self.node['body']:
                self._stream = []
                for stream in self.node['body']['stream']:
                    mtype = self.env.enumeration['stream kind'].find(stream['stream kind'])
                    self._stream.append(Ontology(self.env, mtype.node['namespace'], stream))
        return self._stream
    
    
    @property
    def hint(self):
        if self._hint is None:
            if self.node and 'hint' in self.node:
                self._hint = Ontology(self.env, 'ns.medium.resource.hint', self.node['body']['hint'])
            else:
                self._hint = Ontology(self.env, 'ns.medium.resource.hint')
        return self._hint
    
    
    @hint.setter
    def hint(self, value):
        self._hint = value
        self.volatile = True
    
    
    def flush(self):
        # Flush meta to node
        if self._meta is not None:
            self.node['body']['meta'] = self._meta.node
            self._meta = None
            
        # Flush streams to node
        if self._stream is not None:
            self.node['body']['stream'] = []
            for stream in self._stream:
                self.node['body']['stream'].append(stream.node)
            self._stream = None
            
        # Flush hint to node
        if self._hint is not None:
            self.node['body']['hint'] = self._hint.node
            self._hint = None
    
    
    def commit(self):
        self.flush()
        if self.managed:
            if self.available:
                if self.volatile:
                    self.env.resolver.save(self.node)
                    self.log.debug(u'Saved resource document %s', unicode(self))
                    self._node = None
                    self.volatile = False
            else:
                self.env.resolver.remove(self.uri)
                self.log.debug(u'Dropped orphan resource document %s', unicode(self))
    
    
    
    
    def read(self):
        pass
    
    
    def write(self):
        pass
    
    
    def fetch(self, task):
        if self.remote and \
        not self.available and \
        self.location['path in cache'] and \
        self.env.varify_directory(self.location['path in cache']):
            if self.location['scheme'] == self.env.runtime['resource scheme']:
                command = self.env.initialize_command('rsync', self.log)
                if command:
                    command.append(u'--partial')
                    command.append(u'--rsh')
                    command.append(u'ssh -p {0}'.format(self.env.repository[self.location['host']]['remote']['download port']))
                    command.append(u'{0}:{1}'.format(self.location['domain'], self.location['path'].replace(u' ', ur'\ ')))
                    command.append(self.location['path in cache'])
                    
                    message = u'Fetch \'{0}\' from {1}'.format(self.location['volume relative path'], self.location['domain'])
                    self.env.execute(command, message, False, pipeout=True, pipeerr=False, log=self.log)
                    
            else:
                if self.location['url']:
                    try:
                        self.log.debug(u'Retrieve %s', self.location['url'])
                        filename, headers = urllib.urlretrieve(self.location['url'].encode('utf-8'), self.location['path in cache'].encode('utf-8'))
                        result = True
                    except IOError:
                        result = False
                        self.env.purge_path(self.location['path in cache'])
                        self.log.warning(u'Failed to retrieve %s', self.location['url'])
                        
        self.env.purge_if_not_exist(self.location['path in cache'])
    
    
    def delete(self, task):
        if self.path:
            self.env.purge_path(self.path)
    
    
    def copy(self, task):
        if 'path' in task.ontology:
            if self.env.varify_path_is_available(task.ontology['path'], task.job.ontology['overwrite']):
                command = self.env.initialize_command('rsync', self.log)
                if command:
                    command.extend([self.path, job.ontology['path']])
                    message = u'Copy ' + self.path + u' --> ' + job.ontology['path']
                    self.env.execute(command, message, options.debug, pipeout=True, pipeerr=False, log=self.log)
                    if self.env.purge_if_not_exist(ontology['path']):
                        self.asset.find(ontology)
    
    
    def move(self, job):
        if 'path' in ontology:
            if os.path.exists(ontology['path']) and os.path.samefile(self.path, ontology['path']):
                self.log.debug(u'No move needed for %s', unicode(self))
            else:
                if self.env.varify_path_is_available(ontology['path'], False):
                    command = self.env.initialize_command('mv', self.log)
                    if command:
                        command.extend([self.path, ontology['path']])
                        message = u'Rename {0} --> {1}'.format(self.path, ontology['path'])
                        self.env.execute(command, message, options.debug, pipeout=True, pipeerr=False, log=self.log)
                else:
                    self.log.warning(u'Not renaming %s, destination exists: %s', self.path, ontology['path'])
    
    
    def compare(self, job):
        result = False
        if os.path.exists(self.path) and os.path.exists(ontology['path']):
            source_md5 = hashlib.md5(file(self.path).read()).hexdigest()
            dest_md5 = hashlib.md5(file(ontology['path']).read()).hexdigest()
            if source_md5 == dest_md5:
                self.log.info(u'md5 match: %s %s',source_md5, unicode(self))
                result = True
            else:
                self.log.error(u'md5 mismatch: %s is not %s for %s', source_md5, dest_md5, unicode(self))
        return result
    



class Container(Resource):
    def __init__(self, asset, location):
        Resource.__init__(self, asset, location)
    
    
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
    def __init__(self, asset, location):
        Container.__init__(self, asset, location)
    
    
    @property
    def hd(self):
        return self.meta['width'] >= self.env.constant['hd threshold']
    
    
    
    def extract(self, task): 
        for track in task.transform.single_result.stream:
            if track['enabled'] and track['stream kind'] == 'menu':
                o = Ontology.clone(self.location)
                del o['path']
                del o['url']
                o['host'] = task.job.ontology['host']
                o['volume'] = task.job.ontology['volume']
                o['profile'] = task.job.ontology['profile']
                o['language'] = track['language']
                o['kind'] = track['kind']
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
            
            for track in task.transform.single_result.stream:
                if track['stream kind'] == 'video':
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
                    
                elif track['stream kind'] == 'audio':
                    audio_options['--audio'].append(unicode(track['stream position']))
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
                    command.append(u','.join([ unicode(track['stream id']) for track in pivot.stream if track['stream kind'] == 'audio']))
                    command.append(u'--video-tracks')
                    command.append(u','.join([ unicode(track['stream id']) for track in pivot.stream if track['stream kind'] == 'video']))
                    
                # Iterate the tracks
                for track in pivot.stream:
                    if track['kind'] != 'menu':
                        if 'language' in track:
                            command.append(u'--language')
                            command.append(u'{0}:{1}'.format(track['stream id'], self.env.enumeration['language'].find(track['language']).node['ISO 639-1']))
                            
                        if 'name' in track:
                            command.append(u'--track-name')
                            command.append(u'{0}:{1}'.format(track['stream id'], track['name']))
                            
                        if 'delay' in pivot.resource.hint:
                            command.append(u'--sync')
                            command.append(u'{0}:{1}'.format(track['stream id'], pivot.resource.hint['delay']))
                            
                        if track['kind'] == 'srt':
                            command.append(u'--sub-charset')
                            command.append(u'{0}:{1}'.format(track['stream id'], u'UTF-8'))
                            
                    else:
                        command.append(u'--chapter-language')
                        command.append(self.env.enumeration['language'].find(track['language']).node['ISO 639-1'])
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
    
    
    


class Text(Container):
    def __init__(self, asset, location):
        Container.__init__(self, asset, location)
    
    
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
    def __init__(self, asset, location):
        Container.__init__(self, asset, location)
    
    
    def transcode(self, task):
        from PIL import Image
        product = task.product[0]
        track = [ t for t in transform.single_result.stream if t['stream kind'] == 'image' ]
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
    def __init__(self, asset, location):
        AudioVideoContainer.__init__(self, asset, location)
    
    
    def extract(self, task):
        AudioVideoContainer.extract(self, task)
        command = self.env.initialize_command('mkvextract', self.log)
        if command:
            command.extend([u'tracks', self.path ])
            
            taken = False
            for track in task.transform.single_result.stream:
                if track['enabled']:
                    o = Ontology.clone(self.location)
                    del o['path']
                    del o['url']
                    o['host'] = task.job.ontology['host']
                    o['volume'] = task.job.ontology['volume']
                    o['profile'] = task.job.ontology['profile']
                    o['language'] = track['language']
                    o['kind'] = track['kind']
                    product = self.asset.find(o)
                    self.env.varify_directory(product.path)
                    
                    # Leave a hint about the delay
                    if 'delay' in track:
                        product.hint['delay'] = track['delay']
                        
                    command.append(u'{0}:{1}'.format(unicode(track['stream id']), product.path))
                    task.product.append(product)
                    track['enabled'] = False
                    taken = True
                    
            if taken:
                message = u'Extract tracks from {}'.format(unicode(self))
                self.env.execute(command, message, task.job.ontology['debug'], pipeout=False, pipeerr=False, log=self.log)
    


class MP4(AudioVideoContainer):
    def __init__(self, asset, location):
        AudioVideoContainer.__init__(self, asset, location)
    
    
    def tag(self, task):
        pass
    
    
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
                track = pivot.stream[0]
                message = u'Update subtitles {0} --> {1}'.format(pivot.resource.path, self.path)
                command = self.env.initialize_command('subler', self.log)
                if command:
                    command.extend([
                        u'-o', self.path,
                        u'-i', pivot.resource.path,
                        u'-l', self.env.enumeration['language'].find(track['language']).name,
                        u'-n', track['name'],
                        u'-a', unicode(int(round(self.meta['height'] * track['height'])))
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
    def __init__(self, asset, location):
        Container.__init__(self, asset, location)
    
    
    def transcode(self, task):
        product = task.product[0]
        track = [ t for t in task.transform.single_result.stream if t['stream kind'] == 'audio' ]
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
    def __init__(self, asset, location):
        Text.__init__(self, asset, location)
        self._caption_track = None
        self._caption = None
        
    
    
    @property
    def caption(self):
        if self._caption is None:
            for track in self.stream:
                if track['stream kind'] == 'caption' and 'content' in track:
                    self._caption_track = track
                    self._caption = Caption.from_node(self.env, track['content'])
                    break
                    
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
        track = [ t for t in task.transform.single_result.stream if t['stream kind'] == 'caption' ]
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
    def __init__(self, asset, location):
        Text.__init__(self, asset, location)
        self._menu_track = None
        self._menu = None
    
    
    @property
    def menu(self):
        if self._menu is None:
            for track in self.stream:
                if track['stream kind'] == 'menu' and 'content' in track:
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
        track = [ t for t in transform.single_result.stream if t['stream kind'] == 'menu' ]
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
    

