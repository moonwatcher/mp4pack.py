# -*- coding: utf-8 -*-

{
    'rule':{
        # rule.system.default.host
        # rule.system.default.language
        # rule.system.volume.location
        # rule.system.temp.location

        'rule.job.implementation':{
            'name':'Job implementation',
            'provide':set(('implementation',)),
            'branch':[
                {
                    'requires':set(('action',)),
                    'equal':{'action':'get'},
                    'apply':(
                        {'property':'implementation', 'value':u'ServiceJob',},
                    ),
                },
                {
                    'requires':set(('action',)),
                    'equal':{'action':'remove'},
                    'apply':(
                        {'property':'implementation', 'value':u'ServiceJob',},
                    ),
                },
                {
                    'requires':set(('action',)),
                    'equal':{'action':'report'},
                    'apply':(
                        {'property':'implementation', 'value':u'ResourceJob',},
                    ),
                },
                {
                    'requires':set(('action',)),
                    'equal':{'action':'copy'},
                    'apply':(
                        {'property':'implementation', 'value':u'ResourceJob',},
                    ),
                },
                {
                    'requires':set(('action',)),
                    'equal':{'action':'move'},
                    'apply':(
                        {'property':'implementation', 'value':u'ResourceJob',},
                    ),
                },
                {
                    'requires':set(('action',)),
                    'equal':{'action':'delete'},
                    'apply':(
                        {'property':'implementation', 'value':u'ResourceJob',},
                    ),
                },
                {
                    'requires':set(('action',)),
                    'equal':{'action':'explode'},
                    'apply':(
                        {'property':'implementation', 'value':u'ResourceJob',},
                    ),
                },
                {
                    'requires':set(('action',)),
                    'equal':{'action':'pack'},
                    'apply':(
                        {'property':'implementation', 'value':u'ResourceJob',},
                    ),
                },
                {
                    'requires':set(('action',)),
                    'equal':{'action':'tag'},
                    'apply':(
                        {'property':'implementation', 'value':u'ResourceJob',},
                    ),
                },
                {
                    'requires':set(('action',)),
                    'equal':{'action':'optimize'},
                    'apply':(
                        {'property':'implementation', 'value':u'ResourceJob',},
                    ),
                },
                {
                    'requires':set(('action',)),
                    'equal':{'action':'transcode'},
                    'apply':(
                        {'property':'implementation', 'value':u'ResourceJob',},
                    ),
                },
                {
                    'requires':set(('action',)),
                    'equal':{'action':'update'},
                    'apply':(
                        {'property':'implementation', 'value':u'ResourceJob',},
                    ),
                },
            ]
        },
        'rule.task.default.preset':{
            'name':'Default task preset',
            'provide':set(('preset',)),
            'branch':[
                {
                    'requires':set(('action',)),
                    'equal':{'action':'report'},
                    'apply':(
                        {'property':'preset', 'value':u'normal',},
                    ),
                },
                {
                    'requires':set(('action',)),
                    'equal':{'action':'copy'},
                    'apply':(
                        {'property':'preset', 'value':u'normal',},
                    ),
                },
                {
                    'requires':set(('action',)),
                    'equal':{'action':'move'},
                    'apply':(
                        {'property':'preset', 'value':u'normal',},
                    ),
                },
                {
                    'requires':set(('action',)),
                    'equal':{'action':'delete'},
                    'apply':(
                        {'property':'preset', 'value':u'normal',},
                    ),
                },
                {
                    'requires':set(('action',)),
                    'equal':{'action':'explode'},
                    'apply':(
                        {'property':'preset', 'value':u'normal',},
                    ),
                },
                {
                    'requires':set(('action',)),
                    'equal':{'action':'pack'},
                    'apply':(
                        {'property':'preset', 'value':u'normal',},
                    ),
                },
                {
                    'requires':set(('action',)),
                    'equal':{'action':'tag'},
                    'apply':(
                        {'property':'preset', 'value':u'normal',},
                    ),
                },
                {
                    'requires':set(('action',)),
                    'equal':{'action':'optimize'},
                    'apply':(
                        {'property':'preset', 'value':u'normal',},
                    ),
                },
                {
                    'requires':set(('action',)),
                    'equal':{'action':'transcode'},
                    'apply':(
                        {'property':'preset', 'value':u'normal',},
                    ),
                },
                {
                    'requires':set(('action',)),
                    'equal':{'action':'update'},
                    'apply':(
                        {'property':'preset', 'value':u'normal',},
                    ),
                },
            ]
        },
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
        'rule.system.mongodb.url':{
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
                    'requires':set(('host', 'port',)),
                    'apply':[
                        {
                            'property':'mongodb url',
                            'format':u'mongodb://{host}:{port}',
                        },
                    ],
                },
                {
                    'requires':set(('host',)),
                    'apply':[
                        {
                            'property':'mongodb url',
                            'format':u'mongodb://{host}',
                        },
                    ],
                },
            ],
        },

        'rule.medium.home.umid':{
            'name':'UMID from home id',
            'provide':set(('umid',)),
            'branch':[
                {
                    'requires':set(('home id',)),
                    'apply':[
                        { 'property':'umid', 'digest':['home id', 'media kind'], 'algorithm':'umid' },
                    ],
                },
            ],
        },        
        'rule.medium.home.uri':{
            'name':'Home URI',
            'provide':set(('home uri',)),
            'branch':[
                {
                    'requires':set((
                        'home id',
                    )),
                    'apply':[
                        { 'property':'home uri', 'format':u'/h/{home id}', },
                    ],
                },
                {
                    'requires':set((
                        'media kind',
                        'movie id',
                    )),
                    'equal':{'media kind':9, },
                    'apply':[
                        { 'property':'home uri', 'format':u'/h/movie/{movie id}', },
                    ],
                },
                {
                    'requires':set((
                        'media kind',
                        'movie handle',
                    )),
                    'equal':{'media kind':9, },
                    'apply':[
                        { 'property':'home uri', 'format':u'/h/movie/~/{movie handle}', },
                    ],
                },
                {
                    'requires':set((
                        'media kind',
                        'tmdb movie id',
                    )),
                    'equal':{'media kind':9, },
                    'apply':[
                        { 'property':'home uri', 'format':u'/h/movie/tmdb/{tmdb movie id}', },
                    ],
                },
                {
                    'requires':set((
                        'media kind',
                        'imdb movie id',
                    )),
                    'equal':{'media kind':9, },
                    'apply':[
                        { 'property':'home uri', 'format':u'/h/movie/imdb/{imdb movie id}', },
                    ],
                },
                {
                    'requires':set((
                        'media kind',
                        'rottentomatoes movie id',
                    )),
                    'equal':{'media kind':9, },
                    'apply':[
                        { 'property':'home uri', 'format':u'/h/movie/rottentomatoes/{rottentomatoes movie id}', },
                    ],
                },
                {
                    'requires':set((
                        'media kind',
                        'tv episode id',
                    )),
                    'equal':{'media kind':10, },
                    'apply':[
                        { 'property':'home uri', 'format':u'/h/tv/episode/{tv episode id}', },
                    ],
                },
                {
                    'requires':set((
                        'media kind',
                        'tv season id',
                        'track number',
                    )),
                    'equal':{'media kind':10, },
                    'apply':[
                        { 'property':'home uri', 'format':u'/h/tv/episode/{tv season id}/{track number}', },
                    ],
                },
                {
                    'requires':set((
                        'media kind',
                        'tv show id',
                        'disc number',
                        'track number',
                    )),
                    'equal':{'media kind':10, },
                    'apply':[
                        { 'property':'home uri', 'format':u'/h/tv/episode/{tv show id}/{disc number}/{track number}', },
                    ],
                },
                {
                    'requires':set((
                        'media kind',
                        'tv show handle',
                        'disc number',
                        'track number',
                    )),
                    'equal':{'media kind':10, },
                    'apply':[
                        { 'property':'home uri', 'format':u'/h/tv/episode/~/{tv show handle}/{disc number}/{track number}', },
                    ],
                },
                {
                    'requires':set((
                        'media kind',
                        'tvdb tv episode id',
                    )),
                    'equal':{'media kind':10, },
                    'apply':[
                        { 'property':'home uri', 'format':u'/h/tv/episode/tvdb/{tvdb tv episode id}', },
                    ],
                },
                {
                    'requires':set((
                        'media kind',
                        'tvdb tv season id',
                        'track number',
                    )),
                    'equal':{'media kind':10, },
                    'apply':[
                        { 'property':'home uri', 'format':u'/h/tv/episode/tvdb/{tvdb tv season id}/{track number}', },
                    ],
                },
                {
                    'requires':set((
                        'media kind',
                        'tvdb tv show id',
                        'disc number',
                        'track number',
                    )),
                    'equal':{'media kind':10, },
                    'apply':[
                        { 'property':'home uri', 'format':u'/h/tv/episode/tvdb/{tvdb tv show id}/{disc number}/{track number}', },
                    ],
                },
                {
                    'requires':set((
                        'media kind',
                        'imdb tv episode id',
                    )),
                    'equal':{'media kind':10, },
                    'apply':[
                        { 'property':'home uri', 'format':u'/h/tv/episode/imdb/{imdb tv episode id}', },
                    ],
                },
                {
                    'requires':set((
                        'media kind',
                        'imdb tv show id',
                        'disc number',
                        'track number',
                    )),
                    'equal':{'media kind':10, },
                    'apply':[
                        { 'property':'home uri', 'format':u'/h/tv/episode/imdb/{imdb tv show id}/{disc number}/{track number}', },
                    ],
                },
                {
                    'requires':set((
                        'media kind',
                        'track id',
                    )),
                    'equal':{'media kind':1, },
                    'apply':[
                        { 'property':'home uri', 'format':u'/h/music/track/{track id}', },
                    ],
                },
                {
                    'requires':set((
                        'media kind',
                        'music album id',
                        'disc number',
                        'track number',
                    )),
                    'equal':{'media kind':1, },
                    'apply':[
                        { 'property':'home uri', 'format':u'/h/music/track/{music album id}/{disc number}/{track number}', },
                    ],
                },
                {
                    'requires':set((
                        'media kind',
                        'album handle',
                        'disc number',
                        'track number',
                    )),
                    'equal':{'media kind':1, },
                    'apply':[
                        { 'property':'home uri', 'format':u'/h/music/track/~/{album handle}/{disc number}/{track number}', },
                    ],
                },
            ],
        },
        'rule.medium.asset.uri':{
            'name':'Asset URI',
            'provide':set(('asset uri',)),
            'branch':[
                {
                    'requires':set(('home id',)),
                    'apply':[
                        {
                            'property':'asset uri',
                            'format':u'/m/asset/{home id}',
                        },
                    ],
                },
            ],
        },
        'rule.medium.resource.uri':{
            'name':'Resource URI',
            'provide':set(('resource uri',)),
            'branch':[
                {
                    'requires':set(('path digest',)),
                    'apply':[
                        {
                            'property':'resource uri',
                            'format':u'/m/resource/sha1/{path digest}',
                        },
                    ],
                },
            ],
        },
        'rule.medium.resource.filename.parse':{
            'name':'Parse file name',
            'provide':set((
                'kind',
                'media kind',
                'disc number',
                'track number',
                'imdb movie id',
                'tmdb movie id',
                'itunes movie id',
                'tv show handle',
                'tvdb tv show id',
                'album handle',
                'track name',
                'resource path digest',
                'language',
                'stream id',
                'umid',
            )),
            'branch':[
                {
                    'requires':set(('file name',)),
                    'match':{'property':'file name', 'expression':ur'^[0-9a-f]{40}(?:\.[a-z]{2})?\.[0-9]{2}\.[0-9a-f]{13}\.[^\.]{3,4}$', },
                    'decode':[
                        {'property':'file name', 'expression':ur'^(?P<resource_path_digest>[0-9a-f]{40})(?:\.(?P<language>[a-z]{2}))?\.(?P<stream_id>[0-9]{2})\.(?P<umid>[0-9a-f]{13})\.(?P<kind>[^\.]{3,4})$',},
                    ],
                },
                {
                    'requires':set(('file name',)),
                    'match':{'property':'file name', 'expression':ur'^.{2,} s[0-9]+e[0-9]+(?: .*)?\.[^\.]{3,4}$', },
                    'decode':[
                        {'property':'file name', 'expression':ur'^TVDb(?P<tvdb_tv_show_id>[0-9]+) s(?P<disc_number>[0-9]+)e(?P<track_number>[0-9]+)(?:\s*(?P<track_name>.*))?\.(?P<kind>[^\.]{3,4})$',},
                    ],
                    'apply':[
                        {'property':'media kind', 'value':10,},
                    ],
                },
                {
                    'requires':set(('file name',)),
                    'match':{'property':'file name', 'expression':ur'^.{2,} d[0-9]+t[0-9]+(?: .*)?\.[^\.]{3,4}$', },
                    'decode':[
                        {'property':'file name', 'expression':ur'^(?P<album_handle>.{2,}) d(?P<disc_number>[0-9]+)t(?P<track_number>[0-9]+)(?:\s*(?P<track_name>.*))?\.(?P<kind>[^\.]{3,4})$',},
                    ],
                    'apply':[
                        {'property':'media kind', 'value':1,},
                    ],
                },
                {
                    'requires':set(('file name',)),
                    'match':{'property':'file name', 'expression':ur'^IMDbtt[0-9]+(?: .*)?\.[^\.]{3,4}$', },
                    'decode':[
                        {'property':'file name', 'expression':ur'^IMDb(?P<imdb_movie_id>tt[0-9]+)(?: (?P<track_name>.*))?\.(?P<kind>[^\.]{3,4})$',},
                    ],
                    'apply':[
                        {'property':'media kind', 'value':9,},
                    ],
                },
                {
                    'requires':set(('file name',)),
                    'match':{'property':'file name', 'expression':ur'^TMDb[0-9]+(?: .*)?\.[^\.]{3,4}$', },
                    'decode':[
                        {'property':'file name', 'expression':ur'^TMDb(?P<tmdb_movie_id>[0-9]+)(?: (?P<track_name>.*))?\.(?P<kind>[^\.]{3,4})$',},
                    ],
                    'apply':[
                        {'property':'media kind', 'value':9,},
                    ],
                },
                {
                    'requires':set(('file name',)),
                    'match':{'property':'file name', 'expression':ur'^iTMF[0-9]+(?: .*)?\.[^\.]{3,4}$', },
                    'decode':[
                        {'property':'file name', 'expression':ur'^iTMF(?P<itunes_movie_id>[0-9]+)(?: (?P<track_name>.*))?\.(?P<kind>[^\.]{3,4})$',},
                    ],
                    'apply':[
                        {'property':'media kind', 'value':9,},
                    ],
                },
            ],
        },
        'rule.medium.resource.filename.canonic':{
            'name':'Canonic file name',
            'provide':set(('canonic file name',)),
            'branch':[
                {
                    'requires':set(( 'media kind', 'simple tv show name', 'track genealogy', 'simple tv episode name', 'umid', 'kind', 'localized', )),
                    'equal':{'media kind':10, 'localized':False, },
                    'apply':[
                        {
                            'property':'canonic file name',
                            'format':u'{simple tv show name} {track genealogy} {simple tv episode name}.{umid}.{kind}',
                        },
                    ],
                },                
                {
                    'requires':set(( 'media kind', 'simple tv show name', 'track genealogy', 'simple tv episode name', 'umid', 'kind', 'language', 'localized', )),
                    'equal':{'media kind':10, 'localized':True, },
                    'apply':[
                        {
                            'property':'canonic file name',
                            'format':u'{simple tv show name} {track genealogy} {simple tv episode name}.{language}.{umid}.{kind}',
                        },
                    ],
                },
                {
                    'requires':set(( 'media kind', 'simple movie title', 'umid', 'kind', 'localized', )),
                    'equal':{'media kind':9, 'localized':False, },
                    'apply':[
                        {
                            'property':'canonic file name',
                            'format':u'{simple movie title}.{umid}.{kind}',
                        },
                    ],
                },
                {
                    'requires':set(( 'media kind', 'simple movie title', 'umid', 'kind', 'language', 'localized', )),
                    'equal':{'media kind':9, 'localized':True, },
                    'apply':[
                        {
                            'property':'canonic file name',
                            'format':u'{simple movie title}.{language}.{umid}.{kind}',
                        },
                    ],
                },
            ],
        },
        'rule.medium.resource.directory.canonic':{
            'name':'Canonic directory',
            'provide':set(('canonic directory',)),
            'branch':[
                {
                    'requires':set(('volume path', 'media kind', 'kind', 'profile', 'tv show id', 'disc number', )),
                    'equal':{'media kind':10, },
                    'apply':[
                        {
                            'property':'canonic directory',
                            'format':u'{volume path}/{media kind}/{kind}/{profile}/{tv show id}/{disc number}',
                        },
                    ],
                },
                {
                    'requires':set(('volume path', 'media kind', 'kind', 'profile', )),
                    'equal':{'media kind':9, },
                    'apply':[
                        {
                            'property':'canonic directory',
                            'format':u'{volume path}/{media kind}/{kind}/{profile}',
                        },
                    ],
                },
            ],
        },
        'rule.medium.resource.path.canonic':{
            'name':'canonic path',
            'provide':set(('canonic path',)),
            'branch':[
                {
                    'requires':set(('canonic directory', 'canonic file name')),
                    'apply':[
                        {
                            'property':'canonic path',
                            'format':u'{canonic directory}/{canonic file name}',
                        },
                    ],
                },
            ],
        },
        'rule.medium.resource.filename.implicit':{
            'name':'implicit filename',
            'provide':set(('file name',)),
            'branch':[
                {
                    'requires':set(('canonic file name',)),
                    'apply':[
                        {
                            'property':'file name',
                            'reference':u'canonic file name',
                        },
                    ],
                },
            ],
        },
        'rule.medium.resource.directory.implicit':{
            'name':'implicit directory',
            'provide':set(('directory',)),
            'branch':[
                {
                    'requires':set(('canonic directory',)),
                    'apply':[
                        {
                            'property':'directory',
                            'reference':u'canonic directory',
                        },
                    ],
                },
            ],
        },
        'rule.medium.resource.path.implicit':{
            'name':'implicit path',
            'provide':set(('path',)),
            'branch':[
                {
                    'requires':set(('directory', 'file name',)),
                    'apply':[
                        {
                            'property':'path',
                            'format':u'{directory}/{file name}',
                        },
                    ],
                },
            ],
        },
        'rule.medium.resource.filename.fragment':{
            'name':'Fragment file name',
            'provide':set(('fragment file name',)),
            'branch':[
                {
                    'requires':set(('resource path digest', 'language', 'stream id', 'umid', 'kind', 'localized', )),
                    'equal':{'localized':True, },
                    'apply':[
                        {
                            'property':'fragment file name',
                            'format':u'{resource path digest}.{language}.{stream id:>02}.{umid}.{kind}',
                        },
                    ],
                },
                {
                    'requires':set(('resource path digest', 'stream id', 'umid', 'kind', 'localized', )),
                    'equal':{'localized':False, },
                    'apply':[
                        {
                            'property':'fragment file name',
                            'format':u'{resource path digest}.{stream id:>02}.{umid}.{kind}',
                        },
                    ],
                },
            ],
        },
        'rule.medium.resource.directory.fragment':{
            'name':'Fragment directory',
            'provide':set(('fragment directory',)),
            'branch':[
                {
                    'requires':set(('temp path', )),
                    'apply':[
                        {
                            'property':'fragment directory',
                            'format':u'{temp path}',
                        },
                    ],
                },
            ],
        },
        'rule.medium.resource.path.fragment':{
            'name':'Fragment path',
            'provide':set(('fragment path',)),
            'branch':[
                {
                    'requires':set(('fragment directory', 'fragment file name',)),
                    'apply':[
                        {
                            'property':'fragment path',
                            'format':u'{fragment directory}/{fragment file name}',
                        },
                    ],
                },
            ],
        },        
        'rule.medium.resource.kind.language':{
            'name':'Kind language dependency',
            'provide':set(('localized',)),
            'branch':[
                {
                    'requires':set(('kind',)),
                    'equal':{'kind':'m4v', },
                    'apply':[
                        { 'property':'localized', 'value':False, },
                    ],
                },
                {
                    'requires':set(('kind',)),
                    'equal':{'kind':'m4a', },
                    'apply':[
                        { 'property':'localized', 'value':False, },
                    ],
                },
                {
                    'requires':set(('kind',)),
                    'equal':{'kind':'mkv', },
                    'apply':[
                        { 'property':'localized', 'value':False, },
                    ],
                },
                {
                    'requires':set(('kind',)),
                    'equal':{'kind':'avi', },
                    'apply':[
                        { 'property':'localized', 'value':False, },
                    ],
                },
                {
                    'requires':set(('kind',)),
                    'equal':{'kind':'srt', },
                    'apply':[
                        { 'property':'localized', 'value':True, },
                    ],
                },
                {
                    'requires':set(('kind',)),
                    'equal':{'kind':'ass', },
                    'apply':[
                        { 'property':'localized', 'value':True, },
                    ],
                },
                {
                    'requires':set(('kind',)),
                    'equal':{'kind':'chpl', },
                    'apply':[
                        { 'property':'localized', 'value':True, },
                    ],
                },
                {
                    'requires':set(('kind',)),
                    'equal':{'kind':'ac3', },
                    'apply':[
                        { 'property':'localized', 'value':True, },
                    ],
                },
                {
                    'requires':set(('kind',)),
                    'equal':{'kind':'dts', },
                    'apply':[
                        { 'property':'localized', 'value':True, },
                    ],
                },
                {
                    'requires':set(('kind',)),
                    'equal':{'kind':'flac', },
                    'apply':[
                        { 'property':'localized', 'value':True, },
                    ],
                },
                {
                    'requires':set(('kind',)),
                    'equal':{'kind':'png', },
                    'apply':[
                        { 'property':'localized', 'value':True, },
                    ],
                },
                {
                    'requires':set(('kind',)),
                    'equal':{'kind':'jpg', },
                    'apply':[
                        { 'property':'localized', 'value':True, },
                    ],
                },
            ],
        },
        'rule.medium.resource.track.genealogy':{
            'name':'Compose the track genealogy',
            'provide':set(('track genealogy',)),
            'branch':[
                {
                    'requires':set(('media kind', 'disc number', 'track number')),
                    'equal':{'media kind':10, },
                    'apply':[
                        {
                            'property':'track genealogy',
                            'format':u's{disc number:02d}e{track number:02d}',
                        },
                    ],
                },
                {
                    'requires':set(('media kind', 'disc number', 'track number')),
                    'equal':{'media kind':1, },
                    'apply':[
                        {
                            'property':'track genealogy',
                            'format':u'd{disc number:02d}t{track number:02d}',
                        },
                    ],
                },
            ],
        },
        'rule.medium.resource.path.digest':{
            'name':'Path digest',
            'provide':set(('path digest',)),
            'branch':[
                {
                    'requires':set(('path',)),
                    'apply':[
                        { 'property':'path digest', 'digest':'path', 'algorithm':'sha1' },
                    ],
                },
            ],
        },
        'rule.medium.stream.audio.name':{
            'name':'audio track name',
            'provide':set(('stream name',)),
            'branch':[
                {
                    'requires':set(('stream kind', 'channels')),
                    'equal':{'stream kind':'audio', 'channels':1 },
                    'apply':[
                        { 'property':'stream name', 'value':'Mono' },
                    ],
                },
                {
                    'requires':set(('stream kind', 'channels')),
                    'equal':{'stream kind':'audio', 'channels':2 },
                    'apply':[
                        { 'property':'stream name', 'value':'Stereo' },
                    ],
                },
                {
                    'requires':set(('stream kind', 'channels')),
                    'equal':{'stream kind':'audio', 'channels':3 },
                    'apply':[
                        { 'property':'stream name', 'value':'Stereo' },
                    ],
                },
                {
                    'requires':set(('stream kind', 'channels')),
                    'equal':{'stream kind':'audio', 'channels':4 },
                    'apply':[
                        { 'property':'stream name', 'value':'Quadraphonic' },
                    ],
                },
                {
                    'requires':set(('stream kind', 'channels')),
                    'equal':{'stream kind':'audio', 'channels':5 },
                    'apply':[
                        { 'property':'stream name', 'value':'Surround' },
                    ],
                },
                {
                    'requires':set(('stream kind', 'channels')),
                    'equal':{'stream kind':'audio', 'channels':6 },
                    'apply':[
                        { 'property':'stream name', 'value':'Surround' },
                    ],
                },
                {
                    'requires':set(('stream kind', 'channels')),
                    'equal':{'stream kind':'audio', 'channels':7 },
                    'apply':[
                        { 'property':'stream name', 'value':'Surround' },
                    ],
                },
                {
                    'requires':set(('stream kind', 'channels')),
                    'equal':{'stream kind':'audio', 'channels':8 },
                    'apply':[
                        { 'property':'stream name', 'value':'Surround' },
                    ],
                },
            ],
        },
        'rule.medium.stream.default.position':{
            'name':'Default stream kind position',
            'provide':set(('stream kind position',)),
            'branch':[
                {
                    'apply':[
                        {'property':'stream kind position', 'value':1,},
                    ],
                },
            ],
        },
        'rule.medium.stream.default.primary':{
            'name':'Default primary stream',
            'provide':set(('primary',)),
            'branch':[
                {
                    'apply':[
                        {'property':'primary', 'value':False },
                    ],
                },
            ],
        },
        'rule.medium.stream.default.id':{
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
        'rule.medium.stream.audio.kind':{
            'name':'Kind for audio stream',
            'provide':set(('kind',)),
            'branch':[
                {
                    'requires':set(('format',)),
                    'equal':{'stream kind':'audio', 'format':'AC-3'},
                    'apply':[
                        { 'property':'kind', 'value':'ac3' },
                    ],
                },
                {
                    'requires':set(('format',)),
                    'equal':{'format':'DTS'},
                    'apply':[
                        { 'property':'kind', 'value':'dts' },
                    ],
                },
                {
                    'requires':set(('format',)),
                    'equal':{'format':'MPEG Audio'},
                    'apply':[
                        { 'property':'kind', 'value':'mp3' },
                    ],
                },
                {
                    'requires':set(('format',)),
                    'equal':{'format':'AAC'},
                    'apply':[
                        { 'property':'kind', 'value':'aac' },
                    ],
                },
                {
                    'requires':set(('format',)),
                    'equal':{'format':'PCM'},
                    'apply':[
                        { 'property':'kind', 'value':'pcm' },
                    ],
                },
                {
                    'requires':set(('format',)),
                    'equal':{'format':'FLAC'},
                    'apply':[
                        { 'property':'kind', 'value':'flac' },
                    ],
                },
                {
                    'requires':set(('format',)),
                    'equal':{'format':'Vorbis'},
                    'apply':[
                        { 'property':'kind', 'value':'ogg' },
                    ],
                },
            ],
        },
        'rule.medium.stream.video.kind':{
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
        'rule.medium.stream.image.kind':{
            'name':'Kind for image stream',
            'provide':set(('kind',)),
            'branch':[
                {
                    'requires':set(('format',)),
                    'equal':{'format':'LZ77'},
                    'apply':[
                        { 'property':'kind', 'value':'png' },
                    ],
                },
                {
                    'requires':set(('format',)),
                    'equal':{'format':'JPEG'},
                    'apply':[
                        { 'property':'kind', 'value':'jpg' },
                    ],
                },
            ],
        },
        'rule.medium.stream.text.kind':{
            'name':'Kind for text stream',
            'provide':set(('kind',)),
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
                    'requires':set(('stream kind',)),
                    'equal':{'stream kind':'menu'},
                    'apply':[
                        { 'property':'kind', 'value':'chpl' },
                    ],
                },
            ],
        },
        
        'rule.knowledge.movie.imdb.trimmed':{
            'name':'trimmed imdb movie id',
            'provide':set(('trimmed imdb movie id',)),
            'branch':[
                {
                    'requires':set(('imdb movie id',)),
                    'decode':[
                        {'property':'imdb movie id', 'expression':ur'^tt(?P<trimmed_imdb_movie_id>[0-9]+)$'},
                    ],
                },
            ],
        },        
        'rule.knowledge.track.position':{
            'name':'Compute the composite track position',
            'provide':set(('track position',)),
            'branch':[
                {
                    'requires':set(('media kind', 'track number', 'track count')),
                    'equal':{'media kind':10, },
                    'apply':[
                        { 'property':'track position', 'format':u'{track number} / {track count}', },
                    ],
                },
                {
                    'requires':set(('media kind', 'track number', 'track count')),
                    'equal':{'media kind':1, },
                    'apply':[
                        { 'property':'track position', 'format':u'{track number} / {track count}', },
                    ],
                },
            ],
        },
        'rule.knowledge.disc.position':{
            'name':'Compute the composite disc position',
            'provide':set(('disc position',)),
            'branch':[
                {
                    'requires':set(('disc number', 'disc count')),
                    'equal':{'media kind':10, },
                    'apply':[
                        { 'property':'disc position', 'format':u'{disc number} / {disc count}', },
                    ],
                },
                {
                    'requires':set(('disc number', 'disc count')),
                    'equal':{'media kind':1, },
                    'apply':[
                        { 'property':'disc position', 'format':u'{disc number} / {disc count}', },
                    ],
                },
            ],
        },
        'rule.knowledge.default.track.count':{
            'name':'Default track count',
            'provide':set(('track count',)),
            'branch':[
                {
                    'requires':set(('media kind',)),
                    'equal':{'media kind':10, },
                    'apply':[
                        {'property':'track count', 'value':0},
                    ],
                },
                {
                    'requires':set(('media kind',)),
                    'equal':{'media kind':1, },
                    'apply':[
                        {'property':'track count', 'value':0},
                    ],
                },
            ],
        },
        'rule.knowledge.default.disc.count':{
            'name':'Default disc count',
            'provide':set(('disc count',)),
            'branch':[
                {
                    'requires':set(('media kind',)),
                    'equal':{'media kind':10, },
                    'apply':[
                        {'property':'disc count', 'value':0},
                    ],
                },
                {
                    'requires':set(('media kind',)),
                    'equal':{'media kind':1, },
                    'apply':[
                        {'property':'disc count', 'value':0},
                    ],
                },
            ],
        },
        'rule.knowledge.default.tv.episode':{
            'name':'Default TV episode number',
            'provide':set(('tv episode number', 'tv season number')),
            'branch':[
                {
                    'requires':set(('media kind', 'track number', 'disc number')),
                    'equal':{'media kind':10, },
                    'apply':[
                        { 'property':'tv episode number', 'reference':'track number', },
                        { 'property':'tv season number', 'reference':'disc number', },
                    ],
                },
            ],
        },
        'rule.knowledge.default.music.track':{
            'name':'Default music track number',
            'provide':set(('music track number', 'music disc number')),
            'branch':[
                {
                    'requires':set(('media kind', 'track number', 'disc number')),
                    'equal':{'media kind':1, },
                    'apply':[
                        { 'property':'music track number', 'reference':'track number', },
                        { 'property':'music disc number', 'reference':'disc number', },
                    ],
                },
            ],
        },

        'rule.knowledge.sort.name':{
            'name':'sort name',
            'provide':set(('sort name',)),
            'branch':[
                {
                    'requires':set(('track name',)),
                    'decode':[
                        {'property':'track name', 'expression':ur'^(the |a |an )?(?P<sort_name>.+)$', 'flags':re.IGNORECASE},
                    ],
                },
            ],
        },
        'rule.knowledge.sort.artist':{
            'name':'sort artist',
            'provide':set(('sort artist',)),
            'branch':[
                {
                    'requires':set(('artist name',)),
                    'decode':[
                        {'property':'artist name', 'expression':ur'^(the |a |an )?(?P<sort_artist>.+)$', 'flags':re.IGNORECASE},
                    ],
                },
            ],
        },
        'rule.knowledge.sort.albumartist':{
            'name':'sort album artist',
            'provide':set(('sort album artist',)),
            'branch':[
                {
                    'requires':set(('album artist name',)),
                    'decode':[
                        {'property':'album artist name', 'expression':ur'^(the |a |an )?(?P<sort_album_artist>.+)$', 'flags':re.IGNORECASE},
                    ],
                },
            ],
        },
        'rule.knowledge.sort.album':{
            'name':'sort album',
            'provide':set(('sort album',)),
            'branch':[
                {
                    'requires':set(('album name',)),
                    'decode':[
                        {'property':'album name', 'expression':ur'^(the |a |an )?(?P<sort_album>.+)$', 'flags':re.IGNORECASE},
                    ],
                },
            ],
        },
        'rule.knowledge.sort.composer':{
            'name':'sort composer',
            'provide':set(('sort composer',)),
            'branch':[
                {
                    'requires':set(('composer name',)),
                    'decode':[
                        {'property':'composer name', 'expression':ur'^(the |a |an )?(?P<sort_composer>.+)$', 'flags':re.IGNORECASE},
                    ],
                },
            ],
        },
        'rule.knowledge.sort.show':{
            'name':'sort tv show',
            'provide':set(('sort tv show',)),
            'branch':[
                {
                    'requires':set(('tv show name',)),
                    'decode':[
                        {'property':'tv show name', 'expression':ur'^(the |a |an )?(?P<sort_tv_show>.+)$', 'flags':re.IGNORECASE},
                    ],
                },
            ],
        },
        'rule.knowledge.artist.info':{
            'name':'artist information',
            'provide':set(('artist name', 'album artist name')),
            'branch':[
                {
                    'requires':set(('media kind', 'tv show name')),
                    'equal':{'media kind':10, },
                    'apply':[
                        {
                            'property':'artist name',
                            'format':u'{tv show name}',
                        },
                        {
                            'property':'album artist name',
                            'format':u'{tv show name}',
                        },
                    ],
                },
                {
                    'requires':set(('media kind', 'directors')),
                    'equal':{'media kind':9, },
                    'apply':[
                        {
                            'property':'artist name',
                            'format':u'{directors[0]}',
                        },
                        {
                            'property':'album artist name',
                            'format':u'{directors[0]}',
                        },
                    ],
                },
                {
                    'requires':set(('media kind', 'producers')),
                    'equal':{'media kind':9, },
                    'apply':[
                        {
                            'property':'artist name',
                            'format':u'{producers[0]}',
                        },
                        {
                            'property':'album artist name',
                            'format':u'{producers[0]}',
                        },
                    ],
                },
                {
                    'requires':set(('media kind', 'screenwriters')),
                    'equal':{'media kind':9, },
                    'apply':[
                        {
                            'property':'artist name',
                            'format':u'{screenwriters[0]}',
                        },
                        {
                            'property':'album artist name',
                            'format':u'{screenwriters[0]}',
                        },
                    ],
                },
                {
                    'requires':set(('media kind', 'codirectors')),
                    'equal':{'media kind':9, },
                    'apply':[
                        {
                            'property':'artist name',
                            'format':u'{codirectors[0]}',
                        },
                        {
                            'property':'album artist name',
                            'format':u'{codirectors[0]}',
                        },
                    ],
                },
                {
                    'requires':set(('media kind', 'actors')),
                    'equal':{'media kind':9, },
                    'apply':[
                        {
                            'property':'artist name',
                            'format':u'{actors[0]}',
                        },
                        {
                            'property':'album artist name',
                            'format':u'{actors[0]}',
                        },
                    ],
                },
            ],
        },
        'rule.knowledge.asset.name':{
            'name':'full name',
            'provide':set(('full name',)),
            'branch':[
                {
                    'requires':set(('media kind', 'tv show name', 'tv episode production code', 'track name')),
                    'equal':{'media kind':10, },
                    'apply':[
                        {
                            'property':'full name',
                            'format':u'{tv show name} {tv episode production code} {track name}',
                        },
                    ],
                },
                {
                    'requires':set(('media kind', 'tv show name', 'tv episode production code')),
                    'equal':{'media kind':10, },
                    'apply':[
                        {
                            'property':'full name',
                            'format':u'{tv show name} {tv episode production code}',
                        },
                    ],
                },
                {
                    'requires':set(('media kind', 'imdb movie id', 'track name')),
                    'equal':{'media kind':9, },
                    'apply':[
                        {
                            'property':'full name',
                            'format':u'IMDb{imdb movie id} {track name}',
                        },
                    ],
                },
                {
                    'requires':set(('media kind', 'imdb movie id')),
                    'equal':{'media kind':9, },
                    'apply':[
                        {
                            'property':'full name',
                            'format':u'IMDb{imdb movie id}',
                        },
                    ],
                },
            ],
        },
        'rule.itunes.itunextc.parse':{
            'name':'Parse itunextc atom',
            'provide':set((
                'content advisory standard',
                'content advisory rating',
                'content advisory score',
                'content advisory annotation',
            )),
            'branch':[
                {
                    'requires':set(('itunextc',)),
                    'decode':[
                        {'property':'itunextc', 'expression':ur'(?P<content_advisory_standard>[^|]+)\|(?P<content_advisory_rating>[^|]+)\|(?P<content_advisory_score>[^|]+)\|(?P<content_advisory_annotation>[^|]+)?',},
                    ],
                },
            ],
        },
        'rule.itunes.album.name':{
            'name':'Album name for iTunes',
            'provide':set(('album name',)),
            'branch':[
                {
                    'requires':set(('media kind', 'tv show name', 'tv season number')),
                    'equal':{'media kind':10, },
                    'apply':[
                        {
                            'property':'album name',
                            'format':u'{tv show name}, Season {tv season number}',
                        },
                    ],
                },
            ],
        },
        'rule.itunes.tv.season.parse':{
            'name':'Parse itunes tv season',
            'provide':set(('disc number',)),
            'branch':[
                {
                    'requires':set(('album name',)),
                    'decode':[
                        {'property':'album name', 'expression':ur', Season (?P<disc_number>[0-9]+)$',},
                    ],
                },
            ],
        },        
        'rule.knowledge.release.year':{
            'name':'Release year from date',
            'provide':set(('release year',)),
            'branch':[
                {
                    'requires':set(('release date',)),
                    'apply':[
                        {'property':'release year', 'datetime format':u'%Y', 'reference':'release date', },
                    ],
                },
            ],
        },

        
        'rule.knowledge.simple.name.movie':{
            'name':'Simple movie title',
            'provide':set(('simple movie title',)),
            'branch':[
                {
                    'requires':set(('movie title',)),
                    'decode':[
                        {'property':'movie title', 'expression':ur'^(?P<simple_movie_title>.+)$'},
                    ],
                },
            ],
        },
        'rule.knowledge.simple.name.tv.show':{
            'name':'Simple tv show name',
            'provide':set(('simple tv show name',)),
            'branch':[
                {
                    'requires':set(('tv show name',)),
                    'decode':[
                        {'property':'tv show name', 'expression':ur'^(?P<simple_tv_show_name>.+)$'},
                    ],
                },
            ],
        },
        'rule.knowledge.simple.name.tv.episode':{
            'name':'Simple tv episode name',
            'provide':set(('simple tv episode name',)),
            'branch':[
                {
                    'requires':set(('tv episode name',)),
                    'decode':[
                        {'property':'tv episode name', 'expression':ur'^(?P<simple_tv_episode_name>.+)$'},
                    ],
                },
            ],
        },
        'rule.knowledge.simple.name.music.album':{
            'name':'Simple music album name',
            'provide':set(('simple music album name',)),
            'branch':[
                {
                    'requires':set(('music album name',)),
                    'decode':[
                        {'property':'music album name', 'expression':ur'^(?P<simple_music_album_name>.+)$'},
                    ],
                },
            ],
        },
        'rule.knowledge.simple.name.music.track':{
            'name':'Simple music track name',
            'provide':set(('simple music track name',)),
            'branch':[
                {
                    'requires':set(('music track name',)),
                    'decode':[
                        {'property':'music track name', 'expression':ur'^(?P<simple_music_track_name>.+)$'},
                    ],
                },
            ],
        },
        'rule.knowledge.simple.name.person':{
            'name':'Simple person name',
            'provide':set(('simple person name',)),
            'branch':[
                {
                    'requires':set(('person name',)),
                    'decode':[
                        {'property':'person name', 'expression':ur'^(?P<simple_person_name>.+)$'},
                    ],
                },
            ],
        },
        'rule.knowledge.simple.name.company':{
            'name':'Simple company name',
            'provide':set(('simple company name',)),
            'branch':[
                {
                    'requires':set(('company name',)),
                    'decode':[
                        {'property':'company name', 'expression':ur'^(?P<simple_company_name>.+)$'},
                    ],
                },
            ],
        },
        'rule.knowledge.simple.name.collection':{
            'name':'Simple collection name',
            'provide':set(('simple collection name',)),
            'branch':[
                {
                    'requires':set(('collection name',)),
                    'decode':[
                        {'property':'collection name', 'expression':ur'^(?P<simple_collection_name>.+)$'},
                    ],
                },
            ],
        },
        'rule.knowledge.simple.name.keyword':{
            'name':'Simple keyword name',
            'provide':set(('simple keyword name',)),
            'branch':[
                {
                    'requires':set(('keyword name',)),
                    'decode':[
                        {'property':'keyword name', 'expression':ur'^(?P<simple_keyword_name>.+)$'},
                    ],
                },
            ],
        },
        'rule.knowledge.simple.name.genre':{
            'name':'Simple genre name',
            'provide':set(('simple genre name',)),
            'branch':[
                {
                    'requires':set(('genre name',)),
                    'decode':[
                        {'property':'genre name', 'expression':ur'^(?P<simple_genre_name>.+)$'},
                    ],
                },
            ],
        },
        'rule.knowledge.simple.name.character':{
            'name':'Simple character name',
            'provide':set(('simple character name',)),
            'branch':[
                {
                    'requires':set(('character name',)),
                    'decode':[
                        {'property':'character name', 'expression':ur'^(?P<simple_character_name>.+)$'},
                    ],
                },
            ],
        },
    },
}