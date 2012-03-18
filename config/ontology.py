# -*- coding: utf-8 -*-

ontology = {
    'prototype':[
        'character encoding':{
            'name':'Character encoding',
            'keyword':'character_encoding',
            'type':unicode,
        },
        'file path':{
            'name':'File path',
            'keyword':'file_path',
            'type':unicode,
        },
        'directory':{
            'name':'Directory',
            'keyword':'directory',
            'type':unicode,
        },
        'file name':{
            'name':'File name',
            'keyword':'file_name',
            'type':unicode,
        },
        'file size':{
            'name':'Size',
            'keyword':'file_size',
            'type':int,
            'format':'byte',
        },
        'profile':{
            'name':'Profile',
            'keyword':'profile',
            'type':unicode
        },
        'volume':{
            'name':'Volume',
            'keyword':'profile',
            'type':unicode
        },
        'kind':{
            'name':'Kind',
            'keyword':'kind',
            'type':unicode,
        },
        'tv show key':{
            'name':'TV Show Key',
            'keyword':'tv_show_key',
            'type':unicode,
        },
        'simple name':{
            'name':'Simple Name',
            'keyword':'simple_name',
            'type':unicode,
        },
        'tvdb tv show id':{
            'name':'TVDB TV Show ID',
            'keyword':'tvdb_tv_show_id',
            'type':int,
        },
        'tvdb tv season id':{
            'name':'TVDB TV Season ID',
            'keyword':'tvdb_tv_season_id',
            'type':int,
        },
        'tvdb tv episode id':{
            'name':'TVDB TV Episode ID',
            'keyword':'tvdb_tv_episode_id',
            'type':int,
        },
        'tvdb person id':{
            'name':'TVDB Person ID',
            'keyword':'tvdb_person_id',
            'type':int,
        },
        'tvdb poster id':{
            'name':'TVDB Poster ID',
            'keyword':'tvdb_poster_id',
            'type':int,
        }
        'imdb tv show id':{
            'name':'IMDB TV Show ID',
            'keyword':'imdb_tv_show_id',
            'type':unicode,
        },
        'imdb tv episode id':{
            'name':'IMDB TV Episode ID',
            'keyword':'imdb_tv_episode_id',
            'type':unicode,
        },
        'imdb movie id':{
            'name':'IMDB Movie ID',
            'keyword':'imdb_movie_id',
            'tmdb':'imdb_id',
            'type':unicode
        },
        'tmdb movie id':{
            'name':'TMDB movie ID',
            'keyword':'tmdb_movie_id',
            'type':int,
            'tmdb':'id',
        },
        'tmdb person id':{
            'name':'TMDB person ID',
            'keyword':'tmdb_person_id',
            'type':int,
            'tmdb':'id',
        },
        'zap2it tv show id':{
            'name':'Zap2It TV Show ID',
            'keyword':'zap2it_tv_show_id',
            'type':unicode,
            'tvdb':'zap2it_id',
        },
        'keywords':{
            'name':'Keywords',
            'keyword':'keywords',
            'type':unicode,
            'plural':'list',
        },
        'tv show runtime':{
            'name':'TV Show Runtime',
            'keyword':'tv_show_runtime',
            'type':int,
        },
        'tv show status':{
            'name':'TV Show Status',
            'keyword':'tv_show_status',
            'type':unicode,
        },
        'user rating':{
            'name':'User Rating',
            'keyword':'user_rating',
            'type':float,
            'tvdb':'Rating',
        },
        'user rating count':{
            'name':'User Rating Count',
            'keyword':'user_rating_count',
            'type':int,
            'tvdb':'RatingCount',
        },
        'language':{
            'name':'Language',
            'keyword':'language',
            'type':'enum',
            'mediainfo':'Language_String3',
            'tvdb':'Language',
            'enumeration':'language',
        },
        'media kind':{
            'name':'Media Kind',
            'keyword':'media_kind',
            'type':'enum',
            'atom':'stik',
            'mediainfo':'stik',
            'subler':'Media Kind',
            'enumeration':'media kind',
        },
        'name':{
            'name':'Name',
            'keyword':'name',
            'type':unicode,
            'atom':'©nam',
            'mediainfo':'Title',
            'subler':'Name',
        },
        'artist':{
            'name':'Artist',
            'keyword':'artist',
            'type':unicode,
            'atom':'@ART',
            'mediainfo':'Performer',
            'subler':'Artist',
        },
        'composer':{
            'name':'Composer',
            'keyword':'composer',
            'type':unicode,
            'atom':'©wrt',
            'mediainfo':'ScreenplayBy',
            'subler':'Composer',
        },
        'album artist':{
            'name':'Album Artist',
            'keyword':'album_artist',
            'type':unicode,
            'atom':'aART',
            'mediainfo':'Album_Performer',
            'subler':'Album Artist',
        },
        'album':{
            'name':'Album',
            'keyword':'album',
            'type':unicode,
            'atom':'©alb',
            'mediainfo':'Album',
            'subler':'Album',
        },
        'track #':{
            'name':'Track',
            'keyword':'track',
            'type':unicode,
            'atom':'trkn',
            'subler':'Track #',
        },
        'disk #':{
            'name':'Disk',
            'keyword':'disk',
            'type':unicode,
            'atom':'disk',
            'subler':'Disk #',
        },
        'track position':{
            'name':'Track Position',
            'keyword':'track_position',
            'type':int,
            'atom':'trkn',
            'mediainfo':'Track_Position',
        },
        'track total':{
            'name':'Track Total',
            'keyword':'track_total',
            'type':int,
            'atom':'trkn',
            'mediainfo':'Track_Position_Total',
        },
        'disk position':{
            'name':'Disk Position',
            'keyword':'disk_position',
            'type':int,
            'atom':'disk',
            'mediainfo':'Part_Position',
        },
        'disk total':{
            'name':'Disk Total',
            'keyword':'disk_total',
            'type':int,
            'atom':'disk',
            'mediainfo':'Part_Position_Total',
        },
        'grouping':{
            'name':'Grouping',
            'keyword':'grouping',
            'type':unicode,
            'atom':'©grp',
            'mediainfo':'Grouping',
            'subler':'Grouping',
        },
        'comment':{
            'name':'Comment',
            'keyword':'comment',
            'type':unicode,
            'atom':'©cmt',
            'mediainfo':'Comment',
            'subler':'Comments',
        },
        'description':{
            'name':'Description',
            'keyword':'description',
            'type':unicode,
            'atom':'desc',
            'mediainfo':'desc',
            'subler':'Description',
            'unescape xml':True,
        },
        'long description':{
            'name':'Long Description',
            'keyword':'long_description',
            'type':unicode,
            'atom':'ldes',
            'mediainfo':'ldes',
            'subler':'Long Description',
            'unescape xml':True,
        },
        'lyrics':{
            'name':'Lyrics',
            'keyword':'lyrics',
            'type':unicode,
            'atom':'©lyr',
            'mp4info':'Lyrics',
            'subler':'Lyrics',
            'unescape xml':True,
        },
        'compilation':{
            'name':'Compilation',
            'keyword':'compilation',
            'type':bool,
            'atom':'cpil',
            'mediainfo':'Compilation',
        },
        'copyright':{
            'name':'Copyright',
            'keyword':'copyright',
            'type':unicode,
            'atom':'cprt',
            'mediainfo':'Copyright',
            'subler':'Copyright',
        },
        'tempo':{
            'name':'Tempo',
            'keyword':'tempo',
            'type':int,
            'atom':'tmpo',
            'mediainfo':'BPM',
            'subler':'Tempo',
        },
        'genre type':{
            'name':'Genre Type',
            'keyword':'genre_type',
            'type':'enum',
            'atom':'gnre',
            'mp4info':'GenreType',
            'enumeration':'genre',
        },
        'genre':{
            'name':'Genre',
            'keyword':'genre',
            'type':unicode,
            'atom':'©gen',
            'mp4info':'Genre',
            'subler':'Genre',
        },
        'gapless':{
            'name':'Gapless',
            'keyword':'gapless',
            'type':bool
            'atom':'pgap',
            'mp4info':'Part of Gapless Album',
            'subler':'Gapless',
        },
        'itunes keywords':{
            'name':'iTunes Keywords',
            'keyword':'itunes_keywords',
            'type':unicode,
            'atom':'keyw',
            'mediainfo':'keyw',
        },
        'itunes category':{
            'name':'iTunes Category',
            'keyword':'itunes_category',
            'type':unicode,
            'atom':'catg',
            'mediainfo':'catg',
        },
        'hd video':{
            'name':'HD Video',
            'keyword':'hd_video',
            'type':bool
            'atom':'hdvd',
            'mediainfo':'hdvd',
            'subler':'HD Video',
        },
        'tv show':{
            'name':'TV Show',
            'keyword':'tv_show',
            'type':unicode,
            'atom':'tvsh',
            'mediainfo':'tvsh',
            'subler':'TV Show',
        },
        'tv episode id':{
            'name':'TV Episode ID',
            'keyword':'tv_episode_id',
            'type':unicode,
            'atom':'tven',
            'mediainfo':'tven',
            'subler':'TV Episode ID',
        },
        'tv season':{
            'name':'TV Season',
            'keyword':'tv_season',
            'type':int,
            'atom':'tvsn',
            'mediainfo':'tvsn',
            'subler':'TV Season',
        },
        'tv episode':{
            'name':'TV Episode',
            'keyword':'tv_episode',
            'type':int,
            'atom':'tves',
            'mediainfo':'tves',
            'subler':'TV Episode #',
        },
        'absolute tv episode':{
            'name':'Absolute TV Episode',
            'keyword':'absolute_tv_episode'
            'type':int,
        },
        'tv network':{
            'name':'TV Network',
            'keyword':'tv_network',
            'type':unicode,
            'atom':'tvnn',
            'mediainfo':'tvnn',
            'subler':'TV Network',
            'tvdb':'Network',
        },
        'sort name':{
            'name':'Sort Name',
            'keyword':'sort_name',
            'type':unicode,
            'atom':'sonm',
            'mediainfo':'sonm',
            'subler':'Sort Name',
        },
        'sort artist':{
            'name':'Sort Artist',
            'keyword':'sort_artist',
            'type':unicode,
            'atom':'soar',
            'mediainfo':'soar',
            'subler':'Sort Artist',
        },
        'sort composer':{
            'name':'Sort Composer',
            'keyword':'sort_composer',
            'type':unicode,
            'atom':'soco',
            'mediainfo':'soco',
            'subler':'Sort Composer',
        },
        'sort album artist':{
            'name':'Sort Album Artist',
            'keyword':'sort_album_artist',
            'type':unicode,
            'atom':'soaa',
            'mediainfo':'soaa',
            'subler':'Sort Album Artist',
        },
        'sort album':{
            'name':'Sort Album',
            'keyword':'sort_album',
            'type':unicode,
            'atom':'soal',
            'mediainfo':'soal',
            'subler':'Sort Album',
        },
        'sort tv show':{
            'name':'Sort TV Show',
            'keyword':'sort_tv_show',
            'type':unicode,
            'atom':'sosn',
            'mediainfo':'sosn',
            'subler':'Sort TV Show',
        },
        'encoding tool':{
            # mediainfo seems to mix @enc and @too into Encoded_Application
            'name':'Encoding Tool',
            'keyword':'encoding_tool',
            'type':unicode,
            'atom':'©too',
            'mp4info':'Encoded with',
            'subler':'Encoding Tool',
        },
        'encoded by':{
            # mediainfo seems to mix @enc and @too into Encoded_Application
            'name':'Encoded by',
            'keyword':'encoded_by',
            'type':unicode,
            'atom':'@enc',
            'mp4info':'Encoded by',
            'subler':'Encoded by',
        },
        'modified date':{
            'name':'Modified Date',
            'keyword':'modified_date',
            'type':'date',
            'mediainfo':'File_Modified_Date',
        },
        'tag date':{
            'name':'Tag Date',
            'keyword':'tag_date',
            'type':'date',
            'mediainfo':'Tagged_Date',
        },
        'release date':{
            'name':'Release Date',
            'keyword':'release_date',
            'type':'date',
            'atom':'©day',
            'mediainfo':'Recorded_Date',
            'subler':'Release Date',
            'tvdb':'FirstAired',
        },
        'purchase date':{
            'name':'Purchase Date',
            'keyword':'purchase_date',
            'type':'date',
            'atom':'purd',
            'mediainfo':'purd',
            'subler':'Purchase Date',
        },
        'encoded date':{
            'name':'Encoded Date',
            'keyword':'encoded_date',
            'type':'date',
            'mediainfo':'Encoded_Date',
        },
        'xid':{
            'name':'XID',
            'keyword':'xid',
            'type':unicode,
            'atom':'xid',
            'mediainfo':'xid',
            'subler':'XID',
        },
        'itunes content id':{
            'name':'iTunes content ID',
            'keyword':'itunes_content_id',
            'type':int,
            'atom':'cnID',
            'mediainfo':'cnID',
            'subler':'contentID',
        },
        'itunes account':{
            'name':'iTunes account ID',
            'keyword':'itunes_account_id',
            'type':unicode,
            'atom':'apID',
            'mediainfo':'apID',
            'subler':'iTunes Account',
        },
        'itunes artist id':{
            'name':'iTunes artist ID',
            'keyword':'itunes_artist_id',
            'type':int,
            'atom':'atID',
            'mediainfo':'atID',
        },
        'itunes composer id':{
            'name':'iTunes composer ID',
            'keyword':'itunes_composer_id',
            'type':int,
            'atom':'cmID',
            'mediainfo':'cmID',
        },
        'itunes playlist id':{
            'name':'iTunes playlist ID',
            'keyword':'itunes_playlist_id',
            'type':int,
            'atom':'plID',
            'mediainfo':'plID',
        },
        'itunes genre id':{
            'name':'iTunes genre ID',
            'keyword':'itunes_genre_id',
            'type':int,
            'atom':'geID',
            'mediainfo':'geID',
        },
        'itunes country id':{
            'name':'iTunes country ID',
            'keyword':'itunes_country_id',
            'type':'enum',
            'atom':'sfID',
            'mediainfo':'sfID',
            'enumeration':'country',
        },
        'itunes account type':{
            'name':'iTunes account type',
            'keyword':'itunes_account_type',
            'type':'enum',
            'atom':'akID',
            'mediainfo':'akID',
            'enumeration':'itunes account type',
        },
        'episode global id':{
            'name':'Episode Global ID',
            'keyword':'episode_global_id',
            'type':int,
            'atom':'egid',
        },
        'podcast':{
            'name':'Podcast',
            'keyword':'podcast',
            'type':bool
            'atom':'pcst',
            'mediainfo':'pcst',
        },
        'podcast url':{
            'name':'Podcast URL',
            'keyword':'podcast_url',
            'type':unicode,
            'atom':'purl',
        },
        'content rating':{
            'name':'Content Rating',
            'keyword':'content_rating',
            'type':'enum',
            'atom':'rtng',
            'mediainfo':'rtng',
            'subler':'Content Rating',
            'enumeration':'content rating',
        },
        'itunextc':{
            'name':'iTunEXTC',
            'keyword':'itunextc',
            'type':unicode,
            'atom':'iTunEXTC',
            'mediainfo':'iTunEXTC',
        },
        'itunmovi':{
            'name':'iTunMOVI',
            'keyword':'itunmovi',
            'type':'plist',
            'atom':'iTunMOVI',
            'mediainfo':'iTunMOVI',
        },
        'cast':{
            'name':'Cast',
            'type':unicode,
            'keyword':'cast',
            'atom':'iTunMOVI',
            'subler':'Cast',
            'plural':'list',
        },
        'directors':{
            'name':'Directors',
            'keyword':'directors',
            'type':unicode,
            'atom':'iTunMOVI',
            'subler':'Director',
            'plural':'list',
        },
        'codirectors':{
            'name':'Codirectors',
            'keyword':'codirectors',
            'type':unicode,
            'atom':'iTunMOVI',
            'subler':'Codirectors',
            'plural':'list',
        },
        'producers':{
            'name':'Producers',
            'keyword':'producers',
            'type':unicode,
            'atom':'iTunMOVI',
            'subler':'Producers',
            'plural':'list',
        },
        'screenwriters':{
            'name':'Screenwriters',
            'keyword':'screenwriters',
            'type':unicode,
            'atom':'iTunMOVI',
            'subler':'Screenwriters',
            'plural':'list',
        },
        'studio':{
            'name':'Studio',
            'keyword':'studio',
            'type':unicode,
            'atom':'iTunMOVI',
            'subler':'Studio',
            'plural':'list',
        },
        'rating standard':{
            'name':'Rating Standard',
            'keyword':'rating_standard',
            'type':unicode,
            'atom':'iTunEXTC',
        },
        'rating':{
            'name':'Rating',
            'keyword':'rating',
            'type':unicode,
            'atom':'iTunEXTC',
            'subler':'Rating',
            'tvdb':'ContentRating',
        },
        'rating score':{
            'name':'Rating Score',
            'keyword':'rating_score',
            'type':int,
            'atom':'iTunEXTC',
        },
        'rating annotation':{
            'name':'Rating Annotation',
            'keyword':'rating_annotation',
            'type':unicode,
            'atom':'iTunEXTC',
            'subler':'Rating Annotation',
        },
        'cover':{
            'name':'Cover Pieces',
            'keyword':'cover_pieces',
            'type':int,
            'atom':'covr',
            'mediainfo':'Cover',
            'auto cast':False,
        },
        'stream name':{
            'name':'Stream Name',
            'keyword':'stream_name',
            'type':unicode,
        },
        'stream type':{
            'name':'Stream Type',
            'keyword':'stream_type',
            'type':unicode,
        },
        'format':{
            'name':'Format',
            'keyword':'format',
            'type':unicode,
        },
        'format profile':{
            'name':'Format Profile',
            'type':unicode,
            'plural':'list',
        },
        'channel configuration':{
            'name':'Channel configuration',
            'keyword':'channel_configuration',
            'type':int,
            'plural':'list',
        },
        'channel position':{
            'name':'Channel Position',
            'keyword':'channel_position',
            'type':unicode,
            'plural':'list',
        },
        'stream id':{
            'name':'Stream ID',
            'keyword':'stream_id',
            'type':int,
            'mediainfo':'ID',
        },
        'stream position':{
            'name':'Stream Position',
            'keyword':'stream_position',
            'type':int,
            'mediainfo':'StreamKindID',
        },
        'stream size':{
            'name':'Stream Size',
            'keyword':'stream_size',
            'type':int,
            'mediainfo':'StreamSize',
            'format':'byte',
        },
        'delay':{
            'name':'Delay',
            'keyword':'delay',
            'type':int,
            'mediainfo':'Delay',
        },
        'bit rate':{
            'name':'Bit Rate',
            'keyword':'bit_rate',
            'type':int,
            'format':'bitrate',
        },
        'bit rate mode':{
            'name':'Bit Rate Mode',
            'keyword':'bit_rate_mode',
            'type':unicode,
            'mediainfo':'BitRate_Mode',
        },
        'bit depth':{
            'name':'Bit Depth',
            'keyword':'bit_depth',
            'type':int,
            'mediainfo':'BitDepth',
            'format':'bit',
        },
        'sample rate':{
            'name':'Sample Rate',
            'keyword':'sample_rate',
            'type':int,
            'mediainfo':'SamplingRate',
            'format':'frequency',
        },
        'sample count':{
            'name':'Sample Count',
            'keyword':'sample_count',
            'type':int,
            'mediainfo':'SamplingCount',
        },
        'frame rate':{
            'name':'Frame Rate',
            'keyword':'frame_rate',
            'type':float,
            'mediainfo':'FrameRate',
            'format':'framerate',
        },
        'frame rate mode':{
            'name':'Frame Rate Mode',
            'keyword':'frame_rate_mode',
            'type':unicode,
            'mediainfo':'FrameRate_Mode',
        },
        'frame rate minimum':{
            'name':'Frame Rate Minimum',
            'keyword':'frame_rate_minimum',
            'type':float,
            'mediainfo':'FrameRate_Minimum',
            'format':'framerate',
        },
        'frame rate maximum':{
            'name':'Frame Rate Maximum',
            'keyword':'frame_rate_maximum',
            'type':float,
            'mediainfo':'FrameRate_Maximum',
            'format':'framerate',
        },
        'frame count':{
            'name':'Frame Count',
            'keyword':'frame_count',
            'type':int,
            'mediainfo':'FrameCount',
        },
        'duration':{
            'name':'Duration',
            'keyword':'duration',
            'type':int,
            'mediainfo':'Duration',
            'format':'millisecond',
        },
        'width':{
            'name':'Width',
            'keyword':'width',
            'type':int,
            'mediainfo':'Width',
            'format':'pixel',
        },
        'height':{
            'name':'Height',
            'keyword':'height',
            'type':int,
            'mediainfo':'Height',
            'format':'pixel',
        },
        'pixel aspect ratio':{
            'name':'Pixel Aspect Ratio',
            'keyword':'pixel_aspect_ratio',
            'type':float,
            'mediainfo':'PixelAspectRatio',
        },
        'display aspect ratio':{
            'name':'Display Aspect Ratio',
            'keyword':'display_aspect_ratio',
            'type':float,
            'mediainfo':'DisplayAspectRatio',
        },
        'color space':{
            'name':'Color Space',
            'keyword':'color_space',
            'type':unicode,
            'mediainfo':'ColorSpace',
        },
        'channels':{
            'name':'Channels',
            'keyword':'channels',
            'type':int,
        },
        'dialnorm':{
            'name':'Dialnorm',
            'keyword':'dialnorm',
            'type':int,
            'mediainfo':'dialnorm',
        },
        'bpf':{
            'name':'Bits / Pixel * Frame',
            'keyword':'bpf',
            'type':float,
            'mediainfo':'Bits-_Pixel_Frame_',
        },
        'encoder':{
            'name':'Encoder',
            'keyword':'encoder',
            'type':unicode,
            'mediainfo':'Encoded_Library',
        },
        'encoder settings':{
            'name':'Encoder Settings',
            'keyword':'encoder_settings',
            'type':unicode,
            'mediainfo':'Encoded_Library_Settings',
            'plural':'dict',
            'plural format':'mediainfo key value list',
        },
        'character':{
            'name':'Character',
            'keyword':'character',
            'type':unicode,
        },
    ],
    'namespace':{
        'knowlege':{
            'knowlege.movie':{
                'default':{
                    'auto cast':True,
                    'plural':None,
                    'unescape xml':False,
                    'keyword':None,
                },
                'synonym':['keyword'],
                'element':[
                    'movie id':{
                        'name':'Movie ID',
                        'keyword':'movie_id',
                        'type':int,
                    },
                    'imdb movie id':{
                        'name':'IMDB Movie ID',
                        'keyword':'imdb_movie_id',
                        'type':unicode,
                    },
                    'tmdb movie id':{
                        'name':'TMDB movie ID',
                        'keyword':'tmdb_movie_id',
                        'type':int,
                    },
                ],
            },
            'knowlege.tvshow.show':{
                'default':{
                    'auto cast':True,
                    'plural':None,
                    'unescape xml':False,
                    'keyword':None,
                },
                'synonym':['keyword'],
                'element':[
                    'tv show id':{
                        'name':'TV Show ID',
                        'keyword':'tv_show_id',
                        'type':int,
                    },
                ],
            },
            'knowlege.tvshow.season':{
                'default':{
                    'auto cast':True,
                    'plural':None,
                    'unescape xml':False,
                    'keyword':None,
                },
                'synonym':['keyword'],
                'element':[
                    'tv show id':{
                        'name':'TV Show ID',
                        'keyword':'tv_show_id',
                        'type':int,
                    },
                    'tv season':{
                        'name':'TV Season',
                        'keyword':'tv_season',
                        'type':int,
                    },
                ],
            },
            'knowlege.tvshow.episode':{
                'default':{
                    'auto cast':True,
                    'plural':None,
                    'unescape xml':False,
                    'keyword':None,
                },
                'synonym':['keyword'],
                'element':[
                    'tv show id':{
                        'name':'TV Show ID',
                        'keyword':'tv_show_id',
                        'type':int,
                    },
                    'tv season':{
                        'name':'TV Season',
                        'keyword':'tv_season',
                        'type':int,
                    },
                    'tv episode':{
                        'name':'TV Episode',
                        'keyword':'tv_episode',
                        'type':int,
                    },
                ],
            },
            'knowlege.person':{
                'default':{
                    'auto cast':True,
                    'plural':None,
                    'unescape xml':False,
                    'keyword':None,
                },
                'synonym':['keyword'],
                'element':[
                    'person id':{
                        'name':'Person ID',
                        'keyword':'person_id',
                        'type':int,
                    },
                ],
            },
            'knowlege.network':{
                'default':{
                    'auto cast':True,
                    'plural':None,
                    'unescape xml':False,
                    'keyword':None,
                },
                'synonym':['keyword'],
                'element':[
                    'network id':{
                        'name':'Network ID',
                        'keyword':'network_id',
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
                        'name':'Studio ID',
                        'keyword':'studio_id',
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
                        'name':'Job ID',
                        'keyword':'job_id',
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
                        'name':'Department ID',
                        'keyword':'department_id',
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
                        'name':'Genre ID',
                        'keyword':'genre_id',
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
            #'tmdb.movie.cast':{},
            #'tmdb.movie.poster':{},
            #'tmdb.movie.keyword':{},
            #'tmdb.movie.release':{},
            #'tmdb.movie.trailer':{},
            #'tmdb.movie.translation':{},
            #'tmdb.movie.alternative':{},
            #'tmdb.person.poster':{},
            #'tmdb.person.credit':{},
            'tmdb.movie':{
                'default':{
                    'auto cast':True,
                    'plural':None,
                    'unescape xml':False,
                    'keyword':None,
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
                    'auto cast':True,
                    'plural':None,
                    'unescape xml':False,
                    'keyword':None,
                },
                'synonym':['keyword'],
                'element':[
                    'tmdb person id':{},
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
                        'name':'Poster URL',
                        'keyword':'poster_url',
                        'type':unicode,
                        'tvdb':'Image',
                    },
                    'name':{
                        'tvdb':'Name',
                    },
                    'character':{
                        'tvdb':'Role',
                    },
                    'sort order':{
                        'name':'Sort Order',
                        'keyword':'sort_order',
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
                        'name':'Poster URL',
                        'keyword':'poster_url',
                        'type':unicode,
                        'tvdb':'BannerPath',
                    },
                    'tvdb image context':{
                        # fanart, poster, season, series
                        'name':'TVDB Poster Context',
                        'keyword':'tvdb_poster_context',
                        'type':unicode,
                        'tvdb':'BannerType',
                    },
                    'tvdb_poster_layout':{
                        # season, seasonwide, text, graphical, blank,
                        # 1920x1080, 1280x720, 680x1000
                        'name':'TVDB Poster Layout',
                        'keyword':'tvdb_poster_layout',
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
                        'name':'Contain TV Show Name',
                        'keyword':'contain_tv_show_name',
                        'type':bool,
                        'tvdb':'SeriesName',
                    },
                    'color palette':{
                        'name':'Color Palette',
                        'keyword':'color_palette',
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
                        'name':'Poster URL',
                        'keyword':'poster_url',
                        'type':unicode,
                        'tvdb':'poster',
                    },
                    'banner url':{
                        'name':'Banner URL',
                        'keyword':'banner_url',
                        'type':unicode,
                        'tvdb':'banner',
                    },
                    'fan art url':{
                        'name':'Fan Art URL',
                        'keyword':'fan_art_url',
                        'type':unicode,
                        'tvdb':'fanart',
                    },
                    'tv show air day':{
                        'name':'TV Show Air Day',
                        'keyword':'tv_show_air_day',
                        'type':unicode,
                        'tvdb':'Airs_DayOfWeek',
                        'enabled':False,
                    },
                    'tv show air time':{
                        'name':'TV Show Air Time',
                        'keyword':'tv_show_air_time',
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
                        'name':'Poster URL',
                        'keyword':'poster_url',
                        'type':unicode,
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
                        'name':'TVDB Poster Flag',
                        'keyword':'tvdb_poster_flag',
                        'type':int,
                        'tvdb':'EpImgFlag',
                        'enabled':False,
                    },
                ],
            },
        },
    },
}
