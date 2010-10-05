#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
import re
import getopt
import fnmatch
import logging

from container import load_media_file
from config import repository_config
from db import tag_manager

def load_input_files(path, file_filter, recursive):
    known = []
    file_paths = list_input_files(path, file_filter, recursive)
    for fp in file_paths:
        mf = load_media_file(fp)
        if mf: known.append(mf)
    return known


def list_input_files(path, file_filter, recursive, depth=1):
    result = []
    if os.path.isfile(path):
        dname, fname = os.path.split(path)
        if (file_filter == None or file_filter.search(fname) != None) and invisable_file_path.search(fname) == None:
            result.append(unicode(os.path.abspath(path), 'utf-8'))
    
    elif (recursive or depth > 0) and os.path.isdir(path) and invisable_file_path.search(path) == None:
        for p in os.listdir(path):
            p = os.path.abspath(os.path.join(path,p))
            rec_result = list_input_files(p, file_filter, recursive, depth - 1)
            result += rec_result
    return result


def load_file_filter(file_filter):
    result = None
    if file_filter is not None:
        result = re.compile(file_filter, re.UNICODE)
    return result


def load_options():
    from optparse import OptionParser
    from optparse import OptionGroup
    from config import repository_config as rc
    
    profiles = []
    for k in rc['Kind'].keys():
        profiles += rc['Kind'][k]['Profile'].keys()
    
    profiles = tuple(set(profiles))
    
    parser = OptionParser('%prog [options] [file or directory. default: . ]')
    
    group = OptionGroup(parser, 'Actions', 'An action to preform on files found in the search path.')
    group.add_option('-i', '--info', dest='info', action='store_true', default=False, help='Show info.')
    group.add_option('-c', '--copy', dest='copy', action='store_true', default=False, help='Copy into repository.')
    group.add_option('-n', '--rename', dest='rename', action='store_true', default=False, help='Rename files to standard names.')
    group.add_option('-e', '--extract', dest='extract', action='store_true', default=False, help='Extract subtitle and chapter and transcode the extracted streams.')
    
    group.add_option('--tag', dest='tag', action='store_true', default=False, help='Update meta tags.')
    group.add_option('--optimize', dest='optimize', action='store_true', default=False, help='Optimize file layout.')
    
    group.add_option('-m', '--pack', metavar='KIND', dest='pack', type='choice', choices=rc['Action']['pack'], help='KIND is one of [ {0} ]'.format(', '.join(rc['Action']['pack'])))
    group.add_option('-t', '--transcode', metavar='KIND', dest='transcode', type='choice', choices=rc['Action']['transcode'], help='KIND is one of [ {0} ]'.format(', '.join(rc['Action']['transcode'])))
    group.add_option('-u', '--update', metavar='KIND', dest='update', type='choice', choices=rc['Action']['update'], help='KIND is one of [ {0} ]'.format(', '.join(rc['Action']['update'])))
    
    parser.add_option_group(group)
        
    group = OptionGroup(parser, 'Modifiers')
    group.add_option('-o', '--volume', dest='volume', type='choice', choices=rc['Volume'].keys(), default=None, help='Output volume [ default: auto detect ]')
    group.add_option('-p', '--profile', dest='profile', type='choice', choices=profiles, default=None, help='[ default: auto detect ]')
    group.add_option('-f', '--filter', metavar='REGEX', dest='file_filter', default=None, help='Regex to filter selected file names')
    group.add_option('-w', '--overwrite', dest='overwrite', action='store_true', default=False, help='Overwrite existing files')
    group.add_option('-r', '--recursive', dest='recursive', action='store_true', default=False, help='Recursively process sub directories.')
    group.add_option('-v', '--verbosity', metavar='LEVEL', dest='verbosity', default='info', type='choice', choices=log_levels.keys(), help='Logging verbosity level [ default: %default ]')
    group.add_option('-d', '--debug', dest='debug', action='store_true', default=False, help='Only print commands without executing. Also good for dumping the commands into a text file and editing before execution.')
    group.add_option('-q', '--quality', metavar='QUANTIZER', dest='quality', type='float', help='H.264 transcoding Quantizer.')
    group.add_option('--pixel-width', metavar='WIDTH', type='int', dest='pixel_width', help='Max output pixel width [ default: set by profile ]')
    group.add_option('--language', metavar='CODE', dest='language', default='eng', help='Languge code used when undefined. [ default: %default ]')
    group.add_option('--md5', dest='md5', action='store_true', default=False, help='Verify md5 checksum on copy.')
    parser.add_option_group(group)
    
    group = OptionGroup(parser, 'Options that only apply to subtitles.')
    group.add_option('--input-rate', metavar='RATE', dest='input_rate', default=None, help='Decoding subtitles frame rate.')
    group.add_option('--output-rate', metavar='RATE', dest='output_rate', default=None, help='Encoding subtitles frame rate.')
    group.add_option('--time-shift', metavar='TIME', dest='time_shift', type='int', default=None, help='Subtitles shift offset in milliseconds.')
    parser.add_option_group(group)
    
    group = OptionGroup(parser, 'Service', 'Options for initializing the repository.')
    group.add_option('--initialize', dest='initialize', action='store_true', default=False, help='Run only once to initialize the system.')
    group.add_option('--map-show', metavar="MAP", dest='map_show', help='Map TV Show name to TVDB ID. format: <id>:<name>')
    parser.add_option_group(group)
    
##    Subtitle:
##    	transcode srt: encode a new subtitle file @ profile
        
##    Matroska:
##    	pack mkv: mux to matroska @ profile
##    	transcode m4v: transcode to m4v @ profile
##    	transcode mkv: transcode to mkv @ profile
##    	extract: extract chapters and srt and ass subtitles
        
##    Mpeg4:
##    	pack mkv: mux to matroska @ profile
##    	transcode m4v: transcode to m4v @ profile
##    	transcode mkv: transcode to mkv @ profile
##    	update srt: remux subtitles @ profile
##    	update jpg: update artwork
##    	update txt: update chapters
##    	extract: extract chapters
    
##   Artwork
##   transcode jpg: transcode to jpg @ profile
##   transcode png: transcode to png @ profile
    
    return parser.parse_args()


def preform_operations(files, options):
    if options.initialize:
        tag_manager.base_init()
    
    if options.map_show:
        tag_manager.map_show_with_pair(options.map_show)
    
    known = []
    unknown = []
        
    for f in files:
        f.load()
        if f and not f.valid():
            unknown.append(f.file_path)
            f.unload()
            f = None
            
        else:
            known.append(f)
            
            if options.info:
                print unicode(f).encode('utf-8')
            
            if options.extract:
                f.extract(options)
            
            if options.copy:
                f.copy(options)
    
            if options.rename:
                f.rename(options)
    
            if options.tag:
                f.tag(options)
    
            if options.optimize:
                f.optimize(options)
            
            if options.pack is not None:
                f.pack(options)
    
            if options.transcode is not None:
                f.transcode(options)
    
            if options.update is not None:
                f.update(options)
        
            f.unload()
    return known, unknown 


def main():
    print 'mp4pack.py a media collection manager\nLior Galanti lior.galanti@gmail.com\n'.encode('utf-8')
    options, args = load_options()
    logging.basicConfig(level=log_levels[options.verbosity])
    logger = logging.getLogger('mp4pack')
    input_path = '.'
    
    if len(args) > 0:
        input_path = args[0]
    
    file_filter = load_file_filter(options.file_filter)
    input_path = os.path.abspath(input_path)
    logger.info('Scanning for files in %s', input_path)
    known = load_input_files(input_path, file_filter, options.recursive)
    
    known, unknown = preform_operations(known, options)
    
    if len(known) > 0:
        logger.info(u'%d valid files were found in %s', len(known), input_path)
        for p in known:
            logger.debug(u'Found valid %s', p.file_path)
        
    if len(unknown) > 0:
        logger.warning(u'%d invalid files were found in %s', len(unknown), input_path)
        for p in unknown:
            logger.info(u'Found invalid %s', p)
    
    
    indent = repository_config['Display']['indent']
    margin = repository_config['Display']['margin']
    for idx, arg in enumerate(args):
        logger.debug('Positional %d: %s', idx, arg)
        
    for k, v in options.__dict__.iteritems():
        logger.debug('Option {0:-<{2}}: {1}'.format(k, v, indent - 2 - margin))


log_levels = {
    'debug': logging.DEBUG,
    'info': logging.INFO,
    'warning': logging.WARNING,
    'error': logging.ERROR,
    'critical': logging.CRITICAL
}

invisable_file_path = re.compile(ur'^\.', re.UNICODE)

if __name__ == '__main__':
    main()