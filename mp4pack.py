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

def decode_cli(env):
    
    # Global arguments for all commands
    p = ArgumentParser()
    p.add_argument('-L', '--local',                 dest='location',    metavar='LOC', help='name of local repository')
    p.add_argument('-R', '--repo',                  dest='repository',  metavar='REPO', help='name of repository to use')
    p.add_argument('-v', '--verbosity',             dest='verbosity',   metavar='LEVEL', choices=log_levels.keys(), default='info', help='logging verbosity level [default: %(default)s]')
    p.add_argument('-d', '--debug',                 dest='debug',       action='store_true', default=False, help='only print commands without executing')
    p.add_argument('--conf',                        dest='conf',        metavar='PATH', help='path for external config file')
    p.add_argument('--version',                                         action='version', version='%(prog)s 0.5')
    
    # A different parser for every action
    s = p.add_subparsers(dest='action')
    c = {}
    
    c['report'] = s.add_parser('report', help='print information')
    c['report'].add_argument('scan',                                      metavar='PATH', nargs='*', help='file or directory paths to scan')
    c['report'].add_argument('-f', '--include',       dest='inclusion',   metavar='EXP', help='file name regex filter')
    c['report'].add_argument('-r', '--recursive',     dest='recursive',   action='store_true', default=False, help='recursively process sub directories')
    c['report'].add_argument('-S', '--sync',          dest='sync',        action='store_true', default=False, help='sync encountered records with online service')
    c['report'].add_argument('-U', '--crawl',         dest='crawl',       action='store_true', default=False, help='rebuild physical file index')
    c['report'].add_argument('-D', '--download',      dest='download',    action='store_true', default=False, help='download if local is unavailable')
    c['report'].add_argument('-w', '--overwrite',     dest='overwrite',   action='store_true', default=False, help='overwrite existing files')
    
    c['rename'] = s.add_parser('rename', help='rename files to canonic names')
    c['rename'].add_argument('scan',                                    metavar='PATH', nargs='*', help='file or directory paths to scan')
    c['rename'].add_argument('-f', '--include',     dest='inclusion',   metavar='EXP', help='file name regex filter')
    c['rename'].add_argument('-r', '--recursive',   dest='recursive',   action='store_true', default=False, help='recursively process sub directories')
    c['rename'].add_argument('-S', '--sync',        dest='sync',        action='store_true', default=False, help='sync encountered records with online service')
    c['rename'].add_argument('-U', '--crawl',       dest='crawl',       action='store_true', default=False, help='rebuild physical file index')
    c['rename'].add_argument('-w', '--overwrite',   dest='overwrite',   action='store_true', default=False, help='overwrite existing files')
    
    c['tag'] = s.add_parser('tag', help='update meta tags')
    c['tag'].add_argument('scan',                                       metavar='PATH', nargs='*', help='file or directory paths to scan')
    c['tag'].add_argument('-f', '--include',        dest='inclusion',   metavar='EXP', help='file name regex filter')
    c['tag'].add_argument('-r', '--recursive',      dest='recursive',   action='store_true', default=False, help='recursively process sub directories')
    c['tag'].add_argument('-S', '--sync',           dest='sync',        action='store_true', default=False, help='sync encountered records with online service')
    c['tag'].add_argument('-U', '--crawl',          dest='crawl',       action='store_true', default=False, help='rebuild physical file index')
    
    c['pack'] = s.add_parser('pack', help='pack streams into container')
    c['pack'].add_argument('scan',                                      metavar='PATH', nargs='*', help='file or directory paths to scan')
    c['pack'].add_argument('-k', '--kind',          dest='kind',        metavar='KIND', help='explicit kind to process')
    c['pack'].add_argument('-o', '--volume',        dest='volume',      metavar='VOL', help='explicit volume to use')
    c['pack'].add_argument('-p', '--profile',       dest='profile',     metavar='PROFILE', help='explicit profile to use')
    c['pack'].add_argument('-f', '--include',       dest='inclusion',   metavar='EXP', help='file name regex filter')
    c['pack'].add_argument('-r', '--recursive',     dest='recursive',   action='store_true', default=False, help='recursively process sub directories')
    c['pack'].add_argument('-S', '--sync',          dest='sync',        action='store_true', default=False, help='sync encountered records with online service')
    c['pack'].add_argument('-U', '--crawl',         dest='crawl',       action='store_true', default=False, help='rebuild physical file index')
    c['pack'].add_argument('-w', '--overwrite',     dest='overwrite',   action='store_true', default=False, help='overwrite existing files')
    c['pack'].add_argument('-l', '--lang',          dest='language',    metavar='CODE', default='en', help='languge code to use when und [default: %(default)s]')
    
    c['update'] = s.add_parser('update', help='update streams in container')
    c['update'].add_argument('scan',                                    metavar='PATH', nargs='*', help='file or directory paths to scan')
    c['update'].add_argument('-k', '--kind',        dest='kind',        metavar='KIND', help='explicit kind to process')
    c['update'].add_argument('-o', '--volume',      dest='volume',      metavar='VOL', help='explicit volume to use')
    c['update'].add_argument('-p', '--profile',     dest='profile',     metavar='PROFILE', help='explicit profile to use')
    c['update'].add_argument('-f', '--include',     dest='inclusion',   metavar='EXP', help='file name regex filter')
    c['update'].add_argument('-r', '--recursive',   dest='recursive',   action='store_true', default=False, help='recursively process sub directories')
    c['update'].add_argument('-S', '--sync',        dest='sync',        action='store_true', default=False, help='sync encountered records with online service')
    c['update'].add_argument('-U', '--crawl',       dest='crawl',       action='store_true', default=False, help='rebuild physical file index')
    c['update'].add_argument('-D', '--download',    dest='download',    action='store_true', default=False, help='download if local is unavailable')
    
    c['transcode'] = s.add_parser('transcode', help='transcode into a new profile')
    c['transcode'].add_argument('scan',                                 metavar='PATH', nargs='*', help='file or directory paths to scan')
    c['transcode'].add_argument('-k', '--kind',     dest='kind',        metavar='KIND', help='explicit kind to process')
    c['transcode'].add_argument('-o', '--volume',   dest='volume',      metavar='VOL', help='explicit volume to use')
    c['transcode'].add_argument('-p', '--profile',  dest='profile',     metavar='PROFILE', help='explicit profile to use')
    c['transcode'].add_argument('-f', '--include',  dest='inclusion',   metavar='EXP', help='file name regex filter')
    c['transcode'].add_argument('-r', '--recursive',dest='recursive',   action='store_true', default=False, help='recursively process sub directories')
    c['transcode'].add_argument('-S', '--sync',     dest='sync',        action='store_true', default=False, help='sync encountered records with online service')
    c['transcode'].add_argument('-U', '--crawl',    dest='crawl',       action='store_true', default=False, help='rebuild physical file index')
    c['transcode'].add_argument('-D', '--download', dest='download',    action='store_true', default=False, help='download if local is unavailable')
    c['transcode'].add_argument('-w', '--overwrite',dest='overwrite',   action='store_true', default=False, help='overwrite existing files')
    
    g = c['transcode'].add_argument_group('video processing')
    g.add_argument('-q', '--quality',               dest='quality',     metavar='QUANTIZER', type=float)
    g.add_argument('-W', '--width',                 dest='pixel width', metavar='WIDTH', type=int, help='override profile output pixel width')
    g.add_argument('--crop',                        dest='crop',        metavar='T:B:L:R', help='set HandBrake cropping values [default: autocrop]')
    
    g = c['transcode'].add_argument_group('subtitle processing')
    g.add_argument('--NTSC',                        dest='NTSC',        action='store_true', default=False, help='convert from PAL to NTSC framerate')
    g.add_argument('--PAL',                         dest='PAL',         action='store_true', default=False, help='convert from NTSC to PAL framerate')
    g.add_argument('--shift',                       dest='shift time',  metavar='TIME', type=int, help='shift offset in milliseconds')
    g.add_argument('--source-fps',                  dest='source fps',  metavar='FPS', help='subtitles decoding frame rate')
    g.add_argument('--target-fps',                  dest='target fps',  metavar='FPS', help='subtitles encoding frame rate')
    
    c['copy'] = s.add_parser('copy', help='copy files to repository')
    c['copy'].add_argument('scan',                                      metavar='PATH', nargs='*', help='file or directory paths to scan')
    c['copy'].add_argument('-o', '--volume',        dest='volume',      metavar='VOL', help='explicit volume to use')
    c['copy'].add_argument('-p', '--profile',       dest='profile',     metavar='PROFILE', help='explicit profile to use')
    c['copy'].add_argument('-f', '--include',       dest='inclusion',   metavar='EXP', help='file name regex filter')
    c['copy'].add_argument('-r', '--recursive',     dest='recursive',   action='store_true', default=False, help='recursively process sub directories')
    c['copy'].add_argument('-S', '--sync',          dest='sync',        action='store_true', default=False, help='sync encountered records with online service')
    c['copy'].add_argument('-U', '--crawl',         dest='crawl',       action='store_true', default=False, help='rebuild physical file index')
    c['copy'].add_argument('-w', '--overwrite',     dest='overwrite',   action='store_true', default=False, help='overwrite existing files')
    c['copy'].add_argument('--md5',                 dest='md5',         action='store_true', default=False, help='verify md5 checksum after copy')
    
    c['extract'] = s.add_parser('extract', help='extract streams into repository')
    c['extract'].add_argument('scan',                                   metavar='PATH', nargs='*', help='file or directory paths to scan')
    c['extract'].add_argument('-o', '--volume',     dest='volume',      metavar='VOL', help='explicit volume to use')
    c['extract'].add_argument('-p', '--profile',    dest='profile',     metavar='PROFILE', help='explicit profile to use')
    c['extract'].add_argument('-f', '--include',    dest='inclusion',   metavar='EXP', help='file name regex filter')
    c['extract'].add_argument('-r', '--recursive',  dest='recursive',   action='store_true', default=False, help='recursively process sub directories')
    c['extract'].add_argument('-S', '--sync',       dest='sync',        action='store_true', default=False, help='sync encountered records with online service')
    c['extract'].add_argument('-U', '--crawl',      dest='crawl',       action='store_true', default=False, help='rebuild physical file index')
    c['extract'].add_argument('-w', '--overwrite',  dest='overwrite',   action='store_true', default=False, help='overwrite existing files')
    
    c['optimize'] = s.add_parser('optimize', help='optimize file structure')
    c['optimize'].add_argument('scan',                                  metavar='PATH', nargs='*', help='file or directory paths to scan')
    c['optimize'].add_argument('-f', '--include',   dest='inclusion',   metavar='EXP', help='file name regex filter')
    c['optimize'].add_argument('-r', '--recursive', dest='recursive',   action='store_true', default=False, help='recursively process sub directories')
    c['optimize'].add_argument('-S', '--sync',      dest='sync',        action='store_true', default=False, help='sync encountered records with online service')
    c['optimize'].add_argument('-U', '--crawl',     dest='crawl',       action='store_true', default=False, help='rebuild physical file index')
    
    c['clean'] = s.add_parser('clean', help='clean repository indexes')
    c['initialize'] = s.add_parser('initialize', help='initialize the repository')
    
    o = Ontology(env, vars(p.parse_args()))
    return o


def main():
    # Initialize logging and set the initial log level
    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)
    
    # Initialize the environment
    env = Environment()
    
    # Decode command line arguments
    arguments = decode_cli(env)
    
    # Load the interactive arguments into the environment
    env.load_interactive(arguments)
    
    # Override the initial log level
    logging.getLogger().setLevel(env.verbosity)
    
    # Initialize a processing queue
    queue = Queue(env)
    
    job = Job(queue, arguments)
    job.open()
    job.run()
    job.close()
    print job.node


log_levels = {
    'debug': logging.DEBUG,
    'info': logging.INFO,
    'warning': logging.WARNING,
    'error': logging.ERROR,
    'critical': logging.CRITICAL
}
    
if __name__ == '__main__':
    main()