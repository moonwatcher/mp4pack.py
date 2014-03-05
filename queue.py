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

invisible = lambda path: os.path.basename(path)[0] == '.'
extension = lambda path: os.path.splitext(path)[1]

class Queue(object):
    def __init__(self, env):
        self.log = logging.getLogger('Queue')
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
        if job:
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
        


class Condition(object):
    def __init__(self, task, node):
        self.log = logging.getLogger('Queue')
        self.task = task
        self.node = node
        
    @property
    def env(self):
        return self.queue.env
        
    @property
    def job(self):
        return self.task.job
        
    @property
    def scope(self):
        return self.node['scope']
        
    @property
    def status(self):
        return self.node['status']
        
    @property
    def reference(self):
        return self.node['reference']
        
    @property
    def satisfied(self):
        result = False
        if self.scope == 'task':
            if self.reference in self.job.journal['task'] and \
            self.job.journal['task'][self.reference].status == self.status:
                result = True
                
        elif self.scope == 'group':
            if self.reference in self.job.journal['group']:
                result = True
                for reference, task in self.job.journal['group'][self.reference].iteritems():
                    if task.status != self.status:
                        result = False
        return result
        


class Job(object):
    def __init__(self, queue, node):
        self.log = logging.getLogger('Queue')
        self.queue = queue
        self.node = node
        self.ontology = Ontology(self.env, 'ns.system.job', node['ontology'])
        self.journal = None
        self.task = None
        
        self.execution = None
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
        else:
            queue.log.warning(u'Could not infer job implementation for action')
            
                
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
        
    def load(self):
        self.log.debug('Open job %s', unicode(self))
        self.journal = {'task':{}, 'group':{}}
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
                
    def push(self, task):
        if task:
            self.journal['task'][task.key] = task
            if task.group not in self.journal['group']:
                self.journal['group'][task.group] = {}
            self.journal['group'][task.group][task.group] = task
            self.task.append(task)
            
    def pop(self):
        result = None
        for i,task in enumerate(self.task):
            if task.ready or not task.valid:
                del self.task[i]
                task.load()
                task.run()
                task.unload()
                result = task
                break
        return result
        
    def run(self):
        while self.task:
            task = self.pop()
            if task: self.execution['task'].append(task.node)
            
    def unload(self):
        self.execution['end'] = datetime.now()
        self.execution['duration'] = unicode(self.execution['end'] - self.execution['start'])
        self.log.debug('Close job %s', unicode(self))
        
    def filter(self, path):
        return path and \
        ( self._inclusion is None or self._inclusion.search(path) is not None ) and \
        ( self._exclusion is None or self._exclusion.search(path) is None )
        
    def scan(self):
        def collect(path, recursive, depth=1):
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
                    result.extend(collect(dnext, recursive, depth - 1))
                self.log.debug(u'%d files queued from %s', len(result), path)
            return result
            
        result = []
        if self.ontology['scan path']:
            for path in self.ontology['scan path']:
                if os.path.exists(path):
                    path = os.path.abspath(os.path.expanduser(os.path.expandvars(path)))
                    files = collect(path, self.ontology['recursive'])
                    result.extend(files)
                else:
                    self.log.error(u'Path %s does not exist', path)
        if result: result = sorted(set(result))
        return result
        
    def __unicode__(self):
        return self.node['uuid']
        


class Task(object):
    def __init__(self, job, ontology):
        self.log = logging.getLogger('Queue')
        self.job = job
        self.condition = None
        self.ontology = ontology
        self.node = {
            'uuid':unicode(uuid.uuid4()),
            'ontology':self.ontology.node,
            'status':'queued',
            'start':None,
            'end':None
        }
        self.node['group'] = self.node['uuid']
        
        if self.ontology is None:
            self.invalidate(u'Task ontology can not be NULL')
        
    def __unicode__(self):
        return self.key
        
    @property
    def env(self):
        return self.job.env
        
    @property
    def cache(self):
        return self.job.cache
        
    @property
    def valid(self):
        return self.status != 'invalid'
        
    @property
    def key(self):
        return self.node['uuid']
        
    @property
    def group(self):
        return self.node['group']
        
    @group.setter
    def group(self, value):
        self.node['group'] = value
        
    @property
    def ready(self):
        result = False
        if self.status == 'queued':
            result = True
            if self.condition:
                for condition in self.condition:
                    if not condition.satisfied:
                        result = False
                        break
        return result
        
    @property
    def status(self):
        return self.node['status']
        
    def invalidate(self, message):
        self.node['status'] = 'invalid'
        self.error(message)
        self.log.error(u'%s. aborting task %s', message, unicode(self))
        
    def constrain(self, node):
        if self.condition is None:
            self.condition = []
            self.node['condition'] = []
             
        condition = Condition(self, node)
        self.node['condition'].append(condition.node)
        self.condition.append(condition)
        
    def load(self):
        self.log.debug('Starting task %s', unicode(self))
        self.node['start'] = datetime.now()
        if self.valid: self.node['status'] = 'loaded'
        
    def run(self):
        if self.valid: self.node['status'] = 'running'
        
    def unload(self):
        self.node['end'] = datetime.now()
        self.node['duration'] = unicode(self.node['end'] - self.node['start'])
        if self.valid: self.node['status'] = 'completed'
        self.log.debug('Finished task %s', unicode(self))
        
    def error(self, message):
        if 'error' not in self.node: self.node['error'] = []
        self.node['error'].append(message)
        


class ResourceJob(Job):
    def __init__(self, queue, node):
        Job.__init__(self, queue, node)
        
    def filter(self, path):
        return path and not invisible(path) and Job.filter(self, path)
        
    def load(self):
        Job.load(self)
        
        targets = self.scan()
        if targets:
            self.log.info(u'%d files queued in job %s', len(targets), self)
            for path in targets:
                self.push(ResourceTask(self, self.ontology.project('ns.system.task'), path))
                


class ResourceTask(Task):
    def __init__(self, job, ontology, path):
        Task.__init__(self, job, ontology)
        self.location = self.env.repository[self.env.host].decode_resource_path(path)
        self.resource = None
        self.transform = None
        self.product = None
        self.action = None
        self._preset = None
        
        if self.location is None:
            self.invalidate(u'Invalid resource path provided {}'.format(path))
            
    @property
    def preset(self):
        if self._preset is None:
            if self.ontology['preset'] in self.env.preset:
                self._preset = self.env.preset[self.ontology['preset']]
        return self._preset
        
    def load(self):
        Task.load(self)
        if self.valid:
            if self.preset is None:
                self.invalidate(u'Could not determine preset')
            else:
                # Add the resource location and transform to the node 
                self.node['origin'] = self.location.node
                
                self.resource = self.cache.find(self.location)
                if self.resource:
                    # if the action is defined in the preset, the preset supports the action
                    if self.ontology['action'] in self.preset['action']:
                        
                        # locate a method that implements the action
                        self.action = getattr(self, self.ontology['action'], None)
                        
                        if self.action is None:
                            self.invalidate(u'Unknown action {}'.format(self.ontology['action']))
                    else:
                        self.invalidate(u'Action {} is not defined in preset {}'.format(self.ontology['action'], self.ontology['preset']))
                else:
                    self.invalidate(u'Invalid resource location')
                    
    def unload(self):
        if self.valid:
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
        if self.valid:
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
                
                # if the transform yields not viable input there really is nothing much to do...
                if not any((any(pivot.stream) for pivot in self.transform.pivot.values())):
                    self.invalidate(u'Task did not yield any viable input')
                    
            # if we are still go, invoke the action
            if self.valid: self.action()
            
    def produce(self, override=None):
        # copy the location ontology
        p = Ontology.clone(self.location)
        
        # allow the location to recalculate those concepts 
        del p['volume path']
        del p['file name']
        del p['directory']
        
        # explicitly set the volume and host from the task
        p['host'] = self.env.host
        p['volume'] = self.ontology['volume']
        
        # for copy and move we try to set a profile from the source
        if self.ontology['action'] in set(('copy', 'move', 'pack')):
            if self.resource.meta['profile']:
                p['profile'] = self.resource.meta['profile']
                
        # for transcode we try to set the profile from the transform
        elif self.ontology['action'] == 'transcode':
            for pivot in self.transform.pivot.values():
                if 'profile' in pivot.location:
                    p['profile'] = pivot.location['profile']
                    
        # whatever happened, if a profile has been explicitly provided by the task
        # it will override anything we set implicitly
        if self.ontology['profile']:
            p['profile'] = self.ontology['profile']
            
        # if an override was given set some concepts from it 
        if override:
            for i in set((
                'kind', 
                'language',
                'stream order',
                'resource path digest',
                'routing type'
            )):
                if i in override: p[i] = override[i]
                
        # try to produce a product
        product = self.resource.asset.locate_resource(p)
        if product:
            self.product.append(product)
        else:
            self.log.error(u'Could not determine destination path from:\n%s', self.env.encode_json(p))
            
        return product
        
    def info(self):
        self.resource.info(self)
        
    def copy(self):
        self.resource.copy(self)
        
    def move(self):
        self.resource.move(self)
        
    def delete(self):
        self.resource.delete(self)
        
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
        
    def prepare(self):
        # push a task to explode the resource
        o = self.job.ontology.project('ns.system.task')
        o['action'] = 'explode'
        explode = ResourceTask(self.job, o, self.location['path'])
        explode.constrain({'scope':'task', 'reference':self.key, 'status':'completed'})
        self.job.push(explode)
        
        # push a task to repack the resource fragments
        o = self.job.ontology.project('ns.system.task')
        o['action'] = 'pack'
        o['preset'] = 'fragment'
        pack = ResourceTask(self.job, o, self.location['path'])
        pack.constrain({'scope':'task', 'reference':self.key, 'status':'completed'})
        pack.constrain({'scope':'group', 'reference':explode.key, 'status':'completed'})
        self.job.push(pack)
        


class DocumentJob(Job):
    def __init__(self, queue, node):
        Job.__init__(self, queue, node)
        
    def load(self):
        Job.load(self)
        
        if self.ontology['uris']:
            for uri in self.ontology['uris']:
                self.push(DocumentTask(self, self.ontology.project('ns.system.task'), uri))
                


class DocumentTask(Task):
    def __init__(self, job, ontology, uri):
        Task.__init__(self, job, ontology)
        self.uri = uri
        self.document = None
        self.action = None
        
        if self.uri is None:
            self.invalidate(u'Invalid resource uri provided')
            
    def load(self):
        Task.load(self)
        if self.valid:
            self.document = self.env.resolver.resolve(self.uri, self.ontology['query'])
            if self.document:
                # locate a method that implements the action
                self.action = getattr(self, self.ontology['action'], None)
                
                if self.action is None:
                    self.invalidate(u'Unknown action {}'.format(self.ontology['action']))
            else:
                self.invalidate(u'Could not locate document {}'.format(self.uri))
                
    def run(self):
        Task.run(self)
        if self.valid: self.action()
        
    def get(self):
        if self.env.expression["system runtime document"].match(self.uri):
            handler = self.env.environment_json_handler
        else:
            handler = self.env.default_json_handler
            
        print json.dumps(
            self.document,
            ensure_ascii=False,
            sort_keys=True,
            indent=4,
            default=handler
        ).encode('utf-8')
        
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
        


class TableJob(Job):
    def __init__(self, queue, node):
        Job.__init__(self, queue, node)
        
    def load(self):
        Job.load(self)
        
        # if the --all flag was specificed operate on all known tables
        if self.ontology['all']:
            for table in self.env.table.keys():
                self.push(TableTask(self, self.ontology.project('ns.system.task'), table))
                
        # otherwise, if a table list was specificed, use the list to create the tasks
        elif self.ontology['tables']:
            for table in self.ontology['tables']:
                self.push(TableTask(self, self.ontology.project('ns.system.task'), table))
                


class TableTask(Task):
    def __init__(self, job, ontology, name):
        Task.__init__(self, job, ontology)
        self.action = None
        self.name = name
        self.table = None
        
        if self.name:
            # add the table name to the node
            self.node['table'] = self.name
            
            if self.name in self.env.table:
                self.table = self.env.table[self.name]
            else:
                self.invalidate(u'Unknown table {}'.format(self.name))
        else:
            self.invalidate(u'Table name can not be NULL')
            
    def load(self):
        Task.load(self)
        if self.valid:
            # locate a method that implements the action
            self.action = getattr(self, self.ontology['action'], None)
            
            if self.action is None:
                self.invalidate(u'Unknown action {}'.format(self.ontology['action']))
                
    def run(self):
        Task.run(self)
        if self.valid: self.action()
        
    def rebuild(self):
        for index in self.table['index']:
            self.env.repository[self.ontology['host']].rebuild_index(self.table['name'], index)
            


class InstructionJob(Job):
    def __init__(self, queue, node):
        Job.__init__(self, queue, node)
        
    def filter(self, path):
        return path and not invisible(path) and extension(path) == '.json' and Job.filter(self, path)
        
    def load(self):
        Job.load(self)
        
        targets = self.scan()
        if targets:
            self.log.info(u'%d files queued in job %s', len(targets), self)
            for path in targets:
                self.push(InstructionTask(self, self.ontology.project('ns.system.task'), path))
                


class InstructionTask(Task):
    def __init__(self, job, ontology, path):
        Task.__init__(self, job, ontology)
        self.path = path
        self.action = None
        if not os.path.isfile(self.path):
            self.invalidate(u'File {} does not exists'.format(path))
            
    def load(self):
        Task.load(self)
        if self.valid:
            # locate a method that implements the action
            self.action = getattr(self, self.ontology['action'], None)
            
            if self.action is None:
                self.invalidate(u'Unknown action {}'.format(self.ontology['action']))
                
    def run(self):
        Task.run(self)
        if self.valid: self.action()
        
    def populate(self):
        try:
            content = StringIO(open(self.path, 'rb').read())
        except IOError, e:
            self.invalidate(u'Failed to load file {}'.format(path))
            self.log.debug(u'Exception raised: %s', unicode(e))
        else:
            content.seek(0)
            try:
                instruction = json.load(content)
                self.log.debug(u'Loaded JSON file %s', path)
            except SyntaxError, e:
                self.invalidate(u'Syntax error in file {}'.format(path))
                self.log.debug(u'Exception raised: %s', unicode(e))
            else:
                for node in instruction:
                    self.env.resolver.save(node)
                    


