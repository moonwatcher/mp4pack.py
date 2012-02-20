# -*- coding: utf-8 -*-

import re
import logging

tmdb_apikey = u'a8b9f96dde091408a03cb4c78477bd14'
tvdb_apikey = u'7B3B400B0146EA83'
resource_scheme = u'mp4pack'

runtime = {
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
                                    {'type':'text', 'language':'heb', 'codec':'srt'},
                                    {'type':'text', 'language':'heb', 'codec':'ass'},
                                ],
                            },
                            {
                                'mode':'choose',
                                'branch':[
                                    {'type':'text', 'language':'eng', 'codec':'srt'},
                                    {'type':'text', 'language':'eng', 'codec':'ass'},
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
                        'description':'Hebrew and english subtitles of the clean profile',
                        'mode':'select',
                        'branch':[
                            {'kind':'srt', 'profile':'clean'},
                        ],
                        'track':[
                            {
                                'mode':'choose',
                                'branch':[
                                    {'type':'text', 'language':'heb'},
                                ],
                                'override':{'name':'Normal'},
                            },
                            {
                                'mode':'choose',
                                'branch':[
                                    {'type':'text', 'language':'eng'},
                                ],
                                'override':{'name':'Normal'},
                            },
                        ],
                    },
                    {
                        'description':'First of hebrew or english subtitles as swedish',
                        'mode':'choose',
                        'branch':[
                            {'kind':'srt', 'profile':'clean', 'language':'heb'},
                            {'kind':'srt', 'profile':'clean', 'language':'eng'},
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
                            {'kind':'chpl', 'language':'heb'},
                            {'kind':'chpl', 'language':'eng'},
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
                                    {'type':'text', 'language':'heb'},
                                ],
                                'override':{'name':'Normal', 'height':0.132},
                            },
                            {
                                'mode':'choose',
                                'branch':[
                                    {'type':'text', 'language':'eng'},
                                ],
                                'override':{'name':'Normal', 'height':0.132},
                            },
                        ],
                    },
                    {
                        'description':'First of hebrew or english subtitles as swedish',
                        'mode':'choose',
                        'branch':[
                            {'kind':'srt', 'profile':'clean', 'language':'heb'},
                            {'kind':'srt', 'profile':'clean', 'language':'eng'},
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
                            {'kind':'png', 'profile':'normal', 'language':'heb'},
                            {'kind':'png', 'profile':'normal', 'language':'eng'},
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
                            {'kind':'chpl', 'language':'heb'},
                            {'kind':'chpl', 'language':'eng'},
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
                                    {'type':'text', 'language':'heb'},
                                ],
                                'override':{
                                    'subtitle filters':['noise', 'hebrew noise', 'typo', 'punctuation', 'leftover']
                                },
                            },
                            {
                                'description':'English subtitles',
                                'mode':'choose',
                                'branch':[
                                    {'type':'text', 'language':'eng'},
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
            'name':'invisable file path', 
            'definition':ur'^\.', 
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
            'name':'full numeric time format',
            'definition':u'([0-9]{,2}):([0-9]{,2}):([0-9]{,2})(?:\.|,)([0-9]+)',
            'flags':re.UNICODE,
        },
        {
            'name':'sentence end',
            'definition':ur'[.!?]',
            'flags':re.UNICODE,
        },
        {
            'name':'mediainfo integer list',
            'definition':u'[0-9]+(?:\s*/\s*[0-9]+)+',
            'flags':re.UNICODE,
        },
        {
            'name':'mediainfo value list',
            'definition':ur'^[^/]+(?:\s*/\s*[^/]+)*$',
            'flags':re.UNICODE,
        },
        {
            'name':'prefix to remove from sort',
            'definition':u'^(the |a )(.+)$',
            'flags':re.UNICODE|re.IGNORECASE,
        },
        {
            'name':'clean xml',
            'definition':ur'\s+/\s+(?:\t)*',
            'flags':re.UNICODE,
        },
        {
            'name':'itunextc structure',
            'definition':ur'([^|]+)\|([^|]+)\|([^|]+)\|([^|]+)?',
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
            'name':'mediainfo chapter timecode',
            'definition':u'_([0-9]{2})_([0-9]{2})_([0-9]{2})\.([0-9]{3})',
            'flags':re.UNICODE,
        },
        {
            'name':'mediainfo chapter name with lang',
            'definition':u'^(?:([a-z]{2,3}):)?(.*)$',
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
                'tv episode #',
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
                    'requires':set(('media kind', 'tv season', 'tv episode #')),
                    'equal':{'media kind':'tvshow', },
                    'apply':(
                        {
                            'property':'tv episode id',
                            'format':u's{tv season:02d}e{tv episode #:02d}',
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
                    'requires':set(('media kind', 'tv show key', 'tv season', 'tv episode #')),
                    'equal':{'media kind':'tvshow', },
                    'apply':(
                        {
                            'property':'asset id',
                            'format':u'{media kind}/{tv show key}/{tv season}/{tv episode #}',
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
                    'requires':set(('media kind', 'tv episode #', 'track total')),
                    'equal':{'media kind':'tvshow', },
                    'apply':(
                        {
                            'property':'track position',
                            'format':u'{tv episode #}',
                        },
                        {
                            'property':'track #',
                            'format':u'{tv episode #} / {track total}',
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
    
    # Should become a rule
    'service':{
        'tmdb':{
            'apikey':tmdb_apikey,
            'urls':{
                'Movie.getInfo':u'http://api.themoviedb.org/2.1/Movie.getInfo/en/json/{0}/{{0}}'.format(tmdb_apikey),
                'Movie.imdbLookup':u'http://api.themoviedb.org/2.1/Movie.imdbLookup/en/json/{0}/{{0}}'.format(tmdb_apikey),
                'Person.getInfo':u'http://api.themoviedb.org/2.1/Person.getInfo/en/json/{0}/{{0}}'.format(tmdb_apikey),
                'Person.search':u'http://api.themoviedb.org/2.1/Person.search/en/json/{0}/{{0}}'.format(tmdb_apikey),
                'Genres.getList':u'http://api.themoviedb.org/2.1/Genres.getList/en/json/{0}'.format(tmdb_apikey),
            },
        },
        'tvdb':{
            'apikey':tvdb_apikey,
            'fuzzy':{
                'minimum_person_name_length':3,
            },
            'urls':{
                'Show.getInfo':u'http://www.thetvdb.com/api/{0}/series/{{0}}/all/en.xml'.format(tvdb_apikey),
                'Banner.getImage':u'http://www.thetvdb.com/banners/{0}'
            },
        },
    },
    
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
    'log level':{
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'critical': logging.CRITICAL
    },
    'decimal si prefix':{
        0:u'bit',
        1:u'kbit',
        2:u'Mbit',
        3:u'Gbit',
        4:u'Tbit',
    },
    'binary iec 60027 2 prefix':{
        0:u'Byte',
        1:u'KiB',
        2:u'MiB',
        3:u'GiB',
        4:u'TiB',
    },
    'track with language':set(('audio', 'text', 'video')),
    'kind with language':set(('srt', 'ass', 'ac3', 'dts')),
    'escaped subler tag characters':set((u'{', u'}', u':')),
    'empty string':u'',
    'resource scheme':resource_scheme,
    'PAL framerate':25.0,
    'NTSC framerate':23.976,
}
