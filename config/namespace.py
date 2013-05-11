# -*- coding: utf-8 -*-

{
    'namespace':{
        # Mongodb
        'ns.system.mongodb':{
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
                'query parameters':{
                    'plural format':'eval',
                },
            },
        },
        'ns.system.job':{
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
                'query parameters':None,
                'implementation':None,
            },
            'rule':[
                'rule.job.implementation',
            ],
        },
        'ns.system.task':{
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
                'query parameters':None,
            },
            'rule':[
                'rule.task.default.preset'
            ],
        },

        # Medium
        'ns.service.genealogy':{
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
                'umid':None,
                'movie id':None,
                'music album id':None,
                'tv show id':None,
                'tv season id':None,
                'tv episode id':None,
                'track id':None,
                'person id':None,
                'company id':None,
                'genre id':None,
                'job id':None,
                'department id':None,
                'track number':None,
                'disc number':None,
                'movie handle':None,
                'album handle':None,
                'tv show handle':None,
                'imdb person id':None,
                'imdb character id':None,
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
                'itunes music album id':None,
                'itunes music track id':None,
                'stream id':None,
                'resource path digest':None,

                'person name':None,
                'character name':None,
                'company name':None,
                'genre name':None,
                'tv show name':None,
                'tv episode name':None,
                'movie title':None,
                'music track name':None,
                'music album name':None,
                'track name':None,
                'album name':None,

                'release year':None,
                'release date':None,

                'simple company name':None,
                'simple person name':None,
                'simple genre name':None,
                'simple character name':None,
                'simple tv show name':None,
                'simple tv episode name':None,
                'simple movie title':None,
                'simple music album name':None,
                'simple music track name':None,
            },
            'rule':[
                'rule.medium.resource.filename.fragment',
                'rule.medium.resource.directory.fragment',
                'rule.medium.resource.path.fragment',
                'rule.system.temp.location',
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
                'rule.knowledge.simple.name.company',
                'rule.knowledge.simple.name.person',
                'rule.knowledge.simple.name.genre',
                'rule.knowledge.simple.name.character',
                'rule.knowledge.simple.name.tv.show',
                'rule.knowledge.simple.name.tv.episode',
                'rule.knowledge.simple.name.movie',
                'rule.knowledge.simple.name.music.album',
                'rule.knowledge.simple.name.music.track',
                'rule.knowledge.release.year',
                'rule.medium.home.umid',
            ],
        },
        'ns.medium.resource.location':{
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
                'umid':None,
                'movie id':None,
                'music album id':None,
                'tv show id':None,
                'tv season id':None,
                'tv episode id':None,
                'track id':None,
                'track number':None,
                'disc number':None,
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
                'itunes music album id':None,
                'itunes music track id':None,
                'simple name':None,
                'track genealogy':None,
                'resource uri':None,
                'asset uri':None,
                'home uri':None,
                'stream id':None,
                'resource path digest':None,

                'person name':None,
                'character name':None,
                'company name':None,
                'genre name':None,
                'tv show name':None,
                'tv episode name':None,
                'movie title':None,
                'music track name':None,
                'music album name':None,
                'track name':None,
                'album name':None,

                'simple company name':None,
                'simple person name':None,
                'simple genre name':None,
                'simple character name':None,
                'simple tv show name':None,
                'simple tv episode name':None,
                'simple movie title':None,
                'simple music album name':None,
                'simple music track name':None,
            },
            'rule':[
                'rule.medium.resource.filename.fragment',
                'rule.medium.resource.directory.fragment',
                'rule.medium.resource.path.fragment',
                'rule.system.temp.location',
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
                'rule.medium.home.umid',
                'rule.knowledge.simple.name.company',
                'rule.knowledge.simple.name.person',
                'rule.knowledge.simple.name.genre',
                'rule.knowledge.simple.name.character',
                'rule.knowledge.simple.name.tv.show',
                'rule.knowledge.simple.name.tv.episode',
                'rule.knowledge.simple.name.movie',
                'rule.knowledge.simple.name.music.album',
                'rule.knowledge.simple.name.music.track',
            ],
        },
        'ns.medium.asset.location':{
            'synonym':['keyword'],
            'element':{
                'url':None,
                'scheme':None,
                'host':None,
                'media kind':None,
                'home id':None,
                'umid':None,
                'movie id':None,
                'music album id':None,
                'tv show id':None,
                'tv season id':None,
                'tv episode id':None,
                'track id':None,
                'track number':None,
                'disc number':None,
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
                'simple name':None,
                'asset uri':None,
                'home uri':None,

                'person name':None,
                'character name':None,
                'tv show name':None,
                'tv episode name':None,
                'movie title':None,
                'music track name':None,
                'music album name':None,
                'track name':None,
                'album name':None,
            },
            'rule':[
                'rule.medium.asset.uri',
                'rule.medium.home.uri',
                'rule.medium.home.umid',
            ],
        },
        'ns.medium.resource.url.decode':{
            'synonym':['keyword'],
            'element':{
                'directory':None,
                'file name':None,
                'profile':None,
                'language':None,
                'volume path':None,
                'kind':None,
                'umid':None,
                'home id':None,
                'resource path digest':None,
                'stream id':None,
                'media kind':None,
                'movie id':None,
                'music album id':None,
                'tv show id':None,
                'tv season id':None,
                'tv episode id':None,
                'track id':None,
                'track number':None,
                'disc number':None,
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

                'person name':None,
                'character name':None,
                'tv show name':None,
                'tv episode name':None,
                'movie title':None,
                'music track name':None,
                'music album name':None,
                'track name':None,
                'album name':None,
            },
            'rule':[
                'rule.medium.resource.filename.parse',
            ],
        },
        'ns.medium.resource.hint':{
            'synonym':['keyword'],
            'element':{
            }
        },
        'ns.medium.resource.meta.tag':{
            'synonym':['mediainfo', 'keyword'],
            'description':u'Generating valid tag sets for tagger',
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
                'track number':{
                    'mediainfo':'Track_Position',
                },
                'track count':{
                    'mediainfo':'Track_Position_Total',
                },
                'disc number':{
                    'mediainfo':'Part_Position',
                },
                'disc count':{
                    'mediainfo':'Part_Position_Total',
                },
                'track position':{
                    'subler':'Track #',
                },
                'disc position':{
                    'subler':'Disk #',
                },
                'tv season number':{
                    'mediainfo':'tvsn',
                    'subler':'TV Season',
                },
                'tv episode number':{
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
                'track name':{
                    'mediainfo':'Title',
                    'subler':'Name',
                },
                'artist name':{
                    'mediainfo':'Performer',
                    'subler':'Artist',
                },
                'album artist name':{
                    'mediainfo':'Album_Performer',
                    'subler':'Album Artist',
                },
                'album name':{
                    'mediainfo':'Album',
                    'subler':'Album',
                },
                'tv show name':{
                    'mediainfo':'tvsh',
                    'subler':'TV Show',
                },
                'tv episode production code':{
                    'mediainfo':'tven',
                    'subler':'TV Episode ID',
                },
                'tv network name':{
                    'mediainfo':'tvnn',
                    'subler':'TV Network',
                },
                'grouping':{
                    'mediainfo':'Grouping',
                    'subler':'Grouping',
                },
                'composer name':{
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
                'genre name':{
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
                'itunes person id':{
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
                'content advisory standard':None,
                'content advisory rating':{
                    'subler':'Rating',
                },
                'content advisory score':None,
                'content advisory annotation':{
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
                'rule.knowledge.disc.position',
                'rule.knowledge.track.position',
                'rule.knowledge.default.track.count',
                'rule.knowledge.default.disc.count',
                'rule.knowledge.default.tv.episode',
                'rule.knowledge.default.music.track',
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
                'track number':{
                    'mediainfo':'Track_Position',
                },
                'track count':{
                    'mediainfo':'Track_Position_Total',
                },
                'disc number':{
                    'mediainfo':'Part_Position',
                },
                'disc count':{
                    'mediainfo':'Part_Position_Total',
                },
                'track position':{
                    'subler':'Track #',
                },
                'disc position':{
                    'subler':'Disk #',
                },
                'tv season number':{
                    'mediainfo':'tvsn',
                    'subler':'TV Season',
                },
                'tv episode number':{
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
                'track name':{
                    'mediainfo':'Title',
                    'subler':'Name',
                },
                'artist name':{
                    'mediainfo':'Performer',
                    'subler':'Artist',
                },
                'album artist name':{
                    'mediainfo':'Album_Performer',
                    'subler':'Album Artist',
                },
                'album name':{
                    'mediainfo':'Album',
                    'subler':'Album',
                },
                'tv show name':{
                    'mediainfo':'tvsh',
                    'subler':'TV Show',
                },
                'tv episode production code':{
                    'mediainfo':'tven',
                    'subler':'TV Episode ID',
                },
                'tv network name':{
                    'mediainfo':'tvnn',
                    'subler':'TV Network',
                },
                'grouping':{
                    'mediainfo':'Grouping',
                    'subler':'Grouping',
                },
                'composer name':{
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
                'genre name':{
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
                'itunes person id':{
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
                'content advisory standard':None,
                'content advisory rating':{
                    'subler':'Rating',
                },
                'content advisory score':None,
                'content advisory annotation':{
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
                'rule.knowledge.disc.position',
                'rule.knowledge.track.position',
                'rule.itunes.itunextc.parse',
            ],
        },
        'ns.medium.resource.stream.audio':{
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
                'encoder settings string':{
                    'mediainfo':'Encoded_Library_Settings',
                },
                'encoder settings':{
                    'mediainfo':'Parsed_Encoded_Library_Settings',
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
        'ns.medium.resource.x264':{
            'synonym':['x264'],
            'element':{
                'bit rate':{
                    'x264':'bitrate',
                },
                '8x8 dct':{
                    'x264':u'8x8dct',
                },
                'adaptive bi directional':{
                    'x264':u'b_adapt',
                },
                'bi directional bias':{
                    'x264':u'b_bias',
                },
                'bi directional pyramid':{
                    'x264':u'b_pyramid',
                },
                'bi directional frames':{
                    'x264':u'bframes',
                },
                'cabac':{
                    'x264':u'cabac',
                },
                'chroma motion estimation':{
                    'x264':u'chroma_me',
                },
                'chroma planes quantizer offset':{
                    'x264':u'chroma_qp_offset',
                },
                'constrained intra prediction':{
                    'x264':u'constrained_intra',
                },
                'dct decimation':{
                    'x264':'decimate',
                },
                'direct motion vectors prediction mode':{
                    'x264':'direct',
                },
                'predicted frames early skip detection':{
                    'x264':'fast_pskip',
                },
                'intra frames refresh':{
                    'x264':'intra_refresh',
                },
                'rate control lookahead':{
                    'x264':'rc_lookahead',
                },
                'decoded picture buffer size':{
                    'x264':'ref',
                },
                'scene cut':{
                    'x264':u'scenecut',
                },
                'sliced based threading':{
                    'x264':'sliced_threads',
                },
                'subpixel motion estimation':{
                    'x264':'subme',
                },
                'threads':{
                    'x264':u'threads',
                },
                'trellis quantization':{
                    'x264':'trellis',
                },
                'video buffer verifier size':{
                    'x264':'vbv_bufsize',
                },
                'video buffer verifier maximum rate':{
                    'x264':'vbv_maxrate',
                },
                'weighted predicted frames':{
                    'x264':'wpredp',
                },
                'weighted bi directional frames':{
                    'x264':'wpredb',
                },
                'maximum keyframe interval':{
                    'x264':'keyint',
                },
                'minimum keyframe interval':{
                    'x264':'keyint_min',
                },
                'macroblock adaptive frame field':{
                    'x264':'mbaff',
                },
                'macroblock tree rate control':{
                    'x264':'mbtree',
                },
                'motion estimation method':{
                    'x264':'me',
                },
                'motion estimation range':{
                    'x264':'me_range',
                },
                'mixed references':{
                    'x264':'mixed_ref',
                },
                'noise reduction':{
                    'x264':'nr',
                },
                'minimum quantizer':{
                    'x264':'qpmin',
                },
                'maximum quantizer':{
                    'x264':'qpmax',
                },
                'quantizer step':{
                    'x264':'qpstep',
                },
                'custom quantization matrices':{
                    'x264':'cqm',
                },
                'psychovisual optimization':{
                    'x264':'psy',
                },
                'psychovisual strength':{
                    'x264':'psy_rd',
                },
                'quantizer curve compression factor':{
                    'x264':'qcomp',
                },
                'quantizer curve blur':{
                    'x264':'cplxblur',
                },
                'post compression quantizer curve blur':{
                    'x264':'qblur',
                },
                'rate tolerance':{
                    'x264':'ratetol',
                },
                'intra predicted ratio':{
                    'x264':'ip_ratio',
                },
                'bi directional predicted ratio':{
                    'x264':'pb_ratio',
                },
                'macroblock partitions':{
                    'x264':'analyse',
                },
                'adaptive quantization':{
                    'x264':'aq',
                },
                'deadzone':{
                    'x264':'deadzone',
                },
                'loop filter deblocker':{
                    'x264':'deblock',
                },
                'rate control method':{
                    'x264':'rc',
                },
                'hypothetical reference decoder':{
                    'x264':'nal_hrd',
                },
                'open group of pictures':{
                    'type':'open_gop',
                },
                'interlaced':{
                    'x264':u'interlaced',
                },
                'bluray compatible':{
                    'x264':'bluray_compat',
                },
            },
            'rule':[],
        },

        # Knowledge

        # Canonical
        'ns.knowledge.movie.canonical':{
            'synonym':['keyword',],
            'element':{
                'movie id':None,
                'language':None,
                'homepage':None,
                'movie title':None,
                'original movie title':None,
                'tagline':None,
                'country code':None,
                'budget':None,
                'runtime':None,
                'revenue':None,
                'vote average':None,
                'vote count':None,
                'release date':None,
                'release year':None,
                'description':None,
                'long description':None,
                'genres':None,
                'keywords':None,
                'production companies':None,
                'backdrops':None,
                'posters':None,
                'part of a collection':None,
                'cast':None,
                'crew':None,
                'certifications':None,
                'titles':None,
                'reviews':None,
                'critics consensus':None,
                'audience rating':None,
                'critics rating':None,
                'audience score':None,
                'critics score':None,
                'content advisory rating':None,
                'tmdb popularity':None,
                'artist name':None,
                'simple movie title':None,
            },
            'rule':[
                'rule.knowledge.simple.name.movie',
                'rule.knowledge.release.year',
            ],
        },
        'ns.knowledge.tv.show.canonical':{
            'synonym':['keyword', ],
            'element':{
                'tv show id':None,
                'tv show name':None,
                'modified date':None,
                'release date':None,
                'release year':None,
                'content advisory rating':None,
                'language':None,
                'description':None,
                'vote average':None,
                'vote count':None,
                'tv network name':None,
                'runtime':None,
                'tv show status':None,
                'genres':None,
                'actors':None,
                'image url':None,
                'banner url':None,
                'fan art url':None,
                'tv show air day':None,
                'tv show air time':None,
                'cast':None,
                'posters':None,
                'simple tv show name':None,
                'country code':None,
            },
            'rule':[
                'rule.knowledge.simple.name.tv.show',
                'rule.knowledge.release.year',
            ],
        },
        'ns.knowledge.tv.season.canonical':{
            'synonym':['keyword',],
            'element':{
                'tv show id':None,
                'tv season id':None,
                'tv season number':None,
                'itunes tv show id':None,
                'itunes tv season id':None,
                'tvdb tv show id':None,
                'tvdb tv season id':None,
                'imdb tv show id':None,
                'disc count':None,
                'disc number':None,
                'track count':None,
                'tv show name':None,
                'content advisory rating':None,
                'copyright':None,
                'release year':None,
                'release date':None,
                'long description':None,
                'language':None,
                'album name':None,
                'simple tv show name':None,
                'country code':None,
            },
            'rule':[
                'rule.itunes.tv.season.parse',
                'rule.knowledge.simple.name.tv.show',
                'rule.knowledge.release.year',
            ],
        },
        'ns.knowledge.tv.episode.canonical':{
            'synonym':['keyword', ],
            'element':{
                'tv show id':None,
                'tv season id':None,
                'tv season number':None,
                'tv episode number':None,
                'disc number':None,
                'track number':None,
                'track count':None,
                'tv episode name':None,
                'tv show name':None,
                'absolute tv episode number':None,
                'modified date':None,
                'language':None,
                'release date':None,
                'release year':None,
                'description':None,
                'long description':None,
                'tv episode production code':None,
                'vote average':None,
                'vote count':None,
                'backdrop url':None,
                'actors':None,
                'directors':None,
                'screenwriters':None,
                'content advisory rating':None,
                'simple tv show name':None,
                'simple tv episode name':None,
                'country code':None,
            },
            'rule':[
                'rule.knowledge.simple.name.tv.show',
                'rule.knowledge.simple.name.tv.episode',
                'rule.knowledge.release.year',
            ],
        },
        'ns.knowledge.music.album.canonical':{
            'synonym':['keyword',],
            'element':{
                'music album id':None,
                'album name':None,
                'music album name':None,
                'itunes music album id':None,
                'itunes person id':None,
                'artist name':None,
                'copyright':None,
                'release date':None,
                'release year':None,
                'track count':None,
                'simple music album name':None,
                'country code':None,
            },
            'rule':[
                'rule.knowledge.simple.name.music.album',
                'rule.knowledge.release.year',
            ],
        },
        'ns.knowledge.music.track.canonical':{
            'synonym':['keyword',],
            'element':{
                'music album id':None,
                'track id':None,
                'music disc number':None,
                'music track number':None,
                'album name':None,
                'track name':None,
                'music album name':None,
                'music track name':None,
                'itunes music album id':None,
                'itunes music track id':None,
                'disc number':None,
                'disc count':None,
                'track number':None,
                'track count':None,
                'itunes person id':None,
                'artist name':None,
                'release date':None,
                'release year':None,
                'simple music album name':None,
                'simple music track name':None,
                'country code':None,
            },
            'rule':[
                'rule.knowledge.simple.name.music.album',
                'rule.knowledge.simple.name.music.track',
                'rule.knowledge.release.year',
            ],
        },

        # Reference
        'ns.knowledge.movie.reference':{
            'synonym':['keyword',],
            'element':{
                'movie id':None,
                'itunes movie id':None,
                'tmdb movie id':None,
                'imdb movie id':None,
                'rottentomatoes movie id':None,
                'movie title':None,
                'simple movie title':None,
                'release date':None,
                'release year':None,
            },
            'rule':[
                'rule.knowledge.simple.name.movie',
                'rule.knowledge.release.year',
            ],
        },
        'ns.knowledge.tv.show.reference':{
            'synonym':['keyword',],
            'element':{
                'tv show id':None,
                'itunes tv show id':None,
                'tvdb tv show id':None,
                'imdb tv show id':None,
                'zap2it tv show id':None,
                'tv show name':None,
                'simple tv show name':None,
                'release date':None,
                'release year':None,
            },
            'rule':[
                'rule.knowledge.simple.name.tv.show',
                'rule.knowledge.release.year',
            ],
        },
        'ns.knowledge.tv.season.reference':{
            'synonym':['keyword',],
            'element':{
                'tv show id':None,
                'imdb tv show id':None,
                'itunes tv show id':None,
                'tvdb tv show id':None,
                'tv season id':None,
                'itunes tv season id':None,
                'tvdb tv season id':None,
                'tv season number':None,
                'disc count':None,
                'disc number':None,
                'track count':None,
                'tv show name':None,
                'simple tv show name':None,
                'release date':None,
                'release year':None,
            },
            'rule':[
                'rule.knowledge.simple.name.tv.show',
                'rule.knowledge.release.year',
            ],
        },
        'ns.knowledge.tv.episode.reference':{
            'synonym':['keyword',],
            'element':{
                'tv show id':None,
                'imdb tv show id':None,
                'itunes tv show id':None,
                'tvdb tv show id':None,
                'tv season id':None,
                'itunes tv season id':None,
                'tvdb tv season id':None,
                'imdb tv episode id':None,
                'itunes tv episode id':None,
                'tvdb tv episode id':None,
                'tv season number':None,
                'tv episode number':None,
                'disc count':None,
                'disc number':None,
                'track count':None,
                'track number':None,
                'tv episode name':None,
                'absolute tv episode number':None,
                'tv show name':None,
                'simple tv show name':None,
                'simple tv episode name':None,
                'release date':None,
                'release year':None,
            },
            'rule':[
                'rule.knowledge.simple.name.tv.show',
                'rule.knowledge.simple.name.tv.episode',
                'rule.knowledge.release.year',
            ],
        },
        'ns.knowledge.music.album.reference':{
            'synonym':['keyword',],
            'element':{
                'music album id':None,
                'album name':None,
                'itunes music album id':None,
                'simple music album name':None,
                'release date':None,
                'release year':None,
            },
            'rule':[
                'rule.knowledge.simple.name.music.album',
                'rule.knowledge.release.year',
            ],
        },
        'ns.knowledge.music.track.reference':{
            'synonym':['keyword',],
            'element':{
                'music album id':None,
                'itunes music album id':None,
                'track id':None,
                'itunes music track id':None,
                'album name':None,
                'disc count':None,
                'disc number':None,
                'track count':None,
                'track name':None,
                'track number':None,
                'simple music album name':None,
                'simple music track name':None,
                'release date':None,
                'release year':None,
            },
            'rule':[
                'rule.knowledge.simple.name.music.album',
                'rule.knowledge.simple.name.music.track',
                'rule.knowledge.release.year',
            ],
        },
        'ns.knowledge.person.reference':{
            'synonym':['keyword',],
            'element':{
                'person id':None,
                'itunes person id':None,
                'tmdb person id':None,
                'person name':None,
                'simple person name':None,
            },
            'rule':[
                'rule.knowledge.simple.name.person',
            ],
        },
        'ns.knowledge.company.reference':{
            'synonym':['keyword',],
            'element':{
                'company id':None,
                'tmdb company id':None,
                'company name':None,
                'simple company name':None,
            },
            'rule':[
                'rule.knowledge.simple.name.company',
            ],
        },
        'ns.knowledge.genre.reference':{
            'synonym':['keyword',],
            'element':{
                'genre id':None,
                'tmdb genre id':None,
                'itunes genre id':None,
                'genre name':None,
                'simple genre name':None,
            },
            'rule':[
                'rule.knowledge.simple.name.genre',
            ],
        },
        'ns.knowledge.collection.reference':{
            'synonym':['keyword', ],
            'element':{
                'collection id':None,
                'tmdb collection id':None,
                'collection name':None,
                'simple collection name':None,
            },
            'rule':[
                'rule.knowledge.simple.name.collection',
            ],
        },
        'ns.knowledge.keyword.reference':{
            'synonym':['keyword',],
            'element':{
                'keyword id':None,
                'tmdb keyword id':None,
                'keyword name':None,
                'simple keyword name':None,
            },
            'rule':[
                'rule.knowledge.simple.name.keyword',
            ],
        },
        'ns.knowledge.image.reference':{
            'synonym':['keyword',],
            'element':{
                'image url':None,
                'tvdb image id':None,
            },
        },

        'ns.knowledge.movie':{
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
                'movie title':{
                    'itunes':'trackName',
                    'tmdb':'title',
                    'rottentomatoes':'title',
                },
                'original movie title':{
                    'tmdb':'original_title',
                },
                'tagline':{
                    'tmdb':'tagline',
                },
                'country code':{
                    'tmdb':'iso_3166_1',
                    'itunes':'country',
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
                    'itunes':'releaseDate',
                },
                'release year':None,
                'description':{
                    'tmdb':'overview',
                    'rottentomatoes':'synopsis',
                },
                'long description':{
                    'itunes':'longDescription',
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
                'keywords':{
                    'tmdb':'keywords',
                    'namespace':'ns.knowledge.keyword',
                    'type':'embed',
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
                'part of a collection':{
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
                'content advisory rating':{
                    'rottentomatoes':'mpaa_rating',
                    'itunes':'contentAdvisoryRating',
                },
                'tmdb popularity':{
                    'tmdb':'popularity',
                },
                'artist name':{
                    'itunes':'artistName',
                },
                'simple movie title':None,
            },
            'rule':[
                'rule.knowledge.simple.name.movie',
                'rule.knowledge.release.year',
            ],
        },
        'ns.knowledge.tv.show':{
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
                'tv show name':{
                    'tvdb':'SeriesName',
                    'itunes':'artistName',
                },
                'modified date':{
                    'tvdb':'lastupdated',
                    'format':'unix time',
                },
                'release year':None,
                'release date':{
                    'tvdb':'FirstAired',
                },
                'content advisory rating':{
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
                'tv network name':{
                    'tvdb':'Network',
                },
                'runtime':{
                    'tvdb':'Runtime',
                },
                'tv show status':{
                    'tvdb':'Status',
                },
                'genres':{
                    'tvdb':'Genre',
                    'type':'unicode',
                    'plural format':'tvdb list',
                    'single element name':'genre name',
                },
                'actors':{
                    'tvdb':'Actors',
                    'type':'unicode',
                    'plural format':'tvdb list',
                    'single element name':'person name',
                },
                'image url':{
                    'tvdb':'poster',
                },
                'banner url':{
                    'tvdb':'banner',
                },
                'fan art url':{
                    'tvdb':'fanart',
                },
                'tv show air day':{
                    'tvdb':'Airs_DayOfWeek',
                },
                'tv show air time':{
                    'tvdb':'Airs_Time',
                },
                'cast':{
                    'tvdb':'Actor',
                },
                'posters':{
                    'tvdb':'Banner',
                },
                'simple tv show name':None,
                'country code':{
                    'itunes':'country',
                },
            },
            'rule':[
                'rule.knowledge.simple.name.tv.show',
                'rule.knowledge.release.year',
            ],
        },
        'ns.knowledge.tv.season':{
            'synonym':['keyword', 'tvdb', 'itunes'],
            'element':{
                'tv show id':None,
                'tv season id':None,
                'tv season number':None,
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
                'imdb tv show id':None,
                'disc count':None,
                'disc number':{
                    'tvdb':'SeasonNumber',
                },
                'track count':{
                    'itunes':'trackCount',
                },
                'tv show name':{
                    'itunes':'artistName',
                },
                'content advisory rating':{
                    'itunes':'contentAdvisoryRating',
                },
                'copyright':{
                    'itunes':'copyright',
                },
                'release year':None,
                'release date':{
                    'itunes':'releaseDate',
                },
                'long description':{
                    'itunes':'longDescription',
                },
                'language':{
                    'tvdb':'Language',
                },
                'album name':{
                    'itunes':'collectionName',
                },
                'simple tv show name':None,
                'country code':{
                    'itunes':'country',
                },
            },
            'rule':[
                'rule.itunes.tv.season.parse',
                'rule.knowledge.simple.name.tv.show',
                'rule.knowledge.release.year',
            ],
        },
        'ns.knowledge.tv.episode':{
            'synonym':['keyword', 'tvdb', 'itunes'],
            'element':{
                'tv show id':None,
                'tv season id':None,
                'tv season number':None,
                'tv episode number':None,
                'album name':{
                    'itunes':'collectionName',
                },
                'track name':None,
                'imdb tv episode id':{
                    'tvdb':'IMDB_ID',
                },
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
                'disc number':{
                    'tvdb':'SeasonNumber',
                },
                'track number':{
                    'tvdb':'EpisodeNumber',
                    'itunes':'trackNumber',
                },
                'track count':{
                    'itunes':'trackCount',
                },
                'tv episode name':{
                    'tvdb':'EpisodeName',
                    'itunes':'trackName',
                },
                'tv show name':{
                    'itunes':'artistName',
                },
                'absolute tv episode number':{
                    'tvdb':'absolute_number',
                },
                'modified date':{
                    'tvdb':'lastupdated',
                    'format':'unix time',
                },
                'language':{
                    'tvdb':'Language',
                },
                'release year':None,
                'release date':{
                    'tvdb':'FirstAired',
                    'itunes':'releaseDate',
                },
                'description':{
                    'tvdb':'Overview',
                    'unescape xml':True,
                    'itunes':'shortDescription',
                },
                'long description':{
                    'itunes':'longDescription',
                },
                'tv episode production code':{
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
                    'single element name':'person name',
                },
                'directors':{
                    'tvdb':'Director',
                    'plural format':'tvdb list',
                    'single element name':'person name',
                },
                'screenwriters':{
                    'tvdb':'Writer',
                    'plural format':'tvdb list',
                    'single element name':'person name',
                },
                'content advisory rating':{
                    'itunes':'contentAdvisoryRating',
                },
                'simple tv show name':None,
                'simple tv episode name':None,
                'country code':{
                    'itunes':'country',
                },
            },
            'rule':[
                'rule.itunes.tv.season.parse',
                'rule.knowledge.simple.name.tv.show',
                'rule.knowledge.simple.name.tv.episode',
                'rule.knowledge.release.year',
            ],
        },
        'ns.knowledge.music.album':{
            'synonym':['keyword', 'itunes'],
            'element':{
                'music album id':None,
                'album name':None,
                'music album name':{
                    'itunes':'collectionName',
                },
                'itunes music album id':{
                    'itunes':'collectionId',
                },
                'itunes person id':{
                    'itunes':'artistId',
                },
                'artist name':{
                    'itunes':'artistName',
                },
                'copyright':{
                    'itunes':'copyright',
                },
                'release date':{
                    'itunes':'releaseDate',
                },
                'release year':None,
                'track count':{
                    'itunes':'trackCount',
                },
                'simple music album name':None,
                'country code':{
                    'itunes':'country',
                },
            },
            'rule':[
                'rule.knowledge.simple.name.music.album',
                'rule.knowledge.release.year',
            ],
        },
        'ns.knowledge.music.track':{
            'synonym':['keyword', 'itunes'],
            'element':{
                'music album id':None,
                'track id':None,
                'music disc number':None,
                'music track number':None,
                'album name':None,
                'track name':None,
                'music album name':{
                    'itunes':'collectionName',
                },
                'music track name':{
                    'itunes':'trackName',
                },
                'itunes music album id':{
                    'itunes':'collectionId',
                },
                'itunes music track id':{
                    'itunes':'trackId',
                },
                'disc number':{
                    'itunes':'discNumber',
                },
                'disc count':{
                    'itunes':'discCount',
                },
                'track number':{
                    'itunes':'trackNumber',
                },
                'track count':{
                    'itunes':'trackCount',
                },
                'itunes person id':{
                    'itunes':'artistId',
                },
                'artist name':{
                    'itunes':'artistName',
                },
                'release date':{
                    'itunes':'releaseDate',
                },
                'release year':None,
                'simple music album name':None,
                'simple music track name':None,
                'country code':{
                    'itunes':'country',
                }
            },
            'rule':[
                'rule.knowledge.simple.name.music.album',
                'rule.knowledge.simple.name.music.track',
                'rule.knowledge.release.year',
            ],
        },
        'ns.knowledge.person':{
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
                'person name':{
                    'tmdb':'name',
                    'itunes':'artistName',
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
                'simple person name':None,
            },
            'rule':[
                'rule.knowledge.simple.name.person',
            ],
        },
        'ns.knowledge.company':{
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
                'company name':{
                    'tmdb':'name',
                },
                'simple company name':None,
            },
            'rule':[
                'rule.knowledge.simple.name.company',
            ],
        },
        'ns.knowledge.genre':{
            'synonym':['keyword', 'tmdb', 'itunes'],
            'element':{
                'genre id':None,
                'tmdb genre id':{
                    'tmdb':'id',
                },
                'itunes genre id':{
                    'itunes':'id',
                },
                'genre name':{
                    'tmdb':'name',
                    'itunes':'name',
                },
                'simple genre name':None,
            },
            'rule':[
                'rule.knowledge.simple.name.genre',
            ],
        },
        'ns.knowledge.collection':{
            'synonym':['keyword', 'tmdb'],
            'element':{
                'collection id':None,
                'tmdb collection id':{
                    'tmdb':'id',
                },
                'language':None,
                'collection name':{
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
        'ns.knowledge.country':{
            'synonym':['keyword'],
            'element':{
                'country code':None,
                'itunes country id':None,
                'country name':None,
                'native language name':None,
            },
        },
        'ns.knowledge.language':{
            'synonym':['keyword'],
            'element':{
                'language code':None,
                'language name':None,
                'native language name':None,
            },
        },

        'ns.knowledge.cast':{
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
                'person name':{
                    'tvdb':'Name',
                    'tmdb':'name',
                },
                'character name':{
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
            'rule':[
                'rule.knowledge.simple.name.person',
                'rule.knowledge.simple.name.character',
            ],
        },
        'ns.knowledge.review':{
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
        'ns.knowledge.company.credit':{
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
                'original movie title':{
                    'tmdb':'original_title',
                },
                'movie title':{
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
            'rule':[
                'rule.knowledge.simple.name.tv.show',
                'rule.knowledge.simple.name.tv.episode',
                'rule.knowledge.simple.name.movie',
                'rule.knowledge.simple.name.music.album',
                'rule.knowledge.simple.name.music.track',
            ],
        },
        'ns.knowledge.person.credit':{
            'synonym':['keyword', 'tmdb'],
            'element':{
                'tmdb movie id':{
                    'tmdb':'id',
                },
                'poster url':{
                    'tmdb':'poster_path',
                },
                'original movie title':{
                    'tmdb':'original_title',
                },
                'movie title':{
                    'tmdb':'title',
                },
                'character name':{
                    'tmdb':'character name',
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
            'rule':[
                'rule.knowledge.simple.name.character',
                'rule.knowledge.simple.name.tv.show',
                'rule.knowledge.simple.name.tv.episode',
                'rule.knowledge.simple.name.movie',
                'rule.knowledge.simple.name.music.album',
                'rule.knowledge.simple.name.music.track',
            ],
        },
        'ns.knowledge.certification':{
            'synonym':['keyword', 'tmdb', 'tvdb'],
            'element':{
                'content advisory rating':{
                    'tvdb':'ContentRating',
                    'tmdb':'certification',
                },
                'country code':{
                    'tmdb':'iso_3166_1',
                },
                'release date':{
                    'tvdb':'FirstAired',
                    'tmdb':u'release_date',
                },
            },
        },
        'ns.knowledge.image':{
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
                'thumbnail url':{
                    'tvdb':'ThumbnailPath',
                },
                'tvdb image id':{
                    'tvdb':'id',
                },
                'disc number':{
                    'tvdb':'Season',
                },
            },
        },
        'ns.knowledge.keyword':{
            'synonym':['keyword', 'tmdb'],
            'element':{
                'keyword id':None,
                'tmdb keyword id':{
                    'tmdb':'id',
                },
                'keyword name':{
                    'tmdb':'name',
                },
            },
        },

        'ns.search.query':{
            'synonym':['keyword','tmdb', 'rottentomatoes', 'itunes'],
            'element':{
                'api key':{
                    'tmdb':'api_key',
                    'rottentomatoes':'apikey',
                    'tvdb':'api key',
                },
                'term':{
                    'tmdb':'query',
                    'itunes':'term',
                },
                'movie title':{
                    'tmdb':'query',
                    'itunes':'term',
                },
                'simple movie title':{
                    'tmdb':'query',
                    'itunes':'term',
                },
                'tv show name':{
                    'tvdb':'seriesname',
                    'itunes':'term',
                },
                'simple tv show name':{
                    'tvdb':'seriesname',
                    'itunes':'term',
                },
                'music album name':{
                    'itunes':'term',
                },
                'simple music album name':{
                    'itunes':'term',
                },
                'person name':{
                    'tmdb':'query',
                    'itunes':'term',
                },
                'simple person name':{
                    'tmdb':'query',
                    'itunes':'term',
                },
                'company name':{
                    'tmdb':'query',
                    'itunes':'term',
                },
                'simple company name':{
                    'tmdb':'query',
                    'itunes':'term',
                },
                'page':{
                    'tmdb':'page',
                },
                'language':{
                    'tmdb':'language',
                    'tvdb':'language',
                },
                'release year':{
                    'tmdb':'year',
                },
                'itunes genre id':{
                    'itunes':'id',
                },
                'itunes person id':{
                    'itunes':'id',
                },
                'itunes movie id':{
                    'itunes':'id',
                },
                'itunes tv show id':{
                    'itunes':'id',
                },
                'itunes tv season id':{
                    'itunes':'id',
                },
                'itunes tv episode id':{
                    'itunes':'id',
                },
                'itunes music album id':{
                    'itunes':'id',
                },
                'itunes music track id':{
                    'itunes':'id',
                },
                'trimmed imdb movie id':{
                    'rottentomatoes':'id',
                },
                'imdb tv show id':{
                    'tvdb':'imdbid',
                },
            },
        },

        'ns.knowledge.job':{
            'synonym':['keyword'],
            'element':{
                'job id':None,
            },
        },
        'ns.knowledge.department':{
            'synonym':['keyword'],
            'element':{
                'department id':None,
            },
        },
    },
}
