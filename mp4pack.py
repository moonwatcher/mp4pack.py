#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
import re
import getopt
import logging
import copy


from container import ContainerFactory
from db import EntityManager
from config import Configuration

class MPKProcess(object):
    def __init__(self, configuration):
        self.logger = logging.getLogger('mpk Process')
        self.configuration = configuration
        self.options = configuration.options
        self.entity_manager = None
        self.container_factory = None
        self.valid = False
        self.file_filter = None
        self.media_files = None
        
        self.valid = self.load_config()
        if self.valid:
            self.entity_manager = EntityManager(self.configuration)
            self.container_factory = ContainerFactory(self.entity_manager)
            self.file_filter = self.load_file_filter()
    
    
    def load_config(self):
        result = True
        for c in self.configuration.repository['Command']:
            if self.configuration.repository['Command'][c]['path'] == None:
                self.logger.error(u'Command %s could not be located. Is it installed?', self.configuration.repository['Command'][c]['binary'])
                result = False
        return result
    
    
    def load_file_filter(self):
        result = None
        if self.options.file_filter is not None:
            self.logger.info(u'Filtering file that match %s', self.options.file_filter)
            result = re.compile(self.options.file_filter, re.UNICODE)
        return result
    
    
    def load_files(self, path):
        self.media_files = []
        file_paths = self.find_files_in_path(path, self.options.recursive)
        for file_path in file_paths:
            media_file = self.container_factory.create_media_file(file_path)
            if media_file:
                self.media_files.append(media_file)
    
    
    def transform_media_file(self, media_file):
        result_path = None
        o = copy.deepcopy(self.configuration.options)
        o.transcode = o.transform
        o.transform = None
        result_path = media_file.transcode(o)
        if result_path:
            new_media_file = self.container_factory.create_media_file(result_path)
            new_media_file.load()
            if new_media_file and new_media_file.valid():
                o.transcode = None
                
                # tag the new file
                o.tag = True
                new_media_file.tag(o)
                o.tag = False
                
                # update clean subtitles in the new file
                o.update = 'srt'
                o.profile = 'clean'
                new_media_file.update(o)
                
                # update chapters in the new file
                o.update = 'txt'
                o.profile = 'chapter'
                new_media_file.update(o)
                
                # update artwork on the new file
                o.volume = 'alpha'
                o.update = 'png'
                o.profile = 'normal'
                o.download = True
                new_media_file.update(o)
        return result_path
    
    
    def execute(self):
        if self.options.initialize:
            self.entity_manager.base_init()
            
        if self.options.map_show:
            self.entity_manager.map_show_with_pair(self.options.map_show)
            
        if self.options.choose_movie_poster:
            self.entity_manager.choose_tmdb_movie_poster_with_pair(self.options.choose_movie_poster, True)
            
        valid_files = []
        invalid_files = []
        
        if self.media_files:
            for f in self.media_files:
                f.load(self.options.reindex, self.options.sync)
                if f and f.valid():
                    valid_files.append(f)
                    
                    if self.options.rename:
                        f.rename(self.options)
                        
                    if self.options.extract:
                        f.extract(self.options)
                        
                    if self.options.copy:
                        f.copy(self.options)
                        
                    if self.options.pack is not None:
                        f.pack(self.options)
                        
                    if self.options.transcode is not None:
                        f.transcode(self.options)
                        
                    if self.options.transform is not None:
                        self.transform_media_file(f)
                        
                    if self.options.tag:
                        f.tag(self.options)
                        
                    if self.options.update is not None:
                        f.update(self.options)
                        
                    if self.options.optimize:
                        f.optimize(self.options)
                        
                    if self.options.info:
                        print unicode(f).encode('utf-8')
                        
                    f.unload()
                else:
                    invalid_files.append(f.file_path)
                    f.unload()
                    f = None
        return valid_files, invalid_files 
    
    
    
    def standardize_path(self, path):
        result = path
        realpath = os.path.realpath(os.path.abspath(path))
        for k,v in self.configuration.property_map['volume'].iteritems():
            if os.path.commonprefix([k, realpath]) == k:
                result = realpath.replace(k, v['path'])
                break
        return result
    
    
    def find_files_in_path(self, path, recursive, depth=1):
        result = []
        if os.path.isfile(path):
            dname, fname = os.path.split(path)
            if (self.file_filter == None or self.file_filter.search(fname) != None) and self.invisable_file_path.search(os.path.basename(path)) == None:
                result.append(self.standardize_path(path))
                
        elif (recursive or depth > 0) and os.path.isdir(path) and self.invisable_file_path.search(os.path.basename(path)) == None:
            for p in os.listdir(path):
                p = os.path.abspath(os.path.join(path,p))
                rec_result = self.find_files_in_path(p, recursive, depth - 1)
                result += rec_result
        return sorted(set(result))
    
    
    invisable_file_path = re.compile(ur'^\.', re.UNICODE)


def load_options(configuration):
    from optparse import OptionParser
    from optparse import OptionGroup
    
    rc = configuration.repository
    parser = OptionParser('%prog [options] [path to file or directory]')
    
    group = OptionGroup(parser, 'Actions')
    group.add_option('-i', '--info', dest='info', action='store_true', default=False, help='Show info')
    group.add_option('-n', '--rename', dest='rename', action='store_true', default=False, help='Rename files to standard names')
    group.add_option('-C', '--copy', dest='copy', action='store_true', default=False, help='Copy into repository')
    group.add_option('-e', '--extract', dest='extract', action='store_true', default=False, help='Extract streams for processing')
    group.add_option('-T', '--tag', dest='tag', action='store_true', default=False, help='Update file tags')
    group.add_option('-O', '--optimize', dest='optimize', action='store_true', default=False, help='Optimize file layout')
    group.add_option('-t', '--transcode', metavar='KIND', dest='transcode', type='choice', choices=rc['Action']['transcode']['kind'], help='KIND is one of [{0}]'.format(', '.join(rc['Action']['transcode']['kind'])))
    group.add_option('-c', '--transform', metavar='KIND', dest='transform', type='choice', choices=rc['Action']['transform']['kind'], help='KIND is one of [{0}]'.format(', '.join(rc['Action']['transform']['kind'])))
    group.add_option('-P', '--pack', metavar='KIND', dest='pack', type='choice', choices=rc['Action']['pack']['kind'], help='KIND is one of [{0}]'.format(', '.join(rc['Action']['pack']['kind'])))
    group.add_option('-u', '--update', metavar='KIND', dest='update', type='choice', choices=rc['Action']['update']['kind'], help='KIND is one of [{0}]'.format(', '.join(rc['Action']['update']['kind'])))
    parser.add_option_group(group)
        
    group = OptionGroup(parser, 'Action modifiers')
    group.add_option('-o', '--volume', dest='volume', type='choice', choices=rc['Volume'].keys(), default=None)
    group.add_option('-p', '--profile', dest='profile', type='choice', choices=configuration.available_profiles, default=None)
    group.add_option('-q', '--quality', metavar='QUANTIZER', dest='quality', type='float')
    group.add_option('-r', '--recursive', dest='recursive', action='store_true', default=False, help='Recursively process sub directories')
    group.add_option('-w', '--overwrite', dest='overwrite', action='store_true', default=False, help='Overwrite existing files')
    group.add_option('-W', '--width', metavar='WIDTH', type='int', dest='pixel_width', help='Override profile output pixel width')
    group.add_option('-f', '--filter', metavar='REGEX', dest='file_filter', default=None, help='File name regex filter')
    group.add_option('--crop', dest='crop', metavar='T:B:L:R', help='Set HandBrake cropping values [default: autocrop]')
    parser.add_option_group(group)
    
    group = OptionGroup(parser, 'Subtitles')
    group.add_option('--NTSC', dest='NTSC', action='store_true', default=False, help='Convert PAL to NTSC framerate')
    group.add_option('--PAL', dest='PAL', action='store_true', default=False, help='Convert NTSC to PAL framerate')
    group.add_option('--shift', metavar='TIME', dest='time_shift', type='int', default=None, help='Shift offset in millisec')
    group.add_option('--input-rate', metavar='RATE', dest='input_rate', default=None, help='Subtitles decoding frame rate')
    group.add_option('--output-rate', metavar='RATE', dest='output_rate', default=None, help='Subtitles encoding frame rate')
    parser.add_option_group(group)
    
    group = OptionGroup(parser, 'Environment')
    group.add_option('-S', '--sync', dest='sync', action='store_true', default=False, help='Sync encountered records with online service')
    group.add_option('-U', '--reindex', dest='reindex', action='store_true', default=False, help='Rebuild physical file index')
    group.add_option('-D', '--download', dest='download', action='store_true', default=False, help='Download if local is unavailable')
    group.add_option('-M', '--map-show', metavar="MAP", dest='map_show', help='Map show to tvdb id [tvdb id]:[show name]')
    group.add_option('--choose-movie-poster', metavar='MAP', dest='choose_movie_poster', default=None, help='Choose tmdb movie poster [imdb]:[tmdb]')
    group.add_option('-l', '--language', metavar='CODE', dest='language', default='eng', help='Languge code to use when und [default: %default]')
    group.add_option('--initialize', dest='initialize', action='store_true', default=False, help='Run only once to initialize the system')
    group.add_option('-5', '--md5', dest='md5', action='store_true', default=False, help='Verify md5 checksum after copy')
    group.add_option('-d', '--debug', dest='debug', action='store_true', default=False, help='Only print commands without executing')
    group.add_option('-v', '--verbosity', metavar='LEVEL', dest='verbosity', default='info', type='choice', choices=log_levels.keys(), help='Logging verbosity level [default: %default]')
    parser.add_option_group(group)
    
    options, args = parser.parse_args()
    configuration.options = options
    
    return options, args


def main():
    # Initialize options and scan arguments
    configuration = Configuration()
    options, args = load_options(configuration)
    
    
    # Initialize logging
    logging.basicConfig(level=log_levels[options.verbosity])
    logger = logging.getLogger('mp4pack')
    indent = configuration.repository['Display']['indent']
    margin = configuration.repository['Display']['margin']
    
    mpk_process = MPKProcess(configuration)
    
    if mpk_process.valid:
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
            logger.info(u'Looking up files in %s', input_path)
            mpk_process.load_files(input_path)
            
        # Preform operations on valid files, if any
        valid_files, invalid_files = mpk_process.execute()
        
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