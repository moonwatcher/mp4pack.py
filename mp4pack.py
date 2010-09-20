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
    
    parser = OptionParser("%prog [options] [file or directory. default: . ]")
        
    group = OptionGroup(parser, "Operations", "You must specify at least one operation")
    group.add_option("-i", "--info", dest="info", action="store_true", default=False, help="Show info")
    group.add_option("-c", "--copy", dest="copy", action="store_true", default=False, help="Copy into repository")
    group.add_option("-n", "--rename", dest="rename", action="store_true", default=False, help="Rename files to standard names")
    group.add_option("--tag", dest="tag", action="store_true", default=False, help="Update meta tags")
    group.add_option("--art", dest="art", action="store_true", default=False, help="Update embedded artwork")
    group.add_option("--optimize", dest="optimize", action="store_true", default=False, help="Optimize files")
    
    pack_choices = ['mkv']
    transcode_choices = ['m4v', 'mkv', 'srt']
    extract_choices = ['srt', 'ass']
    update_choices = ['srt']
    
    group.add_option("-m", "--pack", metavar="KIND", dest="pack", type="choice", choices=pack_choices, help="Package to " + pack_choices.__str__())
    group.add_option("-t", "--transcode", metavar="KIND", dest="transcode", type="choice", choices=transcode_choices, help="Transcode to " + transcode_choices.__str__())
    group.add_option("-e", "--extract", metavar="KIND", dest="extract", type="choice", choices=extract_choices, help="Extract to " + extract_choices.__str__())
    group.add_option("-u", "--update", metavar="KIND", dest="update", type="choice", choices=update_choices, help="Update to " + update_choices.__str__())
    
    parser.add_option_group(group)
        
    group = OptionGroup(parser, "Modifiers")
    group.add_option("-o", "--volume", dest="volume", type="choice", choices=repository_config['Volume'].keys(), default=None, help="Output volume [default: %default]")
    group.add_option("-p", "--profile", dest="profile", type="choice", choices=available_profiles, default=None, help="[default: %default]")
    group.add_option("-f", "--filter", metavar="REGEX", dest="file_filter", default=None, help="Regex to filter input file names through")
    group.add_option("-q", "--quality", metavar="QUANTIZER", dest="quality", help="Quantizer for H.264 transcoding [default: %default]")
    group.add_option("-v", "--verbosity", metavar="LEVEL", dest="verbosity", default='info', type="choice", choices=log_levels.keys(), help="Logging verbosity level [default: %default]")
    group.add_option("--media-kind", dest="media_kind", type="choice", choices=repository_config['Media Kind'].keys(), help="[default: %default]")
    group.add_option("--pixel-width", metavar="WIDTH", dest="pixel_width", help="Max output pixel width [default: set by profile]")
    group.add_option("--language", metavar="CODE", dest="language", help="Languge code to set for undefined")
    parser.add_option_group(group)
        
    group = OptionGroup(parser, "Flags")
    group.add_option("-d", "--debug", dest="debug", action="store_true", default=False, help="Only print commands without executing")
    group.add_option("-w", "--overwrite", dest="overwrite", action="store_true", default=False, help="Allow overwriting existing files")
    group.add_option("-r", "--recursive", dest="recursive", action="store_true", default=False, help="Recursivly process sub directories")
    group.add_option("-5", "--md5", dest="md5", action="store_true", default=False, help="Varify md5 checksum on copy")
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
    if options.info:
        for f in files:
            print f.info()
            
    if options.copy:
        for f in files:
            f.copy(options.volume, options.profile, options.overwrite, options.md5)
    
    if options.rename:
        for f in files:
            f.rename()
    
    if options.tag:
        for f in files:
            f.tag()
    
    if options.art:
        for f in files:
            f.art()
            
    if options.optimize:
        for f in files:
            f.optimize()
    
    
    if options.pack != None:
        for f in files:
            f.pack(options.pack, options.volume, options.profile, options.overwrite)
    
    if options.transcode != None:
        for f in files:
            f.transcode(options.transcode, options.volume, options.profile, options.overwrite)
    
    if options.extract != None:
        for f in files:
            f.extract(options.extract, options.volume, options.profile, options.overwrite)
            
    if options.update != None:
        for f in files:
            f.update(options.update, options.volume, options.profile, options.overwrite)
    
    
    if options.initialize:
        tag_manager.base_init()
    


def main():
    print 'mp4pack.py a media collection manager\nLior Galanti lior.galanti@gmail.com\n'
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
    logger.info('Scanning for files in ' + input_path)
    files = load_input_files(input_path, file_filter, options.recursive)
    preform_operations(tag_manager, files, options)
    
    logger.debug('Positional arguments: ' + args.__str__())
    for k, v in options.__dict__.iteritems():
        logger.debug('Property {0}: {1}'.format(k, v))
    
    logger.info('close log')



if __name__ == "__main__":
    main()