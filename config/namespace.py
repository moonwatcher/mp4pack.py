# -*- coding: utf-8 -*-

{
    'namespace':{
        # Mongodb
        'ns.system.mongodb':{
            'default':{
                'keyword':None,
                'plural':None,
                'auto cast':True,
            },
            'synonym':['keyword'],
            'element':{
                'host':None,
                'database':None,
                'port':None,
                'username':None,
                'password':None,
                'mongodb url':None,
            },
            'rule':[
                'rule.system.mongodb.url',
            ],
        },
        
        # System
        'ns.system.command.default':{
            'default':{
                'keyword':None,
                'plural':None,
                'auto cast':True,
                'unescape xml':False,
            },
            'synonym':['key'],
            'element':{
                'domain':None,
                'host':None,
                'volume':None,
                'profile':None,
                'preset':None,
                'recursive':{
                    'auto cast':False,
                },
                'sync':{
                    'auto cast':False,
                },
                'crawl':{
                    'auto cast':False,
                },
                'download':{
                    'auto cast':False,
                },
                'overwrite':{
                    'auto cast':False,
                },
                'kind':None,
                'inclusion':None,
                'exclusion':None,
                'language':None,
                'scan path':{
                    'auto cast':False,
                },
                'uris':{
                    'auto cast':False,
                },
                'quantizer':None,
                'width':None,
                'crop':None,
                'time shift':None,
                'source frame rate':None,
                'target frame rate':None,
                'verbosity':None,
                'debug':{
                    'auto cast':False,
                },
                'configuration path':None,
                'action':None,
            },
        },
        'ns.system.job':{
            'default':{
                'keyword':None,
                'plural':None,
                'auto cast':True,
            },
            'synonym':['keyword'],
            'element':{
                'action':None,
                'preset':None,
                'domain':None,
                'host':None,
                'volume':None,
                'profile':None,
                'recursive':{
                    'auto cast':False,
                },
                'sync':{
                    'auto cast':False,
                },
                'crawl':{
                    'auto cast':False,
                },
                'download':{
                    'auto cast':False,
                },
                'overwrite':{
                    'auto cast':False,
                },
                'kind':None,
                'inclusion':None,
                'exclusion':None,
                'language':None,
                'scan path':{
                    'auto cast':False,
                },
                'uris':{
                    'auto cast':False,
                },
                'quantizer':None,
                'width':None,
                'crop':None,
                'time shift':None,
                'source frame rate':None,
                'target frame rate':None,
                'debug':{
                    'auto cast':False,
                },
            },
        },
        'ns.system.task':{
            'default':{
                'keyword':None,
                'plural':None,
                'auto cast':True,
            },
            'synonym':['keyword'],
            'element':{
                'action':None,
                'preset':None,
                'domain':None,
                'host':None,
                'volume':None,
                'profile':None,
                'sync':{
                    'auto cast':False,
                },
                'crawl':{
                    'auto cast':False,
                },
                'download':{
                    'auto cast':False,
                },
                'overwrite':{
                    'auto cast':False,
                },
                'kind':None,
                'language':None,
                'quantizer':None,
                'width':None,
                'crop':None,
                'time shift':None,
                'source frame rate':None,
                'target frame rate':None,
                'debug':{
                    'auto cast':False,
                },
            },
            'rule':[
                'rule.task.default.preset'
            ],
        },
        
        # Medium
        'ns.service.genealogy':{
            'default':{
                'keyword':None,
                'auto cast':True,
                'plural':None,
                'unescape xml':False,
                'atom':None,
            },
            'synonym':['keyword'],
            'element':{
                'domain':None,
                'url':None,
                'path':None,
                'path digest':None,
                'file name':None,
                'directory':None,
                'scheme':None,
                'host':None,
                'media kind':None,
                'kind':None,
                'language':None,
                'profile':None,
                'volume':None,
                'home id':None,
                'movie id':None,
                'album id':None,
                'tv show id':None,
                'disk id':None,
                'track id':None,
                'person id':None,
                'company id':None,
                'genre id':None,
                'job id':None,
                'department id':None,
                'track position':None,
                'disk position':None,
                'movie handle':None,
                'album handle':None,
                'tv show handle':None,
                'imdb movie id':None,
                'imdb tv show id':None,
                'imdb tv episode id':None,
                'trimmed imdb movie id':None,
                'tmdb movie id':None,
                'tmdb person id':None,
                'tmdb company id':None,
                'tmdb collection id':None,
                'tmdb genre id':None,
                'tvdb tv show id':None,
                'tvdb tv season id':None,
                'tvdb tv episode id':None,
                'rottentomatoes movie id':None,
                'itunes person id':None,
                'itunes movie id':None,
                'itunes tv show id':None,
                'itunes tv season id':None,
                'itunes tv episode id':None,
                'itunes genre id':None,
            },
            'rule':[
                'rule.system.volume.location',
                'rule.medium.resource.track.genealogy',
                'rule.medium.resource.filename.canonic',
                'rule.medium.resource.directory.canonic',
                'rule.medium.resource.path.canonic',
                'rule.medium.resource.filename.implicit',
                'rule.medium.resource.directory.implicit',
                'rule.medium.resource.path.implicit',
                'rule.medium.resource.path.digest',
                'rule.medium.resource.kind.language',
                'rule.system.default.routing',
                'rule.system.default.language',
                'rule.knowledge.movie.imdb.trimmed',
            ],
        },
        'ns.medium.resource.location':{
            'default':{
                'auto cast':True,
                'plural':None,
                'unescape xml':False,
                'mediainfo':None,
                'atom':None,
            },
            'synonym':['keyword'],
            'element':{
                'domain':None,
                'url':None,
                'scheme':None,
                'host':None,
                'path':None,
                'path digest':None,
                'media kind':None,
                'directory':None,
                'file name':None,
                'kind':None,
                'language':None,
                'profile':None,
                'volume':None,
                'home id':None,
                'movie id':None,
                'album id':None,
                'tv show id':None,
                'disk id':None,
                'track id':None,
                'track position':None,
                'disk position':None,
                'movie handle':None,
                'album handle':None,
                'tv show handle':None,
                'imdb movie id':None,
                'imdb tv show id':None,
                'imdb tv episode id':None,
                'tmdb movie id':None,
                'tvdb tv show id':None,
                'tvdb tv season id':None,
                'tvdb tv episode id':None,
                'rottentomatoes movie id':None,
                'itunes person id':None,
                'itunes movie id':None,
                'itunes tv show id':None,
                'itunes tv season id':None,
                'itunes tv episode id':None,
                'itunes genre id':None,
                'name':None,
                'simple name':None,
                'track genealogy':None,
                'resource uri':None,
                'asset uri':None,
                'home uri':None,
            },
            'rule':[
                'rule.system.volume.location',
                'rule.medium.resource.track.genealogy',
                'rule.medium.resource.filename.canonic',
                'rule.medium.resource.directory.canonic',
                'rule.medium.resource.path.canonic',
                'rule.medium.resource.filename.implicit',
                'rule.medium.resource.directory.implicit',
                'rule.medium.resource.path.implicit',
                'rule.medium.resource.path.digest',
                'rule.medium.resource.kind.language',
                'rule.system.default.routing',
                'rule.medium.resource.uri',
                'rule.medium.asset.uri',
                'rule.medium.home.uri',
            ],
        },
        'ns.medium.asset.location':{
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
                'media kind':None,
                'home id':None,
                'movie id':None,
                'album id':None,
                'tv show id':None,
                'disk id':None,
                'track id':None,
                'track position':None,
                'disk position':None,
                'movie handle':None,
                'album handle':None,
                'tv show handle':None,
                'imdb movie id':None,
                'imdb tv show id':None,
                'imdb tv episode id':None,
                'tmdb movie id':None,
                'tvdb tv show id':None,
                'tvdb tv season id':None,
                'tvdb tv episode id':None,
                'rottentomatoes movie id':None,
                'itunes person id':None,
                'itunes movie id':None,
                'itunes tv show id':None,
                'itunes tv season id':None,
                'itunes tv episode id':None,
                'name':None,
                'simple name':None,
                'asset uri':None,
                'home uri':None,
            },
            'rule':[
                'rule.medium.asset.uri',
                'rule.medium.home.uri',
            ],
        },
        'ns.medium.resource.url.decode':{
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
                'movie id':None,
                'album id':None,
                'tv show id':None,
                'disk id':None,
                'track id':None,
                'track position':None,
                'disk position':None,
                'movie handle':None,
                'album handle':None,
                'tv show handle':None,
                'imdb movie id':None,
                'imdb tv show id':None,
                'imdb tv episode id':None,
                'tmdb movie id':None,
                'tvdb tv show id':None,
                'tvdb tv season id':None,
                'tvdb tv episode id':None,
                'rottentomatoes movie id':None,
                'itunes person id':None,
                'itunes movie id':None,
                'itunes tv show id':None,
                'itunes tv season id':None,
                'itunes tv episode id':None,
                'name':None,
            },
            'rule':[
                'rule.medium.resource.directory.parse',
                'rule.medium.resource.filename.parse',
            ],
        },
        'ns.medium.resource.hint':{
            'default':{
                'auto cast':True,
                'plural':None,
                'unescape xml':False,
            },
            'synonym':['keyword'],
            'element':{
            }
        },
        'ns.medium.resource.tag.meta':{
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
                'actors':{
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
                'rule.knowledge.disk.number',
                'rule.knowledge.track.number',
                'rule.knowledge.default.track.total',
                'rule.knowledge.default.disk.total',
                'rule.knowledge.default.episode',
                'rule.knowledge.sort.name',
                'rule.knowledge.sort.artist',
                'rule.knowledge.sort.albumartist',
                'rule.knowledge.sort.album',
                'rule.knowledge.sort.composer',
                'rule.knowledge.sort.show',
                'rule.knowledge.artist.info',
                'rule.itunes.itunextc.parse',
                'rule.itunes.album.name',
            ],
        },
        'ns.medium.resource.meta':{
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
                'rating standard':None,
                'rating':{
                    'subler':'Rating',
                },
                'rating score':None,
                'rating annotation':{
                    'subler':'Rating Annotation',
                },
                'itunmovi':{
                    'mediainfo':'iTunMOVI',
                },
                'actors':{
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
                'rule.knowledge.disk.number',
                'rule.knowledge.track.number',
                'rule.itunes.itunextc.parse',
            ],
        },
        'ns.medium.resource.stream.audio':{
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
                'stream kind position':{
                    'mediainfo':'StreamKindPos',
                },
                'stream type':{
                    'mediainfo':'StreamKind',
                },
                'stream kind':None,
                'kind':None,
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
                'primary':None,
                'handbrake audio encoder settings':None,
            },
            'rule':[
                'rule.medium.stream.default.position',
                'rule.medium.stream.default.id',
                'rule.medium.stream.audio.kind',
                'rule.system.default.enabled',
                'rule.medium.stream.audio.name',
            ],
        },
        'ns.medium.resource.stream.video':{
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
                'stream kind position':{
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
                    'plural format':'mediainfo key value list',
                },
                'encoded date':{
                    'mediainfo':'Encoded_Date',
                },
                'primary':None,
                'handbrake parameters':None,
                'handbrake x264 settings':None,
            },
            'rule':[
                'rule.medium.stream.default.position',
                'rule.medium.stream.default.id',
                'rule.medium.stream.video.kind',
                'rule.medium.stream.default.primary',
                'rule.system.default.enabled',
            ],
        },
        'ns.medium.resource.stream.text':{
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
                'stream kind position':{
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
                'primary':None,
            },
            'rule':[
                'rule.medium.stream.default.position',
                'rule.medium.stream.default.id',
                'rule.medium.stream.text.kind',
                'rule.medium.stream.default.primary',
                'rule.system.default.enabled',
                'rule.system.default.language',
            ],
        },
        'ns.medium.resource.stream.image':{
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
                'stream kind position':{
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
                'primary':None,
            },
            'rule':[
                'rule.medium.stream.default.position',
                'rule.medium.stream.default.id',
                'rule.medium.stream.image.kind',
                'rule.medium.stream.default.primary',
                'rule.system.default.enabled',
            ],
        },
        
        # Knowledge
        'ns.knowledge.keyword':{
            'default':{
                'auto cast':True,
                'plural':None,
                'unescape xml':False,
                'keyword':None,
                'tmdb':None,
            },
            'synonym':['keyword', 'tmdb'],
            'element':{
                'keyword id':None,
                'tmdb keyword id':{
                    'tmdb':'id',
                },
                'name':{
                    'tmdb':'name',
                },
            },
        },
        'ns.knowledge.review':{
            'default':{
                'auto cast':True,
                'plural':None,
                'unescape xml':False,
                'keyword':None,
                'rottentomatoes':None,
            },
            'synonym':['keyword', 'rottentomatoes'],
            'element':{
                'critic name':{
                    'rottentomatoes':u'critic',
                },
                'freshness':{
                    'rottentomatoes':u'freshness',
                },
                'original critic score':{
                    'rottentomatoes':u'original_score',
                },
                'review publication':{
                    'rottentomatoes':u'publication',
                },
                'review quote':{
                    'rottentomatoes':u'quote',
                },
                'review url':{
                    'rottentomatoes':u'review_link',
                },                
            },
        },
        'ns.knowledge.rating':{
            'default':{
                'auto cast':True,
                'plural':None,
                'unescape xml':False,
                'keyword':None,
                'tmdb':None,
                'tvdb':None,
            },
            'synonym':['keyword', 'tmdb', 'tvdb'],
            'element':{
                'rating':{
                    'tvdb':'ContentRating',
                    'tmdb':'certification',
                },
                'country':{
                    'tmdb':'iso_3166_1',
                },
                'release date':{
                    'tvdb':'FirstAired',    
                    'tmdb':u'release_date',
                },
            },
        },
        'ns.knowledge.title':{
            'default':{
                'auto cast':True,
                'plural':None,
                'unescape xml':False,
                'keyword':None,
                'tmdb':None,
            },
            'synonym':['keyword', 'tmdb'],
            'element':{
                'title':{
                    'tmdb':'title',
                },
                'country':{
                    'tmdb':'iso_3166_1',
                },
            },
        },
        'ns.knowledge.company.credit':{
            'default':{
                'auto cast':True,
                'plural':None,
                'unescape xml':False,
                'keyword':None,
                'tmdb':None,
            },
            'synonym':['keyword', 'tmdb'],
            'element':{
                'tmdb movie id':{
                    'tmdb':'id',
                },
                'poster url':{
                    'tmdb':'poster_path',
                },
                'backdrop url':{
                    'tmdb':'backdrop_path',
                },
                'original title':{
                    'tmdb':'original_title',
                },
                'title':{
                    'tmdb':'title',
                },
                'release date':{
                    'tmdb':'release_date',
                },
                'vote average':{
                    'tmdb':u'vote_average',
                },
                'vote count':{
                    'tmdb':u'vote_count',
                },
            },
        },
        'ns.knowledge.person.credit':{
            'default':{
                'auto cast':True,
                'plural':None,
                'unescape xml':False,
                'keyword':None,
                'tmdb':None,
            },
            'synonym':['keyword', 'tmdb'],
            'element':{
                'tmdb movie id':{
                    'tmdb':'id',
                },
                'poster url':{
                    'tmdb':'poster_path',
                },
                'original title':{
                    'tmdb':'original_title',
                },
                'title':{
                    'tmdb':'title',
                },
                'character':{
                    'tmdb':'character',
                },
                'job':{
                    'tmdb':'job',
                },
                'department':{
                    'tmdb':'department',
                },
                'release date':{
                    'tmdb':'release_date',
                },
            },
        },
        'ns.knowledge.cast':{
            'default':{
                'auto cast':True,
                'plural':None,
                'unescape xml':False,
                'keyword':None,
                'tmdb':None,
                'tvdb':None,
            },
            'synonym':['keyword', 'tmdb', 'tvdb'],
            'element':{
                'tvdb person id':{
                    'tvdb':'id',
                },
                'tmdb person id':{
                    'tmdb':'id',
                },
                'profile url':{
                    'tvdb':'Image',
                    'tmdb':'profile_path',
                },
                'name':{
                    'tvdb':'Name',
                    'tmdb':'name',
                },
                'character':{
                    'tvdb':'Role',
                    'tmdb':'character',
                },
                'sort order':{
                    'tvdb':'SortOrder',
                    'tmdb':'order',
                },
                'job':{
                    'tmdb':'job',
                },
                'department':{
                    'tmdb':'department',
                },
            },
        },
        'ns.knowledge.genre':{
            'default':{
                'auto cast':True,
                'plural':None,
                'unescape xml':False,
                'keyword':None,
                'tmdb':None,
                'itunes':None,
            },
            'synonym':['keyword', 'tmdb', 'itunes'],
            'element':{
                'genre id':None,
                'tmdb genre id':{
                    'tmdb':'id',
                },
                'itunes genre id':{
                    'itunes':'id',
                },
                'name':{
                    'tmdb':'name',
                    'itunes':'name',
                },
            },
        },
        'ns.knowledge.image':{
            'default':{
                'keyword':None,
                'plural':None,
                'unescape xml':False,
                'auto cast':True,
                'tmdb':None,
                'tvdb':None,
            },
            'synonym':['keyword', 'tmdb', 'tvdb'],
            'element':{
                'height':{
                    'tmdb':'height',
                },
                'width':{
                    'tmdb':'width',
                },
                'pixel aspect ratio':{
                    'tmdb':'aspect_ratio',
                },
                'vote average':{
                    'tmdb':u'vote_average',
                    'tvdb':'Rating',
                },
                'vote count':{
                    'tmdb':u'vote_count',
                    'tvdb':'RatingCount',
                },
                'language':{
                    'tmdb':'iso_639_1',
                    'tvdb':'Language',
                },
                'image url':{
                    'tmdb':'file_path',
                    'tvdb':'BannerPath',
                },
                'tvdb image id':{
                    'tvdb':'id',
                },
                'disk position':{
                    'tvdb':'Season',
                },
            },
        },
        'ns.knowledge.person':{
            'default':{
                'keyword':None,
                'plural':None,
                'unescape xml':False,
                'auto cast':True,
                'tmdb':None,
                'itunes':None,
            },
            'synonym':['keyword', 'tmdb', 'itunes'],
            'element':{
                'person id':None,
                'itunes person id':{
                    'itunes':'artistId',
                },                
                'tmdb person id':{
                    'tmdb':'id',
                },
                'birthday':{
                    'tmdb':'birthday',
                },
                'deathday':{
                    'tmdb':'deathday',
                },
                'homepage':{
                    'tmdb':'homepage',
                },
                'name':{
                    'tmdb':'name',
                },
                'biography':{
                    'tmdb':u'biography',
                },
                'place of birth':{
                    'tmdb':u'place_of_birth',
                },
                'profile url':{
                    'tmdb':'profile_path',
                },
                'profiles':{
                    'tmdb':'profiles',
                },
                'cast':{
                    'tmdb':'cast',
                    'namespace':'ns.knowledge.person.credit',
                },
                'crew':{
                    'tmdb':'crew',
                    'namespace':'ns.knowledge.person.credit',
                },
            },
        },
        'ns.knowledge.company':{
            'default':{
                'keyword':None,
                'plural':None,
                'unescape xml':False,
                'auto cast':True,
                'tmdb':None,
            },
            'synonym':['keyword', 'tmdb'],
            'element':{
                'company id':None,
                'tmdb company id':{
                    'tmdb':'id',
                },
                'description':{
                    'tmdb':'description',
                },
                'homepage':{
                    'tmdb':'homepage',
                },
                'name':{
                    'tmdb':'name',
                },
            },
        },
        'ns.knowledge.collection':{
            'default':{
                'keyword':None,
                'plural':None,
                'unescape xml':False,
                'auto cast':True,
                'tmdb':None,
            },
            'synonym':['keyword', 'tmdb'],
            'element':{
                'collection id':None,
                'tmdb collection id':{
                    'tmdb':'id',
                },
                'language':None,
                'name':{
                    'tmdb':'name',
                },
                'backdrop url':{
                    'tmdb':'backdrop_path',
                },
                'poster url':{
                    'tmdb':'poster_path',
                },
                'movies':{
                    'tmdb':'parts',
                }
            },
        },
        'ns.knowledge.movie':{
            'default':{
                'keyword':None,
                'plural':None,
                'unescape xml':False,
                'auto cast':True,
                'tmdb':None,
                'rottentomatoes':None,
                'itunes':None,
            },
            'synonym':['keyword','tmdb', 'rottentomatoes', 'itunes'],
            'element':{
                'movie id':None,
                'itunes movie id':{
                    'itunes':'trackId',
                },
                'tmdb movie id':{
                    'tmdb':'id',
                },
                'imdb movie id':{
                    'tmdb':'imdb_id',
                    'rottentomatoes':'imdb_id',
                },
                'rottentomatoes movie id':{
                    'rottentomatoes':'id',
                },
                'language':None,
                'homepage':{
                    'tmdb':'homepage',
                },
                'title':{
                    'tmdb':'title',
                    'rottentomatoes':'title',
                },
                'original title':{
                    'tmdb':'original_title',
                },
                'tagline':{
                    'tmdb':'tagline',
                },
                'budget':{
                    'tmdb':'budget',
                },
                'runtime':{
                    'tmdb':'runtime',
                    'rottentomatoes':'runtime',
                },
                'revenue':{
                    'tmdb':'revenue',
                },                
                'vote average':{
                    'tmdb':u'vote_average',
                },
                'vote count':{
                    'tmdb':u'vote_count',
                },
                'release date':{
                    'tmdb':u'release_date',
                    'rottentomatoes':u'release_date',
                },
                'description':{
                    'tmdb':'overview',
                    'rottentomatoes':'synopsis',
                },
                'backdrop url':{
                    'tmdb':'backdrop_path',
                },
                'poster url':{
                    'tmdb':'poster_path',
                },
                'genres':{
                    'tmdb':'genres',
                },
                'production companies':{
                    'tmdb':'production_companies',
                },
                'backdrops':{
                    'tmdb':'backdrops',
                },
                'posters':{
                    'tmdb':'posters',
                },     
                'belongs to collection':{
                    'tmdb':'belongs_to_collection',
                },
                'cast':{
                    'tmdb':'cast',
                },
                'crew':{
                    'tmdb':'crew',
                },
                'certifications':{
                    'tmdb':'countries',
                },
                'titles':{
                    'tmdb':'titles',
                },
                'critics consensus':{
                    'rottentomatoes':u'critics_consensus',
                },            
                'audience rating':{
                    'rottentomatoes':u'audience_rating',
                },
                'critics rating':{
                    'rottentomatoes':u'critics_rating',
                },
                'audience score':{
                    'rottentomatoes':u'audience_score',
                },
                'critics score':{
                    'rottentomatoes':u'critics_score',
                },
                'reviews':{
                    'rottentomatoes':'reviews',
                },
                'rating':{
                    'rottentomatoes':'mpaa_rating',
                },
            },
        },
        'ns.knowledge.tv.show':{
            'default':{
                'auto cast':True,
                'plural':None,
                'unescape xml':False,
                'tvdb':None,
                'keyword':None,
                'itunes':None,
            },
            'synonym':['tvdb', 'keyword', 'itunes'],
            'element':{
                'tv show id':None,
                'itunes tv show id':{
                    'itunes':'artistId',
                },
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
                'vote average':{
                    'tvdb':'Rating',
                },
                'vote count':{
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
                'actors':{
                    'tvdb':'Actors',
                    'plural format':'tvdb list',
                },
                'image url':{
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
                    'tvdb':'Airs_DayOfWeek',
                    'enabled':False,
                },
                'tv show air time':{
                    'tvdb':'Airs_Time',
                    'enabled':False,
                },
            },
        },
        'ns.knowledge.tv.season':{
            'default':{
                'auto cast':True,
                'plural':None,
                'unescape xml':False,
                'tvdb':None,
                'keyword':None,
                'itunes':None,
            },
            'synonym':['tvdb', 'keyword', 'itunes'],
            'element':{
                'tv show id':None,
                'tv season':None,
                'itunes tv show id':{
                    'itunes':'artistId',
                },
                'itunes tv season id':{
                    'itunes':'collectionId',
                },
                'tvdb tv show id':{
                    'tvdb':'seriesid',
                },
                'tvdb tv season id':{
                    'tvdb':'seasonid',
                },
                'disk position':{
                    'tvdb':'SeasonNumber',
                },
                'language':{
                    'tvdb':'Language',
                },
            },
        },
        'ns.knowledge.tv.episode':{
            'default':{
                'auto cast':True,
                'plural':None,
                'unescape xml':False,
                'tvdb':None,
                'keyword':None,
                'itunes':None,
            },
            'synonym':['tvdb', 'keyword', 'itunes'],
            'element':{
                'tv show id':None,
                'tv season':None,
                'tv episode':None,
                'itunes tv show id':{
                    'itunes':'artistId',
                },
                'itunes tv season id':{
                    'itunes':'collectionId',
                },
                'itunes tv episode id':{
                    'itunes':'trackId',
                },    
                'tvdb tv show id':{
                    'tvdb':'seriesid',
                },
                'tvdb tv season id':{
                    'tvdb':'seasonid',
                },
                'tvdb tv episode id':{
                    'tvdb':'id',
                },
                'disk position':{
                    'tvdb':'SeasonNumber',
                },
                'track position':{
                    'tvdb':'EpisodeNumber',
                    'itunes':'trackNumber',
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
                    'format':'unix time',
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
                'vote average':{
                    'tvdb':'Rating',
                },
                'vote count':{
                    'tvdb':'RatingCount',
                },
                'backdrop url':{
                    'tvdb':'filename',
                },
                'actors':{
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
                'tvdb image flag':{
                    'name':u'TVDb image flag',
                    'keyword':u'tvdb_image_flag',
                    'type':'int',
                    'tvdb':'EpImgFlag',
                    'enabled':False,
                },
            },
        },
        
        'ns.knowledge.job':{
            'default':{
                'auto cast':True,
                'plural':None,
                'unescape xml':False,
                'keyword':None,
            },
            'synonym':['keyword'],
            'element':{
                'job id':None,
            },
        },
        'ns.knowledge.department':{
            'default':{
                'auto cast':True,
                'plural':None,
                'unescape xml':False,
                'keyword':None,
            },
            'synonym':['keyword'],
            'element':{
                'department id':None,
            },
        },
    },
}
