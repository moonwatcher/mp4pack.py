#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import logging
import urlparse
import urllib
import uuid
import json

from ontology import Ontology
from asset import AssetCache
from datetime import datetime
from model import Transform, Query

class Queue(object):
    def __init__(self, env):
        self.log = logging.getLogger('queue')
        self.env = env
        self.cache = AssetCache(env)
        self.job = []
        self.load()
    
    
    @property
    def length(self):
        return len(self.job)
    
    
    def load(self):
        pass
    
    
    def submit(self, job):
        if job and job.valid:
            self.job.append(job)
    
    
    def next(self):
        if self.length > 0:
            job = self.job.pop()
            job.run()
    


class Job(object):
    def __init__(self, queue, ontology):
        self.log = logging.getLogger('Job')
        self.queue = queue
        self.ontology = ontology
        self.uuid = uuid.uuid4()
        self.node = None
        self.task = None
        self._inclusion = None
        self._exclusion = None
    
    
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
        return json.dumps(self.node, sort_keys=True, indent=4,  default=self.env.default_json_handler)
    
    
    def load(self):
        if 'inclusion' in self.ontology:
            try:
                self._inclusion = re.compile(self.ontology['inclusion'], re.UNICODE)
                self.log.info(u'Inclusion filter set to \'%s\'', self.ontology['inclusion'])
            except re.error as err:
                self.log.info(u'Failed to compile inclusion filter \'%s\' because of %s', self.ontology['inclusion'], err)
                
        if 'exclusion' in self.ontology:
            try:
                self._exclusion = re.compile(self.ontology['exclusion'], re.UNICODE)
                self.log.info(u'Exclusion filter set to \'%s\'', self.ontology['exclusion'])
            except re.error as err:
                self.log.info(u'Failed to compile exclusion filter \'%s\' because of %s', self.ontology['exclusion'], err)
    
    
    def enqueue(self, task):
        if task and task.valid:
            self.task.append(task)
    
    
    def run(self):
        self.open()
        self.load()
        for task in self.task:
            task.run()
            self.node['task'].append(task.node)
        self.close()
    
    
    def open(self):
        self.log.debug('Open job %s', unicode(self))
        self.task = []
        self.node = {
            'uuid':unicode(self.uuid),
            'start':datetime.now(),
            'command':self.ontology.node,
            'task':[],
        }
    
    
    def close(self):
        self.node['end'] = datetime.now()
        self.node['duration'] = unicode(self.node['end'] - self.node['start'])
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
    
    
    def load(self):
        pass
    
    
    def open(self):
        self.log.debug('Opening task %s', unicode(self))
        self.node = {
            'uuid':unicode(self.uuid),
            'start':datetime.now(),
            'command':self.ontology.node,
        }
    
    
    def close(self):
        self.node['end'] = datetime.now()
        self.node['duration'] = unicode(self.node['end'] - self.node['start'])
        self.log.debug('Closing task %s', unicode(self))
    
    
    def run(self):
        pass
    


class ResourceJob(Job):
    def __init__(self, queue, ontology):
        Job.__init__(self, queue, ontology)
        self._profile = None
    
    
    @property
    def profile(self):
        if self._profile is None and 'profile' in self.job.ontology:
            self._profile = self.env.profile[self.ontology['profile']]
        return self._profile
    
    
    def load(self):
        Job.load(self)
        
        targets = []
        if self.ontology['scan path']:
            for path in self.ontology['scan path']:
                if os.path.exists(path):
                    path = os.path.realpath(os.path.abspath(os.path.expanduser(os.path.expandvars(path))))
                    files = self._scan_path(path, self.ontology['recursive'])
                    self.log.debug(u'Found %d files in %s', len(files), path)
                    targets.extend(files)
                else:
                    self.log.error(u'Path %s does not exist', path)
        if targets:
            targets = sorted(set(targets))
            self.log.debug(u'Found %d files to process', len(targets))
            for path in targets:
                self.enqueue(ResourceTask(self, self.ontology.project('ns.system.task'), u'file://{}'.format(path)))
    
    
    def filter(self, path):
        return path and os.path.basename(path)[0] != self.env.constant['dot'] and Job.filter(self, path)
    
    
    def _scan_path(self, path, recursive, depth=1):
        result = []
        if os.path.isfile(path):
            dname, fname = os.path.split(path)
            if self.filter(fname):
                result.append(os.path.realpath(path))
                
        # Recursively scan decendent paths and aggregate the results
        elif (recursive or depth > 0) and os.path.isdir(path) and \
        os.path.basename(path)[0] != self.env.constant['dot']:
            for dnext in os.listdir(path):
                dnext = os.path.abspath(os.path.join(path,dnext))
                result.extend(self._scan_path(dnext, recursive, depth - 1))
        return result
    
    


class ResourceTask(Task):
    def __init__(self, job, ontology, url):
        Task.__init__(self, job, ontology)
        self.location = self.env.parse_url(url)
        self.resource = None
        self.query = None
        self.transform = None
        self.product = None
        self._profile = None
    
    
    @property
    def valid(self):
        return Task.valid.fget(self) and self.location is not None
    
    
    @property
    def profile(self):
        if self._profile is None:
            if self._profile is None and 'profile' in self.ontology:
                self._profile = self.env.profile[self.ontology['profile']]
        return self._profile
    
    
    def load(self):
        Task.load(self)
        self.resource = self.cache.find(self.location)
    
    
    def run(self):
        self.open()
        self.load()
        if self.resource:
            self.product = []
            self.resource.asset.touch()
            self.query = Query(self.resource.asset.resource.values())
            self.transform = Transform()
            action = getattr(self, self.ontology['action'], None)
            if action: action()
        else:
            self.debug(u'Resource invalid, aborting task %s', unicode(self))
        self.close()
    
    
    def tag(self):
        self.resource.tag(self)
    
    
    def optimize(self):
        self.resource.optimize(self)
    
    
    def extract(self):
        self.query.add(self.resource)
        self.query.resolve(self.profile['extract'])
        self.transform.resolve(self.query.result, self.profile['extract'])
        self.resource.extract(self)
    
    
    def pack(self):
        self.query.add(self.resource)
        self.query.resolve(self.profile['pack'])
        self.transform.resolve(self.query.result, self.profile['pack'])
        
        o = Ontology.clone(self.location)
        del o['path']
        del o['url']
        o['host'] = self.env.host
        o['volume'] = self.job.ontology['volume']
        o['profile'] = self.job.ontology['profile']
        o['kind'] = self.job.ontology['kind']
        product = self.resource.asset.find(o)
        self.product.append(product)
        self.resource.pack(self)
    
    
    def transcode(self):
        self.query.add(self.resource)
        self.query.resolve(self.profile['transcode'])
        self.transform.resolve(self.query.result, self.profile['transcode'])
        
        o = Ontology.clone(self.location)
        del o['path']
        del o['url']
        o['host'] = self.env.host
        o['volume'] = self.job.ontology['volume']
        o['profile'] = self.job.ontology['profile']
        o['kind'] = self.job.ontology['kind']
        product = self.resource.asset.find(o)
        self.product.append(product)
        self.resource.transcode(self)
    
    
    def update(self):
        self.query.resolve(self.profile['update'])
        self.transform.resolve(self.query.result, self.profile['update'])
        self.resource.update(self)
    
    
    def report(self):
        print self.resource.node
    


class ServiceJob(Job):
    def __init__(self, queue, ontology):
        Job.__init__(self, queue, ontology)
    
    
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
    
    
    @property
    def valid(self):
        return Task.valid.fget(self) and self.uri is not None
    
    
    def load(self):
        Task.load(self)
        self.document = self.env.resolver.resolve(self.uri)
    
    
    def run(self):
        self.open()
        self.load()
        
        if self.document is not None:
            action = getattr(self, self.ontology['action'], None)
            if action: action()
        else:
            self.log.debug(u'Could not resolve document %s, aborting task %s', self.uri, unicode(self))
            
        self.close()
    
    
    def get(self):
        from pymongo import json_util
        #print json.dumps(self.document, sort_keys=True, indent=4,  default=json_util.default)
        print json.dumps(self.document, ensure_ascii=False, sort_keys=True, indent=4,  default=self.env.default_json_handler).encode('utf-8')
    

