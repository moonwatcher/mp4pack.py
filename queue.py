# -*- coding: utf-8 -*-

import os
import re
import logging
import urlparse
import urllib
import uuid
import json
import hashlib 

from ontology import Ontology
from material import MaterialCache
from datetime import datetime
from model import ResourceTransform

class Queue(object):
    def __init__(self, env):
        self.log = logging.getLogger('queue')
        self.env = env
        self.cache = MaterialCache(env)
        self.job = []
        self.load()
    
    
    @property
    def length(self):
        return len(self.job)
    
    
    def load(self):
        pass
    
    
    def submit(self, ontology):
        job = Job.create(self, ontology)
        if job.valid:
            self.job.append(job)
        else:
            self.log.warning(u'Ignoring invalid job %s', unicode(job))
        return job
    
    
    def next(self):
        job = None
        if self.length > 0:
            job = self.job.pop()
            job.load()
            job.run()
            job.unload()
        return job
    


class Job(object):
    def __init__(self, queue, node):
        self.log = logging.getLogger('Job')
        self.queue = queue
        self.node = node
        self.ontology = Ontology(self.env, 'ns.system.job', node['ontology'])
        self.uuid = uuid.UUID(self.node['uuid'])
        self.execution = None
        self.task = None
        self._inclusion = None
        self._exclusion = None
    
    @classmethod
    def instantiate(cls, queue, node):
        result = None
        o = Ontology(queue.env, 'ns.system.job', node['ontology'])
        if 'implementation' in o:
            if o['implementation'] in globals():
                try:
                    result = globals()[o['implementation']](queue, node)
                except TypeError as err:
                    queue.log.error(u'Job implementation mismatch %s, treating as a generic job', o['implementation'])
            else:
                queue.log.warning(u'Unknown job implementation %s, treating as a generic job', o['implementation'])
                        
            if result is None:
                result = Job(queue, node)

        return result
    
    
    @classmethod
    def create(cls, queue, ontology):
        result = None
        if queue and ontology:
            o = Ontology(queue.env, 'ns.system.job', ontology).project('ns.system.job')
            node = {
                'uuid':unicode(uuid.uuid4()),
                'created':datetime.now(),
                'ontology':o.node,
            }
            result = Job.instantiate(queue, node)
        return result


    
    @property
    def valid(self):
        return self.ontology is not None
    
    
    @property
    def env(self):
        return self.queue.env
    
    
    @property
    def cache(self):
        return self.queue.cache
    
    
    @property
    def document(self):
        return json.dumps(self.execution, sort_keys=True, indent=4,  default=self.env.default_json_handler)
    
    
    def load(self):
        self.log.debug('Open job %s', unicode(self))
        self.task = []
        self.execution = {
            'start':datetime.now(),
            'task':[],
            'ontology':self.ontology.node,
        }
        
        if 'inclusion' in self.ontology:
            try:
                self._inclusion = re.compile(self.ontology['inclusion'], re.UNICODE)
                self.log.info(u'Inclusion filter set to \'%s\'', self.ontology['inclusion'])
            except re.error as err:
                self.log.warning(u'Failed to compile inclusion filter \'%s\' because of %s', self.ontology['inclusion'], err)
                
        if 'exclusion' in self.ontology:
            try:
                self._exclusion = re.compile(self.ontology['exclusion'], re.UNICODE)
                self.log.info(u'Exclusion filter set to \'%s\'', self.ontology['exclusion'])
            except re.error as err:
                self.log.warning(u'Failed to compile exclusion filter \'%s\' because of %s', self.ontology['exclusion'], err)
    
    
    def enqueue(self, task):
        if task and task.valid:
            self.task.append(task)
    
    
    def run(self):
        for task in self.task:
            task.load()
            task.run()
            task.unload()
            self.execution['task'].append(task.node)
    
    
    def unload(self):
        self.execution['end'] = datetime.now()
        self.execution['duration'] = unicode(self.execution['end'] - self.execution['start'])
        self.log.debug('Close job %s', unicode(self))
    
    
    def filter(self, path):
        return path and \
        ( self._inclusion is None or self._inclusion.search(path) is not None ) and \
        ( self._exclusion is None or self._exclusion.search(path) is None )
    
    
    def __unicode__(self):
        return unicode(self.uuid)
    


class Task(object):
    def __init__(self, job, ontology):
        self.log = logging.getLogger('task')
        self.job = job
        self.ontology = ontology
        self.uuid = uuid.uuid4()
        self.node = None
    
    
    def __unicode__(self):
        return unicode(self.uuid)
    
    
    @property
    def env(self):
        return self.job.env
    
    
    @property
    def valid(self):
        return self.ontology is not None
    
    
    @property
    def cache(self):
        return self.job.cache
    
    
    @property
    def started(self):
        return self.node and self.node['start'] is not None
    
    
    @property
    def ended(self):
        return self.node and self.node['end'] is not None
    
    
    def load(self):
        self.log.debug('Starting task %s', unicode(self))
        self.node = {
            'uuid':unicode(self.uuid),
            'start':None,
            'end':None,
            'ontology':self.ontology.node,
        }
    
    
    def run(self):
        self.node['start'] = datetime.now()
    
    
    def unload(self):
        self.node['end'] = datetime.now()
        self.node['duration'] = unicode(self.node['end'] - self.node['start'])
        self.log.debug('Done with task %s', unicode(self))
    


class ResourceJob(Job):
    def __init__(self, queue, node):
        Job.__init__(self, queue, node)
    
    
    def load(self):
        Job.load(self)
        
        targets = []
        if self.ontology['scan path']:
            for path in self.ontology['scan path']:
                if os.path.exists(path):
                    path = os.path.abspath(os.path.expanduser(os.path.expandvars(path)))
                    files = self._scan_path(path, self.ontology['recursive'])
                    self.log.debug(u'Found %d files in %s', len(files), path)
                    targets.extend(files)
                else:
                    self.log.error(u'Path %s does not exist', path)
        if targets:
            targets = sorted(set(targets))
            self.log.info(u'Found %d files to process', len(targets))
            for path in targets:
                self.enqueue(ResourceTask(self, self.ontology.project('ns.system.task'), path))
    
    
    def filter(self, path):
        return path and os.path.basename(path)[0] != self.env.constant['dot'] and Job.filter(self, path)
    
    
    def _scan_path(self, path, recursive, depth=1):
        result = []
        if os.path.isfile(path):
            dname, fname = os.path.split(path)
            if self.filter(fname):
                result.append(unicode(path, 'utf-8'))
                
        # Recursively scan decendent paths and aggregate the results
        elif (recursive or depth > 0) and os.path.isdir(path) and \
        os.path.basename(path)[0] != self.env.constant['dot']:
            for dnext in os.listdir(path):
                dnext = os.path.abspath(os.path.join(path,dnext))
                result.extend(self._scan_path(dnext, recursive, depth - 1))
        return result
    
    


class ResourceTask(Task):
    def __init__(self, job, ontology, path):
        Task.__init__(self, job, ontology)
        self.location = self.env.repository[self.env.host].decode_resource_path(path)
        self.resource = None
        self.transform = None
        self.product = None
        self.action = None
        self._preset = None
    
    
    @property
    def valid(self):
        return Task.valid.fget(self) and self.location is not None
    
    
    @property
    def preset(self):
        if self._preset is None:
            if self.ontology['preset'] in self.env.preset:
                self._preset = self.env.preset[self.ontology['preset']]
        return self._preset
    
    def load(self):
        Task.load(self)
        
        if self.location:
    
            # Add the resource location and transform to the node 
            self.node['origin'] = self.location.node
            
            self.resource = self.cache.find(self.location)
            if self.resource:
                # if the action is defined in the preset, the preset supports the action
                if self.ontology['action'] in self.preset['action']:
                    
                    # locate a method that implements the action
                    self.action = getattr(self, self.ontology['action'], None)
                    
                    if self.action is None:
                        self.log.warning(u'Unknown action %s, aborting task %s', self.ontology['action'], unicode(self))
                else:
                    self.log.warning(u'Action %s is not defined for preset %s, aborting task %s', self.ontology['action'], self.ontology['preset'], unicode(self))
            else:
                self.log.debug(u'Invalid resource, aborting task %s', unicode(self))
    
    
    def unload(self):
        if self.action:
            
            # Mark products as volatile to make sure they are indexed
            # and add their location to the task node
            if self.product:
                self.node['product'] = []
                for p in self.product:
                    p.volatile = True
                    self.node['product'].append(p.location.node)
                    
            # Commit the asset 
            self.resource.asset.commit()
            
        Task.unload(self)
    
    
    def run(self):
        Task.run(self)
        if self.action:
            # prepare a task product
            self.product = []
            
            # if the action preset is not None or empty initialize the transform
            if self.preset['action'][self.ontology['action']]:
                
                # ensure all resources are loaded in the asset
                self.resource.asset.touch()
                
                # initialize a transform
                self.transform = ResourceTransform(self.resource)
                self.transform.transform(self.preset, self.ontology['action'])
                self.node['transform'] = self.transform.node
                
            # invoke the action
            self.action()
    
    
    def produce(self, override=None):
        # copy the location ontology
        o = Ontology.clone(self.location)
        
        # allow the location to recalculate those concepts 
        del o['volume path']
        del o['file name']
        del o['directory']
        
        # set some location concepts from the task
        o['host'] = self.env.host
        o['volume'] = self.ontology['volume']
        o['profile'] = self.ontology['profile']
        
        # if an override was given set some concepts from it 
        if override:
            for i in [
                'kind', 
                'language',
                'stream id',
                'resource path digest',
                'routing type'
            ]:
                if i in override: o[i] = override[i]
                
        # try to produce the resource
        product = self.resource.asset.locate_resource(o)
        if product:
            self.product.append(product)
        else:
            self.log.error(u'Could not determine destination path from %s', o)
        
        return product
    
    
    def info(self):
        self.resource.info(self)
    
    
    def copy(self):
        self.resource.copy(self)
    
    
    def move(self):
        self.resource.move(self)
    
    
    def delete(self):
        self.resource.delete(self)
    
    
    def prepare(self):
        # enqueue a task to explode the resource
        o = self.job.ontology.project('ns.system.task')
        o['action'] = 'explode'
        explode = ResourceTask(self.job, o, self.location['path'])
        self.job.enqueue(explode)

        # enqueue a task to repack the resource fragments
        o = self.job.ontology.project('ns.system.task')
        o['action'] = 'pack'
        o['preset'] = 'fragment'
        pack = ResourceTask(self.job, o, self.location['path'])
        self.job.enqueue(pack)
    
    
    def explode(self):
        self.resource.explode(self)
    
    
    def pack(self):
        self.resource.pack(self)
    
    
    def tag(self):
        self.resource.tag(self)
    
    
    def optimize(self):
        self.resource.optimize(self)
    
    
    def transcode(self):
        self.resource.transcode(self)
    
    
    def update(self):
        self.resource.update(self)
    


class ServiceJob(Job):
    def __init__(self, queue, node):
        Job.__init__(self, queue, node)
    
    
    def load(self):
        Job.load(self)
        
        if self.ontology['uris']:
            for uri in self.ontology['uris']:
                self.enqueue(ServiceTask(self, self.ontology.project('ns.system.task'), uri))
    


class ServiceTask(Task):
    def __init__(self, job, ontology, uri):
        Task.__init__(self, job, ontology)
        self.uri = uri
        self.document = None
        self.action = None
    
    
    @property
    def valid(self):
        return Task.valid.fget(self) and self.uri is not None
    
    
    def load(self):
        Task.load(self)
        self.document = self.env.resolver.resolve(self.uri, self.ontology['query'])
        
        # locate a method that implements the action
        self.action = getattr(self, self.ontology['action'], None)
        
        if self.action is None:
            self.log.warning(u'Unknown action %s, aborting task %s', self.ontology['action'], unicode(self))
    
    
    def run(self):
        Task.run(self)
        if self.action and self.document is not None:
            self.action()
    
    
    def get(self):
        print json.dumps(self.document, ensure_ascii=False, sort_keys=True, indent=4,  default=self.env.default_json_handler).encode('utf-8')
    
    
    def set(self):
        genealogy = Ontology(self.env, 'ns.service.genealogy', self.document['head']['genealogy'])
        genealogy.merge_all(self.ontology['genealogy'])
        self.document['head']['genealogy'] = genealogy.node
        
        # persist document
        self.env.resolver.save(self.document)
        
        # refetch the document
        self.document = self.env.resolver.resolve(self.uri, self.ontology['query'])
    
    
    def drop(self):
        self.env.resolver.remove(self.uri)
    




class SystemJob(Job):
    def __init__(self, queue, node):
        Job.__init__(self, queue, node)
    
    
    def load(self):
        Job.load(self)
        
        if self.ontology['all']:
            for table in self.env.table.keys():
                self.enqueue(SystemTask(self, self.ontology.project('ns.system.task'), table))
                
        elif self.ontology['tables']:
            for table in self.ontology['tables']:
                self.enqueue(SystemTask(self, self.ontology.project('ns.system.task'), table))
    


class SystemTask(Task):
    def __init__(self, job, ontology, name):
        Task.__init__(self, job, ontology)
        self.action = None
        self.name = name
        self._table = None
    
    
    @property
    def valid(self):
        return Task.valid.fget(self) and self.table is not None
    
    
    @property
    def table(self):
        if self._table is None and self.name in self.env.table:
            self._table = self.env.table[self.name]
        return self._table
    
    
    def load(self):
        Task.load(self)
        
        # locate a method that implements the action
        self.action = getattr(self, self.ontology['action'], None)
        
        if self.action is None:
            self.log.warning(u'Unknown action %s, aborting task %s', self.ontology['action'], unicode(self))
    
    
    def run(self):
        Task.run(self)
        if self.action:
            self.action()
    
    
    def rebuild(self):
        for index in self.table['index']:
            self.env.repository[self.ontology['host']].rebuild_index(self.table['name'], index)
    


