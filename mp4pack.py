#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
import re
import getopt
import fnmatch
import logging

from container import *

log_levels = {
    'debug': logging.DEBUG,
    'info': logging.INFO,
    'warning': logging.WARNING,
    'error': logging.ERROR,
    'critical': logging.CRITICAL
}

invisable_file_path = re.compile(r'^\..*$')


def load_input_files(path, file_filter, recursive):
    known = list()
    unknown = list()
    file_paths = list_input_files(path, file_filter, recursive)
    for fp in file_paths:
        mf = load_media_file(fp)
        if mf != None:
            known.append(mf)
        else:
            unknown.append(fp)
    return known, unknown


def list_input_files(path, file_filter, recursive):
    result = list()
    if os.path.isfile(path):
        dname, fname = os.path.split(path)
        if (file_filter == None or file_filter.search(fname) != None) and invisable_file_path.search(fname) == None:
            result.append(unicode(os.path.abspath(path), 'utf-8'))
    
    elif recursive and os.path.isdir(path) and invisable_file_path.search(path) == None:
        for p in os.listdir(path):
            p = os.path.abspath(os.path.join(path,p))
            rec_result = list_input_files(p, file_filter, recursive)
            result += rec_result
    return result


def load_file_filter(file_filter):
    result = None
    if file_filter != None:
        result = re.compile(file_filter)
    return result


def load_options():
    from optparse import OptionParser
    from optparse import OptionGroup
    from config import repository_config
    
    available_profiles = list()
    for k in repository_config['Kind'].keys():
        available_profiles += repository_config['Kind'][k]['Profile'].keys()
    
    parser = OptionParser('%prog [options] [file or directory. default: . ]')
        
    group = OptionGroup(parser, 'Operations', 'You must specify at least one operation')
    group.add_option('-i', '--info', dest='info', action='store_true', default=False, help='Show info')
    group.add_option('-c', '--copy', dest='copy', action='store_true', default=False, help='Copy into repository')
    group.add_option('-n', '--rename', dest='rename', action='store_true', default=False, help='Rename files to standard names')
    group.add_option('--tag', dest='tag', action='store_true', default=False, help='Update meta tags')
    group.add_option('--art', dest='art', action='store_true', default=False, help='Update embedded artwork')
    group.add_option('--optimize', dest='optimize', action='store_true', default=False, help='Optimize file layout')
    
    group.add_option('-m', '--pack', metavar='KIND', dest='pack', type='choice', choices=repository_config['Action']['pack'], help='Package to ' + repository_config['Action']['pack'].__str__())
    group.add_option('-t', '--transcode', metavar='KIND', dest='transcode', type='choice', choices=repository_config['Action']['transcode'], help='Transcode to ' + repository_config['Action']['transcode'].__str__())
    group.add_option('-e', '--extract', metavar='KIND', dest='extract', type='choice', choices=repository_config['Action']['extract'], help='Extract to ' + repository_config['Action']['extract'].__str__())
    group.add_option('-u', '--update', metavar='KIND', dest='update', type='choice', choices=repository_config['Action']['update'], help='Update to ' + repository_config['Action']['update'].__str__())
    parser.add_option_group(group)
        
    group = OptionGroup(parser, 'Modifiers')
    group.add_option('-o', '--volume', dest='volume', type='choice', choices=repository_config['Volume'].keys(), default=None, help='Output volume [default: auto detect]')
    group.add_option('-p', '--profile', dest='profile', type='choice', choices=available_profiles, default=None, help='[default: %default]')
    group.add_option('-f', '--filter', metavar='REGEX', dest='file_filter', default=None, help='Regex to filter selected file names')
    group.add_option('-w', '--overwrite', dest='overwrite', action='store_true', default=False, help='Overwrite existing files.')
    group.add_option('-r', '--recursive', dest='recursive', action='store_true', default=False, help='Recursivly process sub directories.')
    group.add_option('-v', '--verbosity', metavar='LEVEL', dest='verbosity', default='info', type='choice', choices=log_levels.keys(), help='Logging verbosity level [default: %default]')
    group.add_option('-d', '--debug', dest='debug', action='store_true', default=False, help='Only print commands without executing. Also good for dumping the commands into a text file and editing before execution.')
    group.add_option('-q', '--quality', metavar='QUANTIZER', dest='quality', type='float', help='H.264 transcoding Quantizer')
    group.add_option('--pixel-width', metavar='WIDTH', type='int', dest='pixel_width', help='Max output pixel width [default: profile dependent]')
    group.add_option('--media-kind', dest='media_kind', type='choice', choices=repository_config['Media Kind'].keys(), help='[default: auto detect]')
    group.add_option('--language', metavar='CODE', dest='language', default='eng', help='Languge code used when undefined')
    group.add_option('--md5', dest='md5', action='store_true', default=False, help='Varify md5 checksum on copy')
    parser.add_option_group(group)
    
    
    group = OptionGroup(parser, 'Options that only apply to text subtitles')
    group.add_option('--input-rate', metavar='RATE', dest='input_rate', default=None, help='Decoding subtitles frame rate.')
    group.add_option('--output-rate', metavar='RATE', dest='output_rate', default=None, help='Encoding subtitles frame rate.')
    group.add_option('--time-shift', metavar='TIME', dest='time_shift', type='int', default=None, help='Subtitles shift offset in miliseconds.')
    parser.add_option_group(group)
    
    
    
    group = OptionGroup(parser, 'Service', 'Options for initializing the repository.')
    group.add_option('--initialize', dest='initialize', action='store_true', default=False, help='Run only once to initialize the system.')
    group.add_option('--map-show', metavar="MAP", dest='map_show', help='For TV Shows you must provide a mapping between the numeric TVDB ID and a simplified name that will be used in file names.')
    parser.add_option_group(group)
    
##    Subtitle:
##    	transcode srt: encode a new subtitle file @ profile
        
##    Matroska:
##    	pack mkv: mux to matroska @ profile
##    	transcode m4v: transcode to m4v @ profile
##    	transcode mkv: transcode to mkv @ profile
##    	transcode srt: extract all subtitles to 'original' profile and than transcode subtitle to srt @ profile
##    	extract srt: extract subtitles to profile
##    	extract ass: extract subtitles to profile
##    	extract txt: extract chapters
        
#    Mpeg4:
##    	pack mkv: mux to matroska @ profile
##    	transcode m4v: transcode to m4v @ profile
##    	transcode mkv: transcode to mkv @ profile
##    	extract txt: extract chapters
#    	update srt: remux subtitles @ profile
#    	update art: update artwork
#    	update txt: update chapters
        
    
    return parser.parse_args()


def preform_operations(files, options):
    if options.info:
        for f in files:
            print f.info(options).encode('utf-8')
            
    if options.copy:
        for f in files:
            f.copy(options)
    
    if options.rename:
        for f in files:
            f.rename(options)
    
    if options.tag:
        for f in files:
            f.tag(options)
    
    if options.art:
        for f in files:
            f.art(options)
            
    if options.optimize:
        for f in files:
            f.optimize(options)
    
    
    if options.pack != None:
        for f in files:
            f.pack(options)
    
    if options.transcode != None:
        for f in files:
            f.transcode(options)
    
    if options.extract != None:
        for f in files:
            f.extract(options)
            
    if options.update != None:
        for f in files:
            f.update(options)
    
    
    if options.initialize:
        from db import TagManager
        t = TagManager()
        t.base_init()
    


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
    logger.info('Scanning for files in ' + input_path)
    known, unknown = load_input_files(input_path, file_filter, options.recursive)
    
    if len(known) > 0:
        preform_operations(known, options)
        logger.info(u'{0} valid files were found in {1}'.format(str(len(known)), input_path))
        for p in known:
            logger.info(u'Found {0}'.format(p.file_path))
        
    if len(unknown) > 0:
        logger.warning(u'{0} file paths could not be understood'.format(str(len(unknown))))
        for p in unknown:
            logger.warning(u'{0} is an unknown path'.format(p))
    
    
    indent = repository_config['Display']['indent']
    margin = repository_config['Display']['margin']
    for index in range(len(args)):
        logger.debug('Positional {0}: {1}'.format(index, args[index]))
        
    for k, v in options.__dict__.iteritems():
        logger.debug('Option {0:-<{2}}: {1}'.format(k, v, indent - 2 - margin))



if __name__ == '__main__':
    main()