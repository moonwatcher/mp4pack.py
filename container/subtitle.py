# -*- coding: utf-8 -*-

import re
import os
import sys
import logging

import container

class LineFilter(object):
    def __init__(self):
        self.remove_pattern_list = []
        self.replace_pattern_list = []
        self.replacement_list = []
        
        from config.subfilter import line_remove
        for remove_filter in line_remove:
            self.remove_pattern_list.append(re.compile(remove_filter,re.UNICODE))
        
        from config.subfilter import line_replace
        for replace_filter in line_replace:
            self.replace_pattern_list.append(re.compile(replace_filter[0], re.MULTILINE|re.UNICODE)) 
            self.replacement_list.append(replace_filter[1])
    
    
    def is_bad_line(self, line):
        for index in range(len(self.remove_pattern_list)):
            if self.remove_pattern_list[index].search(line) != None:
                return True
        return False
    
    
    def clean(self, line):
        line = line.replace('\N', '\n')
        for index in range(len(self.replace_pattern_list)):            
            line = self.replace_pattern_list[index].sub(self.replacement_list[index], line)
        line = line.replace('\n', '\N')
        return line
    


class SubtitleFile(object):
    def __init__(self, file_path=None, input_frame_rate='25', output_frame_rate='25', format=None, line_filter=None):
        self.logger = logging.getLogger('mp4pack.container.subtitle')
        self.file_path = None
        self.file_type = None
        self.format = format
        self.input_frame_rate = input_frame_rate
        self.output_frame_rate = output_frame_rate
        self.time_begin = []
        self.time_end = []
        self.subtitle_list = []
        self.line_filter = line_filter
        if file_path != None:
            self.load(file_path)
    
    
    def load(self, file_path):
        self.change_input_file(file_path)
        file_lines = self.read_subtitle_file()
        self.decode(file_lines)
        if self.input_frame_rate != self.output_frame_rate:
            self.change_framerate()
        if self.line_filter != None:
            self.filter_lines()
        
    
    
    def write(self, output_file=None):
        file_lines = self.encode()
        self.write_subtitle_file(file_lines, output_file)
    
    
    def change_input_file(self, file_path):
        if file_path != None and os.path.isfile(file_path):
            self.file_type = os.path.splitext(file_path)[1]
            match = subtitle_file_type_re.search(self.file_type)
            if match != None:
                self.file_path = os.path.abspath(file_path)
                self.format = match.group(1)
            else:
                self.file_type = None
    
    
    def read_subtitle_file(self):
        file_lines = None
        if self.file_path == None:
            try:
                file_lines = sys.stdin.readlines()
            except:
                sys.stderr.write("Cannot read stdin\n")
        else:
            try:
                file_reader = open(self.file_path, 'r')
            except:
                sys.stderr.write("Cannot open file\n")
            file_lines = file_reader.readlines()
            file_reader.close()
        
        for index in range(len(file_lines)):
            if rmdos.search(file_lines[index]):
                clean_line = rmdos.sub('\n', file_lines[index])
                del file_lines[index]
                file_lines.insert(index, clean_line)
        return file_lines
    
    
    def write_subtitle_file(self, file_lines, output_file=None):
        end = '\n'    
        try:
            if output_file == None:
                for line in file_lines:
                    if line == '\n':
                        sys.stdout.write(end)
                    else:
                        sys.stdout.write(line + end)
            else:
                file_writer = open(output_file, 'w') 
                for line in file_lines:
                    if line == '\n':
                        file_writer.write(end)
                    else:
                        file_writer.write(line + end)
                        
                file_writer.close
        except IOError:
            if output_file == '-':
                sys.stderr.write("Can not write to stdout.\n")
            else:
                sys.stderr.write("Can not write to file " + output_file + ".\n")
    
    
    def encode(self):
        length = int(len(self.subtitle_list))
        index = 0
        file_lines = ['\n']
        while index < length:
            file_lines.append(str(index + 1))
            begin = container.miliseconds_to_time(self.time_begin[index], ',')
            stop = container.miliseconds_to_time(self.time_end[index], ',')
            file_lines.append(str(begin) +' --> '+str(stop))
            file_lines.append(str(self.subtitle_list[index]).replace('\N','\n'))
            file_lines.append('\n')
            index = index + 1
        return file_lines
    
    
    def decode(self, file_lines):
        def decode_srt(file_lines):
            indexlist= []
            for index in range(len(file_lines)):
                match = srt_time_line.search(file_lines[index])
                if match != None and str(file_lines[index - 1].strip('\n')).isdigit():
                    indexlist.append(index)
                    begin = container.timecode_to_miliseconds(match.group(1))
                    end = container.timecode_to_miliseconds(match.group(2))
                    self.time_begin.append(begin)
                    self.time_end.append(end)
            
            indexlist.append(len(file_lines) + 1)
            
            a = 0
            for index in indexlist[0:-1]:
                a = a + 1
                firstline = index + 1
                lastline = indexlist[a] - 1
                subline = ''.join(file_lines[firstline:lastline])
                while True:
                    if subtitle_noneline.search(subline):
                        subline = subtitle_noneline.sub('',subline)
                    else:
                        break
                self.subtitle_list.append(subline.replace('\n', '\N'))
        
        
        def decode_ass(file_lines):
            index = 0
            for line in file_lines:
                if line == '[Events]\n':
                    formation = file_lines[index + 1].replace(':',',').replace(' ','').strip('\n').split(',')
                    break
                index = index + 1
                
            start = formation.index('Start')
            stop = formation.index('End')
            text = formation.index('Text')
            for line in file_lines:
                if ass_subline.search(line):
                    line = re.sub('\n$','',line).split(',')
                    linepart = line[0].split(':')
                    del line[0]
                    line.insert(0, linepart[0])
                    line.insert(1, ':'.join(linepart[1: len(linepart)]))
                    
                    self.time_begin.append(container.timecode_to_miliseconds(line[start]))
                    self.time_end.append(container.timecode_to_miliseconds(line[stop]))
                    
                    subpart = ','.join(line[text:1 + text + (len(line) - len(formation))])
                    subpart = ass_event_command_re.sub('', subpart)
                    self.subtitle_list.append(subpart.replace(r'\n', '\N'))
        
        
        def decode_sub(file_lines, frame_rate):
            frame_rate = _frame_rate_to_float(frame_rate)
            for line in file_lines:
                if sub_line_begin.search(line):
                    line = line.split('}',2)
                    self.time_begin.append(_frame_to_miliseconds(line[0].strip('{'), frame_rate))
                    self.time_end.append(_frame_to_miliseconds(line[1].strip('{'), frame_rate))
                    self.subtitle_list.append(line[2].strip('\n').replace('|', '\N'))
        
        
        if self.format == 'srt':
            decode_srt(file_lines)
        elif self.format == 'sub':
            decode_sub(file_lines, self.input_frame_rate)
        elif self.format == 'ass' or self.format == 'ssa':
            decode_ass(file_lines)
    
    
    def remove_duplicate_lines(self):
        dupindex = []
        for index in range(len(self.time_begin[0:-1])):
            if self.time_begin[index] == self.time_begin[index + 1] and self.time_end[index] == self.time_end[index + 1] and self.subtitle_list[index] == self.subtitle_list[index + 1]:
                dupindex.append(index + 1)
        
        dupindex.reverse()
        
        for index in dupindex:
            del self.time_begin[index]
            del self.time_end[index]
            del self.subtitle_list[index]
    
    
    def filter_lines(self, line_filter=None):
        if line_filter == None and self.line_filter != None:
            line_filter = self.line_filter
            
        if line_filter != None:
            removeindex = []
            for index in range(len(self.subtitle_list)):
                if line_filter.is_bad_line(self.subtitle_list[index]):
                    removeindex.append(index)
                else:
                    self.subtitle_list[index] = line_filter.clean(self.subtitle_list[index])
                    if subtitle_empty_line_re.search(self.subtitle_list[index]) != None:
                        removeindex.append(index)
            
            removeindex.reverse()
            for index in removeindex:
                del self.time_begin[index]
                del self.time_end[index]
                del self.subtitle_list[index]
    
    
    def shift_times(self, offset):
        def move_times_on_list(times, start, stop, offset):
            index = start
            for time in times[start:stop]:
                time = int(time) + int(offset)
                del times[index]
                times.insert(index,time)
                index = index + 1
            return times
        
        begin, stop = _parse_limits(offset, len(self.time_begin))
        offset = container.timecode_to_miliseconds(offset.split(',')[0])
        self.time_begin = move_times_on_list(self.time_begin, begin, stop, offset)
        self.time_end = move_times_on_list(self.time_end, begin, stop, offset)
    
    
    def modify_duration(self, add):
        time = container.timecode_to_miliseconds(add.split(',')[0])
        begin, end = _parse_limits(add, len(self.time_end))
        for index in range(begin, end):
            endtime = self.time_end[index] + int(time) 
            if index + 1 != len(self.time_begin):
                if endtime + 50 > self.time_begin[index + 1]:
                    endtime = self.time_begin[index + 1] - 50
                    
            del self.time_end[index]
            self.time_end.insert(index, endtime)
    
    
    def scale_length(self, factor):
        if str(factor.split(',')[0]).isdigit():
            begin, end = _parse_limits(factor, len(self.time_end))
            for index in range(begin, end):
                endtime = int(round(float(self.time_end[index] - self.time_begin[index]) * float(factor.split(',')[0]))) + self.time_begin[index]
                if index + 1 != len(self.time_begin):
                    if endtime + 50 > self.time_begin[index + 1]:
                        endtime = self.time_begin[index + 1] - 50
                del self.time_end[index]
                self.time_end.insert(index, endtime)
        else:
            sys.stderr.write("Scale factor is not a digit! No alternation done.\n")
    
    
    def change_framerate(self):
        def scale(times, scale_frame_rate):
            index = 0
            for time in times:
                time = int(round(float(time) * float(scale_frame_rate)))
                del times[index]
                times.insert(index, time)
                index = index + 1
            return times
        
        
        input_frame_rate = _frame_rate_to_float(self.input_frame_rate)
        output_frame_rate = _frame_rate_to_float(self.output_frame_rate)
        scale_frame_rate = input_frame_rate/output_frame_rate
        self.time_begin = scale(self.time_begin, scale_frame_rate)
        self.time_end = scale(self.time_end, scale_frame_rate)
    
    


def is_subtitle_file(file_path):
    import os
    extension = os.path.splitext(file_path)[1]
    return subtitle_file_type_re.search(extension) != None




def _frame_rate_to_float(frame_rate):
    frame_rate = str(frame_rate).split('/',1)
    if len(frame_rate) == 2 and str(frame_rate[0]).isdigit() and str(frame_rate[1]).isdigit():
        frame_rate = float(frame_rate[0])/float(frame_rate[1])
    elif str(frame_rate[0].replace('.', '',1)).isdigit():
        frame_rate = float(frame_rate[0])
    else:
        sys.stderr.write("Frame rate must be a number\n")
    return frame_rate


def _parse_limits(limits, length):
    begin = 0
    stop = length
    limits = str(limits).split(',')
    if len(limits) >= 2:
        if str(limits[1]).isdigit():
            begin = int(limits[1]) - 1
            if len(limits) >= 3 and str(limits[2]).isdigit():
                stop = int(limits[2])
                
    if begin < 0:
        begin = 0
    elif begin > length:
        begin = length
        
    if stop > length:
        stop = length
        
    if stop < begin and begin < length:
        stop = begin
        
    return begin, stop


def _frame_to_miliseconds(frame, frame_rate):
    return round(float(1000)/float(frame_rate) * float(frame))


subtitle_file_type_re = re.compile('\.(srt|ass|sub|ssa)')
srt_time_line = re.compile("^([0-9]{2}:[0-9]{2}:[0-9]{2},[0-9]{3}) --> ([0-9]{2}:[0-9]{2}:[0-9]{2},[0-9]{3})$")
subtitle_noneline = re.compile("\n$")
subtitle_empty_line_re = re.compile("^\s*$")
ass_subline = re.compile('^Dialog.*')
ass_event_command_re = re.compile(r'\{\\[^\}]+\}')
sub_line_begin = re.compile('^{(\d+)}{(\d+)}')
rmdos = re.compile('\r\n$')
