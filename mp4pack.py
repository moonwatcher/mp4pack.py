#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
import re
import getopt
import logging
import copy


from container import make_media_file
from db import theEntityManager
from config import theConfiguration as configuration


def standardize_path(path):
    result = path
    realpath = os.path.realpath(os.path.abspath(path))
    for k,v in configuration.volume_map.iteritems():
        if os.path.commonprefix([k, realpath]) == k:
            result = realpath.replace(k, v['path'])
            break
    return result


def make_files(path, file_filter, recursive):
    media_files = []
    file_paths = find_files_in_path(path, file_filter, recursive)
    for file_path in file_paths:
        media_file = make_media_file(file_path)
        if media_file:
            media_files.append(media_file)
    return media_files


def find_files_in_path(path, file_filter, recursive, depth=1):
    result = []
    if os.path.isfile(path):
        dname, fname = os.path.split(path)
        if (file_filter == None or file_filter.search(fname) != None) and invisable_file_path.search(os.path.basename(path)) == None:
            result.append(standardize_path(path))
    
    elif (recursive or depth > 0) and os.path.isdir(path) and invisable_file_path.search(os.path.basename(path)) == None:
        for p in os.listdir(path):
            p = os.path.abspath(os.path.join(path,p))
            rec_result = find_files_in_path(p, file_filter, recursive, depth - 1)
            result += rec_result
    return sorted(set(result))


def load_options():
    from optparse import OptionParser
    from optparse import OptionGroup
    
    rc = configuration.repository
    profiles = []
    for k in rc['Kind'].keys():
        profiles += rc['Kind'][k]['Profile'].keys()
    profiles = tuple(set(profiles))
    
    parser = OptionParser('%prog [options] [file or directory]')
    
    group = OptionGroup(parser, 'Operations', 'An operation to preform on files found in the search path.')
    group.add_option('-i', '--info', dest='info', action='store_true', default=False, help='Show info.')
    group.add_option('-c', '--copy', dest='copy', action='store_true', default=False, help='Copy into repository.')
    group.add_option('-n', '--rename', dest='rename', action='store_true', default=False, help='Rename files to standard names.')
    group.add_option('-e', '--extract', dest='extract', action='store_true', default=False, help='Extract subtitle and chapter and transcode the extracted streams.')
    group.add_option('-T', '--tag', dest='tag', action='store_true', default=False, help='Update meta tags.')
    group.add_option('-O', '--optimize', dest='optimize', action='store_true', default=False, help='Optimize file layout.')
    group.add_option('-P', '--pack', metavar='KIND', dest='pack', type='choice', choices=rc['Action']['pack']['kind'], help='KIND is one of [ {0} ]'.format(', '.join(rc['Action']['pack']['kind'])))
    group.add_option('-t', '--transcode', metavar='KIND', dest='transcode', type='choice', choices=rc['Action']['transcode']['kind'], help='KIND is one of [ {0} ]'.format(', '.join(rc['Action']['transcode']['kind'])))
    group.add_option('-C', '--transform', metavar='KIND', dest='transform', type='choice', choices=rc['Action']['transform']['kind'], help='KIND is one of [ {0} ]'.format(', '.join(rc['Action']['transform']['kind'])))
    group.add_option('-u', '--update', metavar='KIND', dest='update', type='choice', choices=rc['Action']['update']['kind'], help='KIND is one of [ {0} ]'.format(', '.join(rc['Action']['update']['kind'])))
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
    group.add_option('-W', '--pixel-width', metavar='WIDTH', type='int', dest='pixel_width', help='Max output pixel width [ default: set by profile ]')
    group.add_option('-l', '--language', metavar='CODE', dest='language', default='eng', help='Languge code used when undefined. [ default: %default ]')
    group.add_option('-U', '--update-index', metavar='REINDEX', dest='reindex', action='store_true', default=False, help='Rebuild index for encountered files.')
    group.add_option('-5', '--md5', dest='md5', action='store_true', default=False, help='Verify md5 checksum on copy.')
    group.add_option('-D', '--download', dest='download', action='store_true', default=False, help='Download if no local copy found')
    parser.add_option_group(group)
    
    group = OptionGroup(parser, 'Subtitle', 'Options for manipulating subtitles.')
    group.add_option('--input-rate', metavar='RATE', dest='input_rate', default=None, help='Decoding subtitles frame rate.')
    group.add_option('--output-rate', metavar='RATE', dest='output_rate', default=None, help='Encoding subtitles frame rate.')
    group.add_option('--time-shift', metavar='TIME', dest='time_shift', type='int', default=None, help='Subtitles shift offset in milliseconds.')
    group.add_option('--NTSC', dest='NTSC', action='store_true', default=False, help='Convert PAL to NTSC framerate')
    group.add_option('--PAL', dest='PAL', action='store_true', default=False, help='Convert NTSC to PAL framerate')
    parser.add_option_group(group)
    
    group = OptionGroup(parser, 'Database', 'Options for maintaining database records.')
    group.add_option('--initialize', dest='initialize', action='store_true', default=False, help='Run only once to initialize the system.')
    group.add_option('--map-show', metavar="MAP", dest='map_show', help='Map TV Show name to TVDB ID. format: <id>:<name>')
    group.add_option('--refresh-movie', metavar='IMDb', dest='refresh_movie', default=None, help='Refresh the movie entry.')
    group.add_option('--refresh-tvshow', metavar='NAME', dest='refresh_tvshow', default=None, help='Refresh the tv show and episode entries.')
    group.add_option('--refresh-person', metavar='TMDb', type='int', dest='refresh_person', default=None, help='Refresh the person entry.')
    group.add_option('--choose-movie-poster', metavar='MAP', dest='choose_movie_poster', default=None, help='Choose tmdb movie poster. Takes IMDb:TMDb')
    parser.add_option_group(group)
    
    options, args = parser.parse_args()
    
    o = rc['Options'] = options
    
    return options, args


def load_config(logger):
    result = True
    for c in configuration.repository['Command']:
        if configuration.repository['Command'][c]['path'] == None:
            logger.error(u'Command %s could not be located. Is it installed?', configuration.repository['Command'][c]['binary'])
            result = False
    return result


def transform(f, options):
    result = None
    o = copy.deepcopy(options)
    o.transcode = o.transform
    o.transform = None
    result = f.transcode(o)
    if result:
        nf = make_media_file(result)
        nf.load()
        if nf and nf.valid():
            o.transcode = None
            
            o.tag = True
            nf.tag(o)
            o.tag = False
            
            o.update = 'srt'
            o.profile = 'clean'
            nf.update(o)
            
            o.update = 'txt'
            o.profile = 'chapter'
            nf.update(o)
            
            o.update = 'png'
            o.download = True
            o.profile = 'normal'
            o.download = True
            nf.update(o)
    return result


def preform_operations(media_files, options):
    if options.initialize:
        theEntityManager.base_init()
        
    if options.map_show:
        theEntityManager.map_show_with_pair(options.map_show)
        
    if options.refresh_movie:
        theEntityManager.find_movie_by_imdb_id(options.refresh_movie, True)
        
    if options.refresh_tvshow:
        theEntityManager.find_show(options.refresh_tvshow, True)
        
    if options.refresh_person:
        theEntityManager.find_person_by_tmdb_id(options.refresh_person, True)
        
    if options.choose_movie_poster:
        theEntityManager.choose_tmdb_movie_poster_with_pair(options.choose_movie_poster, True)
        
    valid_files = []
    invalid_files = []
    
    if media_files:
        for f in media_files:
            f.load(options.reindex)
            if f and f.valid():
                valid_files.append(f)
                
                if options.rename:
                    f.rename(options)
                    
                if options.extract:
                    f.extract(options)
                    
                if options.copy:
                    f.copy(options)
                    
                if options.pack is not None:
                    f.pack(options)
                    
                if options.transcode is not None:
                    f.transcode(options)
                
                if options.transform is not None:
                    transform(f, options)
                
                if options.tag:
                    f.tag(options)
                    
                if options.update is not None:
                    f.update(options)
                    
                if options.optimize:
                    f.optimize(options)
                    
                if options.info:
                    print unicode(f).encode('utf-8')
                    
                f.unload()
            else:
                invalid_files.append(f.file_path)
                f.unload()
                f = None
    return valid_files, invalid_files 


def main():
    print 'mp4pack. a media collection manager\nLior Galanti lior.galanti@gmail.com\n'.encode('utf-8')
    
    # Initialize options and scan arguments
    options, args = load_options()
    
    # Initialize logging
    logging.basicConfig(level=log_levels[options.verbosity])
    logger = logging.getLogger('mp4pack')
    indent = configuration.repository['Display']['indent']
    margin = configuration.repository['Display']['margin']
    
    if load_config(logger):
        media_files = None
        
        # Check for input path
        input_path = None
        if args:
            input_path = unicode(args[0], 'utf-8')
            if os.path.exists(input_path):
                input_path = os.path.abspath(input_path)
            else:
                logger.error(u'Path %s does not exist', input_path)
                input_path = None
                
        # Check for file filter
        if input_path:
            file_filter = None
            if options.file_filter is not None:
                logger.info(u'Filtering file that match %s', options.file_filter)
                file_filter = re.compile(options.file_filter, re.UNICODE)
            
            logger.info(u'Looking up files in %s', input_path)
            media_files = make_files(input_path, file_filter, options.recursive)
            
        # Preform operations on valid files, if any
        valid_files, invalid_files = preform_operations(media_files, options)
        
        # Report valid files
        if valid_files:
            logger.info(u'%d valid files were found in %s', len(valid_files), input_path)
            for path in valid_files:
                logger.debug(u'Found valid %s', path.file_path)
                
        # Report invalid files
        if invalid_files:
            logger.warning(u'%d invalid files were found in %s', len(invalid_files), input_path)
            for path in invalid_files:
                logger.info(u'Found invalid %s', path)
                    
        # Report positional arguments
        for idx, arg in enumerate(args):
            logger.debug(u'Positional %d: %s', idx, arg)
            
        # Report options
        for k,v in options.__dict__.iteritems():
            logger.debug(u'Option {0:-<{2}}: {1}'.format(k, v, indent - 2 - margin))
            
    else:
        for k,v in configuration.repository['Command'].iteritems():
            logger.info(u'Command {0:-<{2}}: {1}'.format(k, v['path'], indent - 2 - margin))


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