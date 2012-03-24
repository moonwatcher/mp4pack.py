# -*- coding: utf-8 -*-

import re

configuration = {
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
                                    {'stream kind':'caption', 'language':'he'},
                                ],
                                'override':{'name':'Normal'},
                            },
                            {
                                'mode':'choose',
                                'branch':[
                                    {'stream kind':'caption', 'language':'en'},
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
                                    {'stream kind':'caption'},
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
                                    {'stream kind':'caption'},
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
                                    {'stream kind':'video'},
                                    {'stream kind':'audio', 'kind':'ac3'},
                                    {'stream kind':'audio', 'kind':'aac'},
                                    {'stream kind':'audio', 'kind':'dts'},
                                    {'stream kind':'audio', 'kind':'mp3'},
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
                                    {'stream kind':'caption', 'language':'he'},
                                ],
                                'override':{'name':'Normal', 'height':0.132},
                            },
                            {
                                'mode':'choose',
                                'branch':[
                                    {'stream kind':'caption', 'language':'en'},
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
                                    {'stream kind':'caption'},
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
                                    {'stream kind':'video'},
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
                                    {'stream kind':'audio', 'kind':'ac3'},
                                ],
                                'override':{
                                    'encoder settings':{'--aencoder':'copy', '--ab':'auto', '--mixdown':'auto'}
                                },
                            },
                            {
                                'description':'Transcode all ac3 audio tracks to Dolby Pro Logic II aac',
                                'mode':'select',
                                'branch':[
                                    {'stream kind':'audio', 'kind':'ac3'},
                                ],
                                'override':{
                                    'encoder settings':{'--aencoder':'ca_aac', '--ab':160, '--mixdown':'dpl2'}
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
                                    'encoder settings':{'--aencoder':'ca_aac', '--ab':128, '--mixdown':'stereo'}
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
            }
        },
    },
    'system':{
        'home':u'/usr/local/etc/mpk',
        'domain':None,
        'host':None,
        'threads':2,
        'language':'en',
    },
    'archetype':{
        'character encoding':{
            'name':u'Character encoding',
            'keyword':u'character_encoding',
            'type':'unicode',
        },
        'url':{
            'name':u'URL',
            'keyword':u'url',
            'type':'unicode',
        },
        'scheme':{
            'name':u'Scheme',
            'keyword':u'scheme',
            'type':'unicode',
        },
        'host':{
            'name':u'Host',
            'keyword':u'host',
            'type':'unicode',
        },
        'port':{
            'name':u'Port',
            'keyword':u'port',
            'type':'int',
        },
        'path':{
            'name':u'Path',
            'keyword':u'path',
            'type':'unicode',
        },
        'directory':{
            'name':u'Directory',
            'keyword':u'directory',
            'type':'unicode',
        },
        'file name':{
            'name':u'File name',
            'keyword':u'file_name',
            'type':'unicode',
        },
        'cache root':{
            'name':u'Cache root',
            'keyword':u'cache_root',
            'type':'unicode',
        },
        'path in cache':{
            'name':u'Path in cache',
            'keyword':u'path_in_cache',
            'type':'unicode',
        },
        'file size':{
            'name':u'File size',
            'keyword':u'file_size',
            'type':'int',
            'format':'byte',
        },
        'profile':{
            'name':u'Profile',
            'keyword':u'profile',
            'type':'unicode'
        },
        'volume':{
            'name':u'Volume',
            'keyword':u'volume',
            'type':'unicode'
        },
        'volume path':{
            'name':u'Volume path',
            'keyword':u'volume_path',
            'type':'unicode'
        },
        'kind':{
            'name':u'Kind',
            'keyword':u'kind',
            'type':'unicode',
        },
        'simple name':{
            'name':u'Simple name',
            'keyword':u'simple_name',
            'type':'unicode',
            'simplify':True,
        },
        'simple album':{
            'name':u'Simple album',
            'keyword':u'simple_album',
            'type':'unicode',
            'simplify':True,
        },
        'simple tv show':{
            'name':u'Simple TV show',
            'keyword':u'simple_tv_show',
            'type':'unicode',
            'simplify':True,
        },
        'tvdb tv show id':{
            'name':u'TVDb TV Show ID',
            'keyword':u'tvdb_tv_show_id',
            'type':'int',
        },
        'tvdb tv season id':{
            'name':u'TVDb TV Season ID',
            'keyword':u'tvdb_tv_season_id',
            'type':'int',
        },
        'tvdb tv episode id':{
            'name':u'TVDb TV Episode ID',
            'keyword':u'tvdb_tv_episode_id',
            'type':'int',
        },
        'tvdb person id':{
            'name':u'TVDb Person ID',
            'keyword':u'tvdb_person_id',
            'type':'int',
        },
        'tvdb poster id':{
            'name':u'TVDb Poster ID',
            'keyword':u'tvdb_poster_id',
            'type':'int',
        },
        'imdb tv show id':{
            'name':u'IMDb TV Show ID',
            'keyword':u'imdb_tv_show_id',
            'type':'unicode',
        },
        'imdb tv episode id':{
            'name':u'IMDb TV Episode ID',
            'keyword':u'imdb_tv_episode_id',
            'type':'unicode',
        },
        'imdb movie id':{
            'name':u'IMDb Movie ID',
            'keyword':u'imdb_movie_id',
            'type':'unicode'
        },
        'tmdb movie id':{
            'name':u'TMDb Movie ID',
            'keyword':u'tmdb_movie_id',
            'type':'int',
        },
        'tmdb person id':{
            'name':u'TMDb Person ID',
            'keyword':u'tmdb_person_id',
            'type':'int',
        },
        'zap2it tv show id':{
            'name':u'Zap2It TV Show ID',
            'keyword':u'zap2it_tv_show_id',
            'type':'unicode',
        },
        'keywords':{
            'name':u'Keywords',
            'keyword':u'keywords',
            'type':'unicode',
            'plural':'list',
        },
        'tv show runtime':{
            'name':u'TV Show Runtime',
            'keyword':u'tv_show_runtime',
            'type':'int',
        },
        'tv show status':{
            'name':u'TV Show Status',
            'keyword':u'tv_show_status',
            'type':'unicode',
        },
        'user rating':{
            'name':u'User Rating',
            'keyword':u'user_rating',
            'type':'float',
        },
        'user rating count':{
            'name':u'User Rating Count',
            'keyword':u'user_rating_count',
            'type':'int',
        },
        'language':{
            'name':u'Language',
            'keyword':u'language',
            'type':'enum',
            'enumeration':'language',
        },
        'media kind':{
            'name':u'Media Kind',
            'keyword':u'media_kind',
            'type':'enum',
            'atom':'stik',
            'enumeration':'media kind',
        },
        'name':{
            'name':u'Name',
            'keyword':u'name',
            'type':'unicode',
            'atom':'©nam',
        },
        'artist':{
            'name':u'Artist',
            'keyword':u'artist',
            'type':'unicode',
            'atom':'@ART',
        },
        'composer':{
            'name':u'Composer',
            'keyword':u'composer',
            'type':'unicode',
            'atom':'©wrt',
        },
        'album artist':{
            'name':u'Album Artist',
            'keyword':u'album_artist',
            'type':'unicode',
            'atom':'aART',
        },
        'album':{
            'name':u'Album',
            'keyword':u'album',
            'type':'unicode',
            'atom':'©alb',
        },
        'track number':{
            'name':u'Track',
            'keyword':u'track_number',
            'type':'unicode',
            'atom':'trkn',
        },
        'disk number':{
            'name':u'Disk',
            'keyword':u'disk_number',
            'type':'unicode',
            'atom':'disk',
        },
        'track position':{
            'name':u'Track Position',
            'keyword':u'track_position',
            'type':'int',
            'atom':'trkn',
        },
        'track total':{
            'name':u'Track Total',
            'keyword':u'track_total',
            'type':'int',
            'atom':'trkn',
        },
        'disk position':{
            'name':u'Disk Position',
            'keyword':u'disk_position',
            'type':'int',
            'atom':'disk',
        },
        'disk total':{
            'name':u'Disk Total',
            'keyword':u'disk_total',
            'type':'int',
            'atom':'disk',
        },
        'grouping':{
            'name':u'Grouping',
            'keyword':u'grouping',
            'type':'unicode',
            'atom':'©grp',
        },
        'comment':{
            'name':u'Comment',
            'keyword':u'comment',
            'type':'unicode',
            'atom':'©cmt',
        },
        'description':{
            'name':u'Description',
            'keyword':u'description',
            'type':'unicode',
            'atom':'desc',
        },
        'long description':{
            'name':u'Long Description',
            'keyword':u'long_description',
            'type':'unicode',
            'atom':'ldes',
        },
        'lyrics':{
            'name':u'Lyrics',
            'keyword':u'lyrics',
            'type':'unicode',
            'atom':'©lyr',
        },
        'compilation':{
            'name':u'Compilation',
            'keyword':u'compilation',
            'type':'bool',
            'atom':'cpil',
        },
        'copyright':{
            'name':u'Copyright',
            'keyword':u'copyright',
            'type':'unicode',
            'atom':'cprt',
        },
        'tempo':{
            'name':u'Tempo',
            'keyword':u'tempo',
            'type':'int',
            'atom':'tmpo',
        },
        'genre type':{
            'name':u'Genre Type',
            'keyword':u'genre_type',
            'type':'enum',
            'atom':'gnre',
            'enumeration':'genre',
        },
        'genre':{
            'name':u'Genre',
            'keyword':u'genre',
            'type':'unicode',
            'atom':'©gen',
        },
        'gapless':{
            'name':u'Gapless',
            'keyword':u'gapless',
            'type':'bool',
            'atom':'pgap',
        },
        'itunes keywords':{
            'name':u'iTunes Keywords',
            'keyword':u'itunes_keywords',
            'type':'unicode',
            'atom':'keyw',
        },
        'itunes category':{
            'name':u'iTunes Category',
            'keyword':u'itunes_category',
            'type':'unicode',
            'atom':'catg',
        },
        'hd video':{
            'name':u'HD Video',
            'keyword':u'hd_video',
            'type':'bool',
            'atom':'hdvd',
        },
        'tv show':{
            'name':u'TV Show',
            'keyword':u'tv_show',
            'type':'unicode',
            'atom':'tvsh',
        },
        'track genealogy':{
            'name':u'Track genealogy',
            'keyword':u'track_genealogy',
            'type':'unicode',
        },
        'tv episode id':{
            'name':u'TV Episode ID',
            'keyword':u'tv_episode_id',
            'type':'unicode',
            'atom':'tven',
        },
        'tv season':{
            'name':u'TV Season',
            'keyword':u'tv_season',
            'type':'int',
            'atom':'tvsn',
        },
        'tv episode':{
            'name':u'TV Episode',
            'keyword':u'tv_episode',
            'type':'int',
            'atom':'tves',
        },
        'absolute tv episode':{
            'name':u'Absolute TV Episode',
            'keyword':'absolute_tv_episode',
            'type':'int',
        },
        'tv network':{
            'name':u'TV Network',
            'keyword':u'tv_network',
            'type':'unicode',
            'atom':'tvnn',
        },
        'sort name':{
            'name':u'Sort Name',
            'keyword':u'sort_name',
            'type':'unicode',
            'atom':'sonm',
        },
        'sort artist':{
            'name':u'Sort Artist',
            'keyword':u'sort_artist',
            'type':'unicode',
            'atom':'soar',
        },
        'sort composer':{
            'name':u'Sort Composer',
            'keyword':u'sort_composer',
            'type':'unicode',
            'atom':'soco',
        },
        'sort album artist':{
            'name':u'Sort Album Artist',
            'keyword':u'sort_album_artist',
            'type':'unicode',
            'atom':'soaa',
        },
        'sort album':{
            'name':u'Sort Album',
            'keyword':u'sort_album',
            'type':'unicode',
            'atom':'soal',
        },
        'sort tv show':{
            'name':u'Sort TV Show',
            'keyword':u'sort_tv_show',
            'type':'unicode',
            'atom':'sosn',
        },
        'encoding tool':{
            # mediainfo seems to mix @enc and @too into Encoded_Application
            'name':u'Encoding Tool',
            'keyword':u'encoding_tool',
            'type':'unicode',
            'atom':'©too',
        },
        'encoded by':{
            # mediainfo seems to mix @enc and @too into Encoded_Application
            'name':u'Encoded by',
            'keyword':u'encoded_by',
            'type':'unicode',
            'atom':'@enc',
        },
        'modified date':{
            'name':u'Modified Date',
            'keyword':u'modified_date',
            'type':'date',
        },
        'tag date':{
            'name':u'Tag Date',
            'keyword':u'tag_date',
            'type':'date',
        },
        'release date':{
            'name':u'Release Date',
            'keyword':u'release_date',
            'type':'date',
            'atom':'©day',
        },
        'purchase date':{
            'name':u'Purchase Date',
            'keyword':u'purchase_date',
            'type':'date',
            'atom':'purd',
        },
        'encoded date':{
            'name':u'Encoded Date',
            'keyword':u'encoded_date',
            'type':'date',
        },
        'xid':{
            'name':u'iTunes Extra ID',
            'keyword':u'xid',
            'type':'unicode',
            'atom':'xid',
        },
        'itunes content id':{
            'name':u'iTunes content ID',
            'keyword':u'itunes_content_id',
            'type':'int',
            'atom':'cnID',
        },
        'itunes account':{
            'name':u'iTunes account ID',
            'keyword':u'itunes_account_id',
            'type':'unicode',
            'atom':'apID',
        },
        'itunes artist id':{
            'name':u'iTunes artist ID',
            'keyword':u'itunes_artist_id',
            'type':'int',
            'atom':'atID',
        },
        'itunes composer id':{
            'name':u'iTunes composer ID',
            'keyword':u'itunes_composer_id',
            'type':'int',
            'atom':'cmID',
        },
        'itunes playlist id':{
            'name':u'iTunes playlist ID',
            'keyword':u'itunes_playlist_id',
            'type':'int',
            'atom':'plID',
        },
        'itunes genre id':{
            'name':u'iTunes genre ID',
            'keyword':u'itunes_genre_id',
            'type':'int',
            'atom':'geID',
        },
        'itunes country id':{
            'name':u'iTunes country ID',
            'keyword':u'itunes_country_id',
            'type':'enum',
            'atom':'sfID',
            'enumeration':'country',
        },
        'itunes account type':{
            'name':u'iTunes account type',
            'keyword':u'itunes_account_type',
            'type':'enum',
            'atom':'akID',
            'enumeration':'itunes account type',
        },
        'itunes episode global id':{
            'name':u'Episode Global ID',
            'keyword':u'episode_global_id',
            'type':'int',
            'atom':'egid',
        },
        'podcast':{
            'name':u'Podcast',
            'keyword':u'podcast',
            'type':'bool',
            'atom':'pcst',
        },
        'podcast url':{
            'name':u'Podcast URL',
            'keyword':u'podcast_url',
            'type':'unicode',
            'atom':'purl',
        },
        'content rating':{
            'name':u'Content Rating',
            'keyword':u'content_rating',
            'type':'enum',
            'atom':'rtng',
            'enumeration':'content rating',
        },
        'itunextc':{
            'name':u'iTunEXTC',
            'keyword':u'itunextc',
            'type':'unicode',
            'atom':'iTunEXTC',
        },
        'itunmovi':{
            'name':u'iTunMOVI',
            'keyword':u'itunmovi',
            'type':'plist',
            'atom':'iTunMOVI',
        },
        'cast':{
            'name':u'Cast',
            'type':'unicode',
            'keyword':u'cast',
            'atom':'iTunMOVI',
            'plural':'list',
        },
        'directors':{
            'name':u'Directors',
            'keyword':u'directors',
            'type':'unicode',
            'atom':'iTunMOVI',
            'plural':'list',
        },
        'codirectors':{
            'name':u'Codirectors',
            'keyword':u'codirectors',
            'type':'unicode',
            'atom':'iTunMOVI',
            'plural':'list',
        },
        'producers':{
            'name':u'Producers',
            'keyword':u'producers',
            'type':'unicode',
            'atom':'iTunMOVI',
            'plural':'list',
        },
        'screenwriters':{
            'name':u'Screenwriters',
            'keyword':u'screenwriters',
            'type':'unicode',
            'atom':'iTunMOVI',
            'plural':'list',
        },
        'studio':{
            'name':u'Studio',
            'keyword':u'studio',
            'type':'unicode',
            'atom':'iTunMOVI',
            'plural':'list',
        },
        'rating standard':{
            'name':u'Rating Standard',
            'keyword':u'rating_standard',
            'type':'unicode',
            'atom':'iTunEXTC',
        },
        'rating':{
            'name':u'Rating',
            'keyword':u'rating',
            'type':'unicode',
            'atom':'iTunEXTC',
        },
        'rating score':{
            'name':u'Rating Score',
            'keyword':u'rating_score',
            'type':'int',
            'atom':'iTunEXTC',
        },
        'rating annotation':{
            'name':u'Rating Annotation',
            'keyword':u'rating_annotation',
            'type':'unicode',
            'atom':'iTunEXTC',
        },
        'cover':{
            'name':u'Cover Pieces',
            'keyword':u'cover_pieces',
            'type':'int',
            'atom':'covr',
            'auto cast':False,
        },
        'stream name':{
            'name':u'Stream Name',
            'keyword':u'stream_name',
            'type':'unicode',
        },
        'stream type':{
            'name':u'Stream Type',
            'keyword':u'stream_type',
            'type':'enum',
            'enumeration':'mediainfo stream type',
        },
        'stream kind':{
            'name':u'Stream Kind',
            'keyword':u'stream_kind',
            'type':'enum',
            'enumeration':'stream kind',
        },
        'format':{
            'name':u'Format',
            'keyword':u'format',
            'type':'unicode',
        },
        'format profile':{
            'name':u'Format Profile',
            'type':'unicode',
            'plural':'list',
        },
        'channel count':{
            'name':u'Channel count',
            'keyword':u'channel_count',
            'type':'int',
            'plural':'list',
        },
        'channel position':{
            'name':u'Channel Position',
            'keyword':u'channel_position',
            'type':'unicode',
            'plural':'list',
        },
        'stream id':{
            'name':u'Stream ID',
            'keyword':u'stream_id',
            'type':'int',
        },
        'stream position':{
            'name':u'Stream Position',
            'keyword':u'stream_position',
            'type':'int',
        },
        'stream size':{
            'name':u'Stream Size',
            'keyword':u'stream_size',
            'type':'int',
            'format':'byte',
        },
        'stream portion':{
            'name':u'Stream portion',
            'keyword':u'stream_portion',
            'type':'float',
        },
        'default':{
            'name':u'Default',
            'keyword':u'default',
            'type':'bool',
        },
        'primary':{
            'name':u'Primary',
            'keyword':u'primary',
            'type':'bool',
        },
        'delay':{
            'name':u'Delay',
            'keyword':u'delay',
            'type':'int',
        },
        'bit rate':{
            'name':u'Bit Rate',
            'keyword':u'bit_rate',
            'type':'int',
            'format':'bitrate',
        },
        'bit rate mode':{
            'name':u'Bit Rate Mode',
            'keyword':u'bit_rate_mode',
            'type':'unicode',
        },
        'bit depth':{
            'name':u'Bit Depth',
            'keyword':u'bit_depth',
            'type':'int',
            'format':'bit',
        },
        'sample rate':{
            'name':u'Sample Rate',
            'keyword':u'sample_rate',
            'type':'int',
            'format':'frequency',
        },
        'sample count':{
            'name':u'Sample Count',
            'keyword':u'sample_count',
            'type':'int',
        },
        'frame rate':{
            'name':u'Frame Rate',
            'keyword':u'frame_rate',
            'type':'float',
            'format':'framerate',
        },
        'frame rate mode':{
            'name':u'Frame Rate Mode',
            'keyword':u'frame_rate_mode',
            'type':'unicode',
        },
        'frame rate minimum':{
            'name':u'Frame Rate Minimum',
            'keyword':u'frame_rate_minimum',
            'type':'float',
            'format':'framerate',
        },
        'frame rate maximum':{
            'name':u'Frame Rate Maximum',
            'keyword':u'frame_rate_maximum',
            'type':'float',
            'format':'framerate',
        },
        'frame count':{
            'name':u'Frame Count',
            'keyword':u'frame_count',
            'type':'int',
        },
        'duration':{
            'name':u'Duration',
            'keyword':u'duration',
            'type':'int',
            'format':'millisecond',
        },
        'width':{
            'name':u'Width',
            'keyword':u'width',
            'type':'int',
            'format':'pixel',
        },
        'height':{
            'name':u'Height',
            'keyword':u'height',
            'type':'int',
            'format':'pixel',
        },
        'pixel aspect ratio':{
            'name':u'Pixel Aspect Ratio',
            'keyword':u'pixel_aspect_ratio',
            'type':'float',
        },
        'display aspect ratio':{
            'name':u'Display Aspect Ratio',
            'keyword':u'display_aspect_ratio',
            'type':'float',
        },
        'color space':{
            'name':u'Color Space',
            'keyword':u'color_space',
            'type':'unicode',
        },
        'channels':{
            'name':u'Channels',
            'keyword':u'channels',
            'type':'int',
        },
        'dialnorm':{
            'name':u'Dialnorm',
            'keyword':u'dialnorm',
            'type':'int',
        },
        'bpf':{
            'name':u'Bits / Pixel * Frame',
            'keyword':u'bpf',
            'type':'float',
        },
        'encoder':{
            'name':u'Encoder',
            'keyword':u'encoder',
            'type':'unicode',
        },
        'encoder settings':{
            'name':u'Encoder Settings',
            'keyword':u'encoder_settings',
            'type':'unicode',
            'plural':'dict',
        },
        'character':{
            'name':u'Character',
            'keyword':u'character',
            'type':'unicode',
        },
        'poster url':{
            'name':u'Poster URL',
            'keyword':u'poster_url',
            'type':'unicode',
        },
    },
    'enumeration':{
        'frame rate':{
            'synonym':['short', 'long'],
            'element':{
                0:{ 'short':'f',    'long':'film',  'name':u'FILM 24',                  'float':24.0, },
                1:{ 'short':'n',    'long':'ntsc',  'name':u'NTSC FILM 23.976',         'float':24.0*1000.0/1001.0, },
                2:{ 'short':'p',    'long':'pal',   'name':u'PAL 25',                   'float':25.0, },
                3:{ 'short':'t',    'long':'tv',    'name':u'NTSC Television 29.97',    'float':30.0*1000.0/1001.0, }
            },
        },
        'decimal si':{
            'element':{
                0:{ 'name':u'bit',   'base':10,  'exponent':0 },
                1:{ 'name':u'Kbit',  'base':10,  'exponent':3 },
                2:{ 'name':u'Mbit',  'base':10,  'exponent':6 },
                3:{ 'name':u'Gbit',  'base':10,  'exponent':9 },
                4:{ 'name':u'Tbit',  'base':10,  'exponent':12 },
            },
        },
        'binary iec 60027 2':{
            'element':{
                0:{ 'name':u'Byte',  'base':2,   'exponent':0 },
                1:{ 'name':u'KiB',   'base':2,   'exponent':10 },
                2:{ 'name':u'MiB',   'base':2,   'exponent':20 },
                3:{ 'name':u'GiB',   'base':2,   'exponent':30 },
                4:{ 'name':u'TiB',   'base':2,   'exponent':40 },
            },
        },
        'itunmovi':{
            'synonym':['plist'],
            'element':{
                'cast':{            'name':u'Cast',          'plist':'cast' },
                'directors':{       'name':u'Directors',     'plist':'directors' },
                'codirectors':{     'name':u'Codirectors',   'plist':'codirectors' },
                'producers':{       'name':u'Producers',     'plist':'producers' },
                'screenwriters':{   'name':u'Screenwriters', 'plist':'screenwriters' },
                'studio':{          'name':u'Studio',        'plist':'studio' },
            },
        },
        'language':{
            'synonym':['ISO 639-1', 'ISO 639-2/T', 'ISO 639-2/B'],
            'element':{
                'un':{  'ISO 639-1':None,   'ISO 639-2/T':None,     'ISO 639-2/B':None,     'name':u'Unknown' },
                'aa':{  'ISO 639-1':'aa',   'ISO 639-2/T':'aar',    'ISO 639-2/B':'aar',    'name':u'Afar' },
                'ab':{  'ISO 639-1':'ab',   'ISO 639-2/T':'abk',    'ISO 639-2/B':'abk',    'name':u'Abkhazian' },
                'af':{  'ISO 639-1':'af',   'ISO 639-2/T':'afr',    'ISO 639-2/B':'afr',    'name':u'Afrikaans' },
                'ak':{  'ISO 639-1':'ak',   'ISO 639-2/T':'aka',    'ISO 639-2/B':'aka',    'name':u'Akan' },
                'sq':{  'ISO 639-1':'sq',   'ISO 639-2/T':'sqi',    'ISO 639-2/B':'alb',    'name':u'Albanian' },
                'am':{  'ISO 639-1':'am',   'ISO 639-2/T':'amh',    'ISO 639-2/B':'amh',    'name':u'Amharic' },
                'ar':{  'ISO 639-1':'ar',   'ISO 639-2/T':'ara',    'ISO 639-2/B':'ara',    'name':u'Arabic' },
                'an':{  'ISO 639-1':'an',   'ISO 639-2/T':'arg',    'ISO 639-2/B':'arg',    'name':u'Aragonese' },
                'hy':{  'ISO 639-1':'hy',   'ISO 639-2/T':'hye',    'ISO 639-2/B':'arm',    'name':u'Armenian' },
                'as':{  'ISO 639-1':'as',   'ISO 639-2/T':'asm',    'ISO 639-2/B':'asm',    'name':u'Assamese' },
                'av':{  'ISO 639-1':'av',   'ISO 639-2/T':'ava',    'ISO 639-2/B':'ava',    'name':u'Avaric' },
                'ae':{  'ISO 639-1':'ae',   'ISO 639-2/T':'ave',    'ISO 639-2/B':'ave',    'name':u'Avestan' },
                'ay':{  'ISO 639-1':'ay',   'ISO 639-2/T':'aym',    'ISO 639-2/B':'aym',    'name':u'Aymara' },
                'az':{  'ISO 639-1':'az',   'ISO 639-2/T':'aze',    'ISO 639-2/B':'aze',    'name':u'Azerbaijani' },
                'ba':{  'ISO 639-1':'ba',   'ISO 639-2/T':'bak',    'ISO 639-2/B':'bak',    'name':u'Bashkir' },
                'bm':{  'ISO 639-1':'bm',   'ISO 639-2/T':'bam',    'ISO 639-2/B':'bam',    'name':u'Bambara' },
                'eu':{  'ISO 639-1':'eu',   'ISO 639-2/T':'eus',    'ISO 639-2/B':'baq',    'name':u'Basque' },
                'be':{  'ISO 639-1':'be',   'ISO 639-2/T':'bel',    'ISO 639-2/B':'bel',    'name':u'Belarusian' },
                'bn':{  'ISO 639-1':'bn',   'ISO 639-2/T':'ben',    'ISO 639-2/B':'ben',    'name':u'Bengali' },
                'bh':{  'ISO 639-1':'bh',   'ISO 639-2/T':'bih',    'ISO 639-2/B':'bih',    'name':u'Bihari' },
                'bi':{  'ISO 639-1':'bi',   'ISO 639-2/T':'bis',    'ISO 639-2/B':'bis',    'name':u'Bislama' },
                'bs':{  'ISO 639-1':'bs',   'ISO 639-2/T':'bos',    'ISO 639-2/B':'bos',    'name':u'Bosnian' },
                'br':{  'ISO 639-1':'br',   'ISO 639-2/T':'bre',    'ISO 639-2/B':'bre',    'name':u'Breton' },
                'bg':{  'ISO 639-1':'bg',   'ISO 639-2/T':'bul',    'ISO 639-2/B':'bul',    'name':u'Bulgarian' },
                'my':{  'ISO 639-1':'my',   'ISO 639-2/T':'mya',    'ISO 639-2/B':'bur',    'name':u'Burmese' },
                'ca':{  'ISO 639-1':'ca',   'ISO 639-2/T':'cat',    'ISO 639-2/B':'cat',    'name':u'Catalan' },
                'ch':{  'ISO 639-1':'ch',   'ISO 639-2/T':'cha',    'ISO 639-2/B':'cha',    'name':u'Chamorro' },
                'ce':{  'ISO 639-1':'ce',   'ISO 639-2/T':'che',    'ISO 639-2/B':'che',    'name':u'Chechen' },
                'zh':{  'ISO 639-1':'zh',   'ISO 639-2/T':'zho',    'ISO 639-2/B':'chi',    'name':u'Chinese' },
                'cu':{  'ISO 639-1':'cu',   'ISO 639-2/T':'chu',    'ISO 639-2/B':'chu',    'name':u'Church Slavic' },
                'cv':{  'ISO 639-1':'cv',   'ISO 639-2/T':'chv',    'ISO 639-2/B':'chv',    'name':u'Chuvash' },
                'kw':{  'ISO 639-1':'kw',   'ISO 639-2/T':'cor',    'ISO 639-2/B':'cor',    'name':u'Cornish' },
                'co':{  'ISO 639-1':'co',   'ISO 639-2/T':'cos',    'ISO 639-2/B':'cos',    'name':u'Corsican' },
                'cr':{  'ISO 639-1':'cr',   'ISO 639-2/T':'cre',    'ISO 639-2/B':'cre',    'name':u'Cree' },
                'cs':{  'ISO 639-1':'cs',   'ISO 639-2/T':'ces',    'ISO 639-2/B':'cze',    'name':u'Czech' },
                'da':{  'ISO 639-1':'da',   'ISO 639-2/T':'dan',    'ISO 639-2/B':'dan',    'name':u'Danish' },
                'dv':{  'ISO 639-1':'dv',   'ISO 639-2/T':'div',    'ISO 639-2/B':'div',    'name':u'Divehi' },
                'nl':{  'ISO 639-1':'nl',   'ISO 639-2/T':'nld',    'ISO 639-2/B':'dut',    'name':u'Dutch' },
                'dz':{  'ISO 639-1':'dz',   'ISO 639-2/T':'dzo',    'ISO 639-2/B':'dzo',    'name':u'Dzongkha' },
                'en':{  'ISO 639-1':'en',   'ISO 639-2/T':'eng',    'ISO 639-2/B':'eng',    'name':u'English' },
                'eo':{  'ISO 639-1':'eo',   'ISO 639-2/T':'epo',    'ISO 639-2/B':'epo',    'name':u'Esperanto' },
                'et':{  'ISO 639-1':'et',   'ISO 639-2/T':'est',    'ISO 639-2/B':'est',    'name':u'Estonian' },
                'ee':{  'ISO 639-1':'ee',   'ISO 639-2/T':'ewe',    'ISO 639-2/B':'ewe',    'name':u'Ewe' },
                'fo':{  'ISO 639-1':'fo',   'ISO 639-2/T':'fao',    'ISO 639-2/B':'fao',    'name':u'Faroese' },
                'fj':{  'ISO 639-1':'fj',   'ISO 639-2/T':'fij',    'ISO 639-2/B':'fij',    'name':u'Fijian' },
                'fi':{  'ISO 639-1':'fi',   'ISO 639-2/T':'fin',    'ISO 639-2/B':'fin',    'name':u'Finnish' },
                'fr':{  'ISO 639-1':'fr',   'ISO 639-2/T':'fra',    'ISO 639-2/B':'fre',    'name':u'French' },
                'fy':{  'ISO 639-1':'fy',   'ISO 639-2/T':'fry',    'ISO 639-2/B':'fry',    'name':u'Western Frisian' },
                'ff':{  'ISO 639-1':'ff',   'ISO 639-2/T':'ful',    'ISO 639-2/B':'ful',    'name':u'Fulah' },
                'ka':{  'ISO 639-1':'ka',   'ISO 639-2/T':'kat',    'ISO 639-2/B':'geo',    'name':u'Georgian' },
                'de':{  'ISO 639-1':'de',   'ISO 639-2/T':'deu',    'ISO 639-2/B':'ger',    'name':u'German' },
                'gd':{  'ISO 639-1':'gd',   'ISO 639-2/T':'gla',    'ISO 639-2/B':'gla',    'name':u'Gaelic' },
                'ga':{  'ISO 639-1':'ga',   'ISO 639-2/T':'gle',    'ISO 639-2/B':'gle',    'name':u'Irish' },
                'gl':{  'ISO 639-1':'gl',   'ISO 639-2/T':'glg',    'ISO 639-2/B':'glg',    'name':u'Galician' },
                'gv':{  'ISO 639-1':'gv',   'ISO 639-2/T':'glv',    'ISO 639-2/B':'glv',    'name':u'Manx' },
                'el':{  'ISO 639-1':'el',   'ISO 639-2/T':'ell',    'ISO 639-2/B':'gre',    'name':u'Modern Greek' },
                'gn':{  'ISO 639-1':'gn',   'ISO 639-2/T':'grn',    'ISO 639-2/B':'grn',    'name':u'Guarani' },
                'gu':{  'ISO 639-1':'gu',   'ISO 639-2/T':'guj',    'ISO 639-2/B':'guj',    'name':u'Gujarati' },
                'ht':{  'ISO 639-1':'ht',   'ISO 639-2/T':'hat',    'ISO 639-2/B':'hat',    'name':u'Haitian' },
                'ha':{  'ISO 639-1':'ha',   'ISO 639-2/T':'hau',    'ISO 639-2/B':'hau',    'name':u'Hausa' },
                'he':{  'ISO 639-1':'he',   'ISO 639-2/T':'heb',    'ISO 639-2/B':'heb',    'name':u'Hebrew' },
                'hz':{  'ISO 639-1':'hz',   'ISO 639-2/T':'her',    'ISO 639-2/B':'her',    'name':u'Herero' },
                'hi':{  'ISO 639-1':'hi',   'ISO 639-2/T':'hin',    'ISO 639-2/B':'hin',    'name':u'Hindi' },
                'ho':{  'ISO 639-1':'ho',   'ISO 639-2/T':'hmo',    'ISO 639-2/B':'hmo',    'name':u'Hiri Motu' },
                'hu':{  'ISO 639-1':'hu',   'ISO 639-2/T':'hun',    'ISO 639-2/B':'hun',    'name':u'Hungarian' },
                'ig':{  'ISO 639-1':'ig',   'ISO 639-2/T':'ibo',    'ISO 639-2/B':'ibo',    'name':u'Igbo' },
                'is':{  'ISO 639-1':'is',   'ISO 639-2/T':'isl',    'ISO 639-2/B':'ice',    'name':u'Icelandic' },
                'io':{  'ISO 639-1':'io',   'ISO 639-2/T':'ido',    'ISO 639-2/B':'ido',    'name':u'Ido' },
                'ii':{  'ISO 639-1':'ii',   'ISO 639-2/T':'iii',    'ISO 639-2/B':'iii',    'name':u'Sichuan Yi' },
                'iu':{  'ISO 639-1':'iu',   'ISO 639-2/T':'iku',    'ISO 639-2/B':'iku',    'name':u'Inuktitut' },
                'ie':{  'ISO 639-1':'ie',   'ISO 639-2/T':'ile',    'ISO 639-2/B':'ile',    'name':u'Interlingue' },
                'ia':{  'ISO 639-1':'ia',   'ISO 639-2/T':'ina',    'ISO 639-2/B':'ina',    'name':u'Interlingua' },
                'id':{  'ISO 639-1':'id',   'ISO 639-2/T':'ind',    'ISO 639-2/B':'ind',    'name':u'Indonesian' },
                'ik':{  'ISO 639-1':'ik',   'ISO 639-2/T':'ipk',    'ISO 639-2/B':'ipk',    'name':u'Inupiaq' },
                'it':{  'ISO 639-1':'it',   'ISO 639-2/T':'ita',    'ISO 639-2/B':'ita',    'name':u'Italian' },
                'jv':{  'ISO 639-1':'jv',   'ISO 639-2/T':'jav',    'ISO 639-2/B':'jav',    'name':u'Javanese' },
                'ja':{  'ISO 639-1':'ja',   'ISO 639-2/T':'jpn',    'ISO 639-2/B':'jpn',    'name':u'Japanese' },
                'kl':{  'ISO 639-1':'kl',   'ISO 639-2/T':'kal',    'ISO 639-2/B':'kal',    'name':u'Kalaallisut' },
                'kn':{  'ISO 639-1':'kn',   'ISO 639-2/T':'kan',    'ISO 639-2/B':'kan',    'name':u'Kannada' },
                'ks':{  'ISO 639-1':'ks',   'ISO 639-2/T':'kas',    'ISO 639-2/B':'kas',    'name':u'Kashmiri' },
                'kr':{  'ISO 639-1':'kr',   'ISO 639-2/T':'kau',    'ISO 639-2/B':'kau',    'name':u'Kanuri' },
                'kk':{  'ISO 639-1':'kk',   'ISO 639-2/T':'kaz',    'ISO 639-2/B':'kaz',    'name':u'Kazakh' },
                'km':{  'ISO 639-1':'km',   'ISO 639-2/T':'khm',    'ISO 639-2/B':'khm',    'name':u'Central Khmer' },
                'ki':{  'ISO 639-1':'ki',   'ISO 639-2/T':'kik',    'ISO 639-2/B':'kik',    'name':u'Kikuyu' },
                'rw':{  'ISO 639-1':'rw',   'ISO 639-2/T':'kin',    'ISO 639-2/B':'kin',    'name':u'Kinyarwanda' },
                'ky':{  'ISO 639-1':'ky',   'ISO 639-2/T':'kir',    'ISO 639-2/B':'kir',    'name':u'Kirghiz' },
                'kv':{  'ISO 639-1':'kv',   'ISO 639-2/T':'kom',    'ISO 639-2/B':'kom',    'name':u'Komi' },
                'kg':{  'ISO 639-1':'kg',   'ISO 639-2/T':'kon',    'ISO 639-2/B':'kon',    'name':u'Kongo' },
                'ko':{  'ISO 639-1':'ko',   'ISO 639-2/T':'kor',    'ISO 639-2/B':'kor',    'name':u'Korean' },
                'kj':{  'ISO 639-1':'kj',   'ISO 639-2/T':'kua',    'ISO 639-2/B':'kua',    'name':u'Kuanyama' },
                'ku':{  'ISO 639-1':'ku',   'ISO 639-2/T':'kur',    'ISO 639-2/B':'kur',    'name':u'Kurdish' },
                'lo':{  'ISO 639-1':'lo',   'ISO 639-2/T':'lao',    'ISO 639-2/B':'lao',    'name':u'Lao' },
                'la':{  'ISO 639-1':'la',   'ISO 639-2/T':'lat',    'ISO 639-2/B':'lat',    'name':u'Latin' },
                'lv':{  'ISO 639-1':'lv',   'ISO 639-2/T':'lav',    'ISO 639-2/B':'lav',    'name':u'Latvian' },
                'li':{  'ISO 639-1':'li',   'ISO 639-2/T':'lim',    'ISO 639-2/B':'lim',    'name':u'Limburgan' },
                'ln':{  'ISO 639-1':'ln',   'ISO 639-2/T':'lin',    'ISO 639-2/B':'lin',    'name':u'Lingala' },
                'lt':{  'ISO 639-1':'lt',   'ISO 639-2/T':'lit',    'ISO 639-2/B':'lit',    'name':u'Lithuanian' },
                'lb':{  'ISO 639-1':'lb',   'ISO 639-2/T':'ltz',    'ISO 639-2/B':'ltz',    'name':u'Luxembourgish' },
                'lu':{  'ISO 639-1':'lu',   'ISO 639-2/T':'lub',    'ISO 639-2/B':'lub',    'name':u'Luba-Katanga' },
                'lg':{  'ISO 639-1':'lg',   'ISO 639-2/T':'lug',    'ISO 639-2/B':'lug',    'name':u'Ganda' },
                'mk':{  'ISO 639-1':'mk',   'ISO 639-2/T':'mkd',    'ISO 639-2/B':'mac',    'name':u'Macedonian' },
                'mh':{  'ISO 639-1':'mh',   'ISO 639-2/T':'mah',    'ISO 639-2/B':'mah',    'name':u'Marshallese' },
                'ml':{  'ISO 639-1':'ml',   'ISO 639-2/T':'mal',    'ISO 639-2/B':'mal',    'name':u'Malayalam' },
                'mi':{  'ISO 639-1':'mi',   'ISO 639-2/T':'mri',    'ISO 639-2/B':'mao',    'name':u'Maori' },
                'mr':{  'ISO 639-1':'mr',   'ISO 639-2/T':'mar',    'ISO 639-2/B':'mar',    'name':u'Marathi' },
                'ms':{  'ISO 639-1':'ms',   'ISO 639-2/T':'msa',    'ISO 639-2/B':'msa',    'name':u'Malay' },
                'mg':{  'ISO 639-1':'mg',   'ISO 639-2/T':'mlg',    'ISO 639-2/B':'mlg',    'name':u'Malagasy' },
                'mt':{  'ISO 639-1':'mt',   'ISO 639-2/T':'mlt',    'ISO 639-2/B':'mlt',    'name':u'Maltese' },
                'mo':{  'ISO 639-1':'mo',   'ISO 639-2/T':'mol',    'ISO 639-2/B':'mol',    'name':u'Moldavian' },
                'mn':{  'ISO 639-1':'mn',   'ISO 639-2/T':'mon',    'ISO 639-2/B':'mon',    'name':u'Mongolian' },
                'na':{  'ISO 639-1':'na',   'ISO 639-2/T':'nau',    'ISO 639-2/B':'nau',    'name':u'Nauru' },
                'nv':{  'ISO 639-1':'nv',   'ISO 639-2/T':'nav',    'ISO 639-2/B':'nav',    'name':u'Navajo' },
                'nr':{  'ISO 639-1':'nr',   'ISO 639-2/T':'nbl',    'ISO 639-2/B':'nbl',    'name':u'South Ndebele' },
                'nd':{  'ISO 639-1':'nd',   'ISO 639-2/T':'nde',    'ISO 639-2/B':'nde',    'name':u'North Ndebele' },
                'ng':{  'ISO 639-1':'ng',   'ISO 639-2/T':'ndo',    'ISO 639-2/B':'ndo',    'name':u'Ndonga' },
                'ne':{  'ISO 639-1':'ne',   'ISO 639-2/T':'nep',    'ISO 639-2/B':'nep',    'name':u'Nepali' },
                'nn':{  'ISO 639-1':'nn',   'ISO 639-2/T':'nno',    'ISO 639-2/B':'nno',    'name':u'Norwegian Nynorsk' },
                'nb':{  'ISO 639-1':'nb',   'ISO 639-2/T':'nob',    'ISO 639-2/B':'nob',    'name':u'Norwegian Bokmål' },
                'no':{  'ISO 639-1':'no',   'ISO 639-2/T':'nor',    'ISO 639-2/B':'nor',    'name':u'Norwegian' },
                'ny':{  'ISO 639-1':'ny',   'ISO 639-2/T':'nya',    'ISO 639-2/B':'nya',    'name':u'Nyanja' },
                'oc':{  'ISO 639-1':'oc',   'ISO 639-2/T':'oci',    'ISO 639-2/B':'oci',    'name':u'Occitan' },
                'oj':{  'ISO 639-1':'oj',   'ISO 639-2/T':'oji',    'ISO 639-2/B':'oji',    'name':u'Ojibwa' },
                'or':{  'ISO 639-1':'or',   'ISO 639-2/T':'ori',    'ISO 639-2/B':'ori',    'name':u'Oriya' },
                'om':{  'ISO 639-1':'om',   'ISO 639-2/T':'orm',    'ISO 639-2/B':'orm',    'name':u'Oromo' },
                'os':{  'ISO 639-1':'os',   'ISO 639-2/T':'oss',    'ISO 639-2/B':'oss',    'name':u'Ossetian' },
                'pa':{  'ISO 639-1':'pa',   'ISO 639-2/T':'pan',    'ISO 639-2/B':'pan',    'name':u'Panjabi' },
                'fa':{  'ISO 639-1':'fa',   'ISO 639-2/T':'fas',    'ISO 639-2/B':'per',    'name':u'Persian' },
                'pi':{  'ISO 639-1':'pi',   'ISO 639-2/T':'pli',    'ISO 639-2/B':'pli',    'name':u'Pali' },
                'pl':{  'ISO 639-1':'pl',   'ISO 639-2/T':'pol',    'ISO 639-2/B':'pol',    'name':u'Polish' },
                'pt':{  'ISO 639-1':'pt',   'ISO 639-2/T':'por',    'ISO 639-2/B':'por',    'name':u'Portuguese' },
                'ps':{  'ISO 639-1':'ps',   'ISO 639-2/T':'pus',    'ISO 639-2/B':'pus',    'name':u'Pushto' },
                'qu':{  'ISO 639-1':'qu',   'ISO 639-2/T':'que',    'ISO 639-2/B':'que',    'name':u'Quechua' },
                'rm':{  'ISO 639-1':'rm',   'ISO 639-2/T':'roh',    'ISO 639-2/B':'roh',    'name':u'Romansh' },
                'ro':{  'ISO 639-1':'ro',   'ISO 639-2/T':'ron',    'ISO 639-2/B':'rum',    'name':u'Romanian' },
                'rn':{  'ISO 639-1':'rn',   'ISO 639-2/T':'run',    'ISO 639-2/B':'run',    'name':u'Rundi' },
                'ru':{  'ISO 639-1':'ru',   'ISO 639-2/T':'rus',    'ISO 639-2/B':'rus',    'name':u'Russian' },
                'sg':{  'ISO 639-1':'sg',   'ISO 639-2/T':'sag',    'ISO 639-2/B':'sag',    'name':u'Sango' },
                'sa':{  'ISO 639-1':'sa',   'ISO 639-2/T':'san',    'ISO 639-2/B':'san',    'name':u'Sanskrit' },
                'sr':{  'ISO 639-1':'sr',   'ISO 639-2/T':'srp',    'ISO 639-2/B':'scc',    'name':u'Serbian' },
                'hr':{  'ISO 639-1':'hr',   'ISO 639-2/T':'hrv',    'ISO 639-2/B':'scr',    'name':u'Croatian' },
                'si':{  'ISO 639-1':'si',   'ISO 639-2/T':'sin',    'ISO 639-2/B':'sin',    'name':u'Sinhala' },
                'sk':{  'ISO 639-1':'sk',   'ISO 639-2/T':'slk',    'ISO 639-2/B':'slo',    'name':u'Slovak' },
                'sl':{  'ISO 639-1':'sl',   'ISO 639-2/T':'slv',    'ISO 639-2/B':'slv',    'name':u'Slovenian' },
                'se':{  'ISO 639-1':'se',   'ISO 639-2/T':'sme',    'ISO 639-2/B':'sme',    'name':u'Northern Sami' },
                'sm':{  'ISO 639-1':'sm',   'ISO 639-2/T':'smo',    'ISO 639-2/B':'smo',    'name':u'Samoan' },
                'sn':{  'ISO 639-1':'sn',   'ISO 639-2/T':'sna',    'ISO 639-2/B':'sna',    'name':u'Shona' },
                'sd':{  'ISO 639-1':'sd',   'ISO 639-2/T':'snd',    'ISO 639-2/B':'snd',    'name':u'Sindhi' },
                'so':{  'ISO 639-1':'so',   'ISO 639-2/T':'som',    'ISO 639-2/B':'som',    'name':u'Somali' },
                'st':{  'ISO 639-1':'st',   'ISO 639-2/T':'sot',    'ISO 639-2/B':'sot',    'name':u'Southern Sotho' },
                'es':{  'ISO 639-1':'es',   'ISO 639-2/T':'spa',    'ISO 639-2/B':'spa',    'name':u'Spanish' },
                'sc':{  'ISO 639-1':'sc',   'ISO 639-2/T':'srd',    'ISO 639-2/B':'srd',    'name':u'Sardinian' },
                'ss':{  'ISO 639-1':'ss',   'ISO 639-2/T':'ssw',    'ISO 639-2/B':'ssw',    'name':u'Swati' },
                'su':{  'ISO 639-1':'su',   'ISO 639-2/T':'sun',    'ISO 639-2/B':'sun',    'name':u'Sundanese' },
                'sw':{  'ISO 639-1':'sw',   'ISO 639-2/T':'swa',    'ISO 639-2/B':'swa',    'name':u'Swahili' },
                'sv':{  'ISO 639-1':'sv',   'ISO 639-2/T':'swe',    'ISO 639-2/B':'swe',    'name':u'Swedish' },
                'ty':{  'ISO 639-1':'ty',   'ISO 639-2/T':'tah',    'ISO 639-2/B':'tah',    'name':u'Tahitian' },
                'ta':{  'ISO 639-1':'ta',   'ISO 639-2/T':'tam',    'ISO 639-2/B':'tam',    'name':u'Tamil' },
                'tt':{  'ISO 639-1':'tt',   'ISO 639-2/T':'tat',    'ISO 639-2/B':'tat',    'name':u'Tatar' },
                'te':{  'ISO 639-1':'te',   'ISO 639-2/T':'tel',    'ISO 639-2/B':'tel',    'name':u'Telugu' },
                'tg':{  'ISO 639-1':'tg',   'ISO 639-2/T':'tgk',    'ISO 639-2/B':'tgk',    'name':u'Tajik' },
                'tl':{  'ISO 639-1':'tl',   'ISO 639-2/T':'tgl',    'ISO 639-2/B':'tgl',    'name':u'Tagalog' },
                'th':{  'ISO 639-1':'th',   'ISO 639-2/T':'tha',    'ISO 639-2/B':'tha',    'name':u'Thai' },
                'bo':{  'ISO 639-1':'bo',   'ISO 639-2/T':'bod',    'ISO 639-2/B':'tib',    'name':u'Tibetan' },
                'ti':{  'ISO 639-1':'ti',   'ISO 639-2/T':'tir',    'ISO 639-2/B':'tir',    'name':u'Tigrinya' },
                'to':{  'ISO 639-1':'to',   'ISO 639-2/T':'ton',    'ISO 639-2/B':'ton',    'name':u'Tonga' },
                'tn':{  'ISO 639-1':'tn',   'ISO 639-2/T':'tsn',    'ISO 639-2/B':'tsn',    'name':u'Tswana' },
                'ts':{  'ISO 639-1':'ts',   'ISO 639-2/T':'tso',    'ISO 639-2/B':'tso',    'name':u'Tsonga' },
                'tk':{  'ISO 639-1':'tk',   'ISO 639-2/T':'tuk',    'ISO 639-2/B':'tuk',    'name':u'Turkmen' },
                'tr':{  'ISO 639-1':'tr',   'ISO 639-2/T':'tur',    'ISO 639-2/B':'tur',    'name':u'Turkish' },
                'tw':{  'ISO 639-1':'tw',   'ISO 639-2/T':'twi',    'ISO 639-2/B':'twi',    'name':u'Twi' },
                'ug':{  'ISO 639-1':'ug',   'ISO 639-2/T':'uig',    'ISO 639-2/B':'uig',    'name':u'Uighur' },
                'uk':{  'ISO 639-1':'uk',   'ISO 639-2/T':'ukr',    'ISO 639-2/B':'ukr',    'name':u'Ukrainian' },
                'ur':{  'ISO 639-1':'ur',   'ISO 639-2/T':'urd',    'ISO 639-2/B':'urd',    'name':u'Urdu' },
                'uz':{  'ISO 639-1':'uz',   'ISO 639-2/T':'uzb',    'ISO 639-2/B':'uzb',    'name':u'Uzbek' },
                've':{  'ISO 639-1':'ve',   'ISO 639-2/T':'ven',    'ISO 639-2/B':'ven',    'name':u'Venda' },
                'vi':{  'ISO 639-1':'vi',   'ISO 639-2/T':'vie',    'ISO 639-2/B':'vie',    'name':u'Vietnamese' },
                'vo':{  'ISO 639-1':'vo',   'ISO 639-2/T':'vol',    'ISO 639-2/B':'vol',    'name':u'Volapük' },
                'cy':{  'ISO 639-1':'cy',   'ISO 639-2/T':'cym',    'ISO 639-2/B':'wel',    'name':u'Welsh' },
                'wa':{  'ISO 639-1':'wa',   'ISO 639-2/T':'wln',    'ISO 639-2/B':'wln',    'name':u'Walloon' },
                'wo':{  'ISO 639-1':'wo',   'ISO 639-2/T':'wol',    'ISO 639-2/B':'wol',    'name':u'Wolof' },
                'xh':{  'ISO 639-1':'xh',   'ISO 639-2/T':'xho',    'ISO 639-2/B':'xho',    'name':u'Xhosa' },
                'yi':{  'ISO 639-1':'yi',   'ISO 639-2/T':'yid',    'ISO 639-2/B':'yid',    'name':u'Yiddish' },
                'yo':{  'ISO 639-1':'yo',   'ISO 639-2/T':'yor',    'ISO 639-2/B':'yor',    'name':u'Yoruba' },
                'za':{  'ISO 639-1':'za',   'ISO 639-2/T':'zha',    'ISO 639-2/B':'zha',    'name':u'Zhuang' },
                'zu':{  'ISO 639-1':'zu',   'ISO 639-2/T':'zul',    'ISO 639-2/B':'zul',    'name':u'Zulu' },
            },
        },
        'genre':{
            'synonym':['name','mediainfo'],
            'element':{
                1:{     'gnre':1,       'ID3':0,    'mediainfo':u'Genre_000',   'name':u'Blues' },
                2:{     'gnre':2,       'ID3':1,    'mediainfo':u'Genre_001',   'name':u'Classic Rock' },
                3:{     'gnre':3,       'ID3':2,    'mediainfo':u'Genre_002',   'name':u'Country' },
                4:{     'gnre':4,       'ID3':3,    'mediainfo':u'Genre_003',   'name':u'Dance' },
                5:{     'gnre':5,       'ID3':4,    'mediainfo':u'Genre_004',   'name':u'Disco' },
                6:{     'gnre':6,       'ID3':5,    'mediainfo':u'Genre_005',   'name':u'Funk' },
                7:{     'gnre':7,       'ID3':6,    'mediainfo':u'Genre_006',   'name':u'Grunge' },
                8:{     'gnre':8,       'ID3':7,    'mediainfo':u'Genre_007',   'name':u'Hip Hop' },
                9:{     'gnre':9,       'ID3':8,    'mediainfo':u'Genre_008',   'name':u'Jazz' },
                10:{    'gnre':10,      'ID3':9,    'mediainfo':u'Genre_009',   'name':u'Metal' },
                11:{    'gnre':11,      'ID3':10,   'mediainfo':u'Genre_010',   'name':u'New Age' },
                12:{    'gnre':12,      'ID3':11,   'mediainfo':u'Genre_011',   'name':u'Oldies' },
                13:{    'gnre':13,      'ID3':12,   'mediainfo':u'Genre_012',   'name':u'Other' },
                14:{    'gnre':14,      'ID3':13,   'mediainfo':u'Genre_013',   'name':u'Pop' },
                15:{    'gnre':15,      'ID3':14,   'mediainfo':u'Genre_014',   'name':u'R&B' },
                16:{    'gnre':16,      'ID3':15,   'mediainfo':u'Genre_015',   'name':u'Rap' },
                17:{    'gnre':17,      'ID3':16,   'mediainfo':u'Genre_016',   'name':u'Reggae' },
                18:{    'gnre':18,      'ID3':17,   'mediainfo':u'Genre_017',   'name':u'Rock' },
                19:{    'gnre':19,      'ID3':18,   'mediainfo':u'Genre_018',   'name':u'Techno' },
                20:{    'gnre':20,      'ID3':19,   'mediainfo':u'Genre_019',   'name':u'Industrial' },
                21:{    'gnre':21,      'ID3':20,   'mediainfo':u'Genre_020',   'name':u'Alternative' },
                22:{    'gnre':22,      'ID3':21,   'mediainfo':u'Genre_021',   'name':u'Ska' },
                23:{    'gnre':23,      'ID3':22,   'mediainfo':u'Genre_022',   'name':u'Death Metal' },
                24:{    'gnre':24,      'ID3':23,   'mediainfo':u'Genre_023',   'name':u'Pranks' },
                25:{    'gnre':25,      'ID3':24,   'mediainfo':u'Genre_024',   'name':u'Soundtrack' },
                26:{    'gnre':26,      'ID3':25,   'mediainfo':u'Genre_025',   'name':u'Euro Techno' },
                27:{    'gnre':27,      'ID3':26,   'mediainfo':u'Genre_026',   'name':u'Ambient' },
                28:{    'gnre':28,      'ID3':27,   'mediainfo':u'Genre_027',   'name':u'Trip Hop' },
                29:{    'gnre':29,      'ID3':28,   'mediainfo':u'Genre_028',   'name':u'Vocal' },
                30:{    'gnre':30,      'ID3':29,   'mediainfo':u'Genre_029',   'name':u'Jazz Funk' },
                31:{    'gnre':31,      'ID3':30,   'mediainfo':u'Genre_030',   'name':u'Fusion' },
                32:{    'gnre':32,      'ID3':31,   'mediainfo':u'Genre_031',   'name':u'Trance' },
                33:{    'gnre':33,      'ID3':32,   'mediainfo':u'Genre_032',   'name':u'Classical' },
                34:{    'gnre':34,      'ID3':33,   'mediainfo':u'Genre_033',   'name':u'Instrumental' },
                35:{    'gnre':35,      'ID3':34,   'mediainfo':u'Genre_034',   'name':u'Acid' },
                36:{    'gnre':36,      'ID3':35,   'mediainfo':u'Genre_035',   'name':u'House' },
                37:{    'gnre':37,      'ID3':36,   'mediainfo':u'Genre_036',   'name':u'Game' },
                38:{    'gnre':38,      'ID3':37,   'mediainfo':u'Genre_037',   'name':u'Sound Clip' },
                39:{    'gnre':39,      'ID3':38,   'mediainfo':u'Genre_038',   'name':u'Gospel' },
                40:{    'gnre':40,      'ID3':39,   'mediainfo':u'Genre_039',   'name':u'Noise' },
                41:{    'gnre':41,      'ID3':40,   'mediainfo':u'Genre_040',   'name':u'Alternrock' },
                42:{    'gnre':42,      'ID3':41,   'mediainfo':u'Genre_041',   'name':u'Bass' },
                43:{    'gnre':43,      'ID3':42,   'mediainfo':u'Genre_042',   'name':u'Soul' },
                44:{    'gnre':44,      'ID3':43,   'mediainfo':u'Genre_043',   'name':u'Punk' },
                45:{    'gnre':45,      'ID3':44,   'mediainfo':u'Genre_044',   'name':u'Space' },
                46:{    'gnre':46,      'ID3':45,   'mediainfo':u'Genre_045',   'name':u'Meditative' },
                47:{    'gnre':47,      'ID3':46,   'mediainfo':u'Genre_046',   'name':u'Instrumental Pop' },
                48:{    'gnre':48,      'ID3':47,   'mediainfo':u'Genre_047',   'name':u'Instrumental Rock' },
                49:{    'gnre':49,      'ID3':48,   'mediainfo':u'Genre_048',   'name':u'Ethnic' },
                50:{    'gnre':50,      'ID3':49,   'mediainfo':u'Genre_049',   'name':u'Gothic' },
                51:{    'gnre':51,      'ID3':50,   'mediainfo':u'Genre_050',   'name':u'Darkwave' },
                52:{    'gnre':52,      'ID3':51,   'mediainfo':u'Genre_051',   'name':u'Techno Industrial' },
                53:{    'gnre':53,      'ID3':52,   'mediainfo':u'Genre_052',   'name':u'Electronic' },
                54:{    'gnre':54,      'ID3':53,   'mediainfo':u'Genre_053',   'name':u'Pop Folk' },
                55:{    'gnre':55,      'ID3':54,   'mediainfo':u'Genre_054',   'name':u'Eurodance' },
                56:{    'gnre':56,      'ID3':55,   'mediainfo':u'Genre_055',   'name':u'Dream' },
                57:{    'gnre':57,      'ID3':56,   'mediainfo':u'Genre_056',   'name':u'Southern Rock' },
                58:{    'gnre':58,      'ID3':57,   'mediainfo':u'Genre_057',   'name':u'Comedy' },
                59:{    'gnre':59,      'ID3':58,   'mediainfo':u'Genre_058',   'name':u'Cult' },
                60:{    'gnre':60,      'ID3':59,   'mediainfo':u'Genre_059',   'name':u'Gangsta' },
                61:{    'gnre':61,      'ID3':60,   'mediainfo':u'Genre_060',   'name':u'Top 40' },
                62:{    'gnre':62,      'ID3':61,   'mediainfo':u'Genre_061',   'name':u'Christian Rap' },
                63:{    'gnre':63,      'ID3':62,   'mediainfo':u'Genre_062',   'name':u'Pop Funk' },
                64:{    'gnre':64,      'ID3':63,   'mediainfo':u'Genre_063',   'name':u'Jungle' },
                65:{    'gnre':65,      'ID3':64,   'mediainfo':u'Genre_064',   'name':u'Native American' },
                66:{    'gnre':66,      'ID3':65,   'mediainfo':u'Genre_065',   'name':u'Cabaret' },
                67:{    'gnre':67,      'ID3':66,   'mediainfo':u'Genre_066',   'name':u'New Wave' },
                68:{    'gnre':68,      'ID3':67,   'mediainfo':u'Genre_067',   'name':u'Psychedelic' },
                69:{    'gnre':69,      'ID3':68,   'mediainfo':u'Genre_068',   'name':u'Rave' },
                70:{    'gnre':70,      'ID3':69,   'mediainfo':u'Genre_069',   'name':u'Showtunes' },
                71:{    'gnre':71,      'ID3':70,   'mediainfo':u'Genre_070',   'name':u'Trailer' },
                72:{    'gnre':72,      'ID3':71,   'mediainfo':u'Genre_071',   'name':u'Lo Fi' },
                73:{    'gnre':73,      'ID3':72,   'mediainfo':u'Genre_072',   'name':u'Tribal' },
                74:{    'gnre':74,      'ID3':73,   'mediainfo':u'Genre_073',   'name':u'Acid Punk' },
                75:{    'gnre':75,      'ID3':74,   'mediainfo':u'Genre_074',   'name':u'Acid Jazz' },
                76:{    'gnre':76,      'ID3':75,   'mediainfo':u'Genre_075',   'name':u'Polka' },
                77:{    'gnre':77,      'ID3':76,   'mediainfo':u'Genre_076',   'name':u'Retro' },
                78:{    'gnre':78,      'ID3':77,   'mediainfo':u'Genre_077',   'name':u'Musical' },
                79:{    'gnre':79,      'ID3':78,   'mediainfo':u'Genre_078',   'name':u'Rock and Roll' },
                80:{    'gnre':80,      'ID3':79,   'mediainfo':u'Genre_079',   'name':u'Hard Rock' },
                81:{    'gnre':81,      'ID3':80,   'mediainfo':u'Genre_080',   'name':u'Folk' },
                82:{    'gnre':82,      'ID3':81,   'mediainfo':u'Genre_081',   'name':u'Folk-Rock' },
                83:{    'gnre':83,      'ID3':82,   'mediainfo':u'Genre_082',   'name':u'National Folk' },
                84:{    'gnre':84,      'ID3':83,   'mediainfo':u'Genre_083',   'name':u'Swing' },
                85:{    'gnre':85,      'ID3':84,   'mediainfo':u'Genre_084',   'name':u'Fast Fusion' },
                86:{    'gnre':86,      'ID3':85,   'mediainfo':u'Genre_085',   'name':u'Bebob' },
                87:{    'gnre':87,      'ID3':86,   'mediainfo':u'Genre_086',   'name':u'Latin' },
                88:{    'gnre':88,      'ID3':87,   'mediainfo':u'Genre_087',   'name':u'Revival' },
                89:{    'gnre':89,      'ID3':88,   'mediainfo':u'Genre_088',   'name':u'Celtic' },
                90:{    'gnre':90,      'ID3':89,   'mediainfo':u'Genre_089',   'name':u'Bluegrass' },
                91:{    'gnre':91,      'ID3':90,   'mediainfo':u'Genre_090',   'name':u'Avantgarde' },
                92:{    'gnre':92,      'ID3':91,   'mediainfo':u'Genre_091',   'name':u'Gothic Rock' },
                93:{    'gnre':93,      'ID3':92,   'mediainfo':u'Genre_092',   'name':u'Progresive Rock' },
                94:{    'gnre':94,      'ID3':93,   'mediainfo':u'Genre_093',   'name':u'Psychedelic Rock' },
                95:{    'gnre':95,      'ID3':94,   'mediainfo':u'Genre_094',   'name':u'Symphonic Rock' },
                96:{    'gnre':96,      'ID3':95,   'mediainfo':u'Genre_095',   'name':u'Slow Rock' },
                97:{    'gnre':97,      'ID3':96,   'mediainfo':u'Genre_096',   'name':u'Big Band' },
                98:{    'gnre':98,      'ID3':97,   'mediainfo':u'Genre_097',   'name':u'Chorus' },
                99:{    'gnre':99,      'ID3':98,   'mediainfo':u'Genre_098',   'name':u'Easy Listening' },
                100:{   'gnre':100,     'ID3':99,   'mediainfo':u'Genre_099',   'name':u'Acoustic' },
                101:{   'gnre':101,     'ID3':100,  'mediainfo':u'Genre_100',   'name':u'Humor' },
                102:{   'gnre':102,     'ID3':101,  'mediainfo':u'Genre_101',   'name':u'Speech' },
                103:{   'gnre':103,     'ID3':102,  'mediainfo':u'Genre_102',   'name':u'Chason' },
                104:{   'gnre':104,     'ID3':103,  'mediainfo':u'Genre_103',   'name':u'Opera' },
                105:{   'gnre':105,     'ID3':104,  'mediainfo':u'Genre_104',   'name':u'Chamber Music' },
                106:{   'gnre':106,     'ID3':105,  'mediainfo':u'Genre_105',   'name':u'Sonata' },
                107:{   'gnre':107,     'ID3':106,  'mediainfo':u'Genre_106',   'name':u'Symphony' },
                108:{   'gnre':108,     'ID3':107,  'mediainfo':u'Genre_107',   'name':u'Booty Bass' },
                109:{   'gnre':109,     'ID3':108,  'mediainfo':u'Genre_108',   'name':u'Primus' },
                110:{   'gnre':110,     'ID3':109,  'mediainfo':u'Genre_109',   'name':u'Porn Groove' },
                111:{   'gnre':111,     'ID3':110,  'mediainfo':u'Genre_110',   'name':u'Satire' },
                112:{   'gnre':112,     'ID3':111,  'mediainfo':u'Genre_111',   'name':u'Slow Jam' },
                113:{   'gnre':113,     'ID3':112,  'mediainfo':u'Genre_112',   'name':u'Club' },
                114:{   'gnre':114,     'ID3':113,  'mediainfo':u'Genre_113',   'name':u'Tango' },
                115:{   'gnre':115,     'ID3':114,  'mediainfo':u'Genre_114',   'name':u'Samba' },
                116:{   'gnre':116,     'ID3':115,  'mediainfo':u'Genre_115',   'name':u'Folklore' },
                117:{   'gnre':117,     'ID3':116,  'mediainfo':u'Genre_116',   'name':u'Ballad' },
                118:{   'gnre':118,     'ID3':117,  'mediainfo':u'Genre_117',   'name':u'Power Ballad' },
                119:{   'gnre':119,     'ID3':118,  'mediainfo':u'Genre_118',   'name':u'Rhythmic Soul' },
                120:{   'gnre':120,     'ID3':119,  'mediainfo':u'Genre_119',   'name':u'Freestyle' },
                121:{   'gnre':121,     'ID3':120,  'mediainfo':u'Genre_120',   'name':u'Duet' },
                122:{   'gnre':122,     'ID3':121,  'mediainfo':u'Genre_121',   'name':u'Punk Rock' },
                123:{   'gnre':123,     'ID3':122,  'mediainfo':u'Genre_122',   'name':u'Drum Solo' },
                124:{   'gnre':124,     'ID3':123,  'mediainfo':u'Genre_123',   'name':u'A capella' },
                125:{   'gnre':125,     'ID3':124,  'mediainfo':u'Genre_124',   'name':u'Euro-House' },
                126:{   'gnre':126,     'ID3':125,  'mediainfo':u'Genre_125',   'name':u'Dance Hall' },
            },
        },
        'media kind':{
            'synonym':['stik'],
            'element':{
                'oldmovie':{    'name':u'Movie',        'stik':0 },
                'music':{       'name':u'Music',        'stik':1 },
                'audiobook':{   'name':u'Audio Book',   'stik':2 },
                'musicvideo':{  'name':u'Music Video',  'stik':6 },
                'movie':{       'name':u'Movie',        'stik':9 },
                'tvshow':{      'name':u'TV Show',      'stik':10 },
                'booklet':{     'name':u'Booklet',      'stik':11 },
                'ringtone':{    'name':u'Ringtone',     'stik':14 },
            },
        },
        'stream kind':{
            'synonym':['key'],
            'element':{
                'video':{   'name':u'Video'     },
                'audio':{   'name':u'Audio'     },
                'image':{   'name':u'Image'     },
                'caption':{ 'name':u'Caption'   },
                'menu':{    'name':u'Menu'      },
                'preview':{ 'name':u'Preview'   },
            },
        },
        'mediainfo stream type':{
            'synonym':['mediainfo'],
            'element':{
                'video':{   'name':u'Video',    'namespace':'resource.crawl.stream.video',  'mediainfo':u'Video'     },
                'audio':{   'name':u'Audio',    'namespace':'resource.crawl.stream.audio',  'mediainfo':u'Audio'     },
                'image':{   'name':u'Image',    'namespace':'resource.crawl.stream.image',  'mediainfo':u'Image'     },
                'text':{    'name':u'Text',     'namespace':'resource.crawl.stream.text',   'mediainfo':u'Text'   },
                'menu':{    'name':u'Menu',     'namespace':None,                           'mediainfo':u'Menu'      },
                'general':{ 'name':u'General',  'namespace':'resource.crawl.meta',          'mediainfo':u'General'   },
            },
        },
        'kind':{
            'synonym':['key'],
            'element':{
                'm4v':{     'name':u'MPEG-4 video file',    'container':'mp4' },
                'm4a':{     'name':u'MPEG-4 audio file',    'container':'mp4' },
                'mkv':{     'name':u'Matroska video file',  'container':'matroska' },
                'avi':{     'name':u'AVI video file',       'container':'avi' },
                'srt':{     'name':u'SRT subtitles file',   'container':'subtitles' },
                'ass':{     'name':u'ASS subtitle file',    'container':'subtitles' },
                'chpl':{    'name':u'OGG chapter file',     'container':'chapters'},
                'jpg':{     'name':u'JPEG image file',      'container':'image' },
                'png':{     'name':u'PNG image file',       'container':'image' },
                'ac3':{     'name':u'AC-3 raw audio',       'container':'raw audio' },
                'dts':{     'name':u'DTS raw audio',        'container':'raw audio' },
                'flac':{    'name':u'FLAC audio file',      'container':'raw audio' },
            },
        },
        'content rating':{
            'synonym':['rtng'],
            'element':{
                'none':{        'name':u'None',      'rtng':0 },
                'clean':{       'name':u'Clean',     'rtng':2 },
                'explicit':{    'name':u'Explicit',  'rtng':4 },
            },
        },
        'itunes account type':{
            'synonym':['akID'],
            'element':{
                'itunes':{  'name':u'iTunes',    'akID':0 },
                'aol':{     'name':u'AOL',       'akID':1 },
            },
        },
        'country':{
            'synonym':['ISO 3166-1 alpha-2', 'ISO 3166-1 alpha-3'],
            'element':{
                'af':{  'ISO 3166-1 alpha-2':'AF',  'ISO 3166-1 alpha-3':'AFG', 'ISO 3166-1 numeric':'004',                 'name':u'Afghanistan', },
                'ax':{  'ISO 3166-1 alpha-2':'AX',  'ISO 3166-1 alpha-3':'ALA', 'ISO 3166-1 numeric':'248',                 'name':u'Åland Islands', },
                'al':{  'ISO 3166-1 alpha-2':'AL',  'ISO 3166-1 alpha-3':'ALB', 'ISO 3166-1 numeric':'008',                 'name':u'Albania', },
                'dz':{  'ISO 3166-1 alpha-2':'DZ',  'ISO 3166-1 alpha-3':'DZA', 'ISO 3166-1 numeric':'012',                 'name':u'Algeria', },
                'as':{  'ISO 3166-1 alpha-2':'AS',  'ISO 3166-1 alpha-3':'ASM', 'ISO 3166-1 numeric':'016',                 'name':u'American Samoa', },
                'ad':{  'ISO 3166-1 alpha-2':'AD',  'ISO 3166-1 alpha-3':'AND', 'ISO 3166-1 numeric':'020',                 'name':u'Andorra', },
                'ao':{  'ISO 3166-1 alpha-2':'AO',  'ISO 3166-1 alpha-3':'AGO', 'ISO 3166-1 numeric':'024',                 'name':u'Angola', },
                'ai':{  'ISO 3166-1 alpha-2':'AI',  'ISO 3166-1 alpha-3':'AIA', 'ISO 3166-1 numeric':'660',                 'name':u'Anguilla', },
                'aq':{  'ISO 3166-1 alpha-2':'AQ',  'ISO 3166-1 alpha-3':'ATA', 'ISO 3166-1 numeric':'010',                 'name':u'Antarctica', },
                'ag':{  'ISO 3166-1 alpha-2':'AG',  'ISO 3166-1 alpha-3':'ATG', 'ISO 3166-1 numeric':'028',                 'name':u'Antigua and Barbuda', },
                'ar':{  'ISO 3166-1 alpha-2':'AR',  'ISO 3166-1 alpha-3':'ARG', 'ISO 3166-1 numeric':'032',                 'name':u'Argentina', },
                'am':{  'ISO 3166-1 alpha-2':'AM',  'ISO 3166-1 alpha-3':'ARM', 'ISO 3166-1 numeric':'051',                 'name':u'Armenia', },
                'aw':{  'ISO 3166-1 alpha-2':'AW',  'ISO 3166-1 alpha-3':'ABW', 'ISO 3166-1 numeric':'533',                 'name':u'Aruba', },
                'au':{  'ISO 3166-1 alpha-2':'AU',  'ISO 3166-1 alpha-3':'AUS', 'ISO 3166-1 numeric':'036', 'sfID':143460,  'name':u'Australia', },
                'at':{  'ISO 3166-1 alpha-2':'AT',  'ISO 3166-1 alpha-3':'AUT', 'ISO 3166-1 numeric':'040', 'sfID':143445,  'name':u'Austria', },
                'az':{  'ISO 3166-1 alpha-2':'AZ',  'ISO 3166-1 alpha-3':'AZE', 'ISO 3166-1 numeric':'031',                 'name':u'Azerbaijan', },
                'bs':{  'ISO 3166-1 alpha-2':'BS',  'ISO 3166-1 alpha-3':'BHS', 'ISO 3166-1 numeric':'044',                 'name':u'Bahamas', },
                'bh':{  'ISO 3166-1 alpha-2':'BH',  'ISO 3166-1 alpha-3':'BHR', 'ISO 3166-1 numeric':'048',                 'name':u'Bahrain', },
                'bd':{  'ISO 3166-1 alpha-2':'BD',  'ISO 3166-1 alpha-3':'BGD', 'ISO 3166-1 numeric':'050',                 'name':u'Bangladesh', },
                'bb':{  'ISO 3166-1 alpha-2':'BB',  'ISO 3166-1 alpha-3':'BRB', 'ISO 3166-1 numeric':'052',                 'name':u'Barbados', },
                'by':{  'ISO 3166-1 alpha-2':'BY',  'ISO 3166-1 alpha-3':'BLR', 'ISO 3166-1 numeric':'112',                 'name':u'Belarus', },
                'be':{  'ISO 3166-1 alpha-2':'BE',  'ISO 3166-1 alpha-3':'BEL', 'ISO 3166-1 numeric':'056', 'sfID':143446,  'name':u'Belgium', },
                'bz':{  'ISO 3166-1 alpha-2':'BZ',  'ISO 3166-1 alpha-3':'BLZ', 'ISO 3166-1 numeric':'084',                 'name':u'Belize', },
                'bj':{  'ISO 3166-1 alpha-2':'BJ',  'ISO 3166-1 alpha-3':'BEN', 'ISO 3166-1 numeric':'204',                 'name':u'Benin', },
                'bm':{  'ISO 3166-1 alpha-2':'BM',  'ISO 3166-1 alpha-3':'BMU', 'ISO 3166-1 numeric':'060',                 'name':u'Bermuda', },
                'bt':{  'ISO 3166-1 alpha-2':'BT',  'ISO 3166-1 alpha-3':'BTN', 'ISO 3166-1 numeric':'064',                 'name':u'Bhutan', },
                'bo':{  'ISO 3166-1 alpha-2':'BO',  'ISO 3166-1 alpha-3':'BOL', 'ISO 3166-1 numeric':'068',                 'name':u'Bolivia, Plurinational State of', },
                'bq':{  'ISO 3166-1 alpha-2':'BQ',  'ISO 3166-1 alpha-3':'BES', 'ISO 3166-1 numeric':'535',                 'name':u'Bonaire, Saint Eustatius and Saba', },
                'ba':{  'ISO 3166-1 alpha-2':'BA',  'ISO 3166-1 alpha-3':'BIH', 'ISO 3166-1 numeric':'070',                 'name':u'Bosnia and Herzegovina', },
                'bw':{  'ISO 3166-1 alpha-2':'BW',  'ISO 3166-1 alpha-3':'BWA', 'ISO 3166-1 numeric':'072',                 'name':u'Botswana', },
                'bv':{  'ISO 3166-1 alpha-2':'BV',  'ISO 3166-1 alpha-3':'BVT', 'ISO 3166-1 numeric':'074',                 'name':u'Bouvet Island', },
                'br':{  'ISO 3166-1 alpha-2':'BR',  'ISO 3166-1 alpha-3':'BRA', 'ISO 3166-1 numeric':'076',                 'name':u'Brazil', },
                'io':{  'ISO 3166-1 alpha-2':'IO',  'ISO 3166-1 alpha-3':'IOT', 'ISO 3166-1 numeric':'086',                 'name':u'British Indian Ocean Territory', },
                'bn':{  'ISO 3166-1 alpha-2':'BN',  'ISO 3166-1 alpha-3':'BRN', 'ISO 3166-1 numeric':'096',                 'name':u'Brunei Darussalam', },
                'bg':{  'ISO 3166-1 alpha-2':'BG',  'ISO 3166-1 alpha-3':'BGR', 'ISO 3166-1 numeric':'100',                 'name':u'Bulgaria', },
                'bf':{  'ISO 3166-1 alpha-2':'BF',  'ISO 3166-1 alpha-3':'BFA', 'ISO 3166-1 numeric':'854',                 'name':u'Burkina Faso', },
                'bi':{  'ISO 3166-1 alpha-2':'BI',  'ISO 3166-1 alpha-3':'BDI', 'ISO 3166-1 numeric':'108',                 'name':u'Burundi', },
                'kh':{  'ISO 3166-1 alpha-2':'KH',  'ISO 3166-1 alpha-3':'KHM', 'ISO 3166-1 numeric':'116',                 'name':u'Cambodia', },
                'cm':{  'ISO 3166-1 alpha-2':'CM',  'ISO 3166-1 alpha-3':'CMR', 'ISO 3166-1 numeric':'120',                 'name':u'Cameroon', },
                'ca':{  'ISO 3166-1 alpha-2':'CA',  'ISO 3166-1 alpha-3':'CAN', 'ISO 3166-1 numeric':'124', 'sfID':143455,  'name':u'Canada', },
                'cv':{  'ISO 3166-1 alpha-2':'CV',  'ISO 3166-1 alpha-3':'CPV', 'ISO 3166-1 numeric':'132',                 'name':u'Cape Verde', },
                'ky':{  'ISO 3166-1 alpha-2':'KY',  'ISO 3166-1 alpha-3':'CYM', 'ISO 3166-1 numeric':'136',                 'name':u'Cayman Islands', },
                'cf':{  'ISO 3166-1 alpha-2':'CF',  'ISO 3166-1 alpha-3':'CAF', 'ISO 3166-1 numeric':'140',                 'name':u'Central African Republic', },
                'td':{  'ISO 3166-1 alpha-2':'TD',  'ISO 3166-1 alpha-3':'TCD', 'ISO 3166-1 numeric':'148',                 'name':u'Chad', },
                'cl':{  'ISO 3166-1 alpha-2':'CL',  'ISO 3166-1 alpha-3':'CHL', 'ISO 3166-1 numeric':'152',                 'name':u'Chile', },
                'cn':{  'ISO 3166-1 alpha-2':'CN',  'ISO 3166-1 alpha-3':'CHN', 'ISO 3166-1 numeric':'156',                 'name':u'China', },
                'cx':{  'ISO 3166-1 alpha-2':'CX',  'ISO 3166-1 alpha-3':'CXR', 'ISO 3166-1 numeric':'162',                 'name':u'Christmas Island', },
                'cc':{  'ISO 3166-1 alpha-2':'CC',  'ISO 3166-1 alpha-3':'CCK', 'ISO 3166-1 numeric':'166',                 'name':u'Cocos (Keeling) Islands', },
                'co':{  'ISO 3166-1 alpha-2':'CO',  'ISO 3166-1 alpha-3':'COL', 'ISO 3166-1 numeric':'170',                 'name':u'Colombia', },
                'km':{  'ISO 3166-1 alpha-2':'KM',  'ISO 3166-1 alpha-3':'COM', 'ISO 3166-1 numeric':'174',                 'name':u'Comoros', },
                'cg':{  'ISO 3166-1 alpha-2':'CG',  'ISO 3166-1 alpha-3':'COG', 'ISO 3166-1 numeric':'178',                 'name':u'Congo', },
                'cd':{  'ISO 3166-1 alpha-2':'CD',  'ISO 3166-1 alpha-3':'COD', 'ISO 3166-1 numeric':'180',                 'name':u'Congo, the Democratic Republic of the', },
                'ck':{  'ISO 3166-1 alpha-2':'CK',  'ISO 3166-1 alpha-3':'COK', 'ISO 3166-1 numeric':'184',                 'name':u'Cook Islands', },
                'cr':{  'ISO 3166-1 alpha-2':'CR',  'ISO 3166-1 alpha-3':'CRI', 'ISO 3166-1 numeric':'188',                 'name':u'Costa Rica', },
                'ci':{  'ISO 3166-1 alpha-2':'CI',  'ISO 3166-1 alpha-3':'CIV', 'ISO 3166-1 numeric':'384',                 'name':u'Côte d\'Ivoire', },
                'hr':{  'ISO 3166-1 alpha-2':'HR',  'ISO 3166-1 alpha-3':'HRV', 'ISO 3166-1 numeric':'191',                 'name':u'Croatia', },
                'cu':{  'ISO 3166-1 alpha-2':'CU',  'ISO 3166-1 alpha-3':'CUB', 'ISO 3166-1 numeric':'192',                 'name':u'Cuba', },
                'cw':{  'ISO 3166-1 alpha-2':'CW',  'ISO 3166-1 alpha-3':'CUW', 'ISO 3166-1 numeric':'531',                 'name':u'Curaçao', },
                'cy':{  'ISO 3166-1 alpha-2':'CY',  'ISO 3166-1 alpha-3':'CYP', 'ISO 3166-1 numeric':'196',                 'name':u'Cyprus', },
                'cz':{  'ISO 3166-1 alpha-2':'CZ',  'ISO 3166-1 alpha-3':'CZE', 'ISO 3166-1 numeric':'203',                 'name':u'Czech Republic', },
                'dk':{  'ISO 3166-1 alpha-2':'DK',  'ISO 3166-1 alpha-3':'DNK', 'ISO 3166-1 numeric':'208', 'sfID':143458,  'name':u'Denmark', },
                'dj':{  'ISO 3166-1 alpha-2':'DJ',  'ISO 3166-1 alpha-3':'DJI', 'ISO 3166-1 numeric':'262',                 'name':u'Djibouti', },
                'dm':{  'ISO 3166-1 alpha-2':'DM',  'ISO 3166-1 alpha-3':'DMA', 'ISO 3166-1 numeric':'212',                 'name':u'Dominica', },
                'do':{  'ISO 3166-1 alpha-2':'DO',  'ISO 3166-1 alpha-3':'DOM', 'ISO 3166-1 numeric':'214',                 'name':u'Dominican Republic', },
                'ec':{  'ISO 3166-1 alpha-2':'EC',  'ISO 3166-1 alpha-3':'ECU', 'ISO 3166-1 numeric':'218',                 'name':u'Ecuador', },
                'eg':{  'ISO 3166-1 alpha-2':'EG',  'ISO 3166-1 alpha-3':'EGY', 'ISO 3166-1 numeric':'818',                 'name':u'Egypt', },
                'sv':{  'ISO 3166-1 alpha-2':'SV',  'ISO 3166-1 alpha-3':'SLV', 'ISO 3166-1 numeric':'222',                 'name':u'El Salvador', },
                'gq':{  'ISO 3166-1 alpha-2':'GQ',  'ISO 3166-1 alpha-3':'GNQ', 'ISO 3166-1 numeric':'226',                 'name':u'Equatorial Guinea', },
                'er':{  'ISO 3166-1 alpha-2':'ER',  'ISO 3166-1 alpha-3':'ERI', 'ISO 3166-1 numeric':'232',                 'name':u'Eritrea', },
                'ee':{  'ISO 3166-1 alpha-2':'EE',  'ISO 3166-1 alpha-3':'EST', 'ISO 3166-1 numeric':'233',                 'name':u'Estonia', },
                'et':{  'ISO 3166-1 alpha-2':'ET',  'ISO 3166-1 alpha-3':'ETH', 'ISO 3166-1 numeric':'231',                 'name':u'Ethiopia', },
                'fk':{  'ISO 3166-1 alpha-2':'FK',  'ISO 3166-1 alpha-3':'FLK', 'ISO 3166-1 numeric':'238',                 'name':u'Falkland Islands (Malvinas)', },
                'fo':{  'ISO 3166-1 alpha-2':'FO',  'ISO 3166-1 alpha-3':'FRO', 'ISO 3166-1 numeric':'234',                 'name':u'Faroe Islands', },
                'fj':{  'ISO 3166-1 alpha-2':'FJ',  'ISO 3166-1 alpha-3':'FJI', 'ISO 3166-1 numeric':'242',                 'name':u'Fiji', },
                'fi':{  'ISO 3166-1 alpha-2':'FI',  'ISO 3166-1 alpha-3':'FIN', 'ISO 3166-1 numeric':'246', 'sfID':143447,  'name':u'Finland', },
                'fr':{  'ISO 3166-1 alpha-2':'FR',  'ISO 3166-1 alpha-3':'FRA', 'ISO 3166-1 numeric':'250', 'sfID':143442,  'name':u'France', },
                'gf':{  'ISO 3166-1 alpha-2':'GF',  'ISO 3166-1 alpha-3':'GUF', 'ISO 3166-1 numeric':'254',                 'name':u'French Guiana', },
                'pf':{  'ISO 3166-1 alpha-2':'PF',  'ISO 3166-1 alpha-3':'PYF', 'ISO 3166-1 numeric':'258',                 'name':u'French Polynesia', },
                'tf':{  'ISO 3166-1 alpha-2':'TF',  'ISO 3166-1 alpha-3':'ATF', 'ISO 3166-1 numeric':'260',                 'name':u'French Southern Territories', },
                'ga':{  'ISO 3166-1 alpha-2':'GA',  'ISO 3166-1 alpha-3':'GAB', 'ISO 3166-1 numeric':'266',                 'name':u'Gabon', },
                'gm':{  'ISO 3166-1 alpha-2':'GM',  'ISO 3166-1 alpha-3':'GMB', 'ISO 3166-1 numeric':'270',                 'name':u'Gambia', },
                'ge':{  'ISO 3166-1 alpha-2':'GE',  'ISO 3166-1 alpha-3':'GEO', 'ISO 3166-1 numeric':'268',                 'name':u'Georgia', },
                'de':{  'ISO 3166-1 alpha-2':'DE',  'ISO 3166-1 alpha-3':'DEU', 'ISO 3166-1 numeric':'276', 'sfID':143443,  'name':u'Germany', },
                'gh':{  'ISO 3166-1 alpha-2':'GH',  'ISO 3166-1 alpha-3':'GHA', 'ISO 3166-1 numeric':'288',                 'name':u'Ghana', },
                'gi':{  'ISO 3166-1 alpha-2':'GI',  'ISO 3166-1 alpha-3':'GIB', 'ISO 3166-1 numeric':'292',                 'name':u'Gibraltar', },
                'gr':{  'ISO 3166-1 alpha-2':'GR',  'ISO 3166-1 alpha-3':'GRC', 'ISO 3166-1 numeric':'300', 'sfID':143448,  'name':u'Greece', },
                'gl':{  'ISO 3166-1 alpha-2':'GL',  'ISO 3166-1 alpha-3':'GRL', 'ISO 3166-1 numeric':'304',                 'name':u'Greenland', },
                'gd':{  'ISO 3166-1 alpha-2':'GD',  'ISO 3166-1 alpha-3':'GRD', 'ISO 3166-1 numeric':'308',                 'name':u'Grenada', },
                'gp':{  'ISO 3166-1 alpha-2':'GP',  'ISO 3166-1 alpha-3':'GLP', 'ISO 3166-1 numeric':'312',                 'name':u'Guadeloupe', },
                'gu':{  'ISO 3166-1 alpha-2':'GU',  'ISO 3166-1 alpha-3':'GUM', 'ISO 3166-1 numeric':'316',                 'name':u'Guam', },
                'gt':{  'ISO 3166-1 alpha-2':'GT',  'ISO 3166-1 alpha-3':'GTM', 'ISO 3166-1 numeric':'320',                 'name':u'Guatemala', },
                'gg':{  'ISO 3166-1 alpha-2':'GG',  'ISO 3166-1 alpha-3':'GGY', 'ISO 3166-1 numeric':'831',                 'name':u'Guernsey', },
                'gn':{  'ISO 3166-1 alpha-2':'GN',  'ISO 3166-1 alpha-3':'GIN', 'ISO 3166-1 numeric':'324',                 'name':u'Guinea', },
                'gw':{  'ISO 3166-1 alpha-2':'GW',  'ISO 3166-1 alpha-3':'GNB', 'ISO 3166-1 numeric':'624',                 'name':u'Guinea-Bissau', },
                'gy':{  'ISO 3166-1 alpha-2':'GY',  'ISO 3166-1 alpha-3':'GUY', 'ISO 3166-1 numeric':'328',                 'name':u'Guyana', },
                'ht':{  'ISO 3166-1 alpha-2':'HT',  'ISO 3166-1 alpha-3':'HTI', 'ISO 3166-1 numeric':'332',                 'name':u'Haiti', },
                'hm':{  'ISO 3166-1 alpha-2':'HM',  'ISO 3166-1 alpha-3':'HMD', 'ISO 3166-1 numeric':'334',                 'name':u'Heard Island and McDonald Islands', },
                'va':{  'ISO 3166-1 alpha-2':'VA',  'ISO 3166-1 alpha-3':'VAT', 'ISO 3166-1 numeric':'336',                 'name':u'Holy See (Vatican City State)', },
                'hn':{  'ISO 3166-1 alpha-2':'HN',  'ISO 3166-1 alpha-3':'HND', 'ISO 3166-1 numeric':'340',                 'name':u'Honduras', },
                'hk':{  'ISO 3166-1 alpha-2':'HK',  'ISO 3166-1 alpha-3':'HKG', 'ISO 3166-1 numeric':'344',                 'name':u'Hong Kong', },
                'hu':{  'ISO 3166-1 alpha-2':'HU',  'ISO 3166-1 alpha-3':'HUN', 'ISO 3166-1 numeric':'348',                 'name':u'Hungary', },
                'is':{  'ISO 3166-1 alpha-2':'IS',  'ISO 3166-1 alpha-3':'ISL', 'ISO 3166-1 numeric':'352',                 'name':u'Iceland', },
                'in':{  'ISO 3166-1 alpha-2':'IN',  'ISO 3166-1 alpha-3':'IND', 'ISO 3166-1 numeric':'356',                 'name':u'India', },
                'id':{  'ISO 3166-1 alpha-2':'ID',  'ISO 3166-1 alpha-3':'IDN', 'ISO 3166-1 numeric':'360',                 'name':u'Indonesia', },
                'ir':{  'ISO 3166-1 alpha-2':'IR',  'ISO 3166-1 alpha-3':'IRN', 'ISO 3166-1 numeric':'364',                 'name':u'Iran, Islamic Republic of', },
                'iq':{  'ISO 3166-1 alpha-2':'IQ',  'ISO 3166-1 alpha-3':'IRQ', 'ISO 3166-1 numeric':'368',                 'name':u'Iraq', },
                'ie':{  'ISO 3166-1 alpha-2':'IE',  'ISO 3166-1 alpha-3':'IRL', 'ISO 3166-1 numeric':'372', 'sfID':143449,  'name':u'Ireland', },
                'im':{  'ISO 3166-1 alpha-2':'IM',  'ISO 3166-1 alpha-3':'IMN', 'ISO 3166-1 numeric':'833',                 'name':u'Isle of Man', },
                'il':{  'ISO 3166-1 alpha-2':'IL',  'ISO 3166-1 alpha-3':'ISR', 'ISO 3166-1 numeric':'376',                 'name':u'Israel', },
                'it':{  'ISO 3166-1 alpha-2':'IT',  'ISO 3166-1 alpha-3':'ITA', 'ISO 3166-1 numeric':'380', 'sfID':143450,  'name':u'Italy', },
                'jm':{  'ISO 3166-1 alpha-2':'JM',  'ISO 3166-1 alpha-3':'JAM', 'ISO 3166-1 numeric':'388',                 'name':u'Jamaica', },
                'jp':{  'ISO 3166-1 alpha-2':'JP',  'ISO 3166-1 alpha-3':'JPN', 'ISO 3166-1 numeric':'392', 'sfID':143462,  'name':u'Japan', },
                'je':{  'ISO 3166-1 alpha-2':'JE',  'ISO 3166-1 alpha-3':'JEY', 'ISO 3166-1 numeric':'832',                 'name':u'Jersey', },
                'jo':{  'ISO 3166-1 alpha-2':'JO',  'ISO 3166-1 alpha-3':'JOR', 'ISO 3166-1 numeric':'400',                 'name':u'Jordan', },
                'kz':{  'ISO 3166-1 alpha-2':'KZ',  'ISO 3166-1 alpha-3':'KAZ', 'ISO 3166-1 numeric':'398',                 'name':u'Kazakhstan', },
                'ke':{  'ISO 3166-1 alpha-2':'KE',  'ISO 3166-1 alpha-3':'KEN', 'ISO 3166-1 numeric':'404',                 'name':u'Kenya', },
                'ki':{  'ISO 3166-1 alpha-2':'KI',  'ISO 3166-1 alpha-3':'KIR', 'ISO 3166-1 numeric':'296',                 'name':u'Kiribati', },
                'kp':{  'ISO 3166-1 alpha-2':'KP',  'ISO 3166-1 alpha-3':'PRK', 'ISO 3166-1 numeric':'408',                 'name':u'Korea, Democratic People\'s Republic of', },
                'kr':{  'ISO 3166-1 alpha-2':'KR',  'ISO 3166-1 alpha-3':'KOR', 'ISO 3166-1 numeric':'410',                 'name':u'Korea, Republic of', },
                'kw':{  'ISO 3166-1 alpha-2':'KW',  'ISO 3166-1 alpha-3':'KWT', 'ISO 3166-1 numeric':'414',                 'name':u'Kuwait', },
                'kg':{  'ISO 3166-1 alpha-2':'KG',  'ISO 3166-1 alpha-3':'KGZ', 'ISO 3166-1 numeric':'417',                 'name':u'Kyrgyzstan', },
                'la':{  'ISO 3166-1 alpha-2':'LA',  'ISO 3166-1 alpha-3':'LAO', 'ISO 3166-1 numeric':'418',                 'name':u'Lao People\'s Democratic Republic', },
                'lv':{  'ISO 3166-1 alpha-2':'LV',  'ISO 3166-1 alpha-3':'LVA', 'ISO 3166-1 numeric':'428',                 'name':u'Latvia', },
                'lb':{  'ISO 3166-1 alpha-2':'LB',  'ISO 3166-1 alpha-3':'LBN', 'ISO 3166-1 numeric':'422',                 'name':u'Lebanon', },
                'ls':{  'ISO 3166-1 alpha-2':'LS',  'ISO 3166-1 alpha-3':'LSO', 'ISO 3166-1 numeric':'426',                 'name':u'Lesotho', },
                'lr':{  'ISO 3166-1 alpha-2':'LR',  'ISO 3166-1 alpha-3':'LBR', 'ISO 3166-1 numeric':'430',                 'name':u'Liberia', },
                'ly':{  'ISO 3166-1 alpha-2':'LY',  'ISO 3166-1 alpha-3':'LBY', 'ISO 3166-1 numeric':'434',                 'name':u'Libyan Arab Jamahiriya', },
                'li':{  'ISO 3166-1 alpha-2':'LI',  'ISO 3166-1 alpha-3':'LIE', 'ISO 3166-1 numeric':'438',                 'name':u'Liechtenstein', },
                'lt':{  'ISO 3166-1 alpha-2':'LT',  'ISO 3166-1 alpha-3':'LTU', 'ISO 3166-1 numeric':'440',                 'name':u'Lithuania', },
                'lu':{  'ISO 3166-1 alpha-2':'LU',  'ISO 3166-1 alpha-3':'LUX', 'ISO 3166-1 numeric':'442', 'sfID':143451,  'name':u'Luxembourg', },
                'mo':{  'ISO 3166-1 alpha-2':'MO',  'ISO 3166-1 alpha-3':'MAC', 'ISO 3166-1 numeric':'446',                 'name':u'Macao', },
                'mk':{  'ISO 3166-1 alpha-2':'MK',  'ISO 3166-1 alpha-3':'MKD', 'ISO 3166-1 numeric':'807',                 'name':u'Macedonia, the former Yugoslav Republic of', },
                'mg':{  'ISO 3166-1 alpha-2':'MG',  'ISO 3166-1 alpha-3':'MDG', 'ISO 3166-1 numeric':'450',                 'name':u'Madagascar', },
                'mw':{  'ISO 3166-1 alpha-2':'MW',  'ISO 3166-1 alpha-3':'MWI', 'ISO 3166-1 numeric':'454',                 'name':u'Malawi', },
                'my':{  'ISO 3166-1 alpha-2':'MY',  'ISO 3166-1 alpha-3':'MYS', 'ISO 3166-1 numeric':'458',                 'name':u'Malaysia', },
                'mv':{  'ISO 3166-1 alpha-2':'MV',  'ISO 3166-1 alpha-3':'MDV', 'ISO 3166-1 numeric':'462',                 'name':u'Maldives', },
                'ml':{  'ISO 3166-1 alpha-2':'ML',  'ISO 3166-1 alpha-3':'MLI', 'ISO 3166-1 numeric':'466',                 'name':u'Mali', },
                'mt':{  'ISO 3166-1 alpha-2':'MT',  'ISO 3166-1 alpha-3':'MLT', 'ISO 3166-1 numeric':'470',                 'name':u'Malta', },
                'mh':{  'ISO 3166-1 alpha-2':'MH',  'ISO 3166-1 alpha-3':'MHL', 'ISO 3166-1 numeric':'584',                 'name':u'Marshall Islands', },
                'mq':{  'ISO 3166-1 alpha-2':'MQ',  'ISO 3166-1 alpha-3':'MTQ', 'ISO 3166-1 numeric':'474',                 'name':u'Martinique', },
                'mr':{  'ISO 3166-1 alpha-2':'MR',  'ISO 3166-1 alpha-3':'MRT', 'ISO 3166-1 numeric':'478',                 'name':u'Mauritania', },
                'mu':{  'ISO 3166-1 alpha-2':'MU',  'ISO 3166-1 alpha-3':'MUS', 'ISO 3166-1 numeric':'480',                 'name':u'Mauritius', },
                'yt':{  'ISO 3166-1 alpha-2':'YT',  'ISO 3166-1 alpha-3':'MYT', 'ISO 3166-1 numeric':'175',                 'name':u'Mayotte', },
                'mx':{  'ISO 3166-1 alpha-2':'MX',  'ISO 3166-1 alpha-3':'MEX', 'ISO 3166-1 numeric':'484',                 'name':u'Mexico', },
                'fm':{  'ISO 3166-1 alpha-2':'FM',  'ISO 3166-1 alpha-3':'FSM', 'ISO 3166-1 numeric':'583',                 'name':u'Micronesia, Federated States of', },
                'md':{  'ISO 3166-1 alpha-2':'MD',  'ISO 3166-1 alpha-3':'MDA', 'ISO 3166-1 numeric':'498',                 'name':u'Moldova, Republic of', },
                'mc':{  'ISO 3166-1 alpha-2':'MC',  'ISO 3166-1 alpha-3':'MCO', 'ISO 3166-1 numeric':'492',                 'name':u'Monaco', },
                'mn':{  'ISO 3166-1 alpha-2':'MN',  'ISO 3166-1 alpha-3':'MNG', 'ISO 3166-1 numeric':'496',                 'name':u'Mongolia', },
                'me':{  'ISO 3166-1 alpha-2':'ME',  'ISO 3166-1 alpha-3':'MNE', 'ISO 3166-1 numeric':'499',                 'name':u'Montenegro', },
                'ms':{  'ISO 3166-1 alpha-2':'MS',  'ISO 3166-1 alpha-3':'MSR', 'ISO 3166-1 numeric':'500',                 'name':u'Montserrat', },
                'ma':{  'ISO 3166-1 alpha-2':'MA',  'ISO 3166-1 alpha-3':'MAR', 'ISO 3166-1 numeric':'504',                 'name':u'Morocco', },
                'mz':{  'ISO 3166-1 alpha-2':'MZ',  'ISO 3166-1 alpha-3':'MOZ', 'ISO 3166-1 numeric':'508',                 'name':u'Mozambique', },
                'mm':{  'ISO 3166-1 alpha-2':'MM',  'ISO 3166-1 alpha-3':'MMR', 'ISO 3166-1 numeric':'104',                 'name':u'Myanmar', },
                'na':{  'ISO 3166-1 alpha-2':'NA',  'ISO 3166-1 alpha-3':'NAM', 'ISO 3166-1 numeric':'516',                 'name':u'Namibia', },
                'nr':{  'ISO 3166-1 alpha-2':'NR',  'ISO 3166-1 alpha-3':'NRU', 'ISO 3166-1 numeric':'520',                 'name':u'Nauru', },
                'np':{  'ISO 3166-1 alpha-2':'NP',  'ISO 3166-1 alpha-3':'NPL', 'ISO 3166-1 numeric':'524',                 'name':u'Nepal', },
                'nl':{  'ISO 3166-1 alpha-2':'NL',  'ISO 3166-1 alpha-3':'NLD', 'ISO 3166-1 numeric':'528', 'sfID':143452,  'name':u'Netherlands', },
                'nc':{  'ISO 3166-1 alpha-2':'NC',  'ISO 3166-1 alpha-3':'NCL', 'ISO 3166-1 numeric':'540',                 'name':u'New Caledonia', },
                'nz':{  'ISO 3166-1 alpha-2':'NZ',  'ISO 3166-1 alpha-3':'NZL', 'ISO 3166-1 numeric':'554', 'sfID':143461,  'name':u'New Zealand', },
                'ni':{  'ISO 3166-1 alpha-2':'NI',  'ISO 3166-1 alpha-3':'NIC', 'ISO 3166-1 numeric':'558',                 'name':u'Nicaragua', },
                'ne':{  'ISO 3166-1 alpha-2':'NE',  'ISO 3166-1 alpha-3':'NER', 'ISO 3166-1 numeric':'562',                 'name':u'Niger', },
                'ng':{  'ISO 3166-1 alpha-2':'NG',  'ISO 3166-1 alpha-3':'NGA', 'ISO 3166-1 numeric':'566',                 'name':u'Nigeria', },
                'nu':{  'ISO 3166-1 alpha-2':'NU',  'ISO 3166-1 alpha-3':'NIU', 'ISO 3166-1 numeric':'570',                 'name':u'Niue', },
                'nf':{  'ISO 3166-1 alpha-2':'NF',  'ISO 3166-1 alpha-3':'NFK', 'ISO 3166-1 numeric':'574',                 'name':u'Norfolk Island', },
                'mp':{  'ISO 3166-1 alpha-2':'MP',  'ISO 3166-1 alpha-3':'MNP', 'ISO 3166-1 numeric':'580',                 'name':u'Northern Mariana Islands', },
                'no':{  'ISO 3166-1 alpha-2':'NO',  'ISO 3166-1 alpha-3':'NOR', 'ISO 3166-1 numeric':'578', 'sfID':143457,  'name':u'Norway', },
                'om':{  'ISO 3166-1 alpha-2':'OM',  'ISO 3166-1 alpha-3':'OMN', 'ISO 3166-1 numeric':'512',                 'name':u'Oman', },
                'pk':{  'ISO 3166-1 alpha-2':'PK',  'ISO 3166-1 alpha-3':'PAK', 'ISO 3166-1 numeric':'586',                 'name':u'Pakistan', },
                'pw':{  'ISO 3166-1 alpha-2':'PW',  'ISO 3166-1 alpha-3':'PLW', 'ISO 3166-1 numeric':'585',                 'name':u'Palau', },
                'ps':{  'ISO 3166-1 alpha-2':'PS',  'ISO 3166-1 alpha-3':'PSE', 'ISO 3166-1 numeric':'275',                 'name':u'Palestinian Territory, Occupied', },
                'pa':{  'ISO 3166-1 alpha-2':'PA',  'ISO 3166-1 alpha-3':'PAN', 'ISO 3166-1 numeric':'591',                 'name':u'Panama', },
                'pg':{  'ISO 3166-1 alpha-2':'PG',  'ISO 3166-1 alpha-3':'PNG', 'ISO 3166-1 numeric':'598',                 'name':u'Papua New Guinea', },
                'py':{  'ISO 3166-1 alpha-2':'PY',  'ISO 3166-1 alpha-3':'PRY', 'ISO 3166-1 numeric':'600',                 'name':u'Paraguay', },
                'pe':{  'ISO 3166-1 alpha-2':'PE',  'ISO 3166-1 alpha-3':'PER', 'ISO 3166-1 numeric':'604',                 'name':u'Peru', },
                'ph':{  'ISO 3166-1 alpha-2':'PH',  'ISO 3166-1 alpha-3':'PHL', 'ISO 3166-1 numeric':'608',                 'name':u'Philippines', },
                'pn':{  'ISO 3166-1 alpha-2':'PN',  'ISO 3166-1 alpha-3':'PCN', 'ISO 3166-1 numeric':'612',                 'name':u'Pitcairn', },
                'pl':{  'ISO 3166-1 alpha-2':'PL',  'ISO 3166-1 alpha-3':'POL', 'ISO 3166-1 numeric':'616',                 'name':u'Poland', },
                'pt':{  'ISO 3166-1 alpha-2':'PT',  'ISO 3166-1 alpha-3':'PRT', 'ISO 3166-1 numeric':'620', 'sfID':143453,  'name':u'Portugal', },
                'pr':{  'ISO 3166-1 alpha-2':'PR',  'ISO 3166-1 alpha-3':'PRI', 'ISO 3166-1 numeric':'630',                 'name':u'Puerto Rico', },
                'qa':{  'ISO 3166-1 alpha-2':'QA',  'ISO 3166-1 alpha-3':'QAT', 'ISO 3166-1 numeric':'634',                 'name':u'Qatar', },
                're':{  'ISO 3166-1 alpha-2':'RE',  'ISO 3166-1 alpha-3':'REU', 'ISO 3166-1 numeric':'638',                 'name':u'Réunion', },
                'ro':{  'ISO 3166-1 alpha-2':'RO',  'ISO 3166-1 alpha-3':'ROU', 'ISO 3166-1 numeric':'642',                 'name':u'Romania', },
                'ru':{  'ISO 3166-1 alpha-2':'RU',  'ISO 3166-1 alpha-3':'RUS', 'ISO 3166-1 numeric':'643',                 'name':u'Russian Federation', },
                'rw':{  'ISO 3166-1 alpha-2':'RW',  'ISO 3166-1 alpha-3':'RWA', 'ISO 3166-1 numeric':'646',                 'name':u'Rwanda', },
                'bl':{  'ISO 3166-1 alpha-2':'BL',  'ISO 3166-1 alpha-3':'BLM', 'ISO 3166-1 numeric':'652',                 'name':u'Saint Barthélemy', },
                'sh':{  'ISO 3166-1 alpha-2':'SH',  'ISO 3166-1 alpha-3':'SHN', 'ISO 3166-1 numeric':'654',                 'name':u'Saint Helena, Ascension and Tristan da Cunha', },
                'kn':{  'ISO 3166-1 alpha-2':'KN',  'ISO 3166-1 alpha-3':'KNA', 'ISO 3166-1 numeric':'659',                 'name':u'Saint Kitts and Nevis', },
                'lc':{  'ISO 3166-1 alpha-2':'LC',  'ISO 3166-1 alpha-3':'LCA', 'ISO 3166-1 numeric':'662',                 'name':u'Saint Lucia', },
                'mf':{  'ISO 3166-1 alpha-2':'MF',  'ISO 3166-1 alpha-3':'MAF', 'ISO 3166-1 numeric':'663',                 'name':u'Saint Martin (French part)', },
                'pm':{  'ISO 3166-1 alpha-2':'PM',  'ISO 3166-1 alpha-3':'SPM', 'ISO 3166-1 numeric':'666',                 'name':u'Saint Pierre and Miquelon', },
                'vc':{  'ISO 3166-1 alpha-2':'VC',  'ISO 3166-1 alpha-3':'VCT', 'ISO 3166-1 numeric':'670',                 'name':u'Saint Vincent and the Grenadines', },
                'ws':{  'ISO 3166-1 alpha-2':'WS',  'ISO 3166-1 alpha-3':'WSM', 'ISO 3166-1 numeric':'882',                 'name':u'Samoa', },
                'sm':{  'ISO 3166-1 alpha-2':'SM',  'ISO 3166-1 alpha-3':'SMR', 'ISO 3166-1 numeric':'674',                 'name':u'San Marino', },
                'st':{  'ISO 3166-1 alpha-2':'ST',  'ISO 3166-1 alpha-3':'STP', 'ISO 3166-1 numeric':'678',                 'name':u'Sao Tome and Principe', },
                'sa':{  'ISO 3166-1 alpha-2':'SA',  'ISO 3166-1 alpha-3':'SAU', 'ISO 3166-1 numeric':'682',                 'name':u'Saudi Arabia', },
                'sn':{  'ISO 3166-1 alpha-2':'SN',  'ISO 3166-1 alpha-3':'SEN', 'ISO 3166-1 numeric':'686',                 'name':u'Senegal', },
                'rs':{  'ISO 3166-1 alpha-2':'RS',  'ISO 3166-1 alpha-3':'SRB', 'ISO 3166-1 numeric':'688',                 'name':u'Serbia', },
                'sc':{  'ISO 3166-1 alpha-2':'SC',  'ISO 3166-1 alpha-3':'SYC', 'ISO 3166-1 numeric':'690',                 'name':u'Seychelles', },
                'sl':{  'ISO 3166-1 alpha-2':'SL',  'ISO 3166-1 alpha-3':'SLE', 'ISO 3166-1 numeric':'694',                 'name':u'Sierra Leone', },
                'sg':{  'ISO 3166-1 alpha-2':'SG',  'ISO 3166-1 alpha-3':'SGP', 'ISO 3166-1 numeric':'702',                 'name':u'Singapore', },
                'sx':{  'ISO 3166-1 alpha-2':'SX',  'ISO 3166-1 alpha-3':'SXM', 'ISO 3166-1 numeric':'534',                 'name':u'Sint Maarten (Dutch part)', },
                'sk':{  'ISO 3166-1 alpha-2':'SK',  'ISO 3166-1 alpha-3':'SVK', 'ISO 3166-1 numeric':'703',                 'name':u'Slovakia', },
                'si':{  'ISO 3166-1 alpha-2':'SI',  'ISO 3166-1 alpha-3':'SVN', 'ISO 3166-1 numeric':'705',                 'name':u'Slovenia', },
                'sb':{  'ISO 3166-1 alpha-2':'SB',  'ISO 3166-1 alpha-3':'SLB', 'ISO 3166-1 numeric':'090',                 'name':u'Solomon Islands', },
                'so':{  'ISO 3166-1 alpha-2':'SO',  'ISO 3166-1 alpha-3':'SOM', 'ISO 3166-1 numeric':'706',                 'name':u'Somalia', },
                'za':{  'ISO 3166-1 alpha-2':'ZA',  'ISO 3166-1 alpha-3':'ZAF', 'ISO 3166-1 numeric':'710',                 'name':u'South Africa', },
                'gs':{  'ISO 3166-1 alpha-2':'GS',  'ISO 3166-1 alpha-3':'SGS', 'ISO 3166-1 numeric':'239',                 'name':u'South Georgia and the South Sandwich Islands', },
                'es':{  'ISO 3166-1 alpha-2':'ES',  'ISO 3166-1 alpha-3':'ESP', 'ISO 3166-1 numeric':'724', 'sfID':143454,  'name':u'Spain', },
                'lk':{  'ISO 3166-1 alpha-2':'LK',  'ISO 3166-1 alpha-3':'LKA', 'ISO 3166-1 numeric':'144',                 'name':u'Sri Lanka', },
                'sd':{  'ISO 3166-1 alpha-2':'SD',  'ISO 3166-1 alpha-3':'SDN', 'ISO 3166-1 numeric':'736',                 'name':u'Sudan', },
                'sr':{  'ISO 3166-1 alpha-2':'SR',  'ISO 3166-1 alpha-3':'SUR', 'ISO 3166-1 numeric':'740',                 'name':u'Suriname', },
                'sj':{  'ISO 3166-1 alpha-2':'SJ',  'ISO 3166-1 alpha-3':'SJM', 'ISO 3166-1 numeric':'744',                 'name':u'Svalbard and Jan Mayen', },
                'sz':{  'ISO 3166-1 alpha-2':'SZ',  'ISO 3166-1 alpha-3':'SWZ', 'ISO 3166-1 numeric':'748',                 'name':u'Swaziland', },
                'se':{  'ISO 3166-1 alpha-2':'SE',  'ISO 3166-1 alpha-3':'SWE', 'ISO 3166-1 numeric':'752', 'sfID':143456,  'name':u'Sweden', },
                'ch':{  'ISO 3166-1 alpha-2':'CH',  'ISO 3166-1 alpha-3':'CHE', 'ISO 3166-1 numeric':'756', 'sfID':143459,  'name':u'Switzerland', },
                'sy':{  'ISO 3166-1 alpha-2':'SY',  'ISO 3166-1 alpha-3':'SYR', 'ISO 3166-1 numeric':'760',                 'name':u'Syrian Arab Republic', },
                'tw':{  'ISO 3166-1 alpha-2':'TW',  'ISO 3166-1 alpha-3':'TWN', 'ISO 3166-1 numeric':'158',                 'name':u'Taiwan, Province of China', },
                'tj':{  'ISO 3166-1 alpha-2':'TJ',  'ISO 3166-1 alpha-3':'TJK', 'ISO 3166-1 numeric':'762',                 'name':u'Tajikistan', },
                'tz':{  'ISO 3166-1 alpha-2':'TZ',  'ISO 3166-1 alpha-3':'TZA', 'ISO 3166-1 numeric':'834',                 'name':u'Tanzania, United Republic of', },
                'th':{  'ISO 3166-1 alpha-2':'TH',  'ISO 3166-1 alpha-3':'THA', 'ISO 3166-1 numeric':'764',                 'name':u'Thailand', },
                'tl':{  'ISO 3166-1 alpha-2':'TL',  'ISO 3166-1 alpha-3':'TLS', 'ISO 3166-1 numeric':'626',                 'name':u'Timor-Leste', },
                'tg':{  'ISO 3166-1 alpha-2':'TG',  'ISO 3166-1 alpha-3':'TGO', 'ISO 3166-1 numeric':'768',                 'name':u'Togo', },
                'tk':{  'ISO 3166-1 alpha-2':'TK',  'ISO 3166-1 alpha-3':'TKL', 'ISO 3166-1 numeric':'772',                 'name':u'Tokelau', },
                'to':{  'ISO 3166-1 alpha-2':'TO',  'ISO 3166-1 alpha-3':'TON', 'ISO 3166-1 numeric':'776',                 'name':u'Tonga', },
                'tt':{  'ISO 3166-1 alpha-2':'TT',  'ISO 3166-1 alpha-3':'TTO', 'ISO 3166-1 numeric':'780',                 'name':u'Trinidad and Tobago', },
                'tn':{  'ISO 3166-1 alpha-2':'TN',  'ISO 3166-1 alpha-3':'TUN', 'ISO 3166-1 numeric':'788',                 'name':u'Tunisia', },
                'tr':{  'ISO 3166-1 alpha-2':'TR',  'ISO 3166-1 alpha-3':'TUR', 'ISO 3166-1 numeric':'792',                 'name':u'Turkey', },
                'tm':{  'ISO 3166-1 alpha-2':'TM',  'ISO 3166-1 alpha-3':'TKM', 'ISO 3166-1 numeric':'795',                 'name':u'Turkmenistan', },
                'tc':{  'ISO 3166-1 alpha-2':'TC',  'ISO 3166-1 alpha-3':'TCA', 'ISO 3166-1 numeric':'796',                 'name':u'Turks and Caicos Islands', },
                'tv':{  'ISO 3166-1 alpha-2':'TV',  'ISO 3166-1 alpha-3':'TUV', 'ISO 3166-1 numeric':'798',                 'name':u'Tuvalu', },
                'ug':{  'ISO 3166-1 alpha-2':'UG',  'ISO 3166-1 alpha-3':'UGA', 'ISO 3166-1 numeric':'800',                 'name':u'Uganda', },
                'ua':{  'ISO 3166-1 alpha-2':'UA',  'ISO 3166-1 alpha-3':'UKR', 'ISO 3166-1 numeric':'804',                 'name':u'Ukraine', },
                'ae':{  'ISO 3166-1 alpha-2':'AE',  'ISO 3166-1 alpha-3':'ARE', 'ISO 3166-1 numeric':'784',                 'name':u'United Arab Emirates', },
                'gb':{  'ISO 3166-1 alpha-2':'GB',  'ISO 3166-1 alpha-3':'GBR', 'ISO 3166-1 numeric':'826', 'sfID':143444,  'name':u'United Kingdom', },
                'us':{  'ISO 3166-1 alpha-2':'US',  'ISO 3166-1 alpha-3':'USA', 'ISO 3166-1 numeric':'840', 'sfID':143441,  'name':u'United States', },
                'um':{  'ISO 3166-1 alpha-2':'UM',  'ISO 3166-1 alpha-3':'UMI', 'ISO 3166-1 numeric':'581',                 'name':u'United States Minor Outlying Islands', },
                'uy':{  'ISO 3166-1 alpha-2':'UY',  'ISO 3166-1 alpha-3':'URY', 'ISO 3166-1 numeric':'858',                 'name':u'Uruguay', },
                'uz':{  'ISO 3166-1 alpha-2':'UZ',  'ISO 3166-1 alpha-3':'UZB', 'ISO 3166-1 numeric':'860',                 'name':u'Uzbekistan', },
                'vu':{  'ISO 3166-1 alpha-2':'VU',  'ISO 3166-1 alpha-3':'VUT', 'ISO 3166-1 numeric':'548',                 'name':u'Vanuatu', },
                've':{  'ISO 3166-1 alpha-2':'VE',  'ISO 3166-1 alpha-3':'VEN', 'ISO 3166-1 numeric':'862',                 'name':u'Venezuela, Bolivarian Republic of', },
                'vn':{  'ISO 3166-1 alpha-2':'VN',  'ISO 3166-1 alpha-3':'VNM', 'ISO 3166-1 numeric':'704',                 'name':u'Viet Nam', },
                'vg':{  'ISO 3166-1 alpha-2':'VG',  'ISO 3166-1 alpha-3':'VGB', 'ISO 3166-1 numeric':'092',                 'name':u'Virgin Islands, British', },
                'vi':{  'ISO 3166-1 alpha-2':'VI',  'ISO 3166-1 alpha-3':'VIR', 'ISO 3166-1 numeric':'850',                 'name':u'Virgin Islands, U.S.', },
                'wf':{  'ISO 3166-1 alpha-2':'WF',  'ISO 3166-1 alpha-3':'WLF', 'ISO 3166-1 numeric':'876',                 'name':u'Wallis and Futuna', },
                'eh':{  'ISO 3166-1 alpha-2':'EH',  'ISO 3166-1 alpha-3':'ESH', 'ISO 3166-1 numeric':'732',                 'name':u'Western Sahara', },
                'ye':{  'ISO 3166-1 alpha-2':'YE',  'ISO 3166-1 alpha-3':'YEM', 'ISO 3166-1 numeric':'887',                 'name':u'Yemen', },
                'zm':{  'ISO 3166-1 alpha-2':'ZM',  'ISO 3166-1 alpha-3':'ZMB', 'ISO 3166-1 numeric':'894',                 'name':u'Zambia', },
                'zw':{  'ISO 3166-1 alpha-2':'ZW',  'ISO 3166-1 alpha-3':'ZWE', 'ISO 3166-1 numeric':'716',                 'name':u'Zimbabwe', },
            },
        },
    },
    'namespace':{
        'system.job':{
            'default':{
                'keyword':None,
                'plural':None,
                'auto cast':True,
            },
            'synonym':['keyword'],
            'element':{
                'host':None,
                'language':None,
            },
        },
        'system.mongodb':{
            'default':{
                'keyword':None,
                'plural':None,
                'auto cast':True,
            },
            'synonym':['keyword'],
            'element':{
                'host':None,
                'database':{
                    'name':u'Database',
                    'keyword':u'database',
                    'type':'unicode',
                },
                'port':None,
                'username':{
                    'name':u'Username',
                    'keyword':u'username',
                    'type':'unicode',
                },
                'password':{
                    'name':u'Password',
                    'keyword':u'password',
                    'type':'unicode',
                },
                'mongodb url':{
                    'name':u'MongoDB URL',
                    'keyword':u'mongodb_url',
                    'type':'unicode',
                },
            },
            'rule':[
                'rule.mongodb.url',
            ],
        },
        'resource.hint':{
            'default':{
                'auto cast':True,
                'plural':None,
                'unescape xml':False,
            },
            'synonym':['keyword'],
            'element':{
            }
        },
        'resource.file.url':{
            'default':{
                'auto cast':True,
                'plural':None,
                'unescape xml':False,
                'mediainfo':None,
                'atom':None,
            },
            'synonym':['keyword'],
            'element':{
                'url':None,
                'scheme':None,
                'host':None,
                'path':None,
                'media kind':None,
                'directory':None,
                'file name':None,
                'kind':None,
                'language':None,
                'profile':None,
                'volume':None,
                'name':None,
                'simple name':None,
                'simple album':None,
                'simple tv show':None,
                'imdb movie id':None,
                'tmdb movie id':None,
                'track genealogy':None,
                'track position':None,
                'disk position':None,
                'volume relative path':None,
            },
            'rule':[
                'rule.resource.track.genealogy',
                'rule.resource.file.filename.canonic',
                'rule.path.relative.volume',
                'rule.path.canonic',
                'rule.path.implicit',
                'rule.path.cache',
            ],
        },
        'resource.decode.url':{
            'default':{
                'auto cast':True,
                'plural':None,
                'unescape xml':False,
                'atom':None,
            },
            'synonym':['keyword'],
            'element':{
                'directory':None,
                'file name':None,
                'profile':None,
                'language':None,
                'volume path':None,
                'kind':None,
                'media kind':None,
                'simple album':None,
                'simple tv show':None,
                'imdb movie id':None,
                'tmdb movie id':None,
                'disk position':None,
                'track position':None,
                'name':None,
            },
            'rule':[
                'rule.parse.directory',
                'rule.parse.filename',
            ],
        },
        'resource.crawl.meta':{
            'default':{
                'auto cast':True,
                'plural':None,
                'unescape xml':False,
                'mediainfo':None,
                'subler':None,
                'atom':None,
                'keyword':None,
            },
            'synonym':['mediainfo', 'keyword'],
            'element':{
                'kind':None,
                'profile':None,
                'volume':None,
                'language':None,
                'simple name':None,
                'imdb movie id':None,
                'tmdb movie id':None,
                'stream type':{
                    'mediainfo':'StreamKind',
                },
                'file size':{
                    'mediainfo':'FileSize',
                },
                'format':{
                    'mediainfo':'Format',
                },
                'modified date':{
                    'mediainfo':'File_Modified_Date',
                },
                'tag date':{
                    'mediainfo':'Tagged_Date',
                },
                'bit rate':{
                    'mediainfo':'OverallBitRate',
                },
                'duration':{
                    'mediainfo':'Duration',
                },
                'width':{
                    'mediainfo':'Width',
                    'format':'pixel',
                },
                'height':{
                    'mediainfo':'Height',
                    'format':'pixel',
                },
                'media kind':{
                    'mediainfo':'stik',
                    'subler':'Media Kind',
                },
                'track position':{
                    'mediainfo':'Track_Position',
                },
                'track total':{
                    'mediainfo':'Track_Position_Total',
                },
                'disk position':{
                    'mediainfo':'Part_Position',
                },
                'disk total':{
                    'mediainfo':'Part_Position_Total',
                },
                'track number':{
                    'subler':'Track #',
                },
                'disk number':{
                    'subler':'Disk #',
                },
                'tv season':{
                    'mediainfo':'tvsn',
                    'subler':'TV Season',
                },
                'tv episode':{
                    'mediainfo':'tves',
                    'subler':'TV Episode #',
                },
                'sort name':{
                    'mediainfo':'sonm',
                    'subler':'Sort Name',
                },
                'sort artist':{
                    'mediainfo':'soar',
                    'subler':'Sort Artist',
                },
                'sort album artist':{
                    'mediainfo':'soaa',
                    'subler':'Sort Album Artist',
                },
                'sort album':{
                    'mediainfo':'soal',
                    'subler':'Sort Album',
                },
                'sort composer':{
                    'mediainfo':'soco',
                    'subler':'Sort Composer',
                },
                'sort tv show':{
                    'mediainfo':'sosn',
                    'subler':'Sort TV Show',
                },
                'name':{
                    'mediainfo':'Title',
                    'subler':'Name',
                },
                'artist':{
                    'mediainfo':'Performer',
                    'subler':'Artist',
                },
                'album artist':{
                    'mediainfo':'Album_Performer',
                    'subler':'Album Artist',
                },
                'album':{
                    'mediainfo':'Album',
                    'subler':'Album',
                },
                'tv show':{
                    'mediainfo':'tvsh',
                    'subler':'TV Show',
                },
                'tv episode id':{
                    'mediainfo':'tven',
                    'subler':'TV Episode ID',
                },
                'tv network':{
                    'mediainfo':'tvnn',
                    'subler':'TV Network',
                },
                'grouping':{
                    'mediainfo':'Grouping',
                    'subler':'Grouping',
                },
                'composer':{
                    'mediainfo':'ScreenplayBy',
                    'subler':'Composer',
                },
                'comment':{
                    'mediainfo':'Comment',
                    'subler':'Comments',
                },
                'description':{
                    'mediainfo':'desc',
                    'subler':'Description',
                    'unescape xml':True,
                },
                'long description':{
                    'mediainfo':'ldes',
                    'subler':'Long Description',
                    'unescape xml':True,
                },
                'lyrics':{
                    'mediainfo':'lyr',
                    'subler':'Lyrics',
                    'unescape xml':True,
                },
                'copyright':{
                    'mediainfo':'Copyright',
                    'subler':'Copyright',
                },
                'encoding tool':{
                    # mediainfo seems to mix @enc and @too into Encoded_Application
                    'subler':'Encoding Tool',
                },
                'encoded by':{
                    # mediainfo seems to mix @enc and @too into Encoded_Application
                    'subler':'Encoded by',
                },
                'compilation':{
                    'mediainfo':'Compilation',
                },
                'tempo':{
                    'mediainfo':'BPM',
                    'subler':'Tempo',
                },
                'genre type':None,
                'genre':{
                    'mediainfo':'Genre',
                    'subler':'Genre',
                },
                'hd video':{
                    'mediainfo':'hdvd',
                    'subler':'HD Video',
                },
                'gapless':{
                    'subler':'Gapless',
                },
                'podcast':{
                    'mediainfo':'pcst',
                },
                'podcast url':None,
                'itunes keywords':{
                    'mediainfo':'keyw',
                },
                'itunes category':{
                    'mediainfo':'catg',
                },
                'xid':{
                    'mediainfo':'xid',
                    'subler':'XID',
                },
                'itunes content id':{
                    'mediainfo':'cnID',
                    'subler':'contentID',
                },
                'itunes account':{
                    'mediainfo':'apID',
                    'subler':'iTunes Account',
                },
                'itunes artist id':{
                    'mediainfo':'atID',
                },
                'itunes composer id':{
                    'mediainfo':'cmID',
                },
                'itunes playlist id':{
                    'mediainfo':'plID',
                },
                'itunes genre id':{
                    'mediainfo':'geID',
                },
                'itunes country id':{
                    'mediainfo':'sfID',
                },
                'itunes account type':{
                    'mediainfo':'akID',
                },
                'itunes episode global id':None,
                'rating standard':None,
                'rating':{
                    'subler':'Rating',
                },
                'rating score':None,
                'rating annotation':{
                    'subler':'Rating Annotation',
                },
                'purchase date':{
                    'mediainfo':'purd',
                    'subler':'Purchase Date',
                },
                'release date':{
                    'mediainfo':'Recorded_Date',
                    'subler':'Release Date',
                },
                'content rating':{
                    'mediainfo':'rtng',
                    'subler':'Content Rating',
                },
                'itunextc':{
                    'mediainfo':'iTunEXTC',
                },
                'itunmovi':{
                    'mediainfo':'iTunMOVI',
                },
                'cast':{
                    'subler':'Cast',
                },
                'directors':{
                    'subler':'Director',
                },
                'codirectors':{
                    'subler':'Codirectors',
                },
                'producers':{
                    'subler':'Producers',
                },
                'screenwriters':{
                    'subler':'Screenwriters',
                },
                'studio':{
                    'subler':'Studio',
                },
                'cover':{
                    'mediainfo':'Cover',
                    'auto cast':False,
                },
            },
            'rule':[
                'rule.knowlege.disk.number',
                'rule.knowlege.track.number',
                'rule.knowlege.default.track.total',
                'rule.knowlege.default.disk.total',
                'rule.knowlege.default.episode',
                'rule.knowlege.sort.name',
                'rule.knowlege.sort.artist',
                'rule.knowlege.sort.albumartist',
                'rule.knowlege.sort.album',
                'rule.knowlege.sort.composer',
                'rule.knowlege.sort.show',
                'rule.knowlege.artist.info',
                'rule.itunes.itunextc.parse',
                'rule.itunes.album.name',
            ],
        },
        
        'resource.crawl.stream.audio':{
            'default':{
                'auto cast':True,
                'plural':None,
                'unescape xml':False,
                'mediainfo':None,
                'atom':None,
            },
            'synonym':['mediainfo'],
            'element':{
                'stream id':{
                    'mediainfo':'ID',
                },
                'stream position':{
                    'mediainfo':'StreamKindPos',
                },
                'stream type':{
                    'mediainfo':'StreamKind',
                },
                'stream kind':None,
                'stream name':{
                    'mediainfo':'Title',
                },
                'language':{
                    'mediainfo':'Language_String3',
                },
                'default':{
                    'mediainfo':'Default',
                },
                'format':{
                    'mediainfo':'Format',
                },
                'format profile':{
                    'mediainfo':'Format_Profile',
                    'plural format':'mediainfo value list',
                },
                'channels':None,
                'channel count':{
                    'mediainfo':'Channel_s_',
                    'plural format':'mediainfo value list',
                },
                'channel position':{
                    'mediainfo':'ChannelPositions',
                    'plural format':'mediainfo value list',
                },
                'delay':{
                    'mediainfo':'Delay',
                },
                'duration':{
                    'mediainfo':'Duration',
                },
                'bit rate':{
                    'mediainfo':'BitRate',
                    'format':'bitrate',
                },
                'bit rate mode':{
                    'mediainfo':'BitRate_Mode',
                },
                'bit depth':{
                    'mediainfo':'BitDepth',
                    'format':'bit',
                },
                'stream size':{
                    'mediainfo':'StreamSize',
                    'format':'byte',
                },
                'stream portion':{
                    'mediainfo':'StreamSize_Proportion',
                },
                'sample rate':{
                    'mediainfo':'SamplingRate',
                    'format':'frequency',
                },
                'sample count':{
                    'mediainfo':'SamplingCount',
                },
                'dialnorm':{
                    'mediainfo':'dialnorm',
                },
                'encoded date':{
                    'mediainfo':'Encoded_Date',
                },
            },
            'rule':[
                'rule.stream.default.position',
                'rule.stream.default.id',
                'rule.stream.audio.kind',
            ],
        },
        'resource.crawl.stream.video':{
            'default':{
                'auto cast':True,
                'plural':None,
                'unescape xml':False,
                'mediainfo':None,
                'atom':None,
            },
            'synonym':['mediainfo'],
            'element':{
                'stream id':{
                    'mediainfo':'ID',
                },
                'stream position':{
                    'mediainfo':'StreamKindPos',
                },
                'stream type':{
                    'mediainfo':'StreamKind',
                },
                'stream kind':None,
                'stream name':{
                    'mediainfo':'Title',
                },
                'language':{
                    'mediainfo':'Language_String3',
                },
                'default':{
                    'mediainfo':'Default',
                },
                'format':{
                    'mediainfo':'Format',
                },
                'format profile':{
                    'mediainfo':'Format_Profile',
                    'plural format':'mediainfo value list',
                },
                'delay':{
                    'mediainfo':'Delay',
                },
                'duration':{
                    'mediainfo':'Duration',
                },
                'bit rate':{
                    'mediainfo':'BitRate',
                    'format':'bitrate',
                },
                'bit rate mode':{
                    'mediainfo':'BitRate_Mode',
                },
                'bit depth':{
                    'mediainfo':'BitDepth',
                    'format':'bit',
                },
                'stream size':{
                    'mediainfo':'StreamSize',
                    'format':'byte',
                },
                'stream portion':{
                    'mediainfo':'StreamSize_Proportion',
                },
                'width':{
                    'mediainfo':'Width',
                    'format':'pixel',
                },
                'height':{
                    'mediainfo':'Height',
                    'format':'pixel',
                },
                'pixel aspect ratio':{
                    'mediainfo':'PixelAspectRatio',
                },
                'display aspect ratio':{
                    'mediainfo':'DisplayAspectRatio',
                },
                'frame rate mode':{
                    'mediainfo':'FrameRate_Mode',
                },
                'frame rate':{
                    'mediainfo':'FrameRate',
                },
                'frame rate minimum':{
                    'mediainfo':'FrameRate_Minimum',
                },
                'frame rate maximum':{
                    'mediainfo':'FrameRate_Maximum',
                },
                'frame count':{
                    'mediainfo':'FrameCount',
                },
                'color space':{
                    'mediainfo':'ColorSpace',
                },
                'bpf':{
                    'mediainfo':'Bits-_Pixel_Frame_',
                },
                'encoder':{
                    'mediainfo':'Encoded_Library',
                },
                'encoder settings':{
                    'mediainfo':'Encoded_Library_Settings',
                    'plural':'dict',
                    'plural format':'mediainfo key value list',
                },
                'encoded date':{
                    'mediainfo':'Encoded_Date',
                },
                'primary':None,
            },
            'rule':[
                'rule.stream.default.position',
                'rule.stream.default.id',
                'rule.stream.video.kind',
            ],
        },
        'resource.crawl.stream.text':{
            'default':{
                'auto cast':True,
                'plural':None,
                'unescape xml':False,
                'mediainfo':None,
                'atom':None,
            },
            'synonym':['mediainfo'],
            'element':{
                'stream id':{
                    'mediainfo':'ID',
                },
                'stream position':{
                    'mediainfo':'StreamKindPos',
                },
                'stream type':{
                    'mediainfo':'StreamKind',
                },
                'stream kind':None,
                'stream name':{
                    'mediainfo':'Title',
                },
                'language':{
                    'mediainfo':'Language_String3',
                },
                'default':{
                    'mediainfo':'Default',
                },
                'format':{
                    'mediainfo':'Format',
                },
                'format profile':{
                    'mediainfo':'Format_Profile',
                    'plural format':'mediainfo value list',
                },
                'delay':{
                    'mediainfo':'Delay',
                },
                'duration':{
                    'mediainfo':'Duration',
                },
                'bit rate':{
                    'mediainfo':'BitRate',
                    'format':'bitrate',
                },
                'bit rate mode':{
                    'mediainfo':'BitRate_Mode',
                },
                'bit depth':{
                    'mediainfo':'BitDepth',
                    'format':'bit',
                },
                'stream size':{
                    'mediainfo':'StreamSize',
                    'format':'byte',
                },
                'stream portion':{
                    'mediainfo':'StreamSize_Proportion',
                },
                'encoded date':{
                    'mediainfo':'Encoded_Date',
                },
            },
            'rule':[
                'rule.stream.default.position',
                'rule.stream.default.id',
                'rule.stream.text.kind',
            ],
        },
        'resource.crawl.stream.image':{
            'default':{
                'auto cast':True,
                'plural':None,
                'unescape xml':False,
                'mediainfo':None,
                'atom':None,
            },
            'synonym':['mediainfo'],
            'element':{
                'stream id':{
                    'mediainfo':'ID',
                },
                'stream position':{
                    'mediainfo':'StreamKindPos',
                },
                'stream type':{
                    'mediainfo':'StreamKind',
                },
                'stream kind':None,
                'stream name':{
                    'mediainfo':'Title',
                },
                'language':{
                    'mediainfo':'Language_String3',
                },
                'format':{
                    'mediainfo':'Format',
                },
                'format profile':{
                    'mediainfo':'Format_Profile',
                    'plural format':'mediainfo value list',
                },
                'delay':{
                    'mediainfo':'Delay',
                },
                'duration':{
                    'mediainfo':'Duration',
                },
                'bit rate':{
                    'mediainfo':'BitRate',
                    'format':'bitrate',
                },
                'bit rate mode':{
                    'mediainfo':'BitRate_Mode',
                },
                'bit depth':{
                    'mediainfo':'BitDepth',
                    'format':'bit',
                },
                'stream size':{
                    'mediainfo':'StreamSize',
                    'format':'byte',
                },
                'stream portion':{
                    'mediainfo':'StreamSize_Proportion',
                },
                'width':{
                    'mediainfo':'Width',
                    'format':'pixel',
                },
                'height':{
                    'mediainfo':'Height',
                    'format':'pixel',
                },
                'encoded date':{
                    'mediainfo':'Encoded_Date',
                },
            },
            'rule':[
                'rule.stream.default.position',
                'rule.stream.default.id',
                'rule.stream.image.kind',
            ],
        },
        
        'knowlege.movie':{
            'default':{
                'keyword':None,
                'plural':None,
                'unescape xml':False,
                'auto cast':True,
            },
            'synonym':['keyword'],
            'element':{
                'movie id':{
                    'name':u'Movie ID',
                    'keyword':u'movie_id',
                    'type':'int',
                },
                'imdb movie id':{
                    'name':u'IMDb Movie ID',
                    'keyword':u'imdb_movie_id',
                    'type':'unicode',
                },
                'tmdb movie id':{
                    'name':u'TMDb Movie ID',
                    'keyword':u'tmdb_movie_id',
                    'type':'int',
                },
            },
        },
        'knowlege.tvshow.show':{
            'default':{
                'keyword':None,
                'plural':None,
                'unescape xml':False,
                'auto cast':True,
            },
            'synonym':['keyword'],
            'element':{
                'tv show id':{
                    'name':u'TV Show ID',
                    'keyword':u'tv_show_id',
                    'type':'int',
                },
            },
        },
        'knowlege.tvshow.season':{
            'default':{
                'keyword':None,
                'plural':None,
                'unescape xml':False,
                'auto cast':True,
            },
            'synonym':['keyword'],
            'element':{
                'tv show id':{
                    'name':u'TV Show ID',
                    'keyword':u'tv_show_id',
                    'type':'int',
                },
                'tv season':{
                    'name':u'TV Season',
                    'keyword':u'tv_season',
                    'type':'int',
                },
            },
        },
        'knowlege.tvshow.episode':{
            'default':{
                'keyword':None,
                'plural':None,
                'unescape xml':False,
                'auto cast':True,
            },
            'synonym':['keyword'],
            'element':{
                'tv show id':{
                    'name':u'TV Show ID',
                    'keyword':u'tv_show_id',
                    'type':'int',
                },
                'tv season':{
                    'name':u'TV Season',
                    'keyword':u'tv_season',
                    'type':'int',
                },
                'tv episode':{
                    'name':u'TV Episode',
                    'keyword':u'tv_episode',
                    'type':'int',
                },
            },
        },
        'knowlege.person':{
            'default':{
                'keyword':None,
                'plural':None,
                'unescape xml':False,
                'auto cast':True,
            },
            'synonym':['keyword'],
            'element':{
                'person id':{
                    'name':u'Person ID',
                    'keyword':u'person_id',
                    'type':'int',
                },
            },
        },
        'knowlege.network':{
            'default':{
                'keyword':None,
                'plural':None,
                'unescape xml':False,
                'auto cast':True,
            },
            'synonym':['keyword'],
            'element':{
                'network id':{
                    'name':u'Network ID',
                    'keyword':u'network_id',
                    'type':'int',
                },
            },
        },
        'knowlege.studio':{
            'default':{
                'auto cast':True,
                'plural':None,
                'unescape xml':False,
                'keyword':None,
            },
            'synonym':['keyword'],
            'element':{
                'studio id':{
                    'name':u'Studio ID',
                    'keyword':u'studio_id',
                    'type':'int',
                },
            },
        },
        'knowlege.job':{
            'default':{
                'auto cast':True,
                'plural':None,
                'unescape xml':False,
                'keyword':None,
            },
            'synonym':['keyword'],
            'element':{
                'job id':{
                    'name':u'Job ID',
                    'keyword':u'job_id',
                    'type':'int',
                },
            },
        },
        'knowlege.department':{
            'default':{
                'auto cast':True,
                'plural':None,
                'unescape xml':False,
                'keyword':None,
            },
            'synonym':['keyword'],
            'element':{
                'department id':{
                    'name':u'Department ID',
                    'keyword':u'department_id',
                    'type':'int',
                },
            },
        },
        'knowlege.genre':{
            'default':{
                'auto cast':True,
                'plural':None,
                'unescape xml':False,
                'keyword':None,
            },
            'synonym':['keyword'],
            'element':{
                'genre id':{
                    'name':u'Genre ID',
                    'keyword':u'genre_id',
                    'type':'int',
                },
            },
        },
        'tmdb.movie':{
            'default':{
                'keyword':None,
                'plural':None,
                'unescape xml':False,
                'auto cast':True,
                'tmdb':None,
            },
            'synonym':['keyword'],
            'element':{
                'tmdb movie id':{
                    'tmdb':'id',
                },
                'imdb movie id':{
                    'tmdb':'imdb_id',
                },
                'language':None,
            },
        },
        'tmdb.movie.cast':{
            'default':{
                'keyword':None,
                'plural':None,
                'unescape xml':False,
                'auto cast':True,
                'tmdb':None,
            },
            'synonym':['keyword'],
            'element':{},
        },
        'tmdb.movie.poster':{
            'default':{
                'keyword':None,
                'plural':None,
                'unescape xml':False,
                'auto cast':True,
                'tmdb':None,
            },
            'synonym':['keyword'],
            'element':{},
        },
        'tmdb.movie.keyword':{
            'default':{
                'keyword':None,
                'plural':None,
                'unescape xml':False,
                'auto cast':True,
                'tmdb':None,
            },
            'synonym':['keyword'],
            'element':{},
        },
        'tmdb.movie.release':{
            'default':{
                'keyword':None,
                'plural':None,
                'unescape xml':False,
                'auto cast':True,
                'tmdb':None,
            },
            'synonym':['keyword'],
            'element':{},
        },
        'tmdb.movie.trailer':{
            'default':{
                'keyword':None,
                'plural':None,
                'unescape xml':False,
                'auto cast':True,
                'tmdb':None,
            },
            'synonym':['keyword'],
            'element':{},
        },
        'tmdb.movie.translation':{
            'default':{
                'keyword':None,
                'plural':None,
                'unescape xml':False,
                'auto cast':True,
                'tmdb':None,
            },
            'synonym':['keyword'],
            'element':{},
        },
        'tmdb.movie.alternative':{
            'default':{
                'keyword':None,
                'plural':None,
                'unescape xml':False,
                'auto cast':True,
                'tmdb':None,
            },
            'synonym':['keyword'],
            'element':{},
        },
        'tmdb.person':{
            'default':{
                'keyword':None,
                'plural':None,
                'unescape xml':False,
                'auto cast':True,
                'tmdb':None,
            },
            'synonym':['keyword'],
            'element':{
                'tmdb person id':{
                    'tmdb':'id',
                },
            },
        },
        'tmdb.person.poster':{
            'default':{
                'keyword':None,
                'plural':None,
                'unescape xml':False,
                'auto cast':True,
                'tmdb':None,
            },
            'synonym':['keyword'],
            'element':{},
        },
        'tmdb.person.credit':{
            'default':{
                'keyword':None,
                'plural':None,
                'unescape xml':False,
                'auto cast':True,
                'tmdb':None,
            },
            'synonym':['keyword'],
            'element':{},
        },
        'tvdb.show.cast':{
            'default':{
                'auto cast':True,
                'plural':None,
                'unescape xml':False,
                'tvdb':None,
                'keyword':None,
            },
            'synonym':['tvdb', 'keyword'],
            'element':{
                'tvdb tv show id':None,
                'tvdb person id':{
                    'tvdb':'id',
                },
                'poster url':{
                    'tvdb':'Image',
                },
                'name':{
                    'tvdb':'Name',
                },
                'character':{
                    'tvdb':'Role',
                },
                'sort order':{
                    'name':u'Sort Order',
                    'keyword':u'sort_order',
                    'type':'int',
                    'tvdb':'SortOrder',
                },
            },
            'tag':u'Actor',
            'coalesce':True,
        },
        'tvdb.show.poster':{
            'default':{
                'auto cast':True,
                'plural':None,
                'unescape xml':False,
                'tvdb':None,
                'keyword':None,
            },
            'synonym':['tvdb', 'keyword'],
            'element':{
                'tvdb tv show id':None,
                'tvdb poster id':{
                    'tvdb':'id',
                },
                'tv season':{
                    'tvdb':'Season',
                },
                'language':{
                    'tvdb':'Language',
                },
                'poster url':{
                    'tvdb':'BannerPath',
                },
                'tvdb image context':{
                    # fanart, poster, season, series
                    'name':u'TVDb Poster Context',
                    'keyword':u'tvdb_poster_context',
                    'type':'unicode',
                    'tvdb':'BannerType',
                },
                'tvdb_poster_layout':{
                    # season, seasonwide, text, graphical, blank,
                    # 1920x1080, 1280x720, 680x1000
                    'name':u'TVDb Poster Layout',
                    'keyword':u'tvdb_poster_layout',
                    'type':'unicode',
                    'tvdb':'BannerType2',
                },
                'user rating':{
                    'tvdb':'Rating',
                },
                'user rating count':{
                    'tvdb':'RatingCount',
                },
                'contain tv show name':{
                    'name':u'Contain TV Show Name',
                    'keyword':u'contain_tv_show_name',
                    'type':'bool',
                    'tvdb':'SeriesName',
                },
                'color palette':{
                    'name':u'Color Palette',
                    'keyword':u'color_palette',
                    'type':'unicode',
                    'tvdb':'Colors',
                    'enabled':False,
                },
            },
            'tag':u'Banner',
            'coalesce':True,
        },
        'tvdb.show':{
            'default':{
                'auto cast':True,
                'plural':None,
                'unescape xml':False,
                'tvdb':None,
                'keyword':None,
            },
            'synonym':['tvdb', 'keyword'],
            'element':{
                'tvdb tv show id':{
                    'tvdb':'id',
                },
                'imdb tv show id':{
                    'tvdb':'IMDB_ID',
                },
                'zap2it tv show id':{
                    'tvdb':'zap2it_id',
                },
                'tv show':{
                    'tvdb':'SeriesName',
                },
                'modified date':{
                    'tvdb':'lastupdated',
                    # decode from int
                },
                'release date':{
                    'tvdb':'FirstAired',
                },
                'rating':{
                    'tvdb':'ContentRating',
                },
                'language':{
                    'tvdb':'Language',
                },
                'description':{
                    'tvdb':'Overview',
                    'unescape xml':True,
                },
                'user rating':{
                    'tvdb':'Rating',
                },
                'user rating count':{
                    'tvdb':'RatingCount',
                },
                'tv network':{
                    'tvdb':'Network',
                },
                'tv show runtime':{
                    'tvdb':'Runtime',
                },
                'tv show status':{
                    'tvdb':'Status',
                },
                'keywords':{
                    'tvdb':'Genre',
                    'plural format':'tvdb list',
                },
                'cast':{
                    'tvdb':'Actors',
                    'plural format':'tvdb list',
                },
                'poster url':{
                    'tvdb':'poster',
                },
                'banner url':{
                    'name':u'Banner URL',
                    'keyword':u'banner_url',
                    'type':'unicode',
                    'tvdb':'banner',
                },
                'fan art url':{
                    'name':u'Fan Art URL',
                    'keyword':u'fan_art_url',
                    'type':'unicode',
                    'tvdb':'fanart',
                },
                'tv show air day':{
                    'name':u'TV Show Air Day',
                    'keyword':u'tv_show_air_day',
                    'type':'unicode',
                    'tvdb':'Airs_DayOfWeek',
                    'enabled':False,
                },
                'tv show air time':{
                    'name':u'TV Show Air Time',
                    'keyword':u'tv_show_air_time',
                    'type':'time',
                    'tvdb':'Airs_Time',
                    'enabled':False,
                },
            },
            'tag':u'Series',
            'coalesce':False,
        },
        'tvdb.episode':{
            'default':{
                'auto cast':True,
                'plural':None,
                'unescape xml':False,
                'tvdb':None,
                'keyword':None,
            },
            'synonym':['tvdb', 'keyword'],
            'element':{
                'tvdb tv show id':{
                    'tvdb':'seriesid',
                },
                'tvdb tv season id':{
                    'tvdb':'seasonid',
                },
                'tvdb tv episode id':{
                    'tvdb':'id',
                },
                'tv season':{
                    'tvdb':'SeasonNumber',
                },
                'tv episode':{
                    'tvdb':'EpisodeNumber',
                },
                'name':{
                    'tvdb':'EpisodeName',
                },
                'absolute tv episode':{
                    'tvdb':'absolute_number',
                },
                'imdb tv episode id':{
                    'tvdb':'IMDB_ID',
                },
                'modified date':{
                    'tvdb':'lastupdated',
                    # decode from int
                },
                'language':{
                    'tvdb':'Language',
                },
                'release date':{
                    'tvdb':'FirstAired',
                },
                'description':{
                    'tvdb':'Overview',
                    'unescape xml':True,
                },
                'tv episode id':{
                    'tvdb':'ProductionCode',
                },
                'user rating':{
                    'tvdb':'Rating',
                },
                'user rating count':{
                    'tvdb':'RatingCount',
                },
                'poster url':{
                    'tvdb':'filename',
                },
                'cast':{
                    'tvdb':'GuestStars',
                    'plural format':'tvdb list',
                },
                'directors':{
                    'tvdb':'Director',
                    'plural format':'tvdb list',
                },
                'screenwriters':{
                    'tvdb':'Screenwriter',
                    'plural format':'tvdb list',
                },
                'tvdb poster flag':{
                    'name':u'TVDb Poster Flag',
                    'keyword':u'tvdb_poster_flag',
                    'type':'int',
                    'tvdb':'EpImgFlag',
                    'enabled':False,
                },
            },
            'tag':u'Episode',
            'coalesce':False,
        },
    },
    'rule':{
        'rule.system.default.routing':{
            'name':'Default volume and profile',
            'provide':set(('volume', 'profile',)),
        },
        'rule.system.default.enabled':{
            'name':'Default enabled bit',
            'provide':set(('enabled',)),
            'branch':[
                {
                    'apply':[
                        {'property':'enabled', 'value':True,},
                    ],
                },
            ],
        },
        'rule.mongodb.url':{
            'name':'MongoDB connection URL',
            'provide':set(('mongodb url',)),
            'branch':[
                {
                    'requires':set(('host', 'database', 'port', 'username', 'password')),
                    'apply':[
                        {
                            'property':'mongodb url',
                            'format':u'mongodb://{username}:{password}@{host}:{port}/{database}',
                        },
                    ],
                },
                {
                    'requires':set(('host', 'database', 'username', 'password')),
                    'apply':[
                        {
                            'property':'mongodb url',
                            'format':u'mongodb://{username}:{password}@{host}/{database}',
                        },
                    ],
                },
                {
                    'requires':set(('host', 'database', 'port')),
                    'apply':[
                        {
                            'property':'mongodb url',
                            'format':u'mongodb://{host}:{port}/{database}',
                        },
                    ],
                },
                {
                    'requires':set(('host', 'database')),
                    'apply':[
                        {
                            'property':'mongodb url',
                            'format':u'mongodb://{host}/{database}',
                        },
                    ],
                },
            ],
        },
        'rule.parse.directory':{
            'name':'Parse directory fragments',
            'provide':set((
                'volume path',
                'profile',
                'language',
            )),
            'branch':[
                {
                    'requires':set(('directory',)),
                    'match':{'property':'directory', 'expression':ur'^/.+/tvshow|music/[a-z0-9]{3,4}/[^/]{2,}/[^/]{2,}/[0-9]+(?:/[a-z]{2})?$', },
                    'decode':[
                        {
                            'property':'directory',
                            'expression':ur'^(?P<volume_path>/.+)/tvshow|music/[a-z0-9]{3,4}/(?P<profile>[^/]{2,})/[^/]{2,}/[0-9]+(?:/(?P<language>[a-z]{2}))?$',
                        },
                    ],
                },
                {
                    'requires':set(('directory',)),
                    'match':{'property':'directory', 'expression':ur'^/.+/movie/[a-z0-9]{3,4}/[^/]{2,}(?:/[a-z]{2})?$', },
                    'decode':[
                        {
                            'property':'directory',
                            'expression':ur'^(?P<volume_path>/.+)/movie/[a-z0-9]{3,4}/(?P<profile>[^/]{2,})(?:/(?P<language>[a-z]{2}))?$',
                        },
                    ],
                },
                {
                    'requires':set(('directory',)),
                    'match':{'property':'directory', 'expression':ur'^.*/[^/]{2,}/[^/]{2,}/[0-9]+(?:/[a-z]{2})?$', },
                    'decode':[
                        {
                            'property':'directory',
                            'expression':ur'^.*/(?P<profile>[^/]{2,})/[^/]{2,}/[0-9]+(?:/(?P<language>[a-z]{2}))?$',
                        },
                    ],
                },
                {
                    'requires':set(('directory',)),
                    'match':{'property':'directory', 'expression':ur'^.*/[^/]{2,}(?:/[a-z]{2})?$', },
                    'decode':[
                        {
                            'property':'directory',
                            'expression':ur'^.*/(?P<profile>[^/]{2,})(?:/(?P<language>[a-z]{2}))?$',
                        },
                    ],
                },
                {
                    'requires':set(('directory',)),
                    'match':{'property':'directory', 'expression':ur'^.*/[a-z]{2}$', },
                    'decode':[
                        {
                            'property':'directory',
                            'expression':ur'^.*/(?P<language>[a-z]{2})$',
                        },
                    ],
                },
            ],
        },
        'rule.parse.filename':{
            'name':'Parse file name',
            'provide':set((
                'kind',
                'media kind',
                'disk position',
                'track position',
                'imdb movie id',
                'tmdb movie id',
                'simple tv show',
                'simple album',
                'name',
            )),
            'branch':[
                {
                    'requires':set(('file name',)),
                    'match':{'property':'file name', 'expression':ur'^.{2,} s[0-9]+e[0-9]+(?: .*)?\.[^\.]{3,4}$', },
                    'decode':[
                        {'property':'file name', 'expression':ur'^(?P<simple_tv_show>.{2,}) s(?P<disk_position>[0-9]+)e(?P<track_position>[0-9]+)(?:\s*(?P<name>.*))?\.(?P<kind>[^\.]{3,4})$',},
                    ],
                    'apply':[
                        {'property':'media kind', 'value':u'tvshow',},
                    ],
                },
                {
                    'requires':set(('file name',)),
                    'match':{'property':'file name', 'expression':ur'^.{2,} d[0-9]+t[0-9]+(?: .*)?\.[^\.]{3,4}$', },
                    'decode':[
                        {'property':'file name', 'expression':ur'^(?P<simple_album>.{2,}) d(?P<disk_position>[0-9]+)t(?P<track_position>[0-9]+)(?:\s*(?P<name>.*))?\.(?P<kind>[^\.]{3,4})$',},
                    ],
                    'apply':[
                        {'property':'media kind', 'value':u'music',},
                    ],
                },
                {
                    'requires':set(('file name',)),
                    'match':{'property':'file name', 'expression':ur'^IMDbtt[0-9]+(?: .*)?\.[^\.]{3,4}$', },
                    'decode':[
                        {'property':'file name', 'expression':ur'^IMDb(?P<imdb_movie_id>tt[0-9]+)(?: (?P<name>.*))?\.(?P<kind>[^\.]{3,4})$',},
                    ],
                    'apply':[
                        {'property':'media kind', 'value':u'movie',},
                    ],
                },
                {
                    'requires':set(('file name',)),
                    'match':{'property':'file name', 'expression':ur'^TMDb[0-9]+(?: .*)?\.[^\.]{3,4}$', },
                    'decode':[
                        {'property':'file name', 'expression':ur'^TMDb(?P<tmdb_movie_id>[0-9]+)(?: (?P<name>.*))?\.(?P<kind>[^\.]{3,4})$',},
                    ],
                    'apply':[
                        {'property':'media kind', 'value':u'movie',},
                    ],
                },
            ],
        },
        'rule.resource.track.genealogy':{
            'name':'Compose the track genealogy',
            'provide':set(('track genealogy',)),
            'branch':[
                {
                    'requires':set(('media kind', 'disk position', 'track position')),
                    'equal':{'media kind':'tvshow', },
                    'apply':[
                        {
                            'property':'track genealogy',
                            'format':u's{disk position:02d}e{track position:02d}',
                        },
                    ],
                },
                {
                    'requires':set(('media kind', 'disk position', 'track position')),
                    'equal':{'media kind':'music', },
                    'apply':[
                        {
                            'property':'track genealogy',
                            'format':u'd{disk position:02d}t{track position:02d}',
                        },
                    ],
                },
            ],
        },
        'rule.resource.file.filename.canonic':{
            'name':'Compose a canonic file name',
            'provide':set(('canonic file name',)),
            'branch':[
                {
                    'requires':set(('media kind', 'simple tv show', 'track genealogy', 'simple name', 'kind')),
                    'equal':{'media kind':'tvshow', },
                    'apply':[
                        {
                            'property':'canonic file name',
                            'format':u'{simple tv show} {track genealogy} {simple name}.{kind}',
                        },
                    ],
                },
                {
                    'requires':set(('media kind', 'simple tv show', 'track genealogy', 'kind')),
                    'equal':{'media kind':'tvshow', },
                    'apply':[
                        {
                            'property':'canonic file name',
                            'format':u'{simple tv show} {track genealogy}.{kind}',
                        },
                    ],
                },
                {
                    'requires':set(('media kind', 'imdb movie id', 'simple name', 'kind')),
                    'equal':{'media kind':'movie', },
                    'apply':[
                        {
                            'property':'canonic file name',
                            'format':u'IMDb{imdb movie id} {simple name}.{kind}',
                        },
                    ],
                },
                {
                    'requires':set(('media kind', 'tmdb movie id', 'simple name', 'kind')),
                    'equal':{'media kind':'movie', },
                    'apply':[
                        {
                            'property':'canonic file name',
                            'format':u'TMDb{tmdb movie id} {simple name}.{kind}',
                        },
                    ],
                },
                {
                    'requires':set(('media kind', 'imdb movie id', 'kind')),
                    'equal':{'media kind':'movie', },
                    'apply':[
                        {
                            'property':'canonic file name',
                            'format':u'IMDb{imdb movie id}.{kind}',
                        },
                    ],
                },
                {
                    'requires':set(('media kind', 'tmdb movie id', 'kind')),
                    'equal':{'media kind':'movie', },
                    'apply':[
                        {
                            'property':'canonic file name',
                            'format':u'TMDb{tmdb movie id}.{kind}',
                        },
                    ],
                },
            ],
        },
        'rule.path.relative.volume':{
            'name':'volume relative path',
            'provide':set(('volume relative path',)),
            'branch':[
                {
                    'requires':set(('media kind', 'kind', 'profile', 'simple tv show', 'disk position', 'language', 'canonic file name')),
                    'equal':{'media kind':'tvshow', },
                    'apply':[
                        {
                            'property':'volume relative path',
                            'format':u'{media kind}/{kind}/{profile}/{simple tv show}/{disk position}/{language}/{canonic file name}',
                        },
                    ],
                },
                {
                    'requires':set(('media kind', 'kind', 'profile', 'simple tv show', 'disk position', 'canonic file name')),
                    'equal':{'media kind':'tvshow', },
                    'apply':[
                        {
                            'property':'volume relative path',
                            'format':u'{media kind}/{kind}/{profile}/{simple tv show}/{disk position}/{canonic file name}',
                        },
                    ],
                },
                {
                    'requires':set(('media kind', 'kind', 'profile', 'language', 'canonic file name')),
                    'equal':{'media kind':'movie', },
                    'apply':[
                        {
                            'property':'volume relative path',
                            'format':u'{media kind}/{kind}/{profile}/{language}/{canonic file name}',
                        },
                    ],
                },
                {
                    'requires':set(('media kind', 'kind', 'profile', 'canonic file name')),
                    'equal':{'media kind':'movie', },
                    'apply':[
                        {
                            'property':'volume relative path',
                            'format':u'{media kind}/{kind}/{profile}/{canonic file name}',
                        },
                    ],
                },
            ],
        },
        'rule.path.canonic':{
            'name':'canonic path',
            'provide':set(('canonic path',)),
            'branch':[
                {
                    'requires':set(('volume path', 'volume relative path')),
                    'apply':[
                        {
                            'property':'canonic path',
                            'format':u'{volume path}/{volume relative path}',
                        },
                    ],
                },
            ],
        },
        'rule.path.implicit':{
            'name':'implicit path',
            'provide':set(('path',)),
            'branch':[
                {
                    'requires':set(('canonic path',)),
                    'apply':[
                        {
                            'property':'path',
                            'format':u'{canonic path}',
                        },
                    ],
                },
            ],
        },
        'rule.path.cache':{
            'name':'Path in cache',
            'provide':set(('path in cache',)),
            'branch':[
                {
                    'requires':set(('cache root', 'host', 'volume', 'volume relative path')),
                    'apply':[
                        {
                            'property':'path in cache',
                            'format':u'{cache root}/{host}/{volume}/{volume relative path}',
                        },
                    ],
                },
                {
                    'requires':set(('cache root', 'host', 'path')),
                    'apply':[
                        {
                            'property':'path in cache',
                            'format':u'{cache root}/{host}{path}',
                        },
                    ],
                },
            ],
        },
        'rule.knowlege.track.number':{
            'name':'Compute the composite track number',
            'provide':set(('track number',)),
            'branch':[
                {
                    'requires':set(('media kind', 'track position', 'track total')),
                    'equal':{'media kind':'tvshow', },
                    'apply':[
                        { 'property':'track number', 'format':u'{track position} / {track total}', },
                    ],
                },
                {
                    'requires':set(('media kind', 'track position', 'track total')),
                    'equal':{'media kind':'music', },
                    'apply':[
                        { 'property':'track number', 'format':u'{track position} / {track total}', },
                    ],
                },
            ],
        },
        'rule.knowlege.disk.number':{
            'name':'Compute the composite disk number',
            'provide':set(('disk number',)),
            'branch':[
                {
                    'requires':set(('disk position', 'disk total')),
                    'equal':{'media kind':'tvshow', },
                    'apply':[
                        { 'property':'disk number', 'format':u'{disk position} / {disk total}', },
                    ],
                },
                {
                    'requires':set(('disk position', 'disk total')),
                    'equal':{'media kind':'music', },
                    'apply':[
                        { 'property':'disk number', 'format':u'{disk position} / {disk total}', },
                    ],
                },
            ],
        },
        'rule.knowlege.default.track.total':{
            'name':'Default track total',
            'provide':set(('track total',)),
            'branch':[
                {
                    'requires':set(('media kind',)),
                    'equal':{'media kind':'tvshow', },
                    'apply':[
                        {'property':'track total', 'value':0},
                    ],
                },
                {
                    'requires':set(('media kind',)),
                    'equal':{'media kind':'music', },
                    'apply':[
                        {'property':'track total', 'value':0},
                    ],
                },
            ],
        },
        'rule.knowlege.default.disk.total':{
            'name':'Default disk total',
            'provide':set(('disk total',)),
            'branch':[
                {
                    'requires':set(('media kind',)),
                    'equal':{'media kind':'tvshow', },
                    'apply':[
                        {'property':'disk total', 'value':0},
                    ],
                },
                {
                    'requires':set(('media kind',)),
                    'equal':{'media kind':'music', },
                    'apply':[
                        {'property':'disk total', 'value':0},
                    ],
                },
            ],
        },
        'rule.knowlege.default.episode':{
            'name':'Default TV episode number',
            'provide':set(('tv episode', 'tv season')),
            'branch':[
                {
                    'requires':set(('media kind', 'track position', 'disk position')),
                    'equal':{'media kind':'tvshow', },
                    'apply':[
                        { 'property':'tv episode', 'reference':'track position', },
                        { 'property':'tv season', 'reference':'disk position', },
                    ],
                },
            ],
        },
        'rule.knowlege.sort.name':{
            'name':'sort name',
            'provide':set(('sort name',)),
            'branch':[
                {
                    'requires':set(('name',)),
                    'decode':[
                        {'property':'name', 'expression':ur'^(the |a )?(?P<sort_name>.+)$', 'flags':re.IGNORECASE},
                    ],
                },
            ],
        },
        'rule.knowlege.sort.artist':{
            'name':'sort artist',
            'provide':set(('sort artist',)),
            'branch':[
                {
                    'requires':set(('artist',)),
                    'decode':[
                        {'property':'artist', 'expression':ur'^(the |a )?(?P<sort_artist>.+)$', 'flags':re.IGNORECASE},
                    ],
                },
            ],
        },
        'rule.knowlege.sort.albumartist':{
            'name':'sort album artist',
            'provide':set(('sort album artist',)),
            'branch':[
                {
                    'requires':set(('album artist',)),
                    'decode':[
                        {'property':'album artist', 'expression':ur'^(the |a )?(?P<sort_album_artist>.+)$', 'flags':re.IGNORECASE},
                    ],
                },
            ],
        },
        'rule.knowlege.sort.album':{
            'name':'sort album',
            'provide':set(('sort album',)),
            'branch':[
                {
                    'requires':set(('album',)),
                    'decode':[
                        {'property':'album', 'expression':ur'^(the |a )?(?P<sort_album>.+)$', 'flags':re.IGNORECASE},
                    ],
                },
            ],
        },
        'rule.knowlege.sort.composer':{
            'name':'sort composer',
            'provide':set(('sort composer',)),
            'branch':[
                {
                    'requires':set(('composer',)),
                    'decode':[
                        {'property':'composer', 'expression':ur'^(the |a )?(?P<sort_composer>.+)$', 'flags':re.IGNORECASE},
                    ],
                },
            ],
        },
        'rule.knowlege.sort.show':{
            'name':'sort tv show',
            'provide':set(('sort tv show',)),
            'branch':[
                {
                    'requires':set(('tv show',)),
                    'decode':[
                        {'property':'tv show', 'expression':ur'^(the |a )?(?P<sort_tv_show>.+)$', 'flags':re.IGNORECASE},
                    ],
                },
            ],
        },
        'rule.knowlege.artist.info':{
            'name':'artist information',
            'provide':set(('artist', 'album artist')),
            'branch':[
                {
                    'requires':set(('media kind', 'tv show')),
                    'equal':{'media kind':'tvshow', },
                    'apply':[
                        {
                            'property':'artist',
                            'format':u'{tv show}',
                        },
                        {
                            'property':'album artist',
                            'format':u'{tv show}',
                        },
                    ],
                },
                {
                    'requires':set(('media kind', 'directors')),
                    'equal':{'media kind':'movie', },
                    'apply':[
                        {
                            'property':'artist',
                            'format':u'{directors[0]}',
                        },
                        {
                            'property':'album artist',
                            'format':u'{directors[0]}',
                        },
                    ],
                },
                {
                    'requires':set(('media kind', 'producers')),
                    'equal':{'media kind':'movie', },
                    'apply':[
                        {
                            'property':'artist',
                            'format':u'{producers[0]}',
                        },
                        {
                            'property':'album artist',
                            'format':u'{producers[0]}',
                        },
                    ],
                },
                {
                    'requires':set(('media kind', 'screenwriters')),
                    'equal':{'media kind':'movie', },
                    'apply':[
                        {
                            'property':'artist',
                            'format':u'{screenwriters[0]}',
                        },
                        {
                            'property':'album artist',
                            'format':u'{screenwriters[0]}',
                        },
                    ],
                },
                {
                    'requires':set(('media kind', 'codirectors')),
                    'equal':{'media kind':'movie', },
                    'apply':[
                        {
                            'property':'artist',
                            'format':u'{codirectors[0]}',
                        },
                        {
                            'property':'album artist',
                            'format':u'{codirectors[0]}',
                        },
                    ],
                },
                {
                    'requires':set(('media kind', 'cast')),
                    'equal':{'media kind':'movie', },
                    'apply':[
                        {
                            'property':'artist',
                            'format':u'{cast[0]}',
                        },
                        {
                            'property':'album artist',
                            'format':u'{cast[0]}',
                        },
                    ],
                },
            ],
        },
        'rule.itunes.itunextc.parse':{
            'name':'Parse itunextc atom',
            'provide':set((
                'rating standard',
                'rating',
                'rating score',
                'rating annotation',
            )),
            'branch':[
                {
                    'requires':set(('itunextc',)),
                    'decode':[
                        {'property':'itunextc', 'expression':ur'(?P<rating_standard>[^|]+)\|(?P<rating>[^|]+)\|(?P<rating_score>[^|]+)\|(?P<rating_annotation>[^|]+)?',},
                    ],
                },
            ],
        },
        'rule.itunes.album.name':{
            'name':'Album name for iTunes',
            'provide':set(('album',)),
            'branch':[
                {
                    'requires':set(('media kind', 'tv show', 'tv season')),
                    'equal':{'media kind':'tvshow', },
                    'apply':[
                        {
                            'property':'album',
                            'format':u'{tv show}, Season {tv season}',
                        },
                    ],
                },
            ],
        },
        
        'rule.knowlege.asset.id':{
            'name':'asset id',
            'provide':set(('asset id',)),
            'branch':[
                {
                    'requires':set(('media kind', 'simple tv show', 'disk position', 'track position')),
                    'equal':{'media kind':'tvshow', },
                    'apply':[
                        {
                            'property':'asset id',
                            'format':u'{media kind}/{simple tv show}/{disk position}/{track position}',
                        },
                    ],
                },
                {
                    'requires':set(('media kind', 'simple album', 'disk position', 'track position')),
                    'equal':{'media kind':'music', },
                    'apply':[
                        {
                            'property':'asset id',
                            'format':u'{media kind}/{simple album}/{disk position}/{track position}',
                        },
                    ],
                },
                {
                    'requires':set(('media kind', 'imdb movie id',)),
                    'equal':{'media kind':'movie', },
                    'apply':[
                        {
                            'property':'asset id',
                            'format':u'{media kind}/imdb/{imdb movie id}',
                        },
                    ],
                },
                {
                    'requires':set(('media kind', 'tmdb movie id',)),
                    'equal':{'media kind':'movie', },
                    'apply':[
                        {
                            'property':'asset id',
                            'format':u'{media kind}/tmdb/{tmdb movie id}',
                        },
                    ],
                },
            ],
        },
        'rule.knowlege.resource.id':{
            'name':'resource id',
            'provide':set(('resource id',)),
            'branch':[
                {
                    'requires':set(('path', 'host')),
                    'apply':[
                        {
                            'property':'resource id',
                            'format':u'{host}:{path}',
                        },
                    ],
                },
            ],
        },
        'rule.knowlege.resource.uri':{
            'name':'uri',
            'provide':set(('uri',)),
            'branch':[
                {
                    'requires':set(('host', 'volume', 'volume relative path')),
                    'apply':[
                        {
                            'property':'uri',
                            'format':u'resource://{host}/{volume}/{volume relative path}',
                        },
                    ],
                },
            ],
        },
        'rule.knowlege.asset.name':{
            'name':'full name',
            'provide':set(('full name',)),
            'branch':[
                {
                    'requires':set(('media kind', 'tv show', 'tv episode id', 'name')),
                    'equal':{'media kind':'tvshow', },
                    'apply':[
                        {
                            'property':'full name',
                            'format':u'{tv show} {tv episode id} {name}',
                        },
                    ],
                },
                {
                    'requires':set(('media kind', 'tv show', 'tv episode id')),
                    'equal':{'media kind':'tvshow', },
                    'apply':[
                        {
                            'property':'full name',
                            'format':u'{tv show} {tv episode id}',
                        },
                    ],
                },
                {
                    'requires':set(('media kind', 'imdb movie id', 'name')),
                    'equal':{'media kind':'movie', },
                    'apply':[
                        {
                            'property':'full name',
                            'format':u'IMDb{imdb movie id} {name}',
                        },
                    ],
                },
                {
                    'requires':set(('media kind', 'imdb movie id')),
                    'equal':{'media kind':'movie', },
                    'apply':[
                        {
                            'property':'full name',
                            'format':u'IMDb{imdb movie id}',
                        },
                    ],
                },
            ],
        },
        'rule.stream.audio.name':{
            'name':'audio track name',
            'provide':set(('name',)),
            'branch':[
                {
                    'requires':set(('stream kind', 'channels')),
                    'equal':{'stream kind':'audio', 'channels':1 },
                    'apply':[
                        { 'property':'name', 'value':'Mono' },
                    ],
                },
                {
                    'requires':set(('stream kind', 'channels')),
                    'equal':{'stream kind':'audio', 'channels':2 },
                    'apply':[
                        { 'property':'name', 'value':'Stereo' },
                    ],
                },
                {
                    'requires':set(('stream kind', 'channels')),
                    'equal':{'stream kind':'audio', 'channels':3 },
                    'apply':[
                        { 'property':'name', 'value':'Stereo' },
                    ],
                },
                {
                    'requires':set(('stream kind', 'channels')),
                    'equal':{'stream kind':'audio', 'channels':4 },
                    'apply':[
                        { 'property':'name', 'value':'Quadraphonic' },
                    ],
                },
                {
                    'requires':set(('stream kind', 'channels')),
                    'equal':{'stream kind':'audio', 'channels':5 },
                    'apply':[
                        { 'property':'name', 'value':'Surround' },
                    ],
                },
                {
                    'requires':set(('stream kind', 'channels')),
                    'equal':{'stream kind':'audio', 'channels':6 },
                    'apply':[
                        { 'property':'name', 'value':'Surround' },
                    ],
                },
                {
                    'requires':set(('stream kind', 'channels')),
                    'equal':{'stream kind':'audio', 'channels':7 },
                    'apply':[
                        { 'property':'name', 'value':'Surround' },
                    ],
                },
                {
                    'requires':set(('stream kind', 'channels')),
                    'equal':{'stream kind':'audio', 'channels':8 },
                    'apply':[
                        { 'property':'name', 'value':'Surround' },
                    ],
                },
            ],
        },
        'rule.stream.default.position':{
            'name':'Default stream position',
            'provide':set(('stream position',)),
            'branch':[
                {
                    'apply':[
                        {'property':'stream position', 'value':1,},
                    ],
                },
            ],
        },
        'rule.stream.default.id':{
            'name':'Default stream id',
            'provide':set(('stream id',)),
            'branch':[
                {
                    'apply':[
                        {'property':'stream id', 'value':0,},
                    ],
                },
            ],
        },
        'rule.stream.audio.kind':{
            'name':'Kind for audio stream',
            'provide':set(('kind',)),
            'branch':[
                {
                    'requires':set(('format')),
                    'equal':{'format':'AC-3'},
                    'apply':[
                        { 'property':'kind', 'value':'ac3' },
                    ],
                },
                {
                    'requires':set(('format')),
                    'equal':{'format':'DTS'},
                    'apply':[
                        { 'property':'kind', 'value':'dts' },
                    ],
                },
                {
                    'requires':set(('format')),
                    'equal':{'format':'MPEG Audio'},
                    'apply':[
                        { 'property':'kind', 'value':'mp3' },
                    ],
                },
                {
                    'requires':set(('format')),
                    'equal':{'format':'AAC'},
                    'apply':[
                        { 'property':'kind', 'value':'aac' },
                    ],
                },
                {
                    'requires':set(('format')),
                    'equal':{'format':'PCM'},
                    'apply':[
                        { 'property':'kind', 'value':'pcm' },
                    ],
                },
                {
                    'requires':set(('format')),
                    'equal':{'format':'FLAC'},
                    'apply':[
                        { 'property':'kind', 'value':'flac' },
                    ],
                },
                {
                    'requires':set(('format')),
                    'equal':{'format':'Vorbis'},
                    'apply':[
                        { 'property':'kind', 'value':'ogg' },
                    ],
                },
            ],
        },
        'rule.stream.video.kind':{
            'name':'Kind for video stream',
            'provide':set(('kind',)),
            'branch':[
                {
                    'requires':set(('stream kind', 'format')),
                    'equal':{'stream kind':'video', 'format':'AVC'},
                    'apply':[
                        { 'property':'kind', 'value':'h264' },
                    ],
                },
                {
                    'requires':set(('stream kind', 'format')),
                    'equal':{'stream kind':'video', 'format':'MPEG-4 Visual'},
                    'apply':[
                        { 'property':'kind', 'value':'h263' },
                    ],
                },
            ],
        },
        'rule.stream.image.kind':{
            'name':'Kind for image stream',
            'provide':set(('kind',)),
            'branch':[
                {
                    'requires':set(('format')),
                    'equal':{'format':'LZ77'},
                    'apply':[
                        { 'property':'kind', 'value':'png' },
                    ],
                },
                {
                    'requires':set(('format')),
                    'equal':{'format':'JPEG'},
                    'apply':[
                        { 'property':'kind', 'value':'jpg' },
                    ],
                },
            ],
        },
        'rule.stream.text.kind':{
            'name':'Kind for text stream',
            'provide':set(('kind')),
            'branch':[
                {
                    'requires':set(('stream kind', 'format')),
                    'equal':{'stream kind':'caption', 'format':'Timed text'},
                    'apply':[
                        { 'property':'kind', 'value':'tx3g' },
                    ],
                },
                {
                    'requires':set(('stream kind', 'format')),
                    'equal':{'stream kind':'caption', 'format':'UTF-8'},
                    'apply':[
                        { 'property':'kind', 'value':'srt' },
                    ],
                },
                {
                    'requires':set(('stream kind', 'format')),
                    'equal':{'stream kind':'caption', 'format':'ASS'},
                    'apply':[
                        { 'property':'kind', 'value':'ass' },
                    ],
                },
                {
                    'requires':set(('stream kind')),
                    'equal':{'stream kind':'menu'},
                    'apply':[
                        { 'property':'kind', 'value':'chpl' },
                    ],
                },
            ],
        },
        
        'rule.url.tmdb.movie':{
            'name':'tmdb movie url',
            'provide':set(('tmdb movie url',)),
            'branch':[
                {
                    'requires':set(('host', 'tmdb movie id', 'language')),
                    'apply':[
                        {
                            'property':'tmdb movie url',
                            'format':u'resource://{host}/c/tmdb/movie/{language}/{tmdb movie id}',
                        },
                    ],
                },
            ],
        },
        'rule.url.tmdb.movie.cast':{
            'name':'tmdb movie cast url',
            'provide':set(('tmdb movie cast url',)),
            'branch':[
                {
                    'requires':set(('host', 'tmdb movie id')),
                    'apply':[
                        {
                            'property':'tmdb movie cast url',
                            'format':u'resource://{host}/c/tmdb/movie/{tmdb movie id}/cast',
                        },
                    ],
                },
            ],
        },
        'rule.url.tmdb.movie.poster':{
            'name':'tmdb movie poster url',
            'provide':set(('tmdb movie poster url',)),
            'branch':[
                {
                    'requires':set(('host', 'tmdb movie id')),
                    'apply':[
                        {
                            'property':'tmdb movie poster url',
                            'format':u'resource://{host}/c/tmdb/movie/{tmdb movie id}/poster',
                        },
                    ],
                },
            ],
        },
        'rule.url.tmdb.movie.keyword':{
            'name':'tmdb movie keyword url',
            'provide':set(('tmdb movie keyword url',)),
            'branch':[
                {
                    'requires':set(('host', 'tmdb movie id')),
                    'apply':[
                        {
                            'property':'tmdb movie keyword url',
                            'format':u'resource://{host}/c/tmdb/movie/{tmdb movie id}/keyword',
                        },
                    ],
                },
            ],
        },
        'rule.url.tmdb.movie.release':{
            'name':'tmdb movie release url',
            'provide':set(('tmdb movie release url',)),
            'branch':[
                {
                    'requires':set(('host', 'tmdb movie id')),
                    'apply':[
                        {
                            'property':'tmdb movie release url',
                            'format':u'resource://{host}/c/tmdb/movie/{tmdb movie id}/release',
                        },
                    ],
                },
            ],
        },
        'rule.url.tmdb.movie.trailer':{
            'name':'tmdb movie trailer url',
            'provide':set(('tmdb movie trailer url',)),
            'branch':[
                {
                    'requires':set(('host', 'tmdb movie id')),
                    'apply':[
                        {
                            'property':'tmdb movie trailer url',
                            'format':u'resource://{host}/c/tmdb/movie/{tmdb movie id}/trailer',
                        },
                    ],
                },
            ],
        },
        'rule.url.tmdb.movie.translation':{
            'name':'tmdb movie translation url',
            'provide':set(('tmdb movie translation url',)),
            'branch':[
                {
                    'requires':set(('host', 'tmdb movie id', 'language')),
                    'apply':[
                        {
                            'property':'tmdb movie translation url',
                            'format':u'resource://{host}/c/tmdb/movie/{tmdb movie id}/translation',
                        },
                    ],
                },
            ],
        },
        'rule.url.tmdb.movie.alternative url':{
            'name':'tmdb movie alternative url',
            'provide':set(('tmdb movie alternative url',)),
            'branch':[
                {
                    'requires':set(('host', 'tmdb movie id')),
                    'apply':[
                        {
                            'property':'tmdb movie alternative url',
                            'format':u'resource://{host}/c/tmdb/movie/{tmdb movie id}/alternative',
                        },
                    ],
                },
            ],
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
    ],
    'constant':{
        'empty string':u'',
        'hd threshold':720,
        'playback aspect ration':1920.0/1080.0,
        'space':u' ',
    },
    'command':[
        {'name':'rsync',        'binary':u'rsync', },
        {'name':'mv',           'binary':u'mv', },
        {'name':'handbrake',    'binary':u'HandbrakeCLI', },
        {'name':'subler',       'binary':u'SublerCLI', },
        {'name':'mkvmerge',     'binary':u'mkvmerge', },
        {'name':'mkvextract',   'binary':u'mkvextract', },
        {'name':'mp4file',      'binary':u'mp4file', },
        {'name':'mp4art',       'binary':u'mp4art', },
        {'name':'mediainfo',    'binary':u'mediainfo', },
        {'name':'ffmpeg',       'binary':u'ffmpeg', }
    ],
    'action':[
        {
            'name':'info',
            'depend':('mediainfo',),
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
            'language dependent':True,
        },
        'ass':{
            'container':'subtitles',
            'language dependent':True,
        },
        'chpl':{
            'container':'chapters',
            'language dependent':True,
        },
        'jpg':{
            'container':'image',
            'language dependent':True,
        },
        'png':{
            'container':'image',
            'language dependent':True,
        },
        'ac3':{
            'container':'raw audio',
            'language dependent':True,
        },
        'dts':{
            'container':'raw audio',
            'language dependent':True,
        },
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
    'subtitle filter':{
        'punctuation':{
            'scope':'line',
            'action':'replace',
            'ignore case':False,
            'expression':[
                (ur'^[-?\.,!:;"\'\s]+(.*)$', '\\1'),
                (ur'^(.*)[-?\.,!:;"\'\s]+$', '\\1'),
            ],
        },
        'leftover':{
            'scope':'line',
            'action':'drop',
            'ignore case':True,
            'expression':[
                ur'^\([^\)]+\)$',
                ur'^[\[\]\(\)]*$',
                ur'^[-?\.,!:;"\'\s]*$',
            ],
        },
        'hebrew noise':{
            'scope':'slide',
            'action':'drop',
            'ignore case':True,
            'expression':[
                ur':סנכרון',
                ur':תרגום',
                ur':שיפוץ',
                ur':לפרטים',
                ur'סונכרן',
                ur'תורגם על ידי',
                ur'תורגם חלקית',
                ur'סנכרן לגרסה זו',
                ur'תורגם ע"י',
                ur'שופץ ע"י',
                ur'תורגם משמיעה',
                ur'קריעה וסינכרון',
                ur'תוקן על ידי',
                ur'תורגם על-ידי',
                ur'תורגם ע"י',
                ur'תוקן ע"י',
                ur'הובא והוכן ע"י',
                ur'תורגם וסוכנרן',
                ur'תורגם וסונכרן',
                ur'תוקן קלות ע"י',
                ur'תרגום זה בוצע על ידי',
                ur'סונכרן לגירסא זו ע"י',
                ur'תרגום זה נעשה על ידי',
                ur'תורגם עם הרבה זיעה על ידי',
                ur'תורגם מספרדית ע"י אסף פארי',
                ur'כתוביות ע"י',
                ur'הגהה וסנכרון ע"י',
                ur'שנוכל להמשיך לתרגם',
                ur'הפרק מוקדש',
                ur'מצוות טורק',
                ur'shayx ע"י',
                ur'pusel :סנכרון',
                ur'תרגום: רותם ושמעון',
                ur'שיפוץ: השייח\' הסעודי',
                ur'שופץ ע"י השייח\' הסעודי',
                ur'תרגום: שמעון ורותם אברג\'יל',
                ur'כתובית זו הובאה',
                ur'שופצה, נערכה וסונכרנה לגרסה זו',
                ur'ברוכה הבאה אלוירה',
                ur'לצוות מתרגמי האוס',
                ur'אלוירה ברוכה הבאה',
                ur'עמוס נמני',
                ur'אינדיאנית שלי',
                ur'יומולדת שמח',
                ur'מוקדש לך',
                ur'מונחים רפואיים - ג\'ון דו',
                ur'מפורום תפוז',
                ur'מוקדש לפולי שלי',
                ur':כתוביות',
                ur'^בלעדית עבור$',
                ur'הורד מהאתר',
                ur'על ההגהה workbook',
                ur'מוקדש לכל אוהבי האוס אי שם',
                ur'theterminator נערך ותוקן בשיתוף עם',
                ur'התרגום נעשה על ידי המוריד',
                ur'תורגם וסונוכרן משמיעה ע"י',
                ur'\bצפייה מהנה\b',
                ur'\bצפיה מהנה\b',
                ur'נקרע ותוקן',
                ur'אבי דניאלי',
                ur'אוהבים את התרגומים שלנו',
                ur'נקלענו למאבק',
                ur'משפטי מתמשך',
                ur'לבילד המתקשה בהבנת קרדיטים',
                ur'אנא תרמו לנו כדי',
                ur'הגהה על-ידי',
                ur'^עריכה לשונית$',
                ur'^white fang-תרגום: עמית יקיר ו$',
                ur'ערן טלמור',
                ur'\bעדי-בלי-בצל\b',
                ur'\bבקרו אותנו בפורום\b',
                ur'הודה בוז',
                ur'\b-תודה מיוחדת ל\b',
                ur'^extreme מקבוצת$',
                ur'ialfan-ו mb0:עברית',
                ur'י ביצה קשה',
                ur'^ב$',
                ur'^בי$',
                ur'^ביצ$',
                ur'^ביצה$',
                ur'^ביצה ק$',
                ur'^ביצה קש$',
                ur'^ביצה קשה$',
                ur'ליונהארט',
                ur'\bמצוות פושל\b',
                ur'\bassem נקרע ע"י\b',
                ur'\bkawa: סנכרון\b',
                ur'אוהבת לנצח, שרון',
            ],
        },
        'noise':{
            'scope':'slide',
            'action':'drop',
            'ignore case':True,
            'expression':[
                ur'www\.allsubs\.org',
                ur'\bswsub\b',
                ur'\bresync\b',
                ur'\b[a-za-z0-9\.]+@gmail.\s*com\b',
                ur'cync\sby\slanmao',
                ur'www\.1000fr\.com',
                ur'www\.tvsubtitles\.net',
                ur'ytet-vicky8800',
                ur'www\.ydy\.com',
                ur'sync:gagegao',
                ur'frm-lanma',
                ur'nowa\swizja',
                ur'ssmink',
                ur'\blinx\b',
                ur'torec',
                ur'\byanx26\b',
                ur'\bgreenscorpion\b',
                ur'\bneotrix\b',
                ur'\bglfinish\b',
                ur'\bshloogy\b',
                ur'\.co\.il',
                ur'\by0natan\b',
                ur'\belad\b',
                ur'sratim',
                ur'donkey cr3w',
                ur'r-subs',
                ur'\[d-s\]',
                ur'ponkoit',
                ur'\bsubbie\b',
                ur'\bxsesa\b',
                ur'napisy pobrane',
                ur'\bphaelox\b',
                ur'divxstation',
                ur'\bpetabit\b',
                ur'\bronkey\b',
                ur'chococat3@walla',
                ur'warez',
                ur'\bdrsub\b',
                ur'\beliavgold\b',
                ur'^elvira$',
                ur'\blob93\b',
                ur'\belvir\b',
                ur'\boofir\b',
                ur'\bkrok\b',
                ur'\bqsubd\b',
                ur'\bariel046\b',
                ur'\bzipc\b',
                ur'\btecnodrom\b',
                ur'visiontext subtitles',
                ur'english sdh',
                ur'srulikg',
                ur'lh translators team',
                ur'[-=\s]+sub-zero[-=\s]+',
                ur'lionetwork',
                ur'^eric$',
                ur'subz3ro',
                ur'^david-z$',
                ur'drziv@yahoo',
                ur'elran_o',
                ur'mcsnagel',
                ur'\boutwit\b',
                ur'^gimly$',
                ur'\btinyurl\b',
                ur'\bfoxriver\b',
                ur'\bextremesubs\b',
                ur'megalomania tree',
                ur'xmonwow',
                ur'\bciwan\b',
                ur'\bnata4ever\b',
                ur'\byosefff\b',
                ur'\bhentaiman\b',
                ur'\bfoxi9\b',
                ur'\bgamby\b',
                ur'\bbrassica nigra\b',
                ur'\bqsubs\b',
                ur'\bsharetw\b',
                ur'\bserethd\b',
                ur'hazy7868',
                ur'subscenter\.org'
                ur'\blakota\b',
                ur'\bnzigi\b'
                ur'\bqwer90\b',
                ur'roni_eliav',
                ur'subscenter',
                ur'\bkuniva\b',
                ur'hdbits.org',
                ur'addic7ed',
                ur'hdsubs',
                ur'corrected by elderman',
            ],
        },
        'typo':{
            'scope':'line',
            'action':'replace',
            'ignore case':False,
            'expression':[
                (ur'♪', ''),
                (ur'¶', ''),
                (ur'\b +(,|\.|\?|%|!)\b', '\\1 '),
                (ur'\b(,|\.|\?|%|!) +\b', '\\1 '),
                (ur'\.\s*\.\s*\.\.?', '...'),
                (ur'</?[^>]+/?>', ''),
                (ur'\'{2}', '"'),
                (ur'\s+\)', ')'),
                (ur'\(\s+', '('),
                (ur'\s+\]', ']'),
                (ur'\[\s+', '['),
                (ur'\[[^\]]+\]\s*', ''),
                (ur'^[^\]]+\]', ''),
                (ur'\[[^\]]+$', ''),
                (ur'\([#a-zA-Z0-9l\s]+\)', ''),
                (ur'\([#a-zA-Z0-9l\s]+$', ''),
                (ur'^[#a-zA-Z0-9l\s]+\)', ''),
                (ur'^[-\s]+', ''),
                (ur'[-\s]+$', ''),
                (ur'\b^[-A-Z\s]+[0-9]*:\s*', ''),
                (ur'(?<=[a-zA-Z\'])I', 'l'),
                (ur'^[-\s]*$', ''),
            ],
        },
        'english typo':{
            'scope':'line',
            'action':'replace',
            'ignore case':False,
            'expression':[
                (ur'Theysaid', u'They said'),
                (ur'\bIast\b', u'last'),
                (ur'\bIook\b', u'look'),
                (ur'\bIetting\b', u'letting'),
                (ur'\bIet\b', u'let'),
                (ur'\bIooking\b', u'looking'),
                (ur'\bIife\b', u'life'),
                (ur'\bIeft\b', u'left'),
                (ur'\bIike\b', u'like'),
                (ur'\bIittle\b', u'little'),
                (ur'\bIadies\b', u'ladies'),
                (ur'\bIearn\b', u'learn'),
                (ur'\bIanded\b', u'landed'),
                (ur'\bIocked\b', u'locked'),
                (ur'\bIie\b', u'lie'),
                (ur'\bIong\b', u'long'),
                (ur'\bIine\b', u'line'),
                (ur'\bIives\b', u'lives'),
                (ur'\bIeave\b', u'leave'),
                (ur'\bIawyer\b', u'lawyer'),
                (ur'\bIogs\b', u'logs'),
                (ur'\bIack\b', u'lack'),
                (ur'\bIove\b', u'love'),
                (ur'\bIot\b', u'lot'),
                (ur'\bIanding\b', u'landing'),
                (ur'\bIet\'s\b', u'let\'s'),
                (ur'\bIand\b', u'land'),
                (ur'\bIying\b', u'lying'),
                (ur'\bIist\b', u'list'),
                (ur'\bIoved\b', u'loved'),
                (ur'\bIoss\b', u'loss'),
                (ur'\bIied\b', u'lied'),
                (ur'\bIaugh\b', u'laugh'),
                (ur'\b(h|H)avert\b', u'\\1aven\'t'),
                (ur'\b(w|W)asrt\b', u'\\1asn\'t'),
                (ur'\b(d|D)oesrt\b', u'\\1oesn\'t'),
                (ur'\b(d|D)ort\b', u'\\1on\'t'),
                (ur'\b(d|D)idrt\b', u'\\1idn\'t'),
                (ur'\b(a|A)irt\b', u'\\1in\'t'),
                (ur'\b(i|I)srt\b', u'\\1sn\'t'),
                (ur'\b(w|W)ort\b', u'\\1on\'t'),
                (ur'\b(c|C|w|W|s|S)ouldrt\b', u'\\1ouldn\'t'),
                (ur'\barert\b', u'aren\'t'),
                (ur'\bls\b', u'Is'),
                (ur'\b(L|l)f\b', u'If'),
                (ur'\blt\b', u'It'),
                (ur'\blt\'s\b', u'It\'s'),
                (ur'\bl\'m\b', u'I\'m'),
                (ur'\bl\'ll\b', u'I\'ll'),
                (ur'\bl\'ve\b', u'I\'ve'),
                (ur'\bl\b', u'I'),
                (ur'\bln\b', u'In'),
                (ur'\blmpossible\b', u'Impossible'),
                (ur'\bIight\b', u'light'),
                (ur'\bIevitation\b', u'levitation'),
                (ur'\bIeaving\b', u'leaving'),
                (ur'\bIooked\b', u'looked'),
                (ur'\bIucky\b', u'lucky'),
                (ur'\bIuck\b', u'luck'),
                (ur'\bIater\b', u'later'),
                (ur'\bIift\b', u'lift'),
                (ur'\bIip\b', u'lip'),
                (ur'\bIooks\b', u'looks'),
                (ur'\bIaid\b', u'laid'),
                (ur'\bIikely\b', u'likely'),
                (ur'\bIow\b', u'low'),
                (ur'\bIeast\b', u'least'),
                (ur'\bIeader\b', u'leader'),
                (ur'\bIocate\b', u'locate'),
                (ur'\bIaw\b', u'law'),
                (ur'\bIately\b', u'lately'),
                (ur'\bIiar\b', u'liar'),
                (ur'\bIate\b', u'late'),
                (ur'\bIonger\b', u'longer'),
                (ur'\bIive\b', u'live'),
            ],
        },
    },
}
