#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import re
import getopt
import logging
import copy

from queue import Queue, ResourceJob, ServiceJob
from environment import Environment, CommandLineParser
from ontology import Ontology

def main():
    
    # Initialize logging and set the initial log level
    logging.basicConfig()
    logging.getLogger().setLevel(logging.INFO)
    
    # Initialize an environment
    env = Environment()
    
    # Parse the command line
    cli = CommandLineParser(env, env.interface['default'])
    env.load_interactive(cli.parse())
    cli = None
    
    # Override the initial log level
    logging.getLogger().setLevel(env.ontology['verbosity'])
    
    # Initialize a processing queue
    queue = Queue(env)
    
    # Submit a job
    queue.submit(env.ontology)
    
    # execute the next job
    job = queue.next()
    env.log.debug(u'Job %s history:\n%s', unicode(job), job.document)
    
if __name__ == '__main__':
    main()