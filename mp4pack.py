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

class Queue(object):
    def __init__(self, configuration):
        self.logger = logging.getLogger('Queue')
        self.configuration = configuration
        self.entity_manager = None
        self.container_factory = None
        self.valid = False
        self.file_filter = None
        self.media_files = None
        
        # Initialize the runtime environment
        self.valid = self.sanity_check()
        if self.valid:
            self.entity_manager = EntityManager(self.configuration)
            self.container_factory = ContainerFactory(self.entity_manager)
            self.file_filter = self.load_file_filter()
            
        self.load()
    
    
    def sanity_check(self):
        # Any tests we want to preform before executing the queue go here...
        return True
    
    
    def load(self):
        # Collect media files from all provided paths
        canonic_paths = []
        if self.configuration.options.path:
            for p in self.configuration.options.path:
                input_path = unicode(p, 'utf-8')
                if os.path.exists(input_path):
                    input_path = os.path.abspath(input_path)
                else:
                    self.logger.error(u'Path %s does not exist', input_path)
                    input_path = None
                    
                if input_path:
                    p = self.find_files_in_path(input_path, self.configuration.options.recursive)
                    self.logger.debug(u'Found %d files in %s', len(p), input_path)
                    canonic_paths.extend(p)
                    
        # Sort paths and make sure they are unique
        if canonic_paths:
            canonic_paths = sorted(set(canonic_paths))
            self.logger.debug(u'Found %d files to process', len(canonic_paths))
            self.load_queue(canonic_paths)
    
    
    def load_file_filter(self):
        result = None
        if self.configuration.options.file_filter is not None:
            self.logger.info(u'Filtering file that match %s', self.configuration.options.file_filter)
            result = re.compile(self.configuration.options.file_filter, re.UNICODE)
        return result
    
    
    def load_queue(self, canonic_paths):
        self.media_files = []
        for path in canonic_paths:
            media_file = self.container_factory.create_media_file(path)
            if media_file:
                self.media_files.append(media_file)
    
    
    def process_queue(self):
        # Global operations not related to media files
        if self.configuration.options.initialize:
            self.entity_manager.base_init()
            
        if self.configuration.options.cleanup:
            self.container_factory.clean(self.configuration.options)
            
        if self.configuration.options.map_show:
            self.entity_manager.map_show_with_pair(self.configuration.options.map_show)
            
        if self.configuration.options.poster:
            self.entity_manager.choose_tmdb_movie_poster_with_pair(self.configuration.options.poster, True)
            
        # Process media files, one at a time
        if self.media_files:
            for f in self.media_files:
                f.load(self.configuration.options.reindex, self.configuration.options.sync)
                
                # Only process the file if it is valid
                if f and f.valid():
                    if self.configuration.options.rename:
                        f.rename(self.configuration.options)
                        
                    if self.configuration.options.extract:
                        f.extract(self.configuration.options)
                        
                    if self.configuration.options.copy:
                        f.copy(self.configuration.options)
                        
                    if self.configuration.options.pack is not None:
                        f.pack(self.configuration.options)
                        
                    if self.configuration.options.transcode is not None:
                        f.transcode(self.configuration.options)
                        
                    if self.configuration.options.transform is not None:
                        self.transform_media_file(f)
                        
                    if self.configuration.options.tag:
                        f.tag(self.configuration.options)
                        
                    if self.configuration.options.update is not None:
                        f.update(self.configuration.options)
                        
                    if self.configuration.options.optimize:
                        f.optimize(self.configuration.options)
                        
                    if self.configuration.options.info:
                        print f.report_info(self.configuration.options).encode('utf-8')
                        
                # Unload the file to save memory during the process
                f.unload()
    
    
    def find_files_in_path(self, path, recursive, depth=1):
        result = []
        if os.path.isfile(path):
            # This is a file
            # Ignore if it is invisable
            # Ignore if a filter exists and matches
            # Otherwise get a canonic path for the file and add it if its good
            dname, fname = os.path.split(path)
            if (self.file_filter == None or self.file_filter.search(fname) != None) and self.invisable_file_path.search(os.path.basename(path)) == None:
                canonic_path = self.configuration.canonic_path(path)
                if canonic_path:
                    result.append(canonic_path)
                    
        elif (recursive or depth > 0) and os.path.isdir(path) and self.invisable_file_path.search(os.path.basename(path)) == None:
            # This is a non invisable directory
            # and we need to recurse into it
            for p in os.listdir(path):
                # recursively scan decendent paths
                p = os.path.abspath(os.path.join(path,p))
                rec_result = self.find_files_in_path(p, recursive, depth - 1)
                
                # accumulate the recurive results on the stack and return
                result += rec_result
        return result
    
    
    
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
    
    
    def print_execution_report(self):
        if self.media_files:
            processed_media_files = [f for f in self.media_files if f.processed()]
            unprocessed_media_files = [f for f in self.media_files if not f.processed()]
            
            # Report procsessed files
            if processed_media_files:
                self.logger.info(u'%d files processed', len(processed_media_files))
                for f in processed_media_files:
                    self.logger.debug(u'Processing %s took %s', f.file_path, unicode(f.processing_duration()))
            
            # Report ignored files
            if unprocessed_media_files:
                self.logger.warning(u'%d files were not processed', len(unprocessed_media_files))
                for f in unprocessed_media_files:
                    self.logger.info(u'Ignored %s', f.file_path)
    
    
    invisable_file_path = re.compile(ur'^\.', re.UNICODE)


def parse_command_line_arguments(configuration):
    from argparse import ArgumentParser
    
    parser = ArgumentParser()
    
    parser.add_argument('path', metavar='PATH', nargs='*', help='file or directory paths to scan')
    parser.add_argument('--version', action='version', version='%(prog)s 0.4')
    
    group = parser.add_argument_group('media file processing operations')
    group.add_argument('-i', '--info',      dest='info',        action='store_true',    default=False, help='show info')
    group.add_argument('-n', '--rename',    dest='rename',      action='store_true',    default=False, help='rename files to standard names')
    group.add_argument('-C', '--copy',      dest='copy',        action='store_true',    default=False, help='copy into repository')
    group.add_argument('-e', '--extract',   dest='extract',     action='store_true',    default=False, help='extract streams for processing')
    group.add_argument('-T', '--tag',       dest='tag',         action='store_true',    default=False, help='update file tags')
    group.add_argument('-O', '--optimize',  dest='optimize',    action='store_true',    default=False, help='optimize file layout')
    group.add_argument('-t', '--transcode', dest='transcode',   metavar='KIND',         nargs='?', const='m4v', choices=configuration.action['transcode']['kind'], help='one of: %(choices)s. defaults to %(const)s')
    group.add_argument('-c', '--transform', dest='transform',   metavar='KIND',         nargs='?', const='m4v', choices=configuration.action['transform']['kind'], help='one of: %(choices)s. defaults to %(const)s')
    group.add_argument('-P', '--pack',      dest='pack',        metavar='KIND',         nargs='?', const='mkv', choices=configuration.action['pack']['kind'], help='one of: %(choices)s. defaults to %(const)s')
    group.add_argument('-u', '--update',    dest='update',      metavar='KIND',         nargs='?', const='srt', choices=configuration.action['update']['kind'], help='one of: %(choices)s. defaults to %(const)s')
    
    group = parser.add_argument_group('media processing modifiers')
    group.add_argument('-o', '--volume',    dest='volume',      metavar='VOL',          help='explicit volume to use')
    group.add_argument('-p', '--profile',   dest='profile',     metavar='PROFILE',      help='explicit profile to use')
    group.add_argument('-S', '--sync',      dest='sync',        action='store_true',    default=False, help='sync encountered records with online service')
    group.add_argument('-U', '--reindex',   dest='reindex',     action='store_true',    default=False, help='rebuild physical file index')
    group.add_argument('-D', '--download',  dest='download',    action='store_true',    default=False, help='download if local is unavailable')
    group.add_argument('-r', '--recursive', dest='recursive',   action='store_true',    default=False, help='recursively process sub directories')
    group.add_argument('-w', '--overwrite', dest='overwrite',   action='store_true',    default=False, help='overwrite existing files')
    group.add_argument('-f', '--filter',    dest='file_filter', metavar='EXP',          help='file name regex filter')
    group.add_argument('-l', '--lang',      dest='language',    metavar='CODE',         default='eng', help='languge code to use when und [default: %(default)s]')
    group.add_argument('-L', '--local',     dest='location',    metavar='LOC',          help='name of local repository')
    group.add_argument('-R', '--repo',      dest='repository',  metavar='REPO',         help='name of repository to use')
    group.add_argument('-5', '--md5',       dest='md5',         action='store_true',    default=False, help='verify md5 checksum after copy')
    
    group = parser.add_argument_group('video processing')
    group.add_argument('-q', '--quality',   dest='quality',     metavar='QUANTIZER',    type=float)
    group.add_argument('-W', '--width',     dest='pixel_width', metavar='WIDTH',        type=int, help='override profile output pixel width')
    group.add_argument('--crop',            dest='crop',        metavar='T:B:L:R',      help='set HandBrake cropping values [default: autocrop]')
    
    group = parser.add_argument_group('subtitle processing')
    group.add_argument('--NTSC',            dest='NTSC',        action='store_true',    default=False, help='convert from PAL to NTSC framerate')
    group.add_argument('--PAL',             dest='PAL',         action='store_true',    default=False, help='convert from NTSC to PAL framerate')
    group.add_argument('--shift',           dest='time_shift',  metavar='TIME',         type=int, help='shift offset in milliseconds')
    group.add_argument('--input-rate',      dest='input_rate',  metavar='RATE',         help='subtitles decoding frame rate')
    group.add_argument('--output-rate',     dest='output_rate', metavar='RATE',         help='subtitles encoding frame rate')
    
    group = parser.add_argument_group('environment and repository')
    group.add_argument('--clean',           dest='cleanup',     action='store_true',    default=False, help='Remove orphan references')
    group.add_argument('--show',            dest='map_show',    metavar="MAP",          help='map show to tvdb id [tvdb id]:[show name]')
    group.add_argument('--poster',          dest='poster',      metavar='MAP',          help='choose tmdb movie poster [imdb]:[tmdb]')
    group.add_argument('--initialize',      dest='initialize',  action='store_true',    default=False, help='run only once to initialize the system')
    group.add_argument('--conf',            dest='conf',        metavar='PATH',         help='path for external config file')
    group.add_argument('-d', '--debug',     dest='debug',       action='store_true',    default=False, help='only print commands without executing')
    group.add_argument('-v', '--verbosity', dest='verbosity',   metavar='LEVEL',        default='info', choices=log_levels.keys(), help='logging verbosity level [default: %(default)s]')
    
    args = parser.parse_args()
    configuration.load_command_line_arguments(args)


def main():
    logging.basicConfig()
    
    # Log level to be used before we read command line arguments
    logging.getLogger().setLevel(log_levels['info'])
    
    # Initialize options and scan arguments
    configuration = Configuration()
    parse_command_line_arguments(configuration)
    
    # Override the default log level from the command line arguments
    logging.getLogger().setLevel(log_levels[configuration.options.verbosity])
    
    q = Queue(configuration)
    if q.valid:
        # Preform operations
        q.process_queue()
        
        # Print the execution report
        q.print_execution_report()
        
    configuration.print_option_report()
    configuration.print_command_report()


log_levels = {
    'debug': logging.DEBUG,
    'info': logging.INFO,
    'warning': logging.WARNING,
    'error': logging.ERROR,
    'critical': logging.CRITICAL
}

if __name__ == '__main__':
    main()