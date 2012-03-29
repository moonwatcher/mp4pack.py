#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import re
import getopt
import logging
import copy

from queue import Queue, Job
from environment import Environment
from ontology import Ontology
from argparse import ArgumentParser

class CommandLineParser(object):
    def __init__(self, env, node):
        self.env = env
        self.node = node
        self.parser = ArgumentParser()
        self.load()
    
    
    def load(self):
        def add_argument(parser, name):
            node = self.node['prototype'][name]
            parser.add_argument(*node['flag'], **node['parameter'])
        
        
        for argument in self.node['prototype'].values():
            if 'dest' in argument['parameter']:
                archetype = self.env.archetype[argument['parameter']['dest']]
                if archetype['type'] == 'enum':
                    enumeration = self.env.enumeration[archetype['enumeration']]
                    argument['parameter']['choices'] = enumeration.synonym.keys()
                    
        for argument in self.node['global']['argument']:
            add_argument(self.parser, argument)
            
        s = self.parser.add_subparsers(dest='action')
        for action in self.node['action']:
            action_parser = s.add_parser(**action['instruction'])
            for argument in action['argument']:
                add_argument(action_parser, argument)
                
            if 'group' in action:
                for group in action['group']:
                    group_parser = action_parser.add_argument_group(**group['instruction'])
                    for argument in group['argument']:
                        add_argument(group_parser, argument)
    
    
    def parse(self):
        arguments = vars(self.parser.parse_args())
        ontology = Ontology(self.env, self.node['namespace'])
        for k,v in arguments.iteritems():
            ontology.decode(k, v)
        return ontology
    


def main():
    # Initialize logging and set the initial log level
    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)
    
    # Initialize the environment
    env = Environment()
    
    # Decode command line arguments
    cli = CommandLineParser(env, env.interface['default'])
    
    # Load the interactive arguments into the environment
    env.load_interactive(cli.parse())
    
    # Override the initial log level
    logging.getLogger().setLevel(env.ontology['verbosity'])
    
    # Initialize a processing queue
    queue = Queue(env)
    
    #test(env)
    #test2(env)
    
    job = Job(queue, env.ontology)
    job.open()
    job.run()
    job.close()
    print job.node


def test(env):
    env.resolver.cache(u'mpk://yoshi/c/tvdb/show/en/73255/complete')
    print env.resolver.resolve(u'mpk://yoshi/c/tvdb/episode/en/73255/4/7')
    print env.resolver.resolve(u'mpk://yoshi/c/tvdb/show/73255/poster')
    
    print env.resolver.resolve(u'mpk://yoshi/c/tmdb/configuration')
    
    env.resolver.remove(u'mpk://yoshi/c/tmdb/movie/1891/cast')
    print env.resolver.resolve(u'mpk://yoshi/c/tmdb/movie/en/1891')
    print env.resolver.resolve(u'mpk://yoshi/c/tmdb/movie/1891/cast')
    print env.resolver.resolve(u'mpk://yoshi/c/tmdb/movie/1891/poster')
    print env.resolver.resolve(u'mpk://yoshi/c/tmdb/movie/1891/keyword')
    print env.resolver.resolve(u'mpk://yoshi/c/tmdb/movie/1891/release')
    print env.resolver.resolve(u'mpk://yoshi/c/tmdb/movie/1891/trailer')
    print env.resolver.resolve(u'mpk://yoshi/c/tmdb/movie/1891/translation')
    print env.resolver.resolve(u'mpk://yoshi/c/tmdb/movie/1891/alternative')
    
    print env.resolver.resolve(u'mpk://yoshi/c/tmdb/movie/en/tt0080684')
    print env.resolver.resolve(u'mpk://yoshi/c/tmdb/movie/tt0080684/cast')
    print env.resolver.resolve(u'mpk://yoshi/c/tmdb/movie/tt0080684/poster')
    print env.resolver.resolve(u'mpk://yoshi/c/tmdb/movie/tt0080684/keyword')
    print env.resolver.resolve(u'mpk://yoshi/c/tmdb/movie/tt0080684/release')
    print env.resolver.resolve(u'mpk://yoshi/c/tmdb/movie/tt0080684/trailer')
    print env.resolver.resolve(u'mpk://yoshi/c/tmdb/movie/tt0080684/translation')
    print env.resolver.resolve(u'mpk://yoshi/c/tmdb/movie/tt0080684/alternative')
    
    
    
    print env.resolver.resolve(u'mpk://yoshi/c/tmdb/person/1891')
    print env.resolver.resolve(u'mpk://yoshi/c/tmdb/person/1891/credit')
    print env.resolver.resolve(u'mpk://yoshi/c/tmdb/person/1891/poster')


def test2(env):
    from crawler import Crawler
    paths = [
        'file://yoshi/Users/lg/Downloads/samurai jack s01e07 jack and the three blind archers.m4v',
        'file://multivac/net/vito/media/tlv/eta/movie/mkv/1080/IMDbtt0076759 star wars episode iv - a new hope.mkv',
        'file://multivac/net/multivac/Volumes/alphaville/alpha/tvshow/srt/clean/3rd rock from the sun/1/eng/3rd rock from the sun s01e02 post nasal dick.srt',
        'file://yoshi/Users/lg/Downloads/mpk/pool/epsilon/tvshow/dts/original/weeds/7/en/weeds s07e01 bags.dts',
    ]
    import json
    import datetime
    dthandler = lambda obj: obj.isoformat() if isinstance(obj, datetime.datetime) else None
    
    for path in paths:
        o = env.parse_url(path)
        c = Crawler(o)
        n = c.node
        print o['resource uri']
        print o['asset uri']
        #print json.dumps(n, sort_keys=True, indent=4,  default=dthandler)



if __name__ == '__main__':
    main()