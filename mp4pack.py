#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import re
import getopt
import logging
import copy

from queue import Queue, ResourceJob, ServiceJob
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
        
        
        # Add the enumeration constrains
        for argument in self.node['prototype'].values():
            if 'dest' in argument['parameter']:
                archetype = self.env.archetype[argument['parameter']['dest']]
                if archetype['type'] == 'enum':
                    enumeration = self.env.enumeration[archetype['enumeration']]
                    argument['parameter']['choices'] = enumeration.synonym.keys()
                    
        # Add global arguments
        for argument in self.node['global']['argument']:
            add_argument(self.parser, argument)
            
        # Add individual command sections
        s = self.parser.add_subparsers(dest='action')
        for action in self.node['action']:
            action_parser = s.add_parser(**action['instruction'])
            for argument in action['argument']:
                add_argument(action_parser, argument)
                
            # Add groups of arguments, if any.
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
    
    # A node for collecting runtime statistics
    import json
    from datetime import datetime
    node = {
        'start':datetime.now(),
        'job':[],
    }
    
    # Initialize logging and set the initial log level
    logging.basicConfig()
    logging.getLogger().setLevel(logging.INFO)
    
    # Initialize an environment
    env = Environment()
    
    # Parser for the command line
    cli = CommandLineParser(env, env.interface['default'])
    
    # Load the interactive arguments into the environment
    env.load_interactive(cli.parse())
    
    # Discard the parser
    cli = None
    
    # Override the initial log level
    logging.getLogger().setLevel(env.ontology['verbosity'])
    
    # Initialize a processing queue
    queue = Queue(env)
    
    # Submit a job
    queue.submit(env.ontology)
    
    # execute the next job
    job = queue.next()
    
    node['job'].append(job.execution)
    node['end'] = datetime.now()
    node['duration'] = unicode(node['end'] - node['start'])
    sys.stderr.write(json.dumps(node, sort_keys=True, indent=4,  default=env.default_json_handler))


if __name__ == '__main__':
    main()