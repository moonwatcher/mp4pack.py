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


def load_input_files(path, kind, file_filter, recursive):
    files = list()
    file_paths = list_input_files(path, kind, file_filter, recursive)
    for fp in file_paths:
        mf = load_media_file(fp)
        if mf != None:
            files.append(mf)
    
    return files


def list_input_files(path, kind, file_filter, recursive):
    result = list()
    path_list = os.listdir(path)
    for p in path_list:
        if invisable_file_path.search(p) == None:
            p = os.path.normpath(os.path.join(path,p))
            if os.path.isfile(p):
                if (kind == None or fnmatch.fnmatch(p, '*.' + kind)) and (file_filter == None or file_filter.search(p) != None):
                    result.append(unicode(p, 'utf-8'))
            elif os.path.isdir(p):
                if recursive:
                    rec_result = list_input_files(p, kind, file_filter, recursive)
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
    
    parser = OptionParser("usage: %prog [options] arg")
        
    group = OptionGroup(parser, "Operations", "You have to specify at least one operation to preform.")
    group.add_option("-j", "--deposit", dest="deposit", action="store_true", default=False, help="deposit in repository")
    group.add_option("-e", "--extract", dest="extract", action="store_true", default=False, help="extract into repository")
    group.add_option("-n", "--rename", dest="rename", action="store_true", default=False, help="rename to canonic form")
    group.add_option("-m", "--make", dest="make", action="store_true", default=False, help="make a new version")
    group.add_option("-t", "--tag", dest="tag", action="store_true", default=False, help="update meta data tags")
    group.add_option("-x", "--optimize", dest="optimize", action="store_true", default=False, help="optimize files")
    group.add_option("-u", "--update", dest="update", action="store_true", default=False, help="update files in repository")
    group.add_option("-z", "--ac3", dest="ac3", action="store_true", default=False, help="create new ac3 track from existing dts track")
    group.add_option("-y", "--report", dest="report", action="store_true", default=False, help="report inventory")
    group.add_option("--initialize", dest="initialize", action="store_true", default=False, help="First run initialization")
    parser.add_option_group(group)
        
    group = OptionGroup(parser, "Modifiers", "You have to specify at least one action to preform.")
    group.add_option("-o", "--volume", dest="volume", type="choice", choices=repository_config['Volume'].keys(), default=None, help="Output volume [default: %default]")
    group.add_option("-i", "--input", dest="input", default=".", help="Path to scan for input [default: %default]")
    group.add_option("-f", "--filter", dest="file_filter", default=None, help="Regex to filter input file names through")
    group.add_option("-p", "--profile", dest="profile", type="choice", choices=available_profiles, default=None, help="[default: %default]")
    group.add_option("-k", "--kind", dest="kind", type="choice", choices=repository_config['Kind'].keys(), help="[default: %default]")
    group.add_option("--media-kind", dest="media-kind", type="choice", choices=repository_config['Media Kind'].keys(), help="[default: %default]")
    group.add_option("-q", "--quality", dest="quality", help="[default: %default]")
    group.add_option("-s", "--width", dest="width", help="[default: %default]")
    group.add_option("--rate", dest="rate", help="[default: %default]")
    group.add_option("-v", "--verbosity", dest="verbosity", default='info', type="choice", choices=['debug', 'info', 'warning', 'error', 'critical'], help="Set the logging verbosity level [default: %default]")
    parser.add_option_group(group)
        
    group = OptionGroup(parser, "Flags")
    group.add_option("-d", "--debug", dest="debug", action="store_true", default=False, help="Only print commands without executing")
    group.add_option("-w", "--overwrite", dest="overwrite", action="store_true", default=False, help="Allow overwriting existing files")
    group.add_option("-r", "--recursive", dest="recursive", action="store_true", default=False, help="Recursivly process sub directories")
    group.add_option("--hd", dest="hd-flag", action="store_true", default=False, help="Mark the HD flag for resulting m4v files")
    group.add_option("--md5", dest="md5", action="store_true", default=False, help="Calculate md5 checksum")
    group.add_option("--keep-ac3", dest="keep-ac3", action="store_true", default=False, help="Mux ac3 track in addition to the aac track")
    parser.add_option_group(group)
            
#    group = OptionGroup(parser, "Destinations", "Default volumes where media fragments are stored")
#    group.add_option("--root", dest="root", default="/pool", help="repository root")
#    group.add_option("--artwork", metavar="VOLUME", dest="artwork", default="alpha", help="volume to use for artwork")
#    group.add_option("--chapter", metavar="VOLUME", dest="chapter", default="alpha", help="volume to use for chapters")
#    group.add_option("--subtitle", metavar="VOLUME", dest="subtitle", default="alpha", help="volume to use for subtitles")
#    group.add_option("--xml", metavar="VOLUME", dest="xml", default="alpha", help="volume to use for xml")
#    parser.add_option_group(group)
    
    group = OptionGroup(parser, "Service", "service routines")
    group.add_option("--map-show", dest="map_show", help="Map TV Show TVDB to name")
    parser.add_option_group(group)
    
    return parser.parse_args()


def preform_operations(tag_manager, files, options):
    if options.report:
        for f in files:
            print f
        
    if options.deposit:
        for f in files:
            f.copy(options.volume, options.profile, options.overwrite, options.md5)
    
    #if options.extract:
    
    #if options.rename:
    
    #if options.make:
    
    #if options.tag:
    
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
    
    from db import TagManager
    tag_manager = TagManager()
    file_filter = load_file_filter(options.file_filter)
    
    
    
    files = load_input_files(options.input, options.kind, file_filter, options.recursive)
    preform_operations(tag_manager, files, options)
    
    for k, v in options.__dict__.iteritems():
        print '    {0}: {1}'.format(k, v)
    
    logger.info('close log')



if __name__ == "__main__":
    main()