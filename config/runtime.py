# -*- coding: utf-8 -*-

import re
import logging

resource_scheme = u'mpk'

runtime = {
    'command':[
        {'name':'rsync',        'binary':u'rsync', },
        {'name':'mv',           'binary':u'mv', },
        {'name':'handbrake',    'binary':u'HandbrakeCLI', },
        {'name':'subler',       'binary':u'SublerCLI', },
        {'name':'mkvmerge',     'binary':u'mkvmerge', },
        {'name':'mkvextract',   'binary':u'mkvextract', },
        {'name':'mp4info',      'binary':u'mp4info', },
        {'name':'mp4file',      'binary':u'mp4file', },
        {'name':'mp4art',       'binary':u'mp4art', },
        {'name':'mediainfo',    'binary':u'mediainfo', },
        {'name':'ffmpeg',       'binary':u'ffmpeg', }
    ],
    'action':[
        {
            'name':'info',
            'depend':('mediainfo', 'mp4info',),
        },
        {
            'name':'copy',
            'depend':('rsync',),
        },
        {
            'name':'rename',
            'depend':('mv',),
        },
        {
            'name':'extract',
            'depend':('mkvextract',),
        },
        {
            'name':'tag',
            'depend':('subler',),
        },
        {
            'name':'optimize',
            'depend':('mp4file',),
        },
        {
            'name':'pack',
            'depend':('mkvmerge',),
            'kind':('mkv','m4v', ),
        },
        {
            'name':'transcode',
            'depend':('handbrake',),
            'kind':('m4v', 'mkv', 'srt', 'chpl', 'jpg', 'png', 'ac3'),
        },
        {
            'name':'transform',
            'depend':('handbrake',),
            'kind':('m4v',),
        },
        {
            'name':'update',
            'depend':('subler',),
            'kind':('srt', 'png', 'jpg', 'chpl'),
        },
    ],
    'default':{
        'profile':{
            'name':'default',
            'tag':{
                
            },
            'rename':{
                
            },
            'extract':{
                'transform':[
                    {
                        'mode':'select',
                        'branch':[
                            {'kind':'mkv'},
                        ],
                        'track':[
                            {
                                'mode':'choose',
                                'branch':[
                                    {'type':'text', 'language':'he', 'codec':'srt'},
                                    {'type':'text', 'language':'he', 'codec':'ass'},
                                ],
                            },
                            {
                                'mode':'choose',
                                'branch':[
                                    {'type':'text', 'language':'en', 'codec':'srt'},
                                    {'type':'text', 'language':'en', 'codec':'ass'},
                                ],
                            },
                            {
                                'mode':'select',
                                'branch':(
                                    {'type':'audio', 'codec':'dts'},
                                ),
                            },
                            {
                                'mode':'choose',
                                'branch':(
                                    {'type':'text', 'codec':'chpl'},
                                ),
                            },
                        ],
                    },
                    {
                        'mode':'select',
                        'branch':[
                            {'kind':'m4v'},
                        ],
                        'track':[
                            {
                                'mode':'choose',
                                'branch':[
                                    {'type':'text', 'codec':'chpl'},
                                ],
                            },
                        ],
                    },
                ],
            },
            'pack':{
                'query':[
                    { 'action':'select', 'constraint':{'kind':'srt'} },
                    { 'action':'select', 'constraint':{'kind':'chpl'} },
                    { 'action':'select', 'constraint':{'kind':'ac3'} },
                ],
                'transform':[
                    {
                        'description':'Hebrew and english subtitles from the clean profile',
                        'mode':'select',
                        'branch':[
                            {'kind':'srt', 'profile':'clean'},
                        ],
                        'track':[
                            {
                                'mode':'choose',
                                'branch':[
                                    {'type':'text', 'language':'he'},
                                ],
                                'override':{'name':'Normal'},
                            },
                            {
                                'mode':'choose',
                                'branch':[
                                    {'type':'text', 'language':'en'},
                                ],
                                'override':{'name':'Normal'},
                            },
                        ],
                    },
                    {
                        'description':'First of hebrew or english subtitles as swedish',
                        'mode':'choose',
                        'branch':[
                            {'kind':'srt', 'profile':'clean', 'language':'he'},
                            {'kind':'srt', 'profile':'clean', 'language':'en'},
                        ],
                        'track':[
                            {
                                'mode':'choose',
                                'branch':[
                                    {'type':'text'},
                                ],
                                'override':{'name':'Smart', 'language':'swe'},
                            },
                        ],
                    },
                    {
                        'description':'First of hebrew or english or other chapter track',
                        'mode':'choose',
                        'branch':[
                            {'kind':'chpl', 'language':'he'},
                            {'kind':'chpl', 'language':'en'},
                            {'kind':'chpl'},
                        ],
                        'track':[
                            {
                                'mode':'choose',
                                'branch':[
                                    {'type':'text'},
                                ],
                            },
                        ],
                    },
                    {
                        'description':'All ac3 raw streams in the normal profile',
                        'mode':'select',
                        'branch':[
                            {'kind':'ac3', 'profile':'normal'},
                        ],
                        'track':[
                            {
                                'mode':'choose',
                                'branch':[
                                    {'type':'audio', 'codec':'ac3'},
                                ],
                                'override':{'name':'Normal'},
                            },
                        ],
                    },
                    {
                        'description':'Audio and video streams from a matroska file',
                        'mode':'choose',
                        'branch':[
                            {'kind':'mkv'},
                            {'kind':'m4v'},
                            {'kind':'avi'},
                        ],
                        'override':{
                            'mkvmerge flags':[
                                u'--no-global-tags',
                                u'--no-track-tags',
                                u'--no-chapters',
                                u'--no-attachments',
                                u'--no-subtitles',
                            ],
                        },
                        'track':[
                            {
                                'mode':'select',
                                'branch':[
                                    {'type':'video'},
                                    {'type':'audio', 'codec':'ac3'},
                                    {'type':'audio', 'codec':'aac'},
                                    {'type':'audio', 'codec':'dts'},
                                    {'type':'audio', 'codec':'mp3'},
                                ],
                            },
                        ]
                    },
                ],
            },
            'update':{
                'query':[
                    { 'action':'select', 'constraint':{'kind':'srt'} },
                    { 'action':'select', 'constraint':{'kind':'chpl'} },
                    { 'action':'select', 'constraint':{'kind':'png'} },
                ],
                'transform':[
                    {
                        'description':'All hebrew and english subtitles of the clean profile',
                        'mode':'select',
                        'branch':[
                            {'kind':'srt', 'profile':'clean'},
                        ],
                        'track':[
                            {
                                'mode':'choose',
                                'branch':[
                                    {'type':'text', 'language':'he'},
                                ],
                                'override':{'name':'Normal', 'height':0.132},
                            },
                            {
                                'mode':'choose',
                                'branch':[
                                    {'type':'text', 'language':'en'},
                                ],
                                'override':{'name':'Normal', 'height':0.132},
                            },
                        ],
                    },
                    {
                        'description':'First of hebrew or english subtitles as swedish',
                        'mode':'choose',
                        'branch':[
                            {'kind':'srt', 'profile':'clean', 'language':'he'},
                            {'kind':'srt', 'profile':'clean', 'language':'en'},
                        ],
                        'track':[
                            {
                                'mode':'choose',
                                'branch':[
                                    {'type':'text'},
                                ],
                                'override':{'name':'Smart', 'height':0.148, 'language':'swe'},
                            },
                        ],
                    },
                    {
                        'description':'First of hebrew or english artwork',
                        'mode':'choose',
                        'branch':[
                            {'kind':'png', 'profile':'normal', 'language':'he'},
                            {'kind':'png', 'profile':'normal', 'language':'en'},
                        ],
                        'track':[
                            {
                                'mode':'choose',
                                'branch':[
                                    {'type':'image'},
                                ],
                            },
                        ],
                    },
                    {
                        'description':'First of hebrew or english chapter track',
                        'mode':'choose',
                        'branch':[
                            {'kind':'chpl', 'language':'he'},
                            {'kind':'chpl', 'language':'en'},
                        ],
                        'track':[
                            {
                                'mode':'choose',
                                'branch':[
                                    {'type':'text'},
                                ],
                            },
                        ],
                    },
                ],
            },
            'transcode':{
                'transform':[
                    {
                        'description':'Audio and video streams from a matroska or m4v file',
                        'mode':'choose',
                        'branch':[
                            {'kind':'mkv'},
                            {'kind':'m4v'},
                        ],
                        'track':[
                            {
                                'description':'Transcode the main video track to H.264',
                                'mode':'choose',
                                'branch':[
                                    {'type':'video'},
                                ],
                                'override':{
                                    'handbrake flags':[
                                        '--large-file',
                                        '--loose-anamorphic',
                                    ],
                                    'handbrake parameters':{
                                        '--quality':18,
                                        '--encoder':'x264',
                                        '--maxWidth':1280,
                                    },
                                    'handbrake x264 settings':{
                                        'cabac':1,
                                        'me':'umh',
                                        'subme':9,
                                        'bframes':3,
                                        'ref':3,
                                        'b-pyramid':'none',
                                        'mixed-refs':1,
                                        'b-adapt':2,
                                        'trellis':0,
                                        'vbv-maxrate':5500,
                                        'vbv-bufsize':5500,
                                    },
                                },
                            },
                            {
                                'description':'Copy all ac3 audio tracks',
                                'mode':'select',
                                'branch':[
                                    {'type':'audio', 'codec':'ac3'},
                                ],
                                'override':{
                                    'encoder settings':{'--aencoder':'copy', '--ab':'auto', '--mixdown':'auto'}
                                },
                            },
                            {
                                'description':'Transcode all ac3 audio tracks to Dolby Pro Logic II aac',
                                'mode':'select',
                                'branch':[
                                    {'type':'audio', 'codec':'ac3'},
                                ],
                                'override':{
                                    'encoder settings':{'--aencoder':'ca_aac', '--ab':160, '--mixdown':'dpl2'}
                                },
                            },
                            {
                                'description':'Transcode all Stereo aac or mp3 tracks to Stereo aac',
                                'mode':'select',
                                'branch':[
                                    {'type':'audio', 'codec':'mp3', 'channels':2},
                                    {'type':'audio', 'codec':'aac', 'channels':2},
                                ],
                                'override':{
                                    'encoder settings':{'--aencoder':'ca_aac', '--ab':128, '--mixdown':'stereo'}
                                },
                            },
                            {
                                'description':'Transcode all Mono aac or mp3 tracks to Mono aac',
                                'mode':'select',
                                'branch':[
                                    {'type':'audio', 'codec':'mp3', 'channels':1},
                                    {'type':'audio', 'codec':'aac', 'channels':1},
                                ],
                                'override':{
                                    'encoder settings':{'--aencoder':'ca_aac', '--ab':64, '--mixdown':'mono'},
                                },
                            },
                        ]
                    },
                    {
                        'description':'png or jpg artwork',
                        'mode':'choose',
                        'branch':[
                            {'kind':'png'},
                            {'kind':'jpg'},
                        ],
                        'track':[
                            {
                                'description':'Transcode image to png',
                                'mode':'choose',
                                'branch':[
                                    {'type':'image'},
                                ],
                                'override':{
                                    'max length':1024,
                                },
                            },
                        ]
                    },
                    {
                        'description':'raw dts audio stream to ac3',
                        'mode':'choose',
                        'branch':[
                            {'kind':'dts'},
                        ],
                        'track':[
                            {
                                'description':'Transcode 6 channels dts to ac3',
                                'mode':'choose',
                                'branch':[
                                    {'type':'audio', 'codec':'dts', 'channels':6},
                                ],
                                'override':{
                                    'ffmpeg parameters':{'-ab':u'640k', '-acodec':u'ac3', '-ac':6 },
                                },
                            },
                            {
                                'description':'Transcode 5 channels dts to ac3',
                                'mode':'choose',
                                'branch':[
                                    {'type':'audio', 'codec':'dts', 'channels':5},
                                ],
                                'override':{
                                    'ffmpeg parameters':{'-ab':u'640k', '-acodec':u'ac3', '-ac':5 },
                                },
                            },
                            {
                                'description':'Transcode 4 channels dts to ac3',
                                'mode':'choose',
                                'branch':[
                                    {'type':'audio', 'codec':'dts', 'channels':4},
                                ],
                                'override':{
                                    'ffmpeg parameters':{'-ab':u'448k', '-acodec':u'ac3', '-ac':4 },
                                },
                            },
                            {
                                'description':'Transcode 3 channels dts to ac3',
                                'mode':'choose',
                                'branch':[
                                    {'type':'audio', 'codec':'dts', 'channels':3},
                                ],
                                'override':{
                                    'ffmpeg parameters':{'-ab':u'448k', '-acodec':u'ac3', '-ac':3 },
                                },
                            },
                            {
                                'description':'Transcode stereo dts to ac3',
                                'mode':'choose',
                                'branch':[
                                    {'type':'audio', 'codec':'dts', 'channels':2},
                                ],
                                'override':{
                                    'ffmpeg parameters':{'-ab':u'256k', '-acodec':u'ac3', '-ac':2 },
                                },
                            },
                            {
                                'description':'Transcode mono dts to ac3',
                                'mode':'choose',
                                'branch':[
                                    {'type':'audio', 'codec':'dts', 'channels':1},
                                ],
                                'override':{
                                    'ffmpeg parameters':{'-ab':u'192k', '-acodec':u'ac3', '-ac':1 },
                                },
                            },
                        ]
                    },
                    {
                        'description':'subtitles',
                        'mode':'select',
                        'branch':[
                            {'kind':'srt'},
                            {'kind':'ass'},
                        ],
                        'track':[
                            {
                                'description':'Hebrew subtitles',
                                'mode':'choose',
                                'branch':[
                                    {'type':'text', 'language':'he'},
                                ],
                                'override':{
                                    'subtitle filters':['noise', 'hebrew noise', 'typo', 'punctuation', 'leftover']
                                },
                            },
                            {
                                'description':'English subtitles',
                                'mode':'choose',
                                'branch':[
                                    {'type':'text', 'language':'en'},
                                ],
                                'override':{
                                    'subtitle filters':['noise', 'typo', 'english typo', 'leftover']
                                },
                            },
                        ]
                    },
                    {
                        'description':'menu',
                        'mode':'select',
                        'branch':[
                            {'kind':'chpl'},
                        ],
                        'track':[
                            {
                                'description':'menu',
                                'mode':'choose',
                                'branch':[
                                    {'type':'text'},
                                ],
                            },
                        ]
                    },
                ],
            }
        }
    },
    'profile':{
        'normal':{},
        'clean':{},
        'original':{},
        'sd':{},
        '720':{},
        '1080':{},
        'A4':{},
        'universal':{},
        'appletv':{},
        'high':{},
    },
    'expression':[
        {
            'name':'srt time line', 
            'definition':u'^([0-9]{2}:[0-9]{2}:[0-9]{2},[0-9]{3}) --> ([0-9]{2}:[0-9]{2}:[0-9]{2},[0-9]{3})$', 
            'flags':re.UNICODE,
        },
        {
            'name':'ass subtitle line', 
            'definition':ur'^Dialogue\s*:\s*(.*)$', 
            'flags':re.UNICODE,
        },
        {
            'name':'ass formation line', 
            'definition':ur'^Format\s*:\s*(.*)$', 
            'flags':re.UNICODE,
        },
        {
            'name':'ass condense line breaks', 
            'definition':ur'(\\N)+', 
            'flags':re.UNICODE,
        },
        {
            'name':'ass event command', 
            'definition':ur'\{\\[^\}]+\}', 
            'flags':re.UNICODE,
        },
        {
            'name':'whitespace',
            'definition':ur'\s+',
            'flags':re.UNICODE,
        },
        {
            'name':'characters to exclude from filename',
            'definition':ur'[\\\/?<>:*|\'"^\.]',
            'flags':re.UNICODE,
        },
        {
            'name':'sentence end',
            'definition':ur'[.!?]',
            'flags':re.UNICODE,
        },
        {
            'name':'mediainfo value list',
            'definition':ur'^[^/]+(?:\s*/\s*[^/]+)*$',
            'flags':re.UNICODE,
        },
        {
            'name':'tvdb list separators',
            'definition':ur'\||,',
            'flags':re.UNICODE,
        },
        {
            'name':'space around tvdb list item',
            'definition':ur'\s*\|\s*',
            'flags':re.UNICODE,
        },
        {
            'name':'clean xml',
            'definition':ur'\s+/\s+(?:\t)*',
            'flags':re.UNICODE,
        },
        {
            'name':'true value',
            'definition':ur'yes|true|1',
            'flags':re.UNICODE|re.IGNORECASE,
        },
        {
            'name':'full utc datetime',
            'definition':ur'(?:(?P<tzinfo>[A-Za-z/]+) )?(?P<year>[0-9]{4})(?:-(?P<month>[0-9]{2})(?:-(?P<day>[0-9]{2})(?: (?P<hour>[0-9]{2}):(?P<minute>[0-9]{2}):(?P<second>[0-9]{2}))?)?)?',
            'flags':re.UNICODE,
        },
        {
            'name':'mp4info tag',
            'definition':u' ([^:]+): (.*)$',
            'flags':re.UNICODE,
        },
    ],
    'rule':[ 
        {
            'name':'tmdb movie',
            'provides':set(('tmdb movie',)),
            'branch':(
                {
                    'requires':set(('host', 'tmdb movie id', 'language')),
                    'apply':(
                        {
                            'property':'tmdb movie',
                            'format':u'mpk://{host}/c/tmdb/movie/{language}/{tmdb movie id}',
                        },
                    ),
                },
            ),
        },
        {
            'name':'tmdb movie casts',
            'provides':set(('tmdb movie casts',)),
            'branch':(
                {
                    'requires':set(('host', 'tmdb movie id')),
                    'apply':(
                        {
                            'property':'tmdb movie casts',
                            'format':u'mpk://{host}/c/tmdb/movie/{tmdb movie id}/casts',
                        },
                    ),
                },
            ),
        },
        {
            'name':'tmdb movie images',
            'provides':set(('tmdb movie images',)),
            'branch':(
                {
                    'requires':set(('host', 'tmdb movie id')),
                    'apply':(
                        {
                            'property':'tmdb movie images',
                            'format':u'mpk://{host}/c/tmdb/movie/{tmdb movie id}/images',
                        },
                    ),
                },
            ),
        },
        {
            'name':'tmdb movie keywords',
            'provides':set(('tmdb movie keywords',)),
            'branch':(
                {
                    'requires':set(('host', 'tmdb movie id')),
                    'apply':(
                        {
                            'property':'tmdb movie keywords',
                            'format':u'mpk://{host}/c/tmdb/movie/{tmdb movie id}/keywords',
                        },
                    ),
                },
            ),
        },
        {
            'name':'tmdb movie releases',
            'provides':set(('tmdb movie releases',)),
            'branch':(
                {
                    'requires':set(('host', 'tmdb movie id')),
                    'apply':(
                        {
                            'property':'tmdb movie releases',
                            'format':u'mpk://{host}/c/tmdb/movie/{tmdb movie id}/releases',
                        },
                    ),
                },
            ),
        },
        {
            'name':'tmdb movie trailers',
            'provides':set(('tmdb movie trailers',)),
            'branch':(
                {
                    'requires':set(('host', 'tmdb movie id')),
                    'apply':(
                        {
                            'property':'tmdb movie trailers',
                            'format':u'mpk://{host}/c/tmdb/movie/{tmdb movie id}/trailers',
                        },
                    ),
                },
            ),
        },
        {
            'name':'tmdb movie translations',
            'provides':set(('tmdb movie translations',)),
            'branch':(
                {
                    'requires':set(('host', 'tmdb movie id', 'language')),
                    'apply':(
                        {
                            'property':'tmdb movie translations',
                            'format':u'mpk://{host}/c/tmdb/{language}/movie/{tmdb movie id}/translations',
                        },
                    ),
                },
            ),
        },
        {
            'name':'tmdb movie alternative titles',
            'provides':set(('tmdb movie alternative titles',)),
            'branch':(
                {
                    'requires':set(('host', 'tmdb movie id')),
                    'apply':(
                        {
                            'property':'tmdb movie alternative titles',
                            'format':u'mpk://{host}/c/tmdb/movie/{tmdb movie id}/alternative_titles',
                        },
                    ),
                },
            ),
        },
        
        {
            'name':'enabled bit default',
            'provides':set(('enabled',)),
            'branch':(
                {
                    'apply':(
                        {'property':'enabled', 'value':True,},
                    ),
                },
            ),
        },
        {
            'name':'decode path',
            'provides':set((
                'media kind',
                'imdb id',
                'simple name',
                'kind',
                'tv show key',
                'tv season',
                'tv episode',
            )),
            'branch':(
                {
                    'requires':set(('file name',)),
                    'match':{'property':'file name', 'expression':ur'^IMDbtt[0-9]+(?: .*)?\.[^\.]+$', },
                    'decode':(
                        {'property':'file name', 'expression':ur'^IMDb(?P<imdb_id>tt[0-9]+)(?: (?P<simple_name>.*))?\.(?P<kind>[^\.]+)$',},
                    ),
                    'apply':(
                        {'property':'media kind', 'value':u'movie',},
                    ),
                },
                {
                    'requires':set(('file name',)),
                    'match':{'property':'file name', 'expression':ur'^.+ s[0-9]+e[0-9]+(?: .*)?\.[^\.]+$', },
                    'decode':(
                        {'property':'file name', 'expression':ur'^(?P<tv_show_key>.+) s(?P<tv_season>[0-9]+)e(?P<tv_episode>[0-9]+)(?:\s*(?P<simple_name>.*))?\.(?P<kind>[^\.]+)$',},
                    ),
                    'apply':(
                        {'property':'media kind', 'value':u'tvshow',},
                    ),
                },
            ),
        },
        {
            'name':'implicit path',
            'provides':set(('path',)),
            'branch':(
                {
                    'requires':set(('canonic path',)),
                    'apply':(
                        {
                            'property':'path',
                            'format':u'{canonic path}',
                        },
                    ),
                },
            ),
        },
        {
            'name':'global environment',
            'provides':set(('resource uri scheme',)),
            'branch':(
                {
                    'apply':(
                        {'property':'resource uri scheme', 'value':resource_scheme,},
                    ),
                },
            ),
        },
        {
            'name':'mongodb url',
            'provides':set(('mongodb url',)),
            'branch':(
                {
                    'requires':set(('host', 'database', 'port', 'username', 'password')),
                    'apply':(
                        {
                            'property':'mongodb url',
                            'format':u'mongodb://{username}:{password}@{host}:{port}/{database}',
                        },
                    ),
                },
                {
                    'requires':set(('host', 'database', 'username', 'password')),
                    'apply':(
                        {
                            'property':'mongodb url',
                            'format':u'mongodb://{username}:{password}@{host}/{database}',
                        },
                    ),
                },
                {
                    'requires':set(('host', 'database', 'port')),
                    'apply':(
                        {
                            'property':'mongodb url',
                            'format':u'mongodb://{host}:{port}/{database}',
                        },
                    ),
                },
                {
                    'requires':set(('host', 'database')),
                    'apply':(
                        {
                            'property':'mongodb url',
                            'format':u'mongodb://{host}/{database}',
                        },
                    ),
                },
            ),
        },
        {
            'name':'audio track name',
            'provides':set(('name',)),
            'branch':(
                {
                    'requires':set(('type', 'channels')),
                    'equal':{'type':'audio', 'channels':1 },
                    'apply':(
                        { 'property':'name', 'value':'Mono' },
                    ),
                },
                {
                    'requires':set(('type', 'channels')),
                    'equal':{'type':'audio', 'channels':2 },
                    'apply':(
                        { 'property':'name', 'value':'Stereo' },
                    ),
                },
                {
                    'requires':set(('type', 'channels')),
                    'equal':{'type':'audio', 'channels':3 },
                    'apply':(
                        { 'property':'name', 'value':'Stereo' },
                    ),
                },
                {
                    'requires':set(('type', 'channels')),
                    'equal':{'type':'audio', 'channels':4 },
                    'apply':(
                        { 'property':'name', 'value':'Quadraphonic' },
                    ),
                },
                {
                    'requires':set(('type', 'channels')),
                    'equal':{'type':'audio', 'channels':5 },
                    'apply':(
                        { 'property':'name', 'value':'Surround' },
                    ),
                },
                {
                    'requires':set(('type', 'channels')),
                    'equal':{'type':'audio', 'channels':6 },
                    'apply':(
                        { 'property':'name', 'value':'Surround' },
                    ),
                },
                {
                    'requires':set(('type', 'channels')),
                    'equal':{'type':'audio', 'channels':7 },
                    'apply':(
                        { 'property':'name', 'value':'Surround' },
                    ),
                },
                {
                    'requires':set(('type', 'channels')),
                    'equal':{'type':'audio', 'channels':8 },
                    'apply':(
                        { 'property':'name', 'value':'Surround' },
                    ),
                },
            ),
        },
        {
            'name':'tv episode id',
            'provides':set(('tv episode id',)),
            'branch':(
                {
                    'requires':set(('media kind', 'tv season', 'tv episode')),
                    'equal':{'media kind':'tvshow', },
                    'apply':(
                        {
                            'property':'tv episode id',
                            'format':u's{tv season:02d}e{tv episode:02d}',
                        },
                    ),
                },
            ),
        },
        {
            'name':'asset id',
            'provides':set(('asset id',)),
            'branch':(
                {
                    'requires':set(('media kind', 'tv show key', 'tv season', 'tv episode')),
                    'equal':{'media kind':'tvshow', },
                    'apply':(
                        {
                            'property':'asset id',
                            'format':u'{media kind}/{tv show key}/{tv season}/{tv episode}',
                        },
                    ),
                },
                {
                    'requires':set(('media kind', 'imdb id',)),
                    'equal':{'media kind':'movie', },
                    'apply':(
                        {
                            'property':'asset id',
                            'format':u'{media kind}/imdb/{imdb id}',
                        },
                    ),
                },
            ),
        },
        {
            'name':'canonic file name',
            'provides':set(('canonic file name',)),
            'branch':(
                {
                    'requires':set(('media kind', 'tv show key', 'tv episode id', 'simple name', 'kind')),
                    'equal':{'media kind':'tvshow', },
                    'apply':(
                        {
                            'property':'canonic file name',
                            'format':u'{tv show key} {tv episode id} {simple name}.{kind}',
                        },
                    ),
                },
                {
                    'requires':set(('media kind', 'tv show key', 'tv episode id', 'kind')),
                    'equal':{'media kind':'tvshow', },
                    'apply':(
                        {
                            'property':'canonic file name',
                            'format':u'{tv show key} {tv episode id}.{kind}',
                        },
                    ),
                },
                {
                    'requires':set(('media kind', 'imdb id', 'simple name', 'kind')),
                    'equal':{'media kind':'movie', },
                    'apply':(
                        {
                            'property':'canonic file name',
                            'format':u'IMDb{imdb id} {simple name}.{kind}',
                        },
                    ),
                },
                {
                    'requires':set(('media kind', 'imdb id', 'kind')),
                    'equal':{'media kind':'movie', },
                    'apply':(
                        {
                            'property':'canonic file name',
                            'format':u'IMDb{imdb id}.{kind}',
                        },
                    ),
                },
            ),
        },
        {
            'name':'volume relative path',
            'provides':set(('volume relative path',)),
            'branch':(
                {
                    'requires':set(('media kind', 'kind', 'profile', 'tv show key', 'tv season', 'language', 'canonic file name')),
                    'equal':{'media kind':'tvshow', },
                    'apply':(
                        {
                            'property':'volume relative path',
                            'format':u'{media kind}/{kind}/{profile}/{tv show key}/{tv season}/{language}/{canonic file name}',
                        },
                    ),
                },
                {
                    'requires':set(('media kind', 'kind', 'profile', 'tv show key', 'tv season', 'canonic file name')),
                    'equal':{'media kind':'tvshow', },
                    'apply':(
                        {
                            'property':'volume relative path',
                            'format':u'{media kind}/{kind}/{profile}/{tv show key}/{tv season}/{canonic file name}',
                        },
                    ),
                },
                {
                    'requires':set(('media kind', 'kind', 'profile', 'language', 'canonic file name')),
                    'equal':{'media kind':'movie', },
                    'apply':(
                        {
                            'property':'volume relative path',
                            'format':u'{media kind}/{kind}/{profile}/{language}/{canonic file name}',
                        },
                    ),
                },
                {
                    'requires':set(('media kind', 'kind', 'profile', 'canonic file name')),
                    'equal':{'media kind':'movie', },
                    'apply':(
                        {
                            'property':'volume relative path',
                            'format':u'{media kind}/{kind}/{profile}/{canonic file name}',
                        },
                    ),
                },
            ),
        },
        {
            'name':'canonic path',
            'provides':set(('canonic path',)),
            'branch':(
                {
                    'requires':set(('volume path', 'volume relative path')),
                    'apply':(
                        {
                            'property':'canonic path',
                            'format':u'{volume path}/{volume relative path}',
                        },
                    ),
                },
            ),
        },
        {
            'name':'decode itunextc',
            'provides':set((
                'rating standard',
                'rating',
                'rating score',
                'rating annotation',
            )),
            'branch':(
                {
                    'requires':set(('itunextc',)),
                    'decode':(
                        {'property':'itunextc', 'expression':ur'(?P<rating_standard>[^|]+)\|(?P<rating>[^|]+)\|(?P<rating_score>[^|]+)\|(?P<rating_annotation>[^|]+)?',},
                    ),
                },
            ),
        },
        {
            'name':'tv season name',
            'provides':set(('tv season name',)),
            'branch':(
                {
                    'requires':set(('media kind', 'tv show', 'tv season')),
                    'equal':{'media kind':'tvshow', },
                    'apply':(
                        {
                            'property':'tv season name',
                            'format':u'{tv show}, Season {tv season}',
                        },
                        {
                            'property':'album',
                            'format':u'{tv show}, Season {tv season}',
                        },
                    ),
                },
            ),
        },
        {
            'name':'default track total',
            'provides':set(('track total', 'disk total')),
            'branch':(
                {
                    'requires':set(('media kind',)),
                    'equal':{'media kind':'tvshow', },
                    'apply':(
                        {'property':'track total', 'value':0},
                        {'property':'disk total', 'value':0},
                    ),
                },
            ),
        },
        {
            'name':'track information',
            'provides':set(('track position', 'track #')),
            'branch':(
                {
                    'requires':set(('media kind', 'tv episode', 'track total')),
                    'equal':{'media kind':'tvshow', },
                    'apply':(
                        {
                            'property':'track position',
                            'format':u'{tv episode}',
                        },
                        {
                            'property':'track #',
                            'format':u'{tv episode} / {track total}',
                        },
                    ),
                },
            ),
        },
        {
            'name':'disk information',
            'provides':set(('disk position', 'disk #')),
            'branch':(
                {
                    'requires':set(('media kind', 'tv season', 'disk total')),
                    'equal':{'media kind':'tvshow', },
                    'apply':(
                        {
                            'property':'disk position',
                            'format':u'{tv season}',
                        },
                        {
                            'property':'disk #',
                            'format':u'{tv season} / {disk total}',
                        },
                    ),
                },
            ),
        },
        {
            'name':'artist information',
            'provides':set(('artist', 'album artist')),
            'branch':(
                {
                    'requires':set(('media kind', 'tv show')),
                    'equal':{'media kind':'tvshow', },
                    'apply':(
                        {
                            'property':'artist',
                            'format':u'{tv show}',
                        },
                        {
                            'property':'album artist',
                            'format':u'{tv show}',
                        },
                    ),
                },
                {
                    'requires':set(('media kind', 'directors')),
                    'equal':{'media kind':'movie', },
                    'apply':(
                        {
                            'property':'artist',
                            'format':u'{directors[0]}',
                        },
                        {
                            'property':'album artist',
                            'format':u'{directors[0]}',
                        },
                    ),
                },
                {
                    'requires':set(('media kind', 'producers')),
                    'equal':{'media kind':'movie', },
                    'apply':(
                        {
                            'property':'artist',
                            'format':u'{producers[0]}',
                        },
                        {
                            'property':'album artist',
                            'format':u'{producers[0]}',
                        },
                    ),
                },
                {
                    'requires':set(('media kind', 'screenwriters')),
                    'equal':{'media kind':'movie', },
                    'apply':(
                        {
                            'property':'artist',
                            'format':u'{screenwriters[0]}',
                        },
                        {
                            'property':'album artist',
                            'format':u'{screenwriters[0]}',
                        },
                    ),
                },
                {
                    'requires':set(('media kind', 'codirectors')),
                    'equal':{'media kind':'movie', },
                    'apply':(
                        {
                            'property':'artist',
                            'format':u'{codirectors[0]}',
                        },
                        {
                            'property':'album artist',
                            'format':u'{codirectors[0]}',
                        },
                    ),
                },
                {
                    'requires':set(('media kind', 'cast')),
                    'equal':{'media kind':'movie', },
                    'apply':(
                        {
                            'property':'artist',
                            'format':u'{cast[0]}',
                        },
                        {
                            'property':'album artist',
                            'format':u'{cast[0]}',
                        },
                    ),
                },
            ),
        },
        {
            'name':'sort name',
            'provides':set(('sort name',)),
            'branch':(
                {
                    'requires':set(('name',)),
                    'decode':(
                        {'property':'name', 'expression':ur'^(the |a )?(?P<sort_name>.+)$', 'flags':re.IGNORECASE},
                    ),
                },
            ),
        },
        {
            'name':'sort artist',
            'provides':set(('sort artist',)),
            'branch':(
                {
                    'requires':set(('artist',)),
                    'decode':(
                        {'property':'artist', 'expression':ur'^(the |a )?(?P<sort_artist>.+)$', 'flags':re.IGNORECASE},
                    ),
                },
            ),
        },
        {
            'name':'sort album artist',
            'provides':set(('sort album artist',)),
            'branch':(
                {
                    'requires':set(('album artist',)),
                    'decode':(
                        {'property':'album artist', 'expression':ur'^(the |a )?(?P<sort_album_artist>.+)$', 'flags':re.IGNORECASE},
                    ),
                },
            ),
        },
        {
            'name':'sort album',
            'provides':set(('sort album',)),
            'branch':(
                {
                    'requires':set(('album',)),
                    'decode':(
                        {'property':'album', 'expression':ur'^(the |a )?(?P<sort_album>.+)$', 'flags':re.IGNORECASE},
                    ),
                },
            ),
        },
        {
            'name':'sort tv show',
            'provides':set(('sort tv show',)),
            'branch':(
                {
                    'requires':set(('tv show',)),
                    'decode':(
                        {'property':'tv show', 'expression':ur'^(the |a )?(?P<sort_tv_show>.+)$', 'flags':re.IGNORECASE},
                    ),
                },
            ),
        },
        {
            'name':'sort composer',
            'provides':set(('sort composer',)),
            'branch':(
                {
                    'requires':set(('composer',)),
                    'decode':(
                        {'property':'composer', 'expression':ur'^(the |a )?(?P<sort_composer>.+)$', 'flags':re.IGNORECASE},
                    ),
                },
            ),
        },
        {
            'name':'full name',
            'provides':set(('full name',)),
            'branch':(
                {
                    'requires':set(('media kind', 'tv show', 'tv episode id', 'name')),
                    'equal':{'media kind':'tvshow', },
                    'apply':(
                        {
                            'property':'full name',
                            'format':u'{tv show} {tv episode id} {name}',
                        },
                    ),
                },
                {
                    'requires':set(('media kind', 'tv show', 'tv episode id')),
                    'equal':{'media kind':'tvshow', },
                    'apply':(
                        {
                            'property':'full name',
                            'format':u'{tv show} {tv episode id}',
                        },
                    ),
                },
                {
                    'requires':set(('media kind', 'imdb id', 'name')),
                    'equal':{'media kind':'movie', },
                    'apply':(
                        {
                            'property':'full name',
                            'format':u'IMDb{imdb id} {name}',
                        },
                    ),
                },
                {
                    'requires':set(('media kind', 'imdb id')),
                    'equal':{'media kind':'movie', },
                    'apply':(
                        {
                            'property':'full name',
                            'format':u'IMDb{imdb id}',
                        },
                    ),
                },
            ),
        },
        {
            'name':'path in cache',
            'provides':set(('path in cache',)),
            'branch':(
                {
                    'requires':set(('cache root', 'host', 'volume', 'volume relative path')),
                    'apply':(
                        {
                            'property':'path in cache',
                            'format':u'{cache root}/{host}/{volume}/{volume relative path}',
                        },
                    ),
                },
                {
                    'requires':set(('cache root', 'host', 'file path')),
                    'apply':(
                        {
                            'property':'path in cache',
                            'format':u'{cache root}/{host}{file path}',
                        },
                    ),
                },
            ),
        },
        {
            'name':'uri',
            'provides':set(('uri',)),
            'branch':(
                {
                    'requires':set(('resource uri scheme', 'host', 'volume', 'volume relative path')),
                    'apply':(
                        {
                            'property':'uri',
                            'format':u'{resource uri scheme}://{host}/{volume}/{volume relative path}',
                        },
                    ),
                },
            ),
        },
        {
            'name':'resource id',
            'provides':set(('resource id',)),
            'branch':(
                {
                    'requires':set(('path', 'host')),
                    'apply':(
                        {
                            'property':'resource id',
                            'format':u'{host}:{path}',
                        },
                    ),
                },
            ),
        },
    ],
    'kind':{
        'm4v':{
            'container':'mp4',
        },
        'm4a':{
            'container':'mp4',
        },
        'mkv':{
            'container':'matroska',
        },
        'avi':{
            'container':'avi',
        },
        'srt':{
            'container':'subtitles',
        },
        'ass':{
            'container':'subtitles',
        },
        'chpl':{
            'container':'chapters',
        },
        'jpg':{
            'container':'image',
        },
        'png':{
            'container':'image',
        },
        'ac3':{
            'container':'raw audio',
        },
        'dts':{
            'container':'raw audio',
        },
    },
    'service':{
        'knowlege':{
            'match':ur'^mpk://(?P<host>[^/]+)(?P<relative>/k/.*)$',
            'branch':{
                'knowlege.configuration':{
                    'match':ur'/k/configuration',
                    'type':'json',
                    'collection':'knowlege_configuration',
                },
                'knowlege.movie':{
                    'match':ur'/k/movie/(?P<language>[a-z]{2})/(?P<movie_id>[0-9]+)',
                    'type':'json',
                    'collection':'knowlege_movie',
                    'namespace':'knowlege.movie',
                },
                'knowlege.tvshow.show':{
                    'match':ur'/k/tvshow/(?P<language>[a-z]{2})/show/(?P<tv_show_id>[0-9]+)',
                    'type':'json',
                    'collection':'knowlege_tvshow_show',
                    'namespace':'knowlege.tvshow.show',
                },
                'knowlege.tvshow.season':{
                    'match':ur'/k/tvshow/(?P<language>[a-z]{2})/season/(?P<tv_show_id>[0-9]+)/(?P<tv_season>[0-9]+)',
                    'type':'json',
                    'collection':'knowlege_tvshow_season',
                    'namespace':'knowlege.tvshow.season',
                },
                'knowlege.tvshow.episode':{
                    'match':ur'/k/tvshow/(?P<language>[a-z]{2})/episode/(?P<tv_show_id>[0-9]+)/(?P<tv_season>[0-9]+)/(?P<tv_episode>[0-9]+)',
                    'type':'json',
                    'collection':'knowlege_tvshow_episode',
                    'namespace':'knowlege.tvshow.episode',
                },
                'knowlege.person':{
                    'match':ur'/k/person/(?P<person_id>[0-9]+)',
                    'type':'json',
                    'collection':'knowlege_person',
                    'namespace':'knowlege.person',
                },
                'knowlege.network':{
                    'match':ur'/k/network/(?P<network_id>[0-9]+)',
                    'type':'json',
                    'collection':'knowlege_network',
                    'namespace':'knowlege.network',
                },
                'knowlege.studio':{
                    'match':ur'/k/studio/(?P<studio_id>[0-9]+)',
                    'type':'json',
                    'collection':'knowlege_studio',
                    'namespace':'knowlege.studio',
                },
                'knowlege.job':{
                    'match':ur'/k/job/(?P<job_id>[0-9]+)',
                    'type':'json',
                    'collection':'knowlege_job',
                    'namespace':'knowlege.job',
                },
                'knowlege.department':{
                    'match':ur'/k/department/(?P<department_id>[0-9]+)',
                    'type':'json',
                    'collection':'knowlege_department',
                    'namespace':'knowlege.department',
                },
                'knowlege.genre':{
                    'match':ur'/k/genre/(?P<genre_id>[0-9]+)',
                    'type':'json',
                    'collection':'knowlege_genre',
                    'namespace':'knowlege.genre',
                },
            },
        },
        'tmdb':{
            'api key':u'a8b9f96dde091408a03cb4c78477bd14',
            'match':ur'^mpk://(?P<host>[^/]+)(?P<relative>/c/tmdb/.*)$',
            'branch':{
                'tmdb.configuration':{
                    'match':[
                        {
                            'filter':ur'^/c/tmdb/configuration$',
                            'remote':ur'http://api.themoviedb.org/3/configuration?api_key={api key}',
                        },
                    ],
                    'resolvable':[
                        {
                            'name':u'tmdb configuration',
                            'format':ur'/c/tmdb/configuration',
                        },
                    ],
                    'collection':'tmdb_configuration',
                    'namespace':'tmdb.movie',
                    'type':'json',
                },
                'tmdb.movie':{
                    # http://api.themoviedb.org/3/movie/1891?language=en&api_key=a8b9f96dde091408a03cb4c78477bd14
                    'match':[
                        {
                            'filter':ur'^/c/tmdb/movie/(?P<language>[a-z]{2})/(?P<tmdb_movie_id>[0-9]+)$',
                            'remote':ur'http://api.themoviedb.org/3/movie/{tmdb movie id}?language={language}&api_key={api key}',
                        },
                        {
                            'filter':ur'^/c/tmdb/movie/(?P<language>[a-z]{2})/(?P<imdb_movie_id>tt[0-9]+)$',
                            'remote':ur'http://api.themoviedb.org/3/movie/{imdb movie id}?language={language}&api_key={api key}',
                        },
                    ],
                    'resolvable':[
                        {
                            'name':u'tmdb movie by tmdb id',
                            'format':ur'/c/tmdb/movie/{language}/{tmdb movie id}',
                        },
                        {
                            'name':u'tmdb movie by imdb id',
                            'format':ur'/c/tmdb/movie/{language}/{imdb movie id}',
                        }
                    ],
                    'collection':'tmdb_movie',
                    'namespace':'tmdb.movie',
                    'type':'json',
                    'index':['tmdb movie id', 'language', 'imdb movie id'],
                },
                'tmdb.movie.cast':{
                    'match':[
                        {
                            'filter':ur'^/c/tmdb/movie/(?P<tmdb_movie_id>[0-9]+)/cast$',
                            'remote':ur'http://api.themoviedb.org/3/movie/{tmdb movie id}/casts?api_key={api key}',
                        },
                        {
                            'filter':ur'^/c/tmdb/movie/(?P<imdb_movie_id>tt[0-9]+)/cast$',
                            'remote':ur'http://api.themoviedb.org/3/movie/{imdb movie id}/casts?api_key={api key}',
                        },
                    ],
                    'resolvable':[
                        {
                            'name':u'tmdb movie cast by tmdb id',
                            'format':ur'/c/tmdb/movie/{tmdb movie id}/cast',
                        },
                        {
                            'name':u'tmdb movie cast by imdb id',
                            'format':ur'/c/tmdb/movie/{imdb movie id}/cast',
                        },
                    ],
                    'collection':'tmdb_movie_cast',
                    'namespace':'tmdb.movie',
                    'type':'json',
                    'index':['tmdb movie id'],
                },
                'tmdb.movie.poster':{
                    'match':[
                        {
                            'filter':ur'^/c/tmdb/movie/(?P<tmdb_movie_id>[0-9]+)/poster$',
                            'remote':ur'http://api.themoviedb.org/3/movie/{tmdb movie id}/images?api_key={api key}',
                        },
                        {
                            'filter':ur'^/c/tmdb/movie/(?P<imdb_movie_id>tt[0-9]+)/poster$',
                            'remote':ur'http://api.themoviedb.org/3/movie/{imdb movie id}/images?api_key={api key}',
                        },
                    ],
                    'resolvable':[
                        {
                            'name':u'tmdb movie poster by tmdb id',
                            'format':ur'/c/tmdb/movie/{tmdb movie id}/poster',
                        },
                        {
                            'name':u'tmdb movie poster by imdb id',
                            'format':ur'/c/tmdb/movie/{imdb movie id}/poster',
                        },
                    ],
                    'collection':'tmdb_movie_poster',
                    'namespace':'tmdb.movie',
                    'type':'json',
                    'index':['tmdb movie id'],
                },
                'tmdb.movie.keyword':{
                    'match':[
                        {
                            'filter':ur'^/c/tmdb/movie/(?P<tmdb_movie_id>[0-9]+)/keyword$',
                            'remote':ur'http://api.themoviedb.org/3/movie/{tmdb movie id}/keywords?api_key={api key}',
                        },
                        {
                            'filter':ur'^/c/tmdb/movie/(?P<imdb_movie_id>tt[0-9]+)/keyword$',
                            'remote':ur'http://api.themoviedb.org/3/movie/{imdb movie id}/keywords?api_key={api key}',
                        },
                    ],
                    'resolvable':[
                        {
                            'name':u'tmdb movie keyword by tmdb id',
                            'format':ur'/c/tmdb/movie/{tmdb movie id}/keyword',
                        },
                        {
                            'name':u'tmdb movie keyword by imdb id',
                            'format':ur'/c/tmdb/movie/{imdb movie id}/keyword',
                        },
                    ],
                    'collection':'tmdb_movie_keyword',
                    'namespace':'tmdb.movie',
                    'type':'json',
                    'index':['tmdb movie id'],
                },
                'tmdb.movie.release':{
                    'match':[
                        {
                            'filter':ur'^/c/tmdb/movie/(?P<tmdb_movie_id>[0-9]+)/release$',
                            'remote':ur'http://api.themoviedb.org/3/movie/{tmdb movie id}/releases?api_key={api key}',
                        },
                        {
                            'filter':ur'^/c/tmdb/movie/(?P<imdb_movie_id>tt[0-9]+)/release$',
                            'remote':ur'http://api.themoviedb.org/3/movie/{imdb movie id}/releases?api_key={api key}',
                        },
                    ],
                    'resolvable':[
                        {
                            'name':u'tmdb movie release by tmdb id',
                            'format':ur'/c/tmdb/movie/{tmdb movie id}/release',
                        },
                        {
                            'name':u'tmdb movie release by imdb id',
                            'format':ur'/c/tmdb/movie/{imdb movie id}/release',
                        },
                    ],
                    'collection':'tmdb_movie_release',
                    'namespace':'tmdb.movie',
                    'type':'json',
                    'index':['tmdb movie id'],
                },
                'tmdb.movie.trailer':{
                    'match':[
                        {
                            'filter':ur'^/c/tmdb/movie/(?P<tmdb_movie_id>[0-9]+)/trailer$',
                            'remote':ur'http://api.themoviedb.org/3/movie/{tmdb movie id}/trailers?api_key={api key}',
                        },
                        {
                            'filter':ur'^/c/tmdb/movie/(?P<imdb_movie_id>tt[0-9]+)/trailer$',
                            'remote':ur'http://api.themoviedb.org/3/movie/{imdb movie id}/trailers?api_key={api key}',
                        },
                    ],
                    'resolvable':[
                        {
                            'name':u'tmdb movie trailer by tmdb id',
                            'format':ur'/c/tmdb/movie/{tmdb movie id}/trailer',
                        },
                        {
                            'name':u'tmdb movie trailer by imdb id',
                            'format':ur'/c/tmdb/movie/{imdb movie id}/trailer',
                        },
                    ],
                    'collection':'tmdb_movie_trailer',
                    'namespace':'tmdb.movie',
                    'type':'json',
                    'index':['tmdb movie id'],
                },
                'tmdb.movie.translation':{
                    'match':[
                        {
                            'filter':ur'^/c/tmdb/movie/(?P<tmdb_movie_id>[0-9]+)/translation$',
                            'remote':ur'http://api.themoviedb.org/3/movie/{tmdb movie id}/translations?api_key={api key}',
                        },
                        {
                            'filter':ur'^/c/tmdb/movie/(?P<imdb_movie_id>tt[0-9]+)/translation$',
                            'remote':ur'http://api.themoviedb.org/3/movie/{imdb movie id}/translations?api_key={api key}',
                        },
                    ],
                    'resolvable':[
                        {
                            'name':u'tmdb movie translation by tmdb id',
                            'format':ur'/c/tmdb/movie/{tmdb movie id}/translation',
                        },
                        {
                            'name':u'tmdb movie translation by imdb id',
                            'format':ur'/c/tmdb/movie/{imdb movie id}/translation',
                        },
                    ],
                    'collection':'tmdb_movie_translation',
                    'namespace':'tmdb.movie',
                    'type':'json',
                    'index':['tmdb movie id'],
                },
                'tmdb.movie.alternative':{
                    'match':[
                        {
                            'filter':ur'^/c/tmdb/movie/(?P<tmdb_movie_id>[0-9]+)/alternative$',
                            'remote':ur'http://api.themoviedb.org/3/movie/{tmdb movie id}/alternative_titles?api_key={api key}',
                        },
                        {
                            'filter':ur'^/c/tmdb/movie/(?P<imdb_movie_id>tt[0-9]+)/alternative$',
                            'remote':ur'http://api.themoviedb.org/3/movie/{imdb movie id}/alternative_titles?api_key={api key}',
                        },
                    ],
                    'resolvable':[
                        {
                            'name':u'tmdb movie alternative by tmdb id',
                            'format':ur'/c/tmdb/movie/{tmdb movie id}/alternative',
                        },
                        {
                            'name':u'tmdb movie alternative by imdb id',
                            'format':ur'/c/tmdb/movie/{imdb movie id}/alternative',
                        },
                    ],
                    'collection':'tmdb_movie_alternative',
                    'namespace':'tmdb.movie',
                    'type':'json',
                    'index':['tmdb movie id'],
                },
                'tmdb.person':{
                    'match':[
                        {
                            'filter':ur'^/c/tmdb/person/(?P<tmdb_person_id>[0-9]+)$',
                            'remote':ur'http://api.themoviedb.org/3/person/{tmdb person id}?api_key={api key}',
                        },
                    ],
                    'resolvable':[
                        {
                            'name':u'tmdb person by tmdb id',
                            'format':ur'/c/tmdb/person/{tmdb person id}',
                        },
                    ],
                    'collection':'tmdb_person',
                    'namespace':'tmdb.person',
                    'type':'json',
                },
                'tmdb.person.poster':{
                    'match':[
                        {
                            'filter':ur'^/c/tmdb/person/(?P<tmdb_person_id>[0-9]+)/poster$',
                            'remote':ur'http://api.themoviedb.org/3/person/{tmdb person id}?api_key={api key}',
                        },
                    ],
                    'resolvable':[
                        {
                            'name':u'tmdb person poster by tmdb id',
                            'format':ur'/c/tmdb/person/{tmdb person id}/poster',
                        },
                    ],
                    'collection':'tmdb_person_poster',
                    'namespace':'tmdb.person',
                    'type':'json',
                },
                'tmdb.person.credit':{
                    'match':[
                        {
                            'filter':ur'^/c/tmdb/person/(?P<tmdb_person_id>[0-9]+)/credit$',
                            'remote':ur'http://api.themoviedb.org/3/person/{tmdb person id}/credits?api_key={api key}',
                        },
                    ],
                    'resolvable':[
                        {
                            'name':u'tmdb person credit by tmdb id',
                            'format':ur'/c/tmdb/person/{tmdb person id}/credit',
                        },
                    ],
                    'collection':'tmdb_person_credit',
                    'namespace':'tmdb.person',
                    'type':'json',
                },
            },
            'status codes':{
                1:'Success.',
                2:'Invalid service - This service does not exist.',
                3:'Authentication failed - You do not have permissions to access the service.',
                4:'Invalid format - This service doesn\'t exist in that format.',
                5:'Invalid parameters - Your request parameters are incorrect.',
                6:'Invalid id - The pre-requisite id is invalid or not found.',
                7:'Invalid API key - You must be granted a valid key.',
                8:'Duplicate entry - The data you tried to submit already exists.',
                9:'Service offline - This service is temporarily offline. Try again later.',
                10:'Suspended API key - Access to your account has been suspended, contact TMDb.',
                11:'Internal error - Something went wrong. Contact TMDb.',
                12:'The item/record was updated successfully.',
                13:'The item/record was deleted successfully.',
                14:'Authentication failed.',
                15:'Failed.',
                16:'Device denied.',
                17:'Session denied.',
            }
        },
        'tvdb':{
            'api key':u'7B3B400B0146EA83',
            'match':ur'^mpk://(?P<host>[^/]+)(?P<relative>/c/tvdb/.*)$',
            'branch':{
                'tvdb.show':{
                    'match':[
                        {
                            'filter':ur'^/c/tvdb/show/(?P<language>[a-z]{2})/(?P<tvdb_tv_show_id>[0-9]+)$',
                            'remote':ur'http://www.thetvdb.com/api/{api key}/series/{tvdb tv show id}/{language}.xml',
                        },
                    ],
                    'resolvable':[
                        {
                            'name':u'tvdb show by tvdb show id',
                            'format':ur'/c/tvdb/show/{language}/{tvdb tv show id}',
                        },
                    ],
                    'collection':'tvdb_tv_show',
                    'namespace':'tvdb.show',
                    'type':'xml',
                    'produce':['tvdb.show'],
                },
                'tvdb.episode':{
                    # http://www.thetvdb.com/api/7B3B400B0146EA83/series/73255/default/7/1/en.xml
                    'match':[
                        {
                            'filter':ur'^/c/tvdb/episode/(?P<language>[a-z]{2})/(?P<tvdb_tv_episode_id>[0-9]+)$',
                            'remote':ur'http://www.thetvdb.com/api/{api key}/episodes/{tvdb tv episode id}/{language}.xml',
                        },
                        {
                            'filter':ur'^/c/tvdb/episode/(?P<language>[a-z]{2})/(?P<tvdb_tv_show_id>[0-9]+)/(?P<tv_season>[0-9]+)/(?P<tv_episode>[0-9]+)$',
                            'remote':ur'http://www.thetvdb.com/api/{api key}/series/{tvdb tv show id}/default/{tv season}/{tv episode}/{language}.xml',
                        },
                    ],
                    'resolvable':[
                        {
                            'name':u'tvdb episode by tvdb episode id',
                            'format':ur'/c/tvdb/episode/{language}/{tvdb tv episode id}',
                        },
                        {
                            'name':u'tvdb episode by tvdb show id',
                            'format':ur'/c/tvdb/episode/{language}/{tvdb tv show id}/{tv season}/{tv episode}',
                        },
                    ],
                    'collection':'tvdb_tv_episode',
                    'namespace':'tvdb.episode',
                    'type':'xml',
                    'produce':['tvdb.episode'],
                    'index':['tvdb tv show id', 'tvdb tv episode id', 'tv season', 'tv episode'],
                },
                'tvdb.show.poster':{
                    'match':[
                        {
                            'filter':ur'^/c/tvdb/show/(?P<tvdb_tv_show_id>[0-9]+)/poster$',
                            'remote':ur'http://www.thetvdb.com/api/{api key}/series/{tvdb tv show id}/banners.xml',
                        },
                    ],
                    'resolvable':[
                        {
                            'name':u'tvdb show poster by tvdb show id',
                            'format':ur'/c/tvdb/show/{tvdb tv show id}/poster',
                        },
                    ],
                    'collection':'tvdb_tv_show_poster',
                    'namespace':'tvdb.show.poster',
                    'type':'xml',
                    'produce':['tvdb.show.poster'],
                },
                'tvdb.show.cast':{
                    'match':[
                        {
                            'filter':ur'^/c/tvdb/show/(?P<tvdb_tv_show_id>[0-9]+)/cast$',
                            'remote':ur'http://www.thetvdb.com/api/{api key}/series/{tvdb tv show id}/actors.xml',
                        },
                    ],
                    'resolvable':[
                        {
                            'name':u'tvdb show cast by tvdb show id',
                            'format':ur'/c/tvdb/show/{tvdb tv show id}/cast',
                        },
                    ],
                    'collection':'tvdb_tv_show_cast',
                    'namespace':'tvdb.show.cast',
                    'type':'xml',
                    'produce':['tvdb.show.cast'],
                },
                'tvdb.show.complete':{
                    'match':[
                        {
                            'filter':ur'^/c/tvdb/show/(?P<language>[a-z]{2})/(?P<tvdb_tv_show_id>[0-9]+)/complete$',
                            'remote':ur'http://www.thetvdb.com/api/{api key}/series/{tvdb tv show id}/all/{language}.zip',
                        },
                    ],
                    'resolvable':[
                        {
                            'name':u'complete tvdb show by tvdb show id',
                            'format':ur'/c/tvdb/show/{language}/{tvdb tv show id}/complete',
                        },
                    ],
                    'namespace':'tvdb.show',
                    'type':'zip',
                    'produce':['tvdb.show', 'tvdb.episode', 'tvdb.show.poster', 'tvdb.show.cast'],
                },
                'tvdb.update.daily':{
                    'match':[
                        {
                            'filter':ur'^/c/tvdb/update/day$',
                            'remote':ur'http://www.thetvdb.com/api/{api key}/updates/updates_day.zip',
                        },
                    ],
                    'resolvable':[
                        {
                            'name':u'tvdb daily update',
                            'format':ur'/c/tvdb/update/day',
                        },
                    ],
                    'type':'zip',
                },
                'tvdb.update.weekly':{
                    'match':[
                        {
                            'filter':ur'^/c/tvdb/update/week$',
                            'remote':ur'http://www.thetvdb.com/api/{api key}/updates/updates_week.zip',
                        },
                    ],
                    'resolvable':[
                        {
                            'name':u'tvdb weekly update',
                            'format':ur'/c/tvdb/update/week',
                        },
                    ],
                    'type':'zip',
                },
                'tvdb.update.monthly':{
                    'match':[
                        {
                            'filter':ur'^/c/tvdb/update/month$',
                            'remote':ur'http://www.thetvdb.com/api/{api key}/updates/updates_month.zip',
                        },
                    ],
                    'resolvable':[
                        {
                            'name':u'tvdb monthly update',
                            'format':ur'/c/tvdb/update/month',
                        },
                    ],
                    'type':'zip',
                },
                'tvdb.update.episode':{
                    'match':[
                        {
                            'filter':ur'/c/tvdb/update/episode/(?P<time>[0-9]+)',
                            'remote':ur'http://www.thetvdb.com/api/Updates.php?type=episode&time={time}',
                        },
                    ],
                    'resolvable':[
                        {
                            'name':u'tvdb episode update since',
                            'format':ur'/c/tvdb/update/episode/{time}',
                        },
                    ],
                    'type':'xml',
                },
                'tvdb.update.show':{
                    'match':[
                        {
                            'filter':ur'/c/tvdb/update/show/(?P<time>[0-9]+)',
                            'remote':ur'http://www.thetvdb.com/api/Updates.php?type=series&time={time}',
                        },
                    ],
                    'resolvable':[
                        {
                            'name':u'tvdb show update since',
                            'format':ur'/c/tvdb/update/show/{time}',
                        },
                    ],
                    'type':'xml',
                },
            },
        },
    },
    
    'track with language':set(
        ('audio', 'text', 'video')
    ),
    'kind with language':set(
        ('srt', 'ass', 'ac3', 'dts')
    ),
    'escaped subler tag characters':set(
        (u'{', u'}', u':')
    ),
    'empty string':u'',
    'resource scheme':resource_scheme,
    'PAL framerate':25.0,
    'NTSC framerate':23.976,
}
