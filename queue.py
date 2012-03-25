#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import logging
import urlparse
import urllib
import uuid

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
            job.open()
            job.load()
            job.run()
            job.close()
    


class Job(object):
    def __init__(self, queue, ontology):
        self.log = logging.getLogger('job')
        self.queue = queue
        self.ontology = ontology
        self.uuid = uuid.uuid4()
        self._include_filter = None
        self.task = []
        self.node = {
            'command':self.ontology.node,
            'task':[],
        }
    
    
    @property
    def valid(self):
        return self.ontology is not None
    
    
    @property
    def env(self):
        return self.queue.env
    
    
    @property
    def cache(self):
        return self.queue.cache
    
    
    def load(self):
        if self.valid:
            self._load_filter()
    
    
    def add_url(self, url):
        if url:
            ontology = self.env.parse_url(url)
            if ontology:
                self.task.append(Task(self, ontology))
    
    
    def scan(self):
        result = []
        if self.ontology['scan']:
            for path in self.ontology['scan']:
                if os.path.exists(path):
                    path = os.path.realpath(os.path.abspath(os.path.expanduser(os.path.expandvars(path))))
                    files = self._scan_path(path, self.ontology['recursive'])
                    self.log.debug(u'Found %d files in %s', len(files), path)
                    result.extend(files)
                else:
                    self.log.error(u'Path %s does not exist', path)
        if result:
            result = sorted(set(result))
            self.log.debug(u'Found %d files to process', len(result))
            for path in result:
                self.add_url(u'file://{}'.format(path))
    
    
    def run(self):
        start = datetime.now()
        self.node['start'] = unicode(start)
        self.scan()
        for task in self.task:
            if task.valid:
                task.open()
                task.run()
                task.close()
                self.node['task'].append(task.node)
                
        end = datetime.now()
        self.node['end'] = unicode(end)
        self.node['duration'] = unicode(end - start)
    
    
    def open(self):
        self.log.debug('Open job %s', unicode(self))
    
    
    def close(self):
        self.log.debug('Close job %s', unicode(self))
    
    
    def _load_filter(self):
        if 'filter' in self.ontology:
            try:
                self._include_filter = re.compile(self.ontology['filter'], re.UNICODE)
                self.log.info(u'File filter set to \'%s\'', self.ontology['filter'])
            except re.error as err:
                self.log.info(u'Failed to compile filter \'%s\' because of %s', self.ontology['filter'], err)
    
    
    def _filter(self, path):
        return path and os.path.basename(path)[0] != self.env.constant['dot'] and \
        ( self._include_filter is None or self._include_filter.search(path) != None )
    
    
    def _scan_path(self, path, recursive, depth=1):
        result = []
        if os.path.isfile(path):
            dname, fname = os.path.split(path)
            if self._filter(fname):
                result.append(os.path.realpath(path))
                
        # Recursively scan decendent paths and aggregate the results
        elif (recursive or depth > 0) and os.path.isdir(path) and \
        os.path.basename(path)[0] != self.env.constant['dot']:
            for dnext in os.listdir(path):
                dnext = os.path.abspath(os.path.join(path,dnext))
                result.extend(self._scan_path(dnext, recursive, depth - 1))
        return result
    
    
    def __unicode__(self):
        return unicode(self.uuid)
    


class Task(object):
    def __init__(self, job, ontology):
        self.log = logging.getLogger('task')
        self.job = job
        self.ontology = ontology
        self.node = None
        self.uuid = uuid.uuid4()
        self._resource = None
        self.product = None
        self.query = None
        self.transform = None
    
    
    def __unicode__(self):
        return unicode(self.uuid)
    
    
    @property
    def env(self):
        return self.job.env
    
    
    @property
    def valid(self):
        return self.ontology is not None and self.resource is not None
    
    
    @property
    def cache(self):
        return self.job.cache
    
    
    @property
    def resource(self):
        if self._resource is None:
            self._resource = self.cache.find(self.ontology)
        return self._resource
    
    
    @property
    def profile(self):
        result = None
        if 'profile' in self.job.ontology:
            result = self.env.profile[self.job.ontology['profile']]
        elif 'profile' in self.resource.ontology:
            result = self.env.profile[self.resource.ontology['profile']]
        return result
    
    
    def open(self):
        self.log.debug('Open task %s', unicode(self))
        self.node = {
            'uuid':unicode(self.uuid),
            'resource':unicode(self.resource),
        }
    
    
    def close(self):
        self.log.debug('Close task %s', unicode(self))
    
    
    def run(self):
        if self.valid:
            start = datetime.now()
            self.node['start'] = unicode(start)
            
            self.product = []
            self.query = Query(self.resource.asset.resources)
            self.transform = Transform()
            self.resource.load()
            if self.resource.valid:
                action = getattr(self, self.job.ontology['action'], None)
                if action: action()
            else:
                self.log.debug(u'Ignoring invalid resource %s', unicode(self.resource))
                
            end = datetime.now()
            self.node['end'] = unicode(end)
            self.node['duration'] = unicode(end - start)
    
    
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
        
        o = Ontology.clone(self.resource.ontology)
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
        
        o = Ontology.clone(self.resource.ontology)
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
    

