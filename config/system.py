# -*- coding: utf-8 -*-

{
    'system':{
        'home':u'/usr/local/etc/mpk',
        'domain':None,
        'host':None,
        'threads':2,
        'language':'en',
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
        'dot':u'.',
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
                        'help':'Get a JSON formated document by URI',
                    },
                    'argument':[
                        'uris',
                        'sync',
                        'download',
                    ]
                },
                {
                    'instruction':{
                        'name':'report',
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
                                'title':'Subtitle trascoding',
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
            }
        },
    },
}
