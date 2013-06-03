# -*- coding: utf-8 -*-

import os
import logging
import hashlib
import re
import json

from ontology import Ontology
from model.menu import Chapter, Menu
from model.caption import Caption
from crawler import Crawler
import queue

class MaterialCache(object):
    def __init__(self, env):
        self.log = logging.getLogger('cache')
        self.env = env
        self.asset = {}
    
    
    def locate_asset(self, location):
        result = None
        if location:
            if 'asset uri' in location and location['asset uri'] in self.asset:
                result = self.asset[location['asset uri']]
            else:
                result = Asset(self, location)
                if result.valid:
                    self.asset[result.uri] = result
                else: result = None
                
            # complement the location ontology
            if result:
                location.merge_all(result.location)
        return result
    
    
    def find(self, location):
        result = None
        if location:
            asset = self.locate_asset(location)
            if asset:
                result = asset.locate_resource(location)
            else:
                self.log.debug(u'Could not locate asset for %s', location)
        return result
    
    
    def clean(self, options):
        pass
    


class Asset(object):
    def __init__(self, cache, location):
        self.log = logging.getLogger('Asset')
        self.cache = cache
        self.location = location.project('ns.medium.asset.location')
        self.resource = {}
        self.volatile = False
        self._node = None
        
        # If we can identify a home, load it and use it to complement the location ontology
        if 'home uri' in self.location:
            home = self.env.resolver.resolve(self.location['home uri'])
            if home is not None:
                self.location.merge_all(home['head']['genealogy'])
            
    
    
    def __unicode__(self):
        return unicode(self.uri)
    
    
    def locate_resource(self, location):
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
    
    
    def commit(self):
        if self.volatile:
            for resource in self.resource.values():
                resource.commit()
                
            # cleanup
            self._node = None
            self.resource = {}
            self.env.resolver.remove(self.uri)
            self.volatile = False
    
    def touch(self):
        for ref in self.node['body']['reference'].values():
            location = Ontology(self.env, 'ns.medium.resource.location', ref['genealogy'])
            self.locate_resource(location)


    


class Resource(object):
    def __init__(self, asset, location):
        self.log = logging.getLogger('Resource')
        self.asset = asset
        self.location = location.project('ns.medium.resource.location')
        self.volatile = False
        
        self._knowledge = None
        self._node = None
        self._meta = None
        self._stream = None
        self._hint = None
        
        self.location.merge_all(self.asset.location)

    
    
    def __unicode__(self):
        return unicode(self.uri)
    
    
    @classmethod
    def create(cls, asset, location):
        result = None
        if location and 'resource uri' in location:
            kind = location.env.enumeration['kind'].find(location['kind'])
            if kind:
                if kind.node['container'] in globals():
                    try:
                        # Try to instantiate a specific container
                        result = globals()[kind.node['container']](asset, location)
                    except TypeError as err:
                        asset.log.debug(u'Unknown resource type %s, treating as generic', kind.node['container'])
                        
            # If can not handle as a specific container, instantiate as a generic
            if result is None:
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
    def knowledge(self):
        if self._knowledge is None:
            self._knowledge = self.env.resolver.resolve(self.location['knowledge uri'], self.location)
        return self._knowledge
    
    
    @property
    def meta(self):
        if self._meta is None:
            if self.node is not None and 'body' in self.node and 'meta' in self.node['body']:
                self._meta = Ontology(self.env, 'ns.medium.resource.meta', self.node['body']['meta'])
            else:
                self._meta = Ontology(self.env, 'ns.medium.resource.meta')
        return self._meta
    
    
    @property
    def stream(self):
        if self._stream is None:
            self._stream = []
            if self.node is not None and 'body' in self.node and 'stream' in self.node['body']:
                for stream in self.node['body']['stream']:
                    mtype = self.env.enumeration['stream kind'].find(stream['stream kind'])
                    self._stream.append(Ontology(self.env, mtype.node['namespace'], stream))
        return self._stream
    
    
    @property
    def hint(self):
        if self._hint is None:
            if self.node is not None and 'body' in self.node and 'hint' in self.node['body']:
                self._hint = Ontology(self.env, 'ns.medium.resource.hint', self.node['body']['hint'])
            else:
                self._hint = Ontology(self.env, 'ns.medium.resource.hint')
        return self._hint
    
    
    @hint.setter
    def hint(self, value):
        self._hint = value
        self.volatile = True
    
    
    def flush(self):
        if self.node:
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
        if self.available:
            if self.volatile:
                self.env.resolver.save(self.node)
                self._node = None
                self.volatile = False
        else:
            self.env.resolver.remove(self.uri)
            self.log.debug(u'Dropped orphan resource document %s', unicode(self))
    
    
    
    
    def read(self):
        pass
    
    
    def write(self, path):
        pass
    
    
    def info(self, task):
    	print json.dumps(self.node, ensure_ascii=False, sort_keys=True, indent=4,  default=self.env.default_json_handler).encode('utf-8')
    	# print json.dumps(self.knowledge, ensure_ascii=False, sort_keys=True, indent=4,  default=self.env.default_json_handler).encode('utf-8')
    
    
    def copy(self, task):
        product = task.produce()
        if product:
            if self.env.check_path_availability(product.path, task.ontology['overwrite']):
                command = self.env.initialize_command('rsync', self.log)
                if command:
                    # Resolving the real path means the semantic 
                    # for copy is to copy the source, not the link
                    command.append(os.path.realpath(self.path))
                    command.append(product.path)
                    message = u'Copy ' + self.path + u' --> ' + product.path
                    self.env.execute(command, message, task.ontology['debug'], pipeout=False, pipeerr=False, log=self.log)
    
    
    def move(self, task):
        product = task.produce()
        if product:
            if os.path.exists(product.path) and os.path.samefile(self.path, product.path):
                self.log.debug(u'No move necessary for %s', unicode(self))
            else:
                if self.env.check_path_availability(product.path, False):
                    command = self.env.initialize_command('mv', self.log)
                    if command:
                        command.extend([self.path, product.path])
                        message = u'Move {0} --> {1}'.format(self.path, product.path)
                        self.env.execute(command, message, task.ontology['debug'], pipeout=True, pipeerr=False, log=self.log)
                        self.env.purge_if_not_exist(self.path)
                else:
                    self.log.warning(u'Refuse to overwrite destination %s with %s', product.path, self.path)
    
    
    def delete(self, task):
        command = self.env.initialize_command('rm', self.log)
        if command:
            command.append(self.path)
            message = u'Remove {0}'.format(self.path)
            self.env.execute(command, message, task.ontology['debug'], pipeout=True, pipeerr=False, log=self.log)
            self.env.purge_if_not_exist(self.path)
    


class Container(Resource):
    def __init__(self, asset, location):
        Resource.__init__(self, asset, location)
    
    
    def explode(self, task):
        pass
    
    
    def pack(self, task):
        pass
    
    
    def tag(self, task):
        pass
    
    
    def optimize(self, task):
        pass
    
    
    def transcode(self, task):
        pass
    
    
    def update(self, task):
        pass
    


class AudioVideoContainer(Container):
    def __init__(self, asset, location):
        Container.__init__(self, asset, location)
    
    
    @property
    def hd(self):
        return self.meta['width'] >= self.env.constant['hd threshold']
    
    
    def explode(self, task):
        for stream in task.transform.single_pivot.stream:
            if stream['enabled'] and stream['stream kind'] == 'menu':
                stream['enabled'] = False
                product = task.produce(stream)
                if product:
                    if self.env.check_path_availability(product.path, task.ontology['overwrite']):
                        if not task.ontology['debug']:
                            product.menu = Menu.from_node(self.env, stream['content'])
                            product.write(product.path)

                        # enqueue a task for transcoding
                        if 'tasks' in stream:
                            for o in stream['tasks']:
                                t = task.job.ontology.project('ns.system.task')
                                for i in o: t[i] = o[i]
                                task.job.enqueue(queue.ResourceTask(task.job, t, product.path))
    
    
    def pack(self, task):
        if task.ontology['kind'] == 'mkv':
            self._pack_mkv(task)
        elif task.ontology['kind'] == 'm4v':
            self._pack_m4v(task)
        else:
            self.log.error(u'Unknown target container to pack %s', unicode(self))
    
    
    def transcode(self, task):
        product = task.produce(task.ontology)
        if product:
            command = self.env.initialize_command('handbrake', self.log)
            if command:
                audio_options = {'--audio':[]}
                
                for stream in task.transform.single_pivot.stream:
                    if stream['stream kind'] == 'video':
                        for k,v in stream['handbrake parameters'].iteritems():
                            command.append(k)
                            if v is not None: command.append(unicode(v))
                            
                        x264_config = []
                        for k,v in stream['handbrake x264 settings'].iteritems():
                            x264_config.append(u'{0}={1}'.format(k, unicode(v)))
                        x264_config = u':'.join(x264_config)
                        command.append(u'--encopts')
                        command.append(x264_config)
                        
                    elif stream['stream kind'] == 'audio':
                        audio_options['--audio'].append(unicode(stream['stream kind position']))
                        for k,v in stream['handbrake audio encoder settings'].iteritems():
                            if k not in audio_options: audio_options[k] = []
                            audio_options[k].append(unicode(v))
                            
                for k,v in audio_options.iteritems():
                    command.append(k)
                    command.append(u','.join(v))
                    
                command.extend([u'--input', self.path, u'--output', product.path])
                message = u'Transcode {0} --> {1}'.format(self.path, product.path)
                if self.env.check_path_availability(product.path, task.ontology['overwrite']):
                    self.env.execute(command, message, task.ontology['debug'], pipeout=False, pipeerr=False, log=self.log)
    
    
    def _pack_mkv(self, task):
        product = task.produce(task.ontology)
        if product:
            command = self.env.initialize_command('mkvmerge', self.log)
            if command:
                # Output
                command.append(u'--output')
                command.append(product.path)
                
                for pivot in task.transform.pivot.values():
                    # Global resource flags
                    if 'mkvmerge flags' in pivot.location:
                        for flag in pivot.location['mkvmerge flags']:
                            command.append(flag)
                            
                    if pivot.location['kind'] in ('mkv', 'm4v', 'avi'):
                        #command.append(u'--title')
                        #command.append(self.asset.meta['full name'])
                        
                        command.append(u'--audio-tracks')
                        command.append(u','.join([ unicode(stream['stream id']) for stream in pivot.stream if stream['stream kind'] == 'audio']))
                        command.append(u'--video-tracks')
                        command.append(u','.join([ unicode(stream['stream id']) for stream in pivot.stream if stream['stream kind'] == 'video']))
                        
                    # Only if at least one stream was chosen
                    if pivot.stream:
                        # Iterate the tracks
                        for stream in pivot.stream:
                            if stream['stream kind'] != 'menu':
                                if 'language' in stream:
                                    command.append(u'--language')
                                    command.append(u'{0}:{1}'.format(stream['stream id'], self.env.enumeration['language'].find(stream['language']).node['ISO 639-1']))
                                    
                                if 'stream name' in stream:
                                    command.append(u'--track-name')
                                    command.append(u'{0}:{1}'.format(stream['stream id'], stream['stream name']))
                                    
                                if 'delay' in pivot.resource.hint:
                                    command.append(u'--sync')
                                    command.append(u'{0}:{1}'.format(stream['stream id'], pivot.resource.hint['delay']))
                                    
                                if stream['kind'] == 'srt':
                                    command.append(u'--sub-charset')
                                    command.append(u'{0}:{1}'.format(stream['stream id'], u'UTF-8'))
                                    
                            else:
                                command.append(u'--chapter-language')
                                command.append(self.env.enumeration['language'].find(stream['language']).node['ISO 639-1'])
                                command.append(u'--chapter-charset')
                                command.append(u'UTF-8')
                                command.append(u'--chapters')
                                
                        command.append(pivot.resource.path)
                    
                message = u'Pack {0} --> {1}'.format(self.path, product.path)
                if self.env.check_path_availability(product.path, task.ontology['overwrite']):
                    self.env.execute(command, message, task.ontology['debug'], pipeout=False, pipeerr=False, log=self.log)
    
    
    def _pack_m4v(self, task):
        product = task.produce(task.ontology)
        if product:
            command = self.env.initialize_command('subler', self.log)
            if command:
                command.extend([u'-o', product.path, u'-i', self.path])
                message = u'Pack {0} --> {1}'.format(unicode(self), unicode(product))
                if self.env.check_path_availability(product.path, task.ontology['overwrite']):
                    self.env.execute(command, message, task.ontology['debug'], pipeout=False, pipeerr=False, log=self.log)
    
    
    


class Text(Container):
    def __init__(self, asset, location):
        Container.__init__(self, asset, location)
    
    
    def write(self, path):
        content = self.encode()
        if content:
            try:
                writer = open(path, 'w')
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
        product = task.produce(task.ontology)
        if product:
            for pivot in task.transform.pivot.values():
                for stream in pivot.stream:
                    if stream['stream kind'] == 'image':
                        image = Image.open(source.resource.path)
                        factor = None
                        if 'max length' in stream and max(image.size) > stream['max length']:
                            factor = float(stream['max length']) / float(max(image.size))
                            
                        elif 'min length' in stream and min(image.size) > stream['min length']:
                            factor = float(stream['min length']) / float(min(image.size))
                            
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
    
    
    def explode(self, task):
        AudioVideoContainer.explode(self, task)
        command = self.env.initialize_command('mkvextract', self.log)
        if command:
            command.extend([u'tracks', self.path ])
            taken = False
            
            for pivot in task.transform.pivot.values():
                for stream in pivot.stream:
                    if stream['enabled']:
                        product = task.produce(stream)
                        if product:
                            stream['enabled'] = False
    
                            if self.env.check_path_availability(product.path, task.ontology['overwrite']):
                                # Leave a hint about the delay
                                if 'delay' in stream: product.hint['delay'] = stream['delay']
                                
                                # add a clause to the command to extract the stream
                                command.append(u'{0}:{1}'.format(unicode(stream['stream id']), product.path))
                                taken = True
                                
                                # enqueue a task for transcoding
                                if 'tasks' in stream:
                                    for o in stream['tasks']:
                                        t = task.job.ontology.project('ns.system.task')
                                        for i in o: t[i] = o[i]
                                        task.job.enqueue(queue.ResourceTask(task.job, t, product.path))
            if taken:
                message = u'Extract tracks from {}'.format(unicode(self))
                self.env.execute(command, message, task.ontology['debug'], pipeout=False, pipeerr=False, log=self.log)
    



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
            self.env.execute(command, message, task.ontology['debug'], pipeout=True, pipeerr=False, log=self.log)
    
    
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
                self.env.execute(command, message, task.ontology['debug'], pipeout=True, pipeerr=False, log=self.log)
                
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
                self.env.execute(command, message, task.ontology['debug'], pipeout=True, pipeerr=False, log=self.log)
                
        for pivot in task.transform.pivot.values():
            if pivot.location['kind'] == 'srt':
                stream = pivot.stream[0]
                message = u'Update subtitles {0} --> {1}'.format(pivot.resource.path, self.path)
                command = self.env.initialize_command('subler', self.log)
                if command:
                    command.extend([
                        u'-o', self.path,
                        u'-i', pivot.resource.path,
                        u'-l', self.env.enumeration['language'].find(stream['language']).name,
                        u'-n', stream['stream name'],
                        u'-a', unicode(int(round(self.meta['height'] * stream['height'])))
                    ])
                    self.env.execute(command, message, task.ontology['debug'], pipeout=True, pipeerr=False, log=self.log)
                    
            elif pivot.location['kind'] == 'png':
                message = u'Update artwork {0} --> {1}'.format(pivot.resource.path, self.path)
                command = self.env.initialize_command('subler', self.log)
                if command:
                    command.extend([
                        u'-o', self.path, 
                        u'-t', 
                        u'{{{0}:{1}}}'.format(u'Artwork', pivot.resource.path)
                    ])
                    self.env.execute(command, message, task.ontology['debug'], pipeout=True, pipeerr=False, log=self.log)
                    
            elif pivot.location['kind'] == 'chp':
                message = u'Update chapters {0} --> {1}'.format(pivot.resource.path, self.path)
                command = self.env.initialize_command('subler', self.log)
                if command:
                    command.extend([
                        u'-o', self.path,
                        u'-c',
                        pivot.resource.path,
                        u'-p'
                    ])
                    self.env.execute(command, message, task.ontology['debug'], pipeout=True, pipeerr=False, log=self.log)
    


class RawAudio(Container):
    def __init__(self, asset, location):
        Container.__init__(self, asset, location)
    
    
    def transcode(self, task):
        if task.ontology['kind'] == 'ac3':
            self._transcode_ac3(task)
        else:
            self.log.error(u'Unknown target format to transcode %s', unicode(self))
    
    def _transcode_ac3(self, task):
        product = task.produce(task.ontology)
        if product:
            stream = [ t for t in task.transform.single_pivot.stream if t['stream kind'] == 'audio' ]
            if stream: stream = stream[0]
            else: stream = None
            if stream:
                
                # Clone the hint ontology
                product.hint = Ontology.clone(self.hint)
                
                command = self.env.initialize_command('ffmpeg', self.log)
                if command:
                    # make ffmpeg not check for overwrite, we already do this check
                    command.append(u'-y')
                    
                    # set the number of processing threads
                    command.append(u'-threads')
                    command.append(unicode(self.env.system['threads']))
                    
                    # set the input file
                    command.append(u'-i')
                    command.append(self.path)
                    
                    for k,v in stream['ffmpeg parameters'].iteritems():
                        command.append(k)
                        if v is not None: command.append(unicode(v))
                        
                    command.append(product.path)
                    message = u'Transcode {0} --> {1}'.format(self.path, product.path)
                    if self.env.check_path_availability(product.path, task.ontology['overwrite']):
                        self.env.execute(command, message, task.ontology['debug'], pipeout=True, pipeerr=False, log=self.log)
    


class Subtitles(Text):
    def __init__(self, asset, location):
        Text.__init__(self, asset, location)
        self._caption_track = None
        self._caption = None
        
    
    
    @property
    def caption(self):
        if self._caption is None:
            for stream in self.stream:
                if stream['stream kind'] == 'caption' and 'content' in stream:
                    self._caption_track = stream
                    self._caption = Caption.from_node(self.env, stream['content'])
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
        product = task.produce(task.ontology)
        if product:
            product.caption = self.caption
            stream = [ t for t in task.transform.single_pivot.stream if t['stream kind'] == 'caption' ]
            if stream: stream = stream[0]
            else: stream = None
            if stream:
                
                # Apply filters
                for name in stream['subtitle filters']:
                    product.caption.filter(name)
                    
                # Apply time shift
                if 'time shift' in task.ontology:
                    product.caption.shift(task.ontology['time shift'])
                    
                # Apply time scale
                if 'time scale' in task.ontology:
                    product.caption.scale(task.ontology['time scale'])
                    
                # Normalize the stream
                product.caption.normalize()
                
                if self.env.check_path_availability(product.path, task.ontology['overwrite']):
                    product.write(product.path)
    


class TableOfContent(Text):
    def __init__(self, asset, location):
        Text.__init__(self, asset, location)
        self._menu_track = None
        self._menu = None
    
    
    @property
    def menu(self):
        if self._menu is None:
            for stream in self.stream:
                if stream['stream kind'] == 'menu' and 'content' in stream:
                    self._menu_track = stream
                    self._menu = Menu.from_node(self.env, stream['content'])
                    
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
    
    
    def transcode(self, task):did i 
        product = task.produce(task.ontology)
        if product:
            product.menu = self.menu
            stream = [ t for t in task.transform.single_pivot.stream if t['stream kind'] == 'menu' ]
            if stream: stream = stream[0]
            else: stream = None
            if stream:
                
                # Apply time shift
                if 'time shift' in task.ontology:
                    product.menu.shift(task.ontology['time shift'])
                    
                # Apply time scale
                if 'time scale' in task.ontology:
                    product.menu.scale(task.ontology['time scale'])
                    
                # Normalize the stream
                product.menu.normalize()
                
                if self.env.check_path_availability(product.path, task.ontology['overwrite']):
                    product.write(product.path)
    

