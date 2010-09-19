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
    files = list()
    file_paths = list_input_files(path, file_filter, recursive)
    for fp in file_paths:
        mf = load_media_file(fp)
        if mf != None:
            files.append(mf)
    
    return files


def list_input_files(path, file_filter, recursive):
    result = list()
    path_list = os.listdir(path)
    for p in path_list:
        if invisable_file_path.search(p) == None:
            p = os.path.abspath(os.path.join(path,p))
            if os.path.isfile(p):
                if file_filter == None or file_filter.search(p) != None:
                    result.append(unicode(p, 'utf-8'))
            elif os.path.isdir(p):
                if recursive:
                    rec_result = list_input_files(p, file_filter, recursive)
                    result += rec_result
    return result


def load_file_filter(file_filter):
    file_filter_re = None
    if file_filter != None:
        file_filter_re = re.compile(file_filter)
    return file_filter_re


def load_options():
    from optparse import OptionParser
    from optparse import OptionGroup
    from config import repository_config
    
    available_profiles = list()
    for k in repository_config['Kind'].keys():
        available_profiles += repository_config['Kind'][k]['Profile'].keys()
    
    parser = OptionParser("usage: %prog [options] [file or directory. default: . ]")
        
    group = OptionGroup(parser, "Operations", "You have to specify at least one operation to preform.")
    group.add_option("-i", "--info", dest="report", action="store_true", default=False, help="Report files info")
    group.add_option("-c", "--copy", dest="copy", action="store_true", default=False, help="Copy into repository")
    group.add_option("-n", "--rename", dest="rename", action="store_true", default=False, help="Rename to canonic file name")
    group.add_option("--tag", dest="tag", action="store_true", default=False, help="Update meta tags")
    group.add_option("--art", dest="art", action="store_true", default=False, help="Update embedded artwork")
    group.add_option("--optimize", dest="optimize", action="store_true", default=False, help="Optimize files")
    
#    group.add_option("-m", "--pack", dest="pack", help="Package to kind")
#    group.add_option("-t", "--transcode", dest="pack", help="Transcode to kind")
#    group.add_option("-e", "--extract", dest="pack", help="Extract kind")
#    group.add_option("-u", "--update", dest="pack", help="Update kind")
    
    group.add_option("-e", "--extract", dest="extract", action="store_true", default=False, help="extract into repository")
    group.add_option("-m", "--make", dest="make", action="store_true", default=False, help="make a new version")
    parser.add_option_group(group)
        
    group = OptionGroup(parser, "Modifiers", "Modify the runtime environment.")
    group.add_option("-k", "--kind", dest="kind", type="choice", choices=repository_config['Kind'].keys(), help="[default: %default]")
    group.add_option("-o", "--volume", dest="volume", type="choice", choices=repository_config['Volume'].keys(), default=None, help="Output volume [default: %default]")
    group.add_option("-p", "--profile", dest="profile", type="choice", choices=available_profiles, default=None, help="[default: %default]")
    group.add_option("-f", "--filter", dest="file_filter", default=None, help="Regex to filter input file names through")
    group.add_option("-q", "--quality", dest="quality", help="Quantizer for H.264 transcoding [default: %default]")
    group.add_option("-v", "--verbosity", dest="verbosity", default='info', type="choice", choices=log_levels.keys(), help="Logging verbosity level [default: %default]")
    group.add_option("--media-kind", dest="media-kind", type="choice", choices=repository_config['Media Kind'].keys(), help="[default: %default]")
    group.add_option("--pixel-width", dest="pixel_width", help="Max output pixel width [default: set by profile]")
    group.add_option("--language", dest="language", help="Languge code to set for undefined")
    parser.add_option_group(group)
        
    group = OptionGroup(parser, "Flags")
    group.add_option("-d", "--debug", dest="debug", action="store_true", default=False, help="Only print commands without executing")
    group.add_option("-w", "--overwrite", dest="overwrite", action="store_true", default=False, help="Allow overwriting existing files")
    group.add_option("-r", "--recursive", dest="recursive", action="store_true", default=False, help="Recursivly process sub directories")
    group.add_option("--md5", dest="md5", action="store_true", default=False, help="Calculate md5 checksum")
    parser.add_option_group(group)
    
    group = OptionGroup(parser, "Service", "service routines")
    group.add_option("--initialize", dest="initialize", action="store_true", default=False, help="Initialize the system")
    group.add_option("--map-show", dest="map_show", help="Map a TV Show TVDB ID to a name")
    parser.add_option_group(group)
    
#    Subtitle:
#    	transcode srt: encode a new subtitle file @ profile
        
#    Matroska:
#    	pack mkv: mux to matroska @ profile
#    	transcode m4v: transcode to m4v @ profile
#    	transcode mkv: transcode to mkv @ profile
#    	transcode srt: extract all subtitles to 'original' profile and than transcode subtitle to srt @ profile
#    	extract srt: extract subtitles to profile
#    	extract ass: extract subtitles to profile
#    	extract chap: extract chapters
        
#    Mpeg4:
#    	pack mkv: mux to matroska @ profile
#    	transcode m4v: transcode to m4v @ profile
#    	transcode mkv: transcode to mkv @ profile
#    	extract chap: extract chapters
#    	update srt: remux subtitles @ profile
#    	update art: update artwork
#    	update chap: update chapters
        
    
    return parser.parse_args()


def preform_operations(tag_manager, files, options):
    if options.report:
        for f in files:
            print f.__str__().encode('utf-8')
        
    if options.copy:
        for f in files:
            f.copy(options.volume, options.profile, options.overwrite, options.md5)
    
    if options.extract:
        for f in files:
            print f.extract(options.volume, options.profile, options.overwrite)
    
    if options.rename:
        for f in files:
            print f.rename()
    
    if options.make:
        for f in files:
            print f.make(options.volume, options.profile, options.overwrite)
    
    if options.tag:
        for f in files:
            print f.tag()
    
    #if options.optimize:
    
    #if options.update:
    
    #if options.ac3:
    
    if options.initialize:
        tag_manager.base_init()
    


def main():
    options, args = load_options()
    logging.basicConfig(level=log_levels[options.verbosity])
    logger = logging.getLogger('mp4pack')
    logger.info('open log')
    input_path = '.'
    
    if len(args) > 0:
        input_path = args[0]
    
    from db import TagManager
    tag_manager = TagManager()
    file_filter = load_file_filter(options.file_filter)
    
    input_path = os.path.abspath(input_path)
    logger.info('Loading file from ' + input_path)
    files = load_input_files(input_path, file_filter, options.recursive)
    preform_operations(tag_manager, files, options)
    
    logger.debug('Positional arguments: ' + args.__str__())
    for k, v in options.__dict__.iteritems():
        logger.debug('Property {0}: {1}'.format(k, v))
    
    logger.info('close log')



if __name__ == "__main__":
    main()