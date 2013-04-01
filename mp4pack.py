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
    env.log.debug(job.document)


if __name__ == '__main__':
    main()