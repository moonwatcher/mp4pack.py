# -*- coding: utf-8 -*-

import os
import logging
import hashlib
import re
import json
import queue

from ontology import Ontology
from model.menu import Chapter, Menu
from model.caption import Caption
from crawler import Crawler

class MaterialCache(object):
    def __init__(self, env):
        self.log = logging.getLogger('Material')
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
                self.log.debug(u'Failed to locate asset for %s', location)
        return result
        
    def clean(self, options):
        pass
        


class Asset(object):
    def __init__(self, cache, location):
        self.log = logging.getLogger('Material')
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
        self.log = logging.getLogger('Material')
        self.asset = asset
        self.location = location.project('ns.medium.resource.location')
        self.volatile = False
        
        self._node = None
        self._fragment = None
        self._knowledge = None
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
                    except TypeError:
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
    def fragment(self):
        if self._fragment is None:
            self._fragment = self.env.resolver.resolve(self.location['resource fragment uri'], self.location)
        return self._fragment
        
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
            self.log.debug(u'Orphan resource document dropped %s', unicode(self))
            
    def read(self):
        pass
        
    def write(self, path):
        pass
        
    def info(self, task):
        print json.dumps(self.node, ensure_ascii=False, sort_keys=True, indent=4,  default=self.env.default_json_handler).encode('utf-8')
        # print json.dumps(self.knowledge, ensure_ascii=False, sort_keys=True, indent=4, default=self.env.default_json_handler).encode('utf-8')
        
    def copy(self, task):
        product = task.produce()
        if product:
            if self.env.check_path_available(product.path, task.ontology['overwrite']):
                command = self.env.initialize_command('rsync', self.log)
                if command:
                    # Resolving the real path means the semantic 
                    # for copy is to copy the source, not the link
                    command.append(os.path.realpath(self.path))
                    command.append(product.path)
                    message = u'Copy {} --> {}'.format(self.path, product.path)
                    self.env.execute(command, message, task.ontology['debug'], pipeout=False, pipeerr=False, log=self.log)
                    
    def move(self, task):
        product = task.produce()
        if product:
            if os.path.exists(product.path) and os.path.samefile(self.path, product.path):
                self.log.debug(u'No move necessary for %s', unicode(self))
            else:
                if self.env.check_path_available(product.path, False):
                    command = self.env.initialize_command('mv', self.log)
                    if command:
                        command.extend([self.path, product.path])
                        message = u'Move {} --> {}'.format(self.path, product.path)
                        self.env.execute(command, message, task.ontology['debug'], pipeout=True, pipeerr=False, log=self.log)
                        self.env.clean_path(self.path)
                        
    def delete(self, task):
        command = self.env.initialize_command('rm', self.log)
        if command:
            command.append(self.path)
            message = u'Remove {}'.format(self.path)
            self.env.execute(command, message, task.ontology['debug'], pipeout=True, pipeerr=False, log=self.log)
            self.env.clean_path(self.path)
            


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
        for pivot in task.transform.pivot.values():
            for stream in pivot.stream:
                if stream['enabled'] and stream['stream kind'] == 'menu':
                    stream['enabled'] = False
                    product = task.produce(stream)
                    if product:
                        if self.env.check_path_available(product.path, task.ontology['overwrite']):
                            if not task.ontology['debug']:
                                product.menu = Menu.from_node(self.env, stream['content'])
                                product.write(product.path)
                                
                                # push a task for transcoding
                                if 'tasks' in stream:
                                    for template in stream['tasks']:
                                        o = task.job.ontology.project('ns.system.task')
                                        for i in template: o[i] = template[i]
                                        t = queue.ResourceTask(task.job, o, product.path)
                                        t.group = task.key
                                        t.constrain({'scope':'task', 'reference':task.key, 'status':'completed'})
                                        task.job.push(t)
                                        
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
            taken = False
            if command:
                audio_options = {'--audio':[]}
                for pivot in task.transform.pivot.values():
                    for stream in pivot.stream:
                        if stream['stream kind'] == 'video':
                            taken = True
                            for k,v in stream['handbrake parameters'].iteritems():
                                command.append(k)
                                if v is not None: command.append(unicode(v))
                                
                            x264_config = []
                            for k,v in stream['handbrake x264 settings'].iteritems():
                                x264_config.append(u'{}={}'.format(k, unicode(v)))
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
                        
                if taken and self.env.check_path_available(product.path, task.ontology['overwrite']):
                    message = u'Transcode {} --> {}'.format(self.path, product.path)
                    command.extend([u'--input', self.path, u'--output', product.path])
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
                        command.append(u'--title')
                        command.append(self.asset.location['full name'])
                        
                        tracks = [ unicode(stream['stream order']) for stream in pivot.stream if stream['stream kind'] == 'audio']
                        if tracks:
                            command.append(u'--audio-tracks')
                            command.append(u','.join(tracks))
                        else:
                            command.append(u'--no-audio')
                            
                        tracks = [ unicode(stream['stream order']) for stream in pivot.stream if stream['stream kind'] == 'video']
                        if tracks:
                            command.append(u'--video-tracks')
                            command.append(u','.join(tracks))
                        else:
                            command.append(u'--no-video')
                            
                    # Only if at least one stream was chosen
                    if pivot.stream:
                        # Iterate the tracks
                        for stream in pivot.stream:
                            del stream['stream name']
                            if stream['stream kind'] != 'menu':
                                if 'language' in stream:
                                    command.append(u'--language')
                                    command.append(u'{}:{}'.format(
                                        stream['stream order'],
                                        self.env.enumeration['language'].find(stream['language']).node['ISO 639-1'])
                                    )
                                    
                                if 'stream name' in stream:
                                    command.append(u'--track-name')
                                    command.append(u'{}:{}'.format(stream['stream order'], stream['stream name']))
                                    # command.append(u'{0}:{1}'.format(
                                    #    stream['stream order'],
                                    #    self.env.enumeration['language'].find(stream['language']).node['name'])
                                    #)
                                    
                                if 'delay' in pivot.resource.hint:
                                    command.append(u'--sync')
                                    command.append(u'{}:{}'.format(stream['stream order'], pivot.resource.hint['delay']))
                                    
                                if stream['kind'] == 'srt':
                                    command.append(u'--sub-charset')
                                    command.append(u'{}:{}'.format(stream['stream order'], u'UTF-8'))
                                    
                            else:
                                command.append(u'--chapter-language')
                                command.append(self.env.enumeration['language'].find(stream['language']).node['ISO 639-1'])
                                command.append(u'--chapter-charset')
                                command.append(u'UTF-8')
                                command.append(u'--chapters')
                                
                        command.append(pivot.resource.path)
                        
                if self.env.check_path_available(product.path, task.ontology['overwrite']):
                    message = u'Pack {} --> {}'.format(self.path, product.path)
                    self.env.execute(command, message, task.ontology['debug'], pipeout=False, pipeerr=False, log=self.log)
                    
    def _pack_m4v(self, task):
        product = task.produce(task.ontology)
        if product:
            command = self.env.initialize_command('subler', self.log)
            if command:
                if self.env.check_path_available(product.path, task.ontology['overwrite']):
                    message = u'Pack {} --> {}'.format(unicode(self), unicode(product))
                    command.extend([u'-o', product.path, u'-i', self.path])
                    self.env.execute(command, message, task.ontology['debug'], pipeout=False, pipeerr=False, log=self.log)
                    


class Image(Container):
    def __init__(self, asset, location):
        Container.__init__(self, asset, location)
        
    def transcode(self, task):
        from PIL import Image
        product = task.produce(task.ontology)
        if product:
            for pivot in task.transform.pivot.values():
                for stream in pivot.stream:
                    if stream['stream kind'] == 'image':
                        image = Image.open(self.path)
                        factor = None
                        if 'max length' in stream and max(image.size) > stream['max length']:
                            factor = float(stream['max length']) / float(max(image.size))
                            
                        elif 'min length' in stream and min(image.size) > stream['min length']:
                            factor = float(stream['min length']) / float(min(image.size))
                            
                        if factor is not None:
                            resize = (int(round(image.size[0] * factor)), int(round(image.size[1] * factor)))
                            self.log.debug(u'Resize image: %dx%d --> %dx%d', image.size[0], image.size[1], resize[0], resize[1])
                            image = image.resize(resize, Image.ANTIALIAS)
                            
                        if self.env.check_path_available(product.path, task.ontology['overwrite']):
                            try:
                                image.save(product.path)
                                self.log.info(u'Transcode %s --> %s', self.path, product.path)
                                
                            except IOError as e:
                                self.log.error(u'Failed to transcode artwork %s', unicode(self))
                                self.log.debug(u'Exception raised: %s', e)
                                


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
                            
                            if self.env.check_path_available(product.path, task.ontology['overwrite']):
                                # Leave a hint about the delay
                                if 'delay' in stream: product.hint['delay'] = stream['delay']
                                
                                # add a clause to the command to extract the stream
                                command.append(u'{}:{}'.format(unicode(stream['stream order']), product.path))
                                taken = True
                                
                                # push a task for transcoding
                                if 'tasks' in stream:
                                    for template in stream['tasks']:
                                        o = task.job.ontology.project('ns.system.task')
                                        for i in template: o[i] = template[i]
                                        t = queue.ResourceTask(task.job, o, product.path)
                                        t.group = task.key
                                        t.constrain({'scope':'task', 'reference':task.key, 'status':'completed'})
                                        task.job.push(t)
                                        
            if taken:
                message = u'Explode {}'.format(unicode(self))
                self.env.execute(command, message, task.ontology['debug'], pipeout=False, pipeerr=False, log=self.log)
                


class MP4(AudioVideoContainer):
    def __init__(self, asset, location):
        AudioVideoContainer.__init__(self, asset, location)
        
    def optimize(self, task):
        AudioVideoContainer.optimize(self, task)
        message = u'Optimize {}'.format(self.path)
        command = self.env.initialize_command('subler', self.log)
        if command:
            command.extend([u'-optimize', u'-dest', self.path])
            self.env.execute(command, message, task.ontology['debug'], pipeout=True, pipeerr=False, log=self.log)
            
    def tag(self, task):
        update = Ontology(self.env, 'ns.medium.resource.meta.tag')
        meta = self.meta.project('ns.medium.resource.meta.tag')
        knowledge = Ontology(self.env, 'ns.medium.resource.meta.tag', self.knowledge['body'])
        genealogy = Ontology(self.env, 'ns.service.genealogy', self.knowledge['head']['genealogy'])
        knowledge.merge_all(genealogy)
        
        # Everything that is in meta but doesn't fit knowledge
        # should be replaced with the value in knowledge 
        for i in meta.keys():
            if meta[i] != knowledge[i]:
                update[i] = knowledge[i]
                
        # Everything that is in knowledge but not in meta
        # should be set to the value in knowledge 
        for i in knowledge.keys():
            if i not in meta:
                update[i] = knowledge[i]
                
        modify = []
        for k,v in update.iteritems():
            prototype = update.namespace.find(k)
            if prototype and prototype.node['subler']:
                modify.append(u'{{{}:{}}}'.format(prototype.node['subler'],v))
                
        print unicode(modify).encode('utf-8')
        
    def update(self, task):
        AudioVideoContainer.update(self, task)
        
        # Drop subtitles
        message = u'Drop existing subtitle tracks from {0}'.format(self.path)
        command = self.env.initialize_command('subler', self.log)
        if command:
            command.extend([
                u'-remove',
                u'-dest', self.path,
            ])
            self.env.execute(command, message, task.ontology['debug'], pipeout=True, pipeerr=False, log=self.log)
            
        # Drop chapters
        message = u'Drop existing chapters in {0}'.format(self.path)
        command = self.env.initialize_command('subler', self.log)
        if command:
            command.extend([
                u'-chapters', u'/dev/null',
                u'-dest', self.path,
            ])
            self.env.execute(command, message, task.ontology['debug'], pipeout=True, pipeerr=False, log=self.log)
            
        for pivot in task.transform.pivot.values():
            # add subtitles
            if pivot.location['kind'] == 'srt':
                stream = pivot.stream[0]
                message = u'Update subtitles {} --> {}'.format(pivot.resource.path, self.path)
                command = self.env.initialize_command('subler', self.log)
                if command:
                    command.extend([
                        u'-source', pivot.resource.path,
                        u'-language', self.env.enumeration['language'].find(stream['language']).name,
                        u'-height', unicode(int(round(self.meta['height'] * stream['height']))),
                        u'-itunesfriendly',
                        u'-dest', self.path,
                    ])
                    self.env.execute(command, message, task.ontology['debug'], pipeout=True, pipeerr=False, log=self.log)
                    
            # add artwork
            elif pivot.location['kind'] == 'png':
                message = u'Update artwork {} --> {}'.format(pivot.resource.path, self.path)
                command = self.env.initialize_command('subler', self.log)
                if command:
                    command.extend([
                        u'-dest', self.path, 
                        u'-metadata', 
                        u'{{{0}:{1}}}'.format(u'Artwork', pivot.resource.path)
                    ])
                    self.env.execute(command, message, task.ontology['debug'], pipeout=True, pipeerr=False, log=self.log)
                    
            # add chapters
            elif pivot.location['kind'] == 'chp':
                message = u'Update chapters {} --> {}'.format(pivot.resource.path, self.path)
                command = self.env.initialize_command('subler', self.log)
                if command:
                    command.extend([
                        u'-chapters', pivot.resource.path,
                        u'-chapterspreview',
                        u'-dest', self.path,
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
            taken = False
            
            for pivot in task.transform.pivot.values():
                for stream in pivot.stream:
                    if not taken and stream['stream kind'] == 'audio':
                        taken = True
                        
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
                                
                if taken: break
            if taken and self.env.check_path_available(product.path, task.ontology['overwrite']):
                command.append(product.path)
                message = u'Transcode {} --> {}'.format(self.path, product.path)
                self.env.execute(command, message, task.ontology['debug'], pipeout=True, pipeerr=False, log=self.log)
                


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
            except IOError as e:
                self.log.error(str(e))
                
    def encode(self):
        return None
        


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
            taken = False
            product.caption = self.caption
            
            for pivot in task.transform.pivot.values():
                for stream in pivot.stream:
                    if not taken and stream['stream kind'] == 'caption':
                        taken = True
                        
                        # Apply filters
                        if 'subtitle filters' in stream:
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
                        
                if taken: break
            if taken and self.env.check_path_available(product.path, task.ontology['overwrite']):
                self.log.info(u'Transcode %s --> %s', self.path, product.path)
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
        
    def transcode(self, task):
        product = task.produce(task.ontology)
        if product:
            taken = False
            product.menu = self.menu
            
            for pivot in task.transform.pivot.values():
                for stream in pivot.stream:
                    if not taken and stream['stream kind'] == 'menu':
                        taken = True
                        # Apply time shift
                        if 'time shift' in task.ontology:
                            product.menu.shift(task.ontology['time shift'])
                            
                        # Apply time scale
                        if 'time scale' in task.ontology:
                            product.menu.scale(task.ontology['time scale'])
                            
                        # Normalize the stream
                        product.menu.normalize()
                        
                if taken: break
            if taken and self.env.check_path_available(product.path, task.ontology['overwrite']):
                self.log.info(u'Transcode %s --> %s', self.path, product.path)
                product.write(product.path)
                


