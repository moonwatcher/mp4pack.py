# -*- coding: utf-8 -*-
{
    'preset':{
        'normal':{
        	'description':u'Base empty profile to mirror the default profile',
            'action':{
                'info':{},
                'copy':{},
                'move':{},
                'delete':{},
                'explode':{
                    'pivot':[
                        { 'operator':'this' },
                    ],
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
                                        {'stream kind':'caption', 'language':'he'},
                                    ],
                                },
                                {
                                    'mode':'choose',
                                    'branch':[
                                        {'stream kind':'caption', 'language':'en'},
                                    ],
                                },
                                {
                                    'mode':'select',
                                    'branch':(
                                        {'stream kind':'audio', 'kind':'dts'},
                                    ),
                                },
                                {
                                    'mode':'select',
                                    'branch':(
                                        {'stream kind':'audio', 'kind':'flac'},
                                    ),
                                },
                                {
                                    'mode':'choose',
                                    'branch':(
                                        {'stream kind':'menu'},
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
                                        {'stream kind':'menu'},
                                    ],
                                },
                            ],
                        },
                    ],
                },
                'pack':{
                    'pivot':[
                        { 'operator':'this' },
                        { 'operator':'select', 'constraint':{'kind':'srt'} },
                        { 'operator':'select', 'constraint':{'kind':'chpl'} },
                        { 'operator':'select', 'constraint':{'kind':'ac3'} },
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
                                        {'stream kind':'caption', 'language':'he'},
                                    ],
                                    'override':{'stream name':'Normal'},
                                },
                                {
                                    'mode':'choose',
                                    'branch':[
                                        {'stream kind':'caption', 'language':'en'},
                                    ],
                                    'override':{'stream name':'Normal'},
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
                                        {'stream kind':'caption'},
                                    ],
                                    'override':{'stream name':'Smart', 'language':'sv'},
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
                                        {'stream kind':'menu'},
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
                                        {'stream kind':'audio', 'kind':'ac3'},
                                    ],
                                    'override':{'stream name':'Normal'},
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
                                        {'stream kind':'video'},
                                        {'stream kind':'audio', 'kind':'ac3'},
                                        {'stream kind':'audio', 'kind':'aac'},
                                        {'stream kind':'audio', 'kind':'dts'},
                                        {'stream kind':'audio', 'kind':'flac'},
                                        {'stream kind':'audio', 'kind':'mp3'},
                                    ],
                                },
                            ]
                        },
                    ],
                },
                'tag':{},
                'optimize':{},
                'transcode':{
                    'pivot':[
                        { 'operator':'this' },
                    ],
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
                                        {'stream kind':'video'},
                                    ],
                                    'override':{
                                        'handbrake parameters':{
                                            '--large-file':None,
                                            '--loose-anamorphic':None,
                                            '--quality':18,
                                            '--maxWidth':1280,
                                            '--encoder':'x264',
                                            '--x264-profile':'high',
                                            '--h264-level':'4.0',
                                            '--x264-preset':'slow',
                                        },
                                        'handbrake x264 settings':{
                                            'subme':9,
                                            'trellis':2,
                                        },
                                    },
                                },
                                {
                                    'description':'Copy all ac3 audio tracks',
                                    'mode':'select',
                                    'branch':[
                                        {'stream kind':'audio', 'kind':'ac3'},
                                    ],
                                    'override':{
                                        'handbrake audio encoder settings':{'--aencoder':'copy', '--ab':'auto', '--mixdown':'auto'}
                                    },
                                },
                                {
                                    'description':'Transcode all ac3 audio tracks to Dolby Pro Logic II aac',
                                    'mode':'select',
                                    'branch':[
                                        {'stream kind':'audio', 'kind':'ac3'},
                                    ],
                                    'override':{
                                        'handbrake audio encoder settings':{'--aencoder':'ca_aac', '--ab':160, '--mixdown':'dpl2'}
                                    },
                                },
                                {
                                    'description':'Transcode all Stereo aac or mp3 tracks to Stereo aac',
                                    'mode':'select',
                                    'branch':[
                                        {'stream kind':'audio', 'kind':'mp3', 'channels':2},
                                        {'stream kind':'audio', 'kind':'aac', 'channels':2},
                                    ],
                                    'override':{
                                        'handbrake audio encoder settings':{'--aencoder':'ca_aac', '--ab':128, '--mixdown':'stereo'}
                                    },
                                },
                                {
                                    'description':'Transcode all Mono aac or mp3 tracks to Mono aac',
                                    'mode':'select',
                                    'branch':[
                                        {'stream kind':'audio', 'kind':'mp3', 'channels':1},
                                        {'stream kind':'audio', 'kind':'aac', 'channels':1},
                                    ],
                                    'override':{
                                        'handbrake audio encoder settings':{'--aencoder':'ca_aac', '--ab':64, '--mixdown':'mono'},
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
                                        {'stream kind':'image'},
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
                                        {'stream kind':'audio', 'kind':'dts', 'channels':6},
                                    ],
                                    'override':{
                                        'ffmpeg parameters':{'-ab':u'640k', '-acodec':u'ac3', '-ac':6 },
                                    },
                                },
                                {
                                    'description':'Transcode 5 channels dts to ac3',
                                    'mode':'choose',
                                    'branch':[
                                        {'stream kind':'audio', 'kind':'dts', 'channels':5},
                                    ],
                                    'override':{
                                        'ffmpeg parameters':{'-ab':u'640k', '-acodec':u'ac3', '-ac':5 },
                                    },
                                },
                                {
                                    'description':'Transcode 4 channels dts to ac3',
                                    'mode':'choose',
                                    'branch':[
                                        {'stream kind':'audio', 'kind':'dts', 'channels':4},
                                    ],
                                    'override':{
                                        'ffmpeg parameters':{'-ab':u'448k', '-acodec':u'ac3', '-ac':4 },
                                    },
                                },
                                {
                                    'description':'Transcode 3 channels dts to ac3',
                                    'mode':'choose',
                                    'branch':[
                                        {'stream kind':'audio', 'kind':'dts', 'channels':3},
                                    ],
                                    'override':{
                                        'ffmpeg parameters':{'-ab':u'448k', '-acodec':u'ac3', '-ac':3 },
                                    },
                                },
                                {
                                    'description':'Transcode stereo dts to ac3',
                                    'mode':'choose',
                                    'branch':[
                                        {'stream kind':'audio', 'kind':'dts', 'channels':2},
                                    ],
                                    'override':{
                                        'ffmpeg parameters':{'-ab':u'256k', '-acodec':u'ac3', '-ac':2 },
                                    },
                                },
                                {
                                    'description':'Transcode mono dts to ac3',
                                    'mode':'choose',
                                    'branch':[
                                        {'stream kind':'audio', 'kind':'dts', 'channels':1},
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
                                        {'stream kind':'caption', 'language':'he'},
                                    ],
                                    'override':{
                                        'subtitle filters':['noise', 'hebrew noise', 'typo', 'punctuation', 'leftover']
                                    },
                                },
                                {
                                    'description':'English subtitles',
                                    'mode':'choose',
                                    'branch':[
                                        {'stream kind':'caption', 'language':'en'},
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
                                        {'stream kind':'menu'},
                                    ],
                                },
                            ]
                        },
                    ],
                },
                'update':{
                    'pivot':[
                        { 'operator':'select', 'constraint':{'kind':'srt'} },
                        { 'operator':'select', 'constraint':{'kind':'chpl'} },
                        { 'operator':'select', 'constraint':{'kind':'png'} },
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
                                        {'stream kind':'caption', 'language':'he'},
                                    ],
                                    'override':{'stream name':'Normal', 'height':0.132},
                                },
                                {
                                    'mode':'choose',
                                    'branch':[
                                        {'stream kind':'caption', 'language':'en'},
                                    ],
                                    'override':{'stream name':'Normal', 'height':0.132},
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
                                        {'stream kind':'caption'},
                                    ],
                                    'override':{'stream name':'Smart', 'height':0.148, 'language':'sv'},
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
                                        {'stream kind':'image'},
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
                                        {'stream kind':'menu'},
                                    ],
                                },
                            ],
                        },
                    ],
                },
            }
        },
    },
    'profile':{
        'normal':{},
        'clean':{},
        'original':{},
        'sd':{},
        '720':{},
        '1080':{},
        'iA4':{},
        'universal':{},
        'appletv':{},
        'high':{},
    },
}
