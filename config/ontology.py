# -*- coding: utf-8 -*-

ontology = {
    'prototype':[
        'character encoding':{
            'name':u'Character encoding',
            'keyword':u'character_encoding',
            'type':unicode,
        },
        'file path':{
            'name':u'File path',
            'keyword':u'file_path',
            'type':unicode,
        },
        'directory':{
            'name':u'Directory',
            'keyword':u'directory',
            'type':unicode,
        },
        'file name':{
            'name':u'File name',
            'keyword':u'file_name',
            'type':unicode,
        },
        'file size':{
            'name':u'File size',
            'keyword':u'file_size',
            'type':int,
            'format':'byte',
        },
        'profile':{
            'name':u'Profile',
            'keyword':u'profile',
            'type':unicode
        },
        'volume':{
            'name':u'Volume',
            'keyword':u'profile',
            'type':unicode
        },
        'kind':{
            'name':u'Kind',
            'keyword':u'kind',
            'type':unicode,
        },
        'tv show key':{
            'name':u'TV Show Key',
            'keyword':u'tv_show_key',
            'type':unicode,
        },
        'simple name':{
            'name':u'Simple Name',
            'keyword':u'simple_name',
            'type':unicode,
        },
        'tvdb tv show id':{
            'name':u'TVDb TV Show ID',
            'keyword':u'tvdb_tv_show_id',
            'type':int,
        },
        'tvdb tv season id':{
            'name':u'TVDb TV Season ID',
            'keyword':u'tvdb_tv_season_id',
            'type':int,
        },
        'tvdb tv episode id':{
            'name':u'TVDb TV Episode ID',
            'keyword':u'tvdb_tv_episode_id',
            'type':int,
        },
        'tvdb person id':{
            'name':u'TVDb Person ID',
            'keyword':u'tvdb_person_id',
            'type':int,
        },
        'tvdb poster id':{
            'name':u'TVDb Poster ID',
            'keyword':u'tvdb_poster_id',
            'type':int,
        }
        'imdb tv show id':{
            'name':u'IMDb TV Show ID',
            'keyword':u'imdb_tv_show_id',
            'type':unicode,
        },
        'imdb tv episode id':{
            'name':u'IMDb TV Episode ID',
            'keyword':u'imdb_tv_episode_id',
            'type':unicode,
        },
        'imdb movie id':{
            'name':u'IMDb Movie ID',
            'keyword':u'imdb_movie_id',
            'type':unicode
        },
        'tmdb movie id':{
            'name':u'TMDb Movie ID',
            'keyword':u'tmdb_movie_id',
            'type':int,
        },
        'tmdb person id':{
            'name':u'TMDb Person ID',
            'keyword':u'tmdb_person_id',
            'type':int,
        },
        'zap2it tv show id':{
            'name':u'Zap2It TV Show ID',
            'keyword':u'zap2it_tv_show_id',
            'type':unicode,
        },
        'keywords':{
            'name':u'Keywords',
            'keyword':u'keywords',
            'type':unicode,
            'plural':'list',
        },
        'tv show runtime':{
            'name':u'TV Show Runtime',
            'keyword':u'tv_show_runtime',
            'type':int,
        },
        'tv show status':{
            'name':u'TV Show Status',
            'keyword':u'tv_show_status',
            'type':unicode,
        },
        'user rating':{
            'name':u'User Rating',
            'keyword':u'user_rating',
            'type':float,
        },
        'user rating count':{
            'name':u'User Rating Count',
            'keyword':u'user_rating_count',
            'type':int,
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
            'type':unicode,
            'atom':'©nam',
        },
        'artist':{
            'name':u'Artist',
            'keyword':u'artist',
            'type':unicode,
            'atom':'@ART',
        },
        'composer':{
            'name':u'Composer',
            'keyword':u'composer',
            'type':unicode,
            'atom':'©wrt',
        },
        'album artist':{
            'name':u'Album Artist',
            'keyword':u'album_artist',
            'type':unicode,
            'atom':'aART',
        },
        'album':{
            'name':u'Album',
            'keyword':u'album',
            'type':unicode,
            'atom':'©alb',
        },
        'track #':{
            'name':u'Track',
            'keyword':u'track',
            'type':unicode,
            'atom':'trkn',
        },
        'disk #':{
            'name':u'Disk',
            'keyword':u'disk',
            'type':unicode,
            'atom':'disk',
        },
        'track position':{
            'name':u'Track Position',
            'keyword':u'track_position',
            'type':int,
            'atom':'trkn',
        },
        'track total':{
            'name':u'Track Total',
            'keyword':u'track_total',
            'type':int,
            'atom':'trkn',
        },
        'disk position':{
            'name':u'Disk Position',
            'keyword':u'disk_position',
            'type':int,
            'atom':'disk',
        },
        'disk total':{
            'name':u'Disk Total',
            'keyword':u'disk_total',
            'type':int,
            'atom':'disk',
        },
        'grouping':{
            'name':u'Grouping',
            'keyword':u'grouping',
            'type':unicode,
            'atom':'©grp',
        },
        'comment':{
            'name':u'Comment',
            'keyword':u'comment',
            'type':unicode,
            'atom':'©cmt',
        },
        'description':{
            'name':u'Description',
            'keyword':u'description',
            'type':unicode,
            'atom':'desc',
        },
        'long description':{
            'name':u'Long Description',
            'keyword':u'long_description',
            'type':unicode,
            'atom':'ldes',
        },
        'lyrics':{
            'name':u'Lyrics',
            'keyword':u'lyrics',
            'type':unicode,
            'atom':'©lyr',
        },
        'compilation':{
            'name':u'Compilation',
            'keyword':u'compilation',
            'type':bool,
            'atom':'cpil',
        },
        'copyright':{
            'name':u'Copyright',
            'keyword':u'copyright',
            'type':unicode,
            'atom':'cprt',
        },
        'tempo':{
            'name':u'Tempo',
            'keyword':u'tempo',
            'type':int,
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
            'type':unicode,
            'atom':'©gen',
        },
        'gapless':{
            'name':u'Gapless',
            'keyword':u'gapless',
            'type':bool
            'atom':'pgap',
        },
        'itunes keywords':{
            'name':u'iTunes Keywords',
            'keyword':u'itunes_keywords',
            'type':unicode,
            'atom':'keyw',
        },
        'itunes category':{
            'name':u'iTunes Category',
            'keyword':u'itunes_category',
            'type':unicode,
            'atom':'catg',
        },
        'hd video':{
            'name':u'HD Video',
            'keyword':u'hd_video',
            'type':bool
            'atom':'hdvd',
        },
        'tv show':{
            'name':u'TV Show',
            'keyword':u'tv_show',
            'type':unicode,
            'atom':'tvsh',
        },
        'tv episode id':{
            'name':u'TV Episode ID',
            'keyword':u'tv_episode_id',
            'type':unicode,
            'atom':'tven',
        },
        'tv season':{
            'name':u'TV Season',
            'keyword':u'tv_season',
            'type':int,
            'atom':'tvsn',
        },
        'tv episode':{
            'name':u'TV Episode',
            'keyword':u'tv_episode',
            'type':int,
            'atom':'tves',
        },
        'absolute tv episode':{
            'name':u'Absolute TV Episode',
            'keyword':'absolute_tv_episode'
            'type':int,
        },
        'tv network':{
            'name':u'TV Network',
            'keyword':u'tv_network',
            'type':unicode,
            'atom':'tvnn',
        },
        'sort name':{
            'name':u'Sort Name',
            'keyword':u'sort_name',
            'type':unicode,
            'atom':'sonm',
        },
        'sort artist':{
            'name':u'Sort Artist',
            'keyword':u'sort_artist',
            'type':unicode,
            'atom':'soar',
        },
        'sort composer':{
            'name':u'Sort Composer',
            'keyword':u'sort_composer',
            'type':unicode,
            'atom':'soco',
        },
        'sort album artist':{
            'name':u'Sort Album Artist',
            'keyword':u'sort_album_artist',
            'type':unicode,
            'atom':'soaa',
        },
        'sort album':{
            'name':u'Sort Album',
            'keyword':u'sort_album',
            'type':unicode,
            'atom':'soal',
        },
        'sort tv show':{
            'name':u'Sort TV Show',
            'keyword':u'sort_tv_show',
            'type':unicode,
            'atom':'sosn',
        },
        'encoding tool':{
            # mediainfo seems to mix @enc and @too into Encoded_Application
            'name':u'Encoding Tool',
            'keyword':u'encoding_tool',
            'type':unicode,
            'atom':'©too',
        },
        'encoded by':{
            # mediainfo seems to mix @enc and @too into Encoded_Application
            'name':u'Encoded by',
            'keyword':u'encoded_by',
            'type':unicode,
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
            'type':unicode,
            'atom':'xid',
        },
        'itunes content id':{
            'name':u'iTunes content ID',
            'keyword':u'itunes_content_id',
            'type':int,
            'atom':'cnID',
        },
        'itunes account':{
            'name':u'iTunes account ID',
            'keyword':u'itunes_account_id',
            'type':unicode,
            'atom':'apID',
        },
        'itunes artist id':{
            'name':u'iTunes artist ID',
            'keyword':u'itunes_artist_id',
            'type':int,
            'atom':'atID',
        },
        'itunes composer id':{
            'name':u'iTunes composer ID',
            'keyword':u'itunes_composer_id',
            'type':int,
            'atom':'cmID',
        },
        'itunes playlist id':{
            'name':u'iTunes playlist ID',
            'keyword':u'itunes_playlist_id',
            'type':int,
            'atom':'plID',
        },
        'itunes genre id':{
            'name':u'iTunes genre ID',
            'keyword':u'itunes_genre_id',
            'type':int,
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
        'episode global id':{
            'name':u'Episode Global ID',
            'keyword':u'episode_global_id',
            'type':int,
            'atom':'egid',
        },
        'podcast':{
            'name':u'Podcast',
            'keyword':u'podcast',
            'type':bool
            'atom':'pcst',
        },
        'podcast url':{
            'name':u'Podcast URL',
            'keyword':u'podcast_url',
            'type':unicode,
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
            'type':unicode,
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
            'type':unicode,
            'keyword':u'cast',
            'atom':'iTunMOVI',
            'plural':'list',
        },
        'directors':{
            'name':u'Directors',
            'keyword':u'directors',
            'type':unicode,
            'atom':'iTunMOVI',
            'plural':'list',
        },
        'codirectors':{
            'name':u'Codirectors',
            'keyword':u'codirectors',
            'type':unicode,
            'atom':'iTunMOVI',
            'plural':'list',
        },
        'producers':{
            'name':u'Producers',
            'keyword':u'producers',
            'type':unicode,
            'atom':'iTunMOVI',
            'plural':'list',
        },
        'screenwriters':{
            'name':u'Screenwriters',
            'keyword':u'screenwriters',
            'type':unicode,
            'atom':'iTunMOVI',
            'plural':'list',
        },
        'studio':{
            'name':u'Studio',
            'keyword':u'studio',
            'type':unicode,
            'atom':'iTunMOVI',
            'plural':'list',
        },
        'rating standard':{
            'name':u'Rating Standard',
            'keyword':u'rating_standard',
            'type':unicode,
            'atom':'iTunEXTC',
        },
        'rating':{
            'name':u'Rating',
            'keyword':u'rating',
            'type':unicode,
            'atom':'iTunEXTC',
        },
        'rating score':{
            'name':u'Rating Score',
            'keyword':u'rating_score',
            'type':int,
            'atom':'iTunEXTC',
        },
        'rating annotation':{
            'name':u'Rating Annotation',
            'keyword':u'rating_annotation',
            'type':unicode,
            'atom':'iTunEXTC',
        },
        'cover':{
            'name':u'Cover Pieces',
            'keyword':u'cover_pieces',
            'type':int,
            'atom':'covr',
            'auto cast':False,
        },
        'stream name':{
            'name':u'Stream Name',
            'keyword':u'stream_name',
            'type':unicode,
        },
        'stream type':{
            'name':u'Stream Type',
            'keyword':u'stream_type',
            'type':unicode,
        },
        'format':{
            'name':u'Format',
            'keyword':u'format',
            'type':unicode,
        },
        'format profile':{
            'name':u'Format Profile',
            'type':unicode,
            'plural':'list',
        },
        'channel configuration':{
            'name':u'Channel configuration',
            'keyword':u'channel_configuration',
            'type':int,
            'plural':'list',
        },
        'channel position':{
            'name':u'Channel Position',
            'keyword':u'channel_position',
            'type':unicode,
            'plural':'list',
        },
        'stream id':{
            'name':u'Stream ID',
            'keyword':u'stream_id',
            'type':int,
        },
        'stream position':{
            'name':u'Stream Position',
            'keyword':u'stream_position',
            'type':int,
        },
        'stream size':{
            'name':u'Stream Size',
            'keyword':u'stream_size',
            'type':int,
            'format':'byte',
        },
        'delay':{
            'name':u'Delay',
            'keyword':u'delay',
            'type':int,
        },
        'bit rate':{
            'name':u'Bit Rate',
            'keyword':u'bit_rate',
            'type':int,
            'format':'bitrate',
        },
        'bit rate mode':{
            'name':u'Bit Rate Mode',
            'keyword':u'bit_rate_mode',
            'type':unicode,
        },
        'bit depth':{
            'name':u'Bit Depth',
            'keyword':u'bit_depth',
            'type':int,
            'format':'bit',
        },
        'sample rate':{
            'name':u'Sample Rate',
            'keyword':u'sample_rate',
            'type':int,
            'format':'frequency',
        },
        'sample count':{
            'name':u'Sample Count',
            'keyword':u'sample_count',
            'type':int,
        },
        'frame rate':{
            'name':u'Frame Rate',
            'keyword':u'frame_rate',
            'type':float,
            'format':'framerate',
        },
        'frame rate mode':{
            'name':u'Frame Rate Mode',
            'keyword':u'frame_rate_mode',
            'type':unicode,
        },
        'frame rate minimum':{
            'name':u'Frame Rate Minimum',
            'keyword':u'frame_rate_minimum',
            'type':float,
            'format':'framerate',
        },
        'frame rate maximum':{
            'name':u'Frame Rate Maximum',
            'keyword':u'frame_rate_maximum',
            'type':float,
            'format':'framerate',
        },
        'frame count':{
            'name':u'Frame Count',
            'keyword':u'frame_count',
            'type':int,
        },
        'duration':{
            'name':u'Duration',
            'keyword':u'duration',
            'type':int,
            'format':'millisecond',
        },
        'width':{
            'name':u'Width',
            'keyword':u'width',
            'type':int,
            'format':'pixel',
        },
        'height':{
            'name':u'Height',
            'keyword':u'height',
            'type':int,
            'format':'pixel',
        },
        'pixel aspect ratio':{
            'name':u'Pixel Aspect Ratio',
            'keyword':u'pixel_aspect_ratio',
            'type':float,
        },
        'display aspect ratio':{
            'name':u'Display Aspect Ratio',
            'keyword':u'display_aspect_ratio',
            'type':float,
        },
        'color space':{
            'name':u'Color Space',
            'keyword':u'color_space',
            'type':unicode,
        },
        'channels':{
            'name':u'Channels',
            'keyword':u'channels',
            'type':int,
        },
        'dialnorm':{
            'name':u'Dialnorm',
            'keyword':u'dialnorm',
            'type':int,
        },
        'bpf':{
            'name':u'Bits / Pixel * Frame',
            'keyword':u'bpf',
            'type':float,
        },
        'encoder':{
            'name':u'Encoder',
            'keyword':u'encoder',
            'type':unicode,
        },
        'encoder settings':{
            'name':u'Encoder Settings',
            'keyword':u'encoder_settings',
            'type':unicode,
            'plural':'dict',
        },
        'character':{
            'name':u'Character',
            'keyword':u'character',
            'type':unicode,
        },
        'poster url':{
            'name':u'Poster URL',
            'keyword':u'poster_url',
            'type':unicode,
        },
    ],
    'namespace':{
        'knowlege':{
            'knowlege.movie':{
                'default':{
                    'keyword':None,
                    'plural':None,
                    'unescape xml':False,
                    'auto cast':True,
                },
                'synonym':['keyword'],
                'element':[
                    'movie id':{
                        'name':u'Movie ID',
                        'keyword':u'movie_id',
                        'type':int,
                    },
                    'imdb movie id':{
                        'name':u'IMDb Movie ID',
                        'keyword':u'imdb_movie_id',
                        'type':unicode,
                    },
                    'tmdb movie id':{
                        'name':u'TMDb Movie ID',
                        'keyword':u'tmdb_movie_id',
                        'type':int,
                    },
                ],
            },
            'knowlege.tvshow.show':{
                'default':{
                    'keyword':None,
                    'plural':None,
                    'unescape xml':False,
                    'auto cast':True,
                },
                'synonym':['keyword'],
                'element':[
                    'tv show id':{
                        'name':u'TV Show ID',
                        'keyword':u'tv_show_id',
                        'type':int,
                    },
                ],
            },
            'knowlege.tvshow.season':{
                'default':{
                    'keyword':None,
                    'plural':None,
                    'unescape xml':False,
                    'auto cast':True,
                },
                'synonym':['keyword'],
                'element':[
                    'tv show id':{
                        'name':u'TV Show ID',
                        'keyword':u'tv_show_id',
                        'type':int,
                    },
                    'tv season':{
                        'name':u'TV Season',
                        'keyword':u'tv_season',
                        'type':int,
                    },
                ],
            },
            'knowlege.tvshow.episode':{
                'default':{
                    'keyword':None,
                    'plural':None,
                    'unescape xml':False,
                    'auto cast':True,
                },
                'synonym':['keyword'],
                'element':[
                    'tv show id':{
                        'name':u'TV Show ID',
                        'keyword':u'tv_show_id',
                        'type':int,
                    },
                    'tv season':{
                        'name':u'TV Season',
                        'keyword':u'tv_season',
                        'type':int,
                    },
                    'tv episode':{
                        'name':u'TV Episode',
                        'keyword':u'tv_episode',
                        'type':int,
                    },
                ],
            },
            'knowlege.person':{
                'default':{
                    'keyword':None,
                    'plural':None,
                    'unescape xml':False,
                    'auto cast':True,
                },
                'synonym':['keyword'],
                'element':[
                    'person id':{
                        'name':u'Person ID',
                        'keyword':u'person_id',
                        'type':int,
                    },
                ],
            },
            'knowlege.network':{
                'default':{
                    'keyword':None,
                    'plural':None,
                    'unescape xml':False,
                    'auto cast':True,
                },
                'synonym':['keyword'],
                'element':[
                    'network id':{
                        'name':u'Network ID',
                        'keyword':u'network_id',
                        'type':int,
                    },
                ],
            },
            'knowlege.studio':{
                'default':{
                    'auto cast':True,
                    'plural':None,
                    'unescape xml':False,
                    'keyword':None,
                },
                'synonym':['keyword'],
                'element':[
                    'studio id':{
                        'name':u'Studio ID',
                        'keyword':u'studio_id',
                        'type':int,
                    },
                ],
            },
            'knowlege.job':{
                'default':{
                    'auto cast':True,
                    'plural':None,
                    'unescape xml':False,
                    'keyword':None,
                },
                'synonym':['keyword'],
                'element':[
                    'job id':{
                        'name':u'Job ID',
                        'keyword':u'job_id',
                        'type':int,
                    },
                ],
            },
            'knowlege.department':{
                'default':{
                    'auto cast':True,
                    'plural':None,
                    'unescape xml':False,
                    'keyword':None,
                },
                'synonym':['keyword'],
                'element':[
                    'department id':{
                        'name':u'Department ID',
                        'keyword':u'department_id',
                        'type':int,
                    },
                ],
            },
            'knowlege.genre':{
                'default':{
                    'auto cast':True,
                    'plural':None,
                    'unescape xml':False,
                    'keyword':None,
                },
                'synonym':['keyword'],
                'element':[
                    'genre id':{
                        'name':u'Genre ID',
                        'keyword':u'genre_id',
                        'type':int,
                    },
                ],
            },
        },
        'crawl':{
            'file':{
                'default':{
                    'auto cast':True,
                    'plural':None,
                    'unescape xml':False,
                    'mediainfo':None,
                    'atom':None,
                },
                'synonym':['mediainfo'],
                'element':[
                    'character encoding':{},
                    'file path':{},
                    'directory':{},
                    'file name':{},
                    'kind':{},
                    'file size':{
                        'mediainfo':'FileSize',
                    },
                    'format':{
                        'mediainfo':'Format',
                    },
                ],
            },
            'tag':{
                'default':{
                    'auto cast':True,
                    'plural':None,
                    'unescape xml':False,
                    'mediainfo':None,
                    'mp4info':None,
                    'subler':None,
                    'atom':None,
                    'keyword':None,
                },
                'synonym':['mediainfo', 'mp4info', 'keyword'],
                'element':[
                    'kind':{},
                    'language':{
                        'mediainfo':'Language_String3',
                    },
                    'profile':{},
                    'volume':{},
                    'media kind':{
                        'mediainfo':'stik',
                        'subler':'Media Kind',
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
                    'track #':{
                        'subler':'Track #',
                    },
                    'disk #':{
                        'subler':'Disk #',
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
                    'tv show':{
                        'mediainfo':'tvsh',
                        'subler':'TV Show',
                    },
                    'tv episode id':{
                        'mediainfo':'tven',
                        'subler':'TV Episode ID',
                    },
                    'tv season':{
                        'mediainfo':'tvsn',
                        'subler':'TV Season',
                    },
                    'tv episode':{
                        'mediainfo':'tves',
                        'subler':'TV Episode #',
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
                        'mp4info':'Lyrics',
                        'subler':'Lyrics',
                        'unescape xml':True,
                    },
                    'copyright':{
                        'mediainfo':'Copyright',
                        'subler':'Copyright',
                    },
                    'encoding tool':{
                        # mediainfo seems to mix @enc and @too into Encoded_Application
                        'mp4info':'Encoded with',
                        'subler':'Encoding Tool',
                    },
                    'encoded by':{
                        # mediainfo seems to mix @enc and @too into Encoded_Application
                        'mp4info':'Encoded by',
                        'subler':'Encoded by',
                    },
                    'release date':{
                        'mediainfo':'Recorded_Date',
                        'subler':'Release Date',
                    },
                    'compilation':{
                        'mediainfo':'Compilation',
                    },
                    'tempo':{
                        'mediainfo':'BPM',
                        'subler':'Tempo',
                    },
                    'genre type':{
                        'mp4info':'GenreType',
                    },
                    'genre':{
                        'mp4info':'Genre',
                        'subler':'Genre',
                    },
                    'hd video':{
                        'mediainfo':'hdvd',
                        'subler':'HD Video',
                    },
                    'gapless':{
                        'mp4info':'Part of Gapless Album',
                        'subler':'Gapless',
                    },
                    'podcast':{
                        'mediainfo':'pcst',
                    },
                    'podcast url':{},
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
                    'episode global id':{},
                    'purchase date':{
                        'mediainfo':'purd',
                        'subler':'Purchase Date',
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
                    'rating standard':{},
                    'rating':{
                        'subler':'Rating',
                    },
                    'rating score':{},
                    'rating annotation':{
                        'subler':'Rating Annotation',
                    },
                    'cover':{
                        'mediainfo':'Cover',
                        'auto cast':False,
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
                    'tv show key':{},
                    'simple name':{},
                    'imdb movie id':{},
                    'imdb tv show id':{},
                    'imdb tv episode id':{},
                    'tmdb movie id':{},
                ],
            }
        },
        'track':{
            'audio':{
                'default':{
                    'auto cast':True,
                    'plural':None,
                    'unescape xml':False,
                    'mediainfo':None,
                    'atom':None,
                },
                'synonym':['mediainfo'],
                'element':[
                    'stream name':{
                        'mediainfo':'Title',
                    },
                    'stream type':{},
                    'format':{
                        'mediainfo':'Format',
                    },
                    'format profile':{
                        'mediainfo':'Format_Profile',
                        'plural format':'mediainfo value list',
                    },
                    'channel configuration':{
                        'mediainfo':'Channel_s_',
                        'plural format':'mediainfo value list',
                    },
                    'channel position':{
                        'mediainfo':'ChannelPositions',
                        'plural format':'mediainfo value list',
                    },
                    'language':{
                        'mediainfo':'Language_String3',
                    },
                    'stream id':{
                        'mediainfo':'ID',
                    },
                    'stream position':{
                        'mediainfo':'StreamKindID',
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
                    'encoded date':{
                        'mediainfo':'Encoded_Date',
                    },
                    'channels':{},
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
                ],
            },
            'video':{
                'default':{
                    'auto cast':True,
                    'plural':None,
                    'unescape xml':False,
                    'mediainfo':None,
                    'atom':None,
                },
                'synonym':['mediainfo'],
                'element':[
                    'stream name':{
                        'mediainfo':'Title',
                    },
                    'stream type':{},
                    'format':{
                        'mediainfo':'Format',
                    },
                    'format profile':{
                        'mediainfo':'Format_Profile',
                        'plural format':'mediainfo value list',
                    },
                    'language':{
                        'mediainfo':'Language_String3',
                    },
                    'stream id':{
                        'mediainfo':'ID',
                    },
                    'stream position':{
                        'mediainfo':'StreamKindID',
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
                    'encoded date':{
                        'mediainfo':'Encoded_Date',
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
                ],
            },
            'text':{
                'default':{
                    'auto cast':True,
                    'plural':None,
                    'unescape xml':False,
                    'mediainfo':None,
                    'atom':None,
                },
                'synonym':['mediainfo'],
                'element':[
                    'stream name':{
                        'mediainfo':'Title',
                    },
                    'stream type':{},
                    'format':{
                        'mediainfo':'Format',
                    },
                    'format profile':{
                        'mediainfo':'Format_Profile',
                        'plural format':'mediainfo value list',
                    },
                    'language':{
                        'mediainfo':'Language_String3',
                    },
                    'stream id':{
                        'mediainfo':'ID',
                    },
                    'delay':{
                        'mediainfo':'Delay',
                    },
                    'stream position':{
                        'mediainfo':'StreamKindID',
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
                    'encoded date':{
                        'mediainfo':'Encoded_Date',
                    },
                ],
            },
            'image':{
                'default':{
                    'auto cast':True,
                    'plural':None,
                    'unescape xml':False,
                    'mediainfo':None,
                    'atom':None,
                },
                'synonym':['mediainfo'],
                'element':[
                    'stream name':{
                        'mediainfo':'Title',
                    },
                    'stream type':{},
                    'format':{
                        'mediainfo':'Format',
                    },
                    'format profile':{
                        'mediainfo':'Format_Profile',
                        'plural format':'mediainfo value list',
                    },
                    'language':{
                        'mediainfo':'Language_String3',
                    },
                    'stream id':{
                        'mediainfo':'ID',
                    },
                    'delay':{
                        'mediainfo':'Delay',
                    },
                    'stream position':{
                        'mediainfo':'StreamKindID',
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
                    'encoded date':{
                        'mediainfo':'Encoded_Date',
                    },
                    'width':{
                        'mediainfo':'Width',
                        'format':'pixel',
                    },
                    'height':{
                        'mediainfo':'Height',
                        'format':'pixel',
                    },
                ],
            }
        },
        'tmdb':{
            'tmdb.movie.cast':{
                'default':{
                    'keyword':None,
                    'plural':None,
                    'unescape xml':False,
                    'auto cast':True,
                    'tmdb':None,
                },
                'synonym':['keyword'],
                'element':[],
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
                'element':[],
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
                'element':[],
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
                'element':[],
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
                'element':[],
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
                'element':[],
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
                'element':[],
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
                'element':[],
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
                'element':[],
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
                'element':[
                    'tmdb movie id':{
                        'tmdb':'id',
                    },
                    'imdb movie id':{
                        'tmdb':'imdb_id',
                    },
                    'language':{},
                ],
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
                'element':[
                    'tmdb person id':{
                        'tmdb':'id',
                    },
                ],
            },
        },
        'tvdb':{
            'tvdb.show.cast':{
                'default':{
                    'auto cast':True,
                    'plural':None,
                    'unescape xml':False,
                    'tvdb':None,
                    'keyword':None,
                },
                'tag':'Actor',
                'coalesce':True,
                'synonym':['tvdb', 'keyword'],
                'element':[
                    'tvdb tv show id':{},
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
                        'type':int,
                        'tvdb':'SortOrder',
                    },
                ],
            },
            'tvdb.show.poster':{
                'default':{
                    'auto cast':True,
                    'plural':None,
                    'unescape xml':False,
                    'tvdb':None,
                    'keyword':None,
                },
                'tag':'Banner',
                'coalesce':True,
                'synonym':['tvdb', 'keyword'],
                'element':[
                    'tvdb tv show id':{},
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
                        'type':unicode,
                        'tvdb':'BannerType',
                    },
                    'tvdb_poster_layout':{
                        # season, seasonwide, text, graphical, blank,
                        # 1920x1080, 1280x720, 680x1000
                        'name':u'TVDb Poster Layout',
                        'keyword':u'tvdb_poster_layout',
                        'type':unicode,
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
                        'type':bool,
                        'tvdb':'SeriesName',
                    },
                    'color palette':{
                        'name':u'Color Palette',
                        'keyword':u'color_palette',
                        'type':unicode,
                        'tvdb':'Colors',
                        'enabled':False,
                    },
                ],
            },
            'tvdb.show':{
                'default':{
                    'auto cast':True,
                    'plural':None,
                    'unescape xml':False,
                    'tvdb':None,
                    'keyword':None,
                },
                'tag':'Series',
                'coalesce':False,
                'synonym':['tvdb', 'keyword'],
                'element':[
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
                        'type':unicode,
                        'tvdb':'banner',
                    },
                    'fan art url':{
                        'name':u'Fan Art URL',
                        'keyword':u'fan_art_url',
                        'type':unicode,
                        'tvdb':'fanart',
                    },
                    'tv show air day':{
                        'name':u'TV Show Air Day',
                        'keyword':u'tv_show_air_day',
                        'type':unicode,
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
                ],
            },
            'tvdb.episode':{
                'default':{
                    'auto cast':True,
                    'plural':None,
                    'unescape xml':False,
                    'tvdb':None,
                    'keyword':None,
                },
                'tag':'Episode',
                'coalesce':False,
                'synonym':['tvdb', 'keyword'],
                'element':[
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
                        'type':int,
                        'tvdb':'EpImgFlag',
                        'enabled':False,
                    },
                ],
            },
        },
    },
}
