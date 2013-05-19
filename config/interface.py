# -*- coding: utf-8 -*-

{
    'interface':{
        'default':{
            'namespace':'ns.system.command.default',
            'global':{
                'argument':[
                    'verbosity',
                    'domain',
                    'host',
                    'configuration path',
                    'debug',
                    'version',
                ],
            },
            'action':[
                {
                    'instruction':{
                        'name':'get',
                        'help':'Get documents',
                    },
                    'argument':[
                        'uris',
                        'sync',
                        'download',
                        'query',
                    ]
                },
                {
                    'instruction':{
                        'name':'drop',
                        'help':'Drop documents',
                    },
                    'argument':[
                        'uris',
                        'sync',
                        'download',
                    ]
                },
                {
                    'instruction':{
                        'name':'info',
                        'help':'Report information about resource',
                    },
                    'argument':[
                        'scan path',
                        'inclusion',
                        'exclusion',
                        'recursive',
                        'overwrite',
                        'sync',
                        'crawl',
                        'download',
                    ]
                },
                {
                    'instruction':{
                        'name':'copy',
                        'help':'Copy resource into location',
                    },
                    'argument':[
                        'scan path',
                        'volume',
                        'profile',
                        'inclusion',
                        'exclusion',
                        'recursive',
                        'overwrite',
                        'sync',
                        'crawl',
                        'download',
                    ]
                },
                {
                    'instruction':{
                        'name':'move',
                        'help':'Move resource into location',
                    },
                    'argument':[
                        'scan path',
                        'volume',
                        'profile',
                        'inclusion',
                        'exclusion',
                        'recursive',
                        'overwrite',
                        'sync',
                        'crawl',
                        'download',
                    ]
                },
                {
                    'instruction':{
                        'name':'delete',
                        'help':'Delete resource',
                    },
                    'argument':[
                        'scan path',
                        'inclusion',
                        'exclusion',
                        'recursive',
                    ]
                },
                {
                    'instruction':{
                        'name':'explode',
                        'help':'Explode streams from container',
                    },
                    'argument':[
                        'scan path',
                        'preset',
                        'inclusion',
                        'exclusion',
                        'recursive',
                        'overwrite',
                        'sync',
                        'crawl',
                    ]
                },
                {
                    'instruction':{
                        'name':'pack',
                        'help':'Pack streams into a container',
                    },
                    'argument':[
                        'scan path',
                        'kind',
                        'volume',
                        'profile',
                        'preset',
                        'inclusion',
                        'exclusion',
                        'recursive',
                        'overwrite',
                        'sync',
                        'crawl',
                        'language',
                    ]
                },
                {
                    'instruction':{
                        'name':'tag',
                        'help':'Update meta tags',
                    },
                    'argument':[
                        'scan path',
                        'preset',
                        'inclusion',
                        'exclusion',
                        'recursive',
                        'sync',
                        'crawl',
                        'language',
                    ]
                },
                {
                    'instruction':{
                        'name':'optimize',
                        'help':'Optimize file structure',
                    },
                    'argument':[
                        'scan path',
                        'inclusion',
                        'exclusion',
                        'recursive',
                        'sync',
                        'crawl',
                    ]
                },
                {
                    'instruction':{
                        'name':'transcode',
                        'help':'Transcode files to profile',
                    },
                    'argument':[
                        'scan path',
                        'kind',
                        'volume',
                        'profile',
                        'preset',
                        'inclusion',
                        'exclusion',
                        'recursive',
                        'overwrite',
                        'sync',
                        'crawl',
                        'download',
                    ],
                    'group':[
                        {
                            'instruction':{
                                'title':'Video transcoding',
                            },
                            'argument':[
                                'quantizer',
                                'width',
                                'crop',
                            ],
                        },
                        {
                            'instruction':{
                                'title':'Subtitle transcoding',
                            },
                            'argument':[
                                'time shift',
                                'source frame rate',
                                'target frame rate',
                            ],
                        }
                    ]
                },
                {
                    'name':'update',
                    'instruction':{
                        'name':'update',
                        'help':'Update streams in container',
                    },
                    'argument':[
                        'scan path',
                        'kind',
                        'volume',
                        'preset',
                        'profile',
                        'inclusion',
                        'exclusion',
                        'recursive',
                        'sync',
                        'crawl',
                        'download',
                        'language',
                    ]
                },
                {
                    'instruction':{
                        'name':'rebuild',
                        'help':'Rebuild database',
                    },
                    'argument':[
                        'all',
                        'tables',
                    ]
                },
            ],
            'prototype':{
                'domain':{
                    'flag':['--domain'],
                    'parameter':{
                        'help':'Local network domain',
                        'metavar':'DOMAIN',
                        'dest':'domain',
                    },
                },
                'host':{
                    'flag':['--host'],
                    'parameter':{ 
                        'help':'Repository host name',
                        'metavar':'HOST',
                        'dest':'host',
                    },
                },
                'volume':{
                    'flag':['-o', '--volume'],
                    'parameter':{ 
                        'help':'Select volume',
                        'metavar':'VOL',
                        'dest':'volume',
                    },
                },
                'profile':{
                    'flag':['-p', '--profile'],
                    'parameter':{ 
                        'help':'Select profile',
                        'metavar':'PROFILE',
                        'dest':'profile',
                    },
                },
                'preset':{
                    'flag':['-s', '--preset'],
                    'parameter':{ 
                        'help':'Select preset',
                        'metavar':'PRESET',
                        'dest':'preset',
                    },
                },
                'all':{
                    'flag':['-a', '--all'],
                    'parameter':{ 
                        'action':'store_true',
                        'default':False,
                        'help':'All',
                        'dest':'all',
                    },
                },
                'recursive':{
                    'flag':['-r', '--recursive'],
                    'parameter':{ 
                        'action':'store_true',
                        'default':False,
                        'help':'Recurse into directories',
                        'dest':'recursive',
                    },
                },
                'sync':{
                    'flag':['-S', '--sync'],
                    'parameter':{ 
                        'action':'store_true',
                        'default':False,
                        'help':'Synchronize service',
                        'dest':'sync',
                    },
                },
                'crawl':{
                    'flag':['-U', '--crawl'],
                    'parameter':{ 
                        'action':'store_true',
                        'default':False,
                        'help':'Force rebuilding meta data index for resources',
                        'dest':'crawl',
                    },
                },
                'download':{
                    'flag':['-D', '--download'],
                    'parameter':{ 
                        'action':'store_true',
                        'default':False,
                        'help':'Download remote resources if local is unavailable',
                        'dest':'download',
                    },
                },
                'overwrite':{
                    'flag':['-w', '--overwrite'],
                    'parameter':{
                        'action':'store_true',
                        'default':False,
                        'help':'Overwrite existing files',
                        'dest':'overwrite',
                    },
                },
                'kind':{
                    'flag':['-k', '--kind'],
                    'parameter':{
                        'help':'Select kind',
                        'metavar':'KIND',
                        'dest':'kind',
                    },
                },
                'inclusion':{
                    'flag':['-f', '--include'],
                    'parameter':{
                        'help':'Inclusion regex filter',
                        'metavar':'EXP',
                        'dest':'inclusion',
                    },
                },
                'exclusion':{
                    'flag':['--exclude'],
                    'parameter':{
                        'help':'Exclusion regex filter',
                        'metavar':'EXP',
                        'dest':'exclusion',
                    },
                },
                'language':{
                    'flag':['-l', '--lang'],
                    'parameter':{
                        'help':'Select language by ISO 639-1 2 letter code',
                        'metavar':'CODE',
                        'dest':'language',
                    },
                },
                'scan path':{
                    'flag':['scan path'],
                    'parameter':{
                        'help':'File or directory paths to scan',
                        'nargs':'*',
                        'metavar':'PATH',
                    },
                },
                'uris':{
                    'flag':['uris'],
                    'parameter':{
                        'help':'List of URIs',
                        'nargs':'*',
                        'metavar':'URI',
                    },
                },
                'query':{
                    'flag':['-q', '--query'],
                    'parameter':{ 
                        'help':'Query parameters for lookup',
                        'dest':'query',
                        'metavar':'DICT',
                    },
                },
                'quantizer':{
                    'flag':['-q', '--quantizer'],
                    'parameter':{
                        'help':'Override the x264 quantizer value',
                        'metavar':'QUANTIZER',
                        'dest':'quantizer',
                        'type':float,
                    },
                },
                'width':{
                    'flag':['-W', '--width'],
                    'parameter':{
                        'help':'Override profile set maximum pixel width',
                        'metavar':'PIXEL',
                        'dest':'width',
                        'type':int,
                    },
                },
                'crop':{
                    'flag':['--crop'],
                    'parameter':{
                        'help':'Override HandBrake automatic crop',
                        'metavar':'T:B:L:R',
                        'dest':'crop',
                    },
                },
                'time shift':{
                    'flag':['--shift'],
                    'parameter':{
                        'help':'Offset in milliseconds',
                        'metavar':'MILLISECOND',
                        'dest':'time shift',
                        'type':int,
                    },
                },
                'source frame rate':{
                    'flag':['--from'],
                    'parameter':{
                        'help':'Source frame rate',
                        'dest':'source frame rate',
                    },
                },
                'target frame rate':{
                    'flag':['--to'],
                    'parameter':{
                        'help':'Target frame rate',
                        'dest':'target frame rate',
                    },
                },
                'verbosity':{
                    'flag':['-v', '--verbosity'],
                    'parameter':{ 
                        'default':'info',
                        'help':'logging verbosity level',
                        'dest':'verbosity',
                    },
                },
                'debug':{
                    'flag':['-d', '--debug'],
                    'parameter':{
                        'action':'store_true',
                        'default':False,
                        'help':'Only print commands without executing',
                        'dest':'debug',
                    },
                },
                'configuration path':{
                    'flag':['--conf'],
                    'parameter':{ 
                        'help':'Configuration file path',
                        'metavar':'PATH',
                        'dest':'configuration path',
                    },
                },
                'version':{
                    'flag':['--version'],
                    'parameter':{ 
                        'action':'version',
                        'version':'%(prog)s 0.5'
                    },
                },
                'tables':{
                    'flag':['tables'],
                    'parameter':{ 
                        'help':'List of tables',
                        'nargs':'*',
                        'metavar':'NAME',
                    },
                },
            }
        },
    },
    'command':[
        {'name':'rsync',        'binary':u'rsync', },
        {'name':'mv',           'binary':u'mv', },
        {'name':'rm',           'binary':u'rm', },
        {'name':'handbrake',    'binary':u'HandbrakeCLI', },
        {'name':'subler',       'binary':u'SublerCLI', },
        {'name':'mkvmerge',     'binary':u'mkvmerge', },
        {'name':'mkvextract',   'binary':u'mkvextract', },
        {'name':'mp4file',      'binary':u'mp4file', },
        {'name':'mp4art',       'binary':u'mp4art', },
        {'name':'mediainfo',    'binary':u'mediainfo', },
        {'name':'ffmpeg',       'binary':u'ffmpeg', }
    ],
}
