# -*- coding: utf-8 -*-

{
    'system':{
        'domain':u'galanti.no-ip.info',
        'host':u'shaft',
    },
    'repository':{
        'shaft':{
            'domain':u'galanti.no-ip.info',
            'temp':{
                'path':u'/Users/lg/Downloads/mpk/temp',
            },
            'mongodb':{
                'database':u'mp4pack',
                'host':u'localhost',
            },
            'remote':{
                'download port':u'22040',
                'priority port':u'22010',
                'tunneled mongodb port':u'27018',
            },
            'volume':{
                'default':{
                    'index':True,
                    'scan':True,
                },
                'synonym':['path'],
                'element':{
                    'alpha':{
                        'name':u'Alpha',
                        'path':u'/Users/lg/Downloads/mpk/pool/alpha',
                    },
                    'epsilon':{
                        'name':u'Epsilon',
                        'path':u'/Users/lg/Downloads/mpk/pool/epsilon',
                    },
                },
            },
            'mapping':[
                {
                    'enable':False,
                    'path':u'/Users',
                    'alternate':[
                        u'/net/shaft/Users',
                    ],
                },
            ],
            'routing':[
                {
                    'requires':set(('kind', 'host',)),
                    'equal':{'host':'shaft', 'kind':'srt',},
                    'apply':(
                        {'property':'volume', 'value':u'epsilon',},
                        {'property':'profile', 'value':u'clean',},
                    ),
                },
                {
                    'requires':set(('kind', 'host',)),
                    'equal':{'host':'shaft', 'kind':'png',},
                    'apply':(
                        {'property':'volume', 'value':u'alpha',},
                        {'property':'profile', 'value':u'normal',},
                    ),
                },
                {
                    'requires':set(('kind', 'host',)),
                    'equal':{'host':'shaft', 'kind':'chpl',},
                    'apply':(
                        {'property':'volume', 'value':u'alpha',},
                        {'property':'profile', 'value':u'normal',},
                    ),
                },
                {
                    'requires':set(('kind', 'host',)),
                    'equal':{'host':'shaft', 'kind':'m4v',},
                    'apply':(
                        {'property':'volume', 'value':u'epsilon',},
                        {'property':'profile', 'value':u'A4',},
                    ),
                },
                {
                    'requires':set(('kind', 'host',)),
                    'equal':{'host':'shaft', 'kind':'mkv',},
                    'apply':(
                        {'property':'volume', 'value':u'epsilon',},
                        {'property':'profile', 'value':u'720',},
                    ),
                },
                {
                    'requires':set(('kind', 'host',)),
                    'equal':{'host':'shaft', 'kind':'avi',},
                    'apply':(
                        {'property':'volume', 'value':u'epsilon',},
                        {'property':'profile', 'value':u'sd',},
                    ),
                },
                {
                    'requires':set(('kind', 'host',)),
                    'equal':{'host':'shaft', 'kind':'ac3',},
                    'apply':(
                        {'property':'volume', 'value':u'epsilon',},
                        {'property':'profile', 'value':u'normal',},
                    ),
                },
                {
                    'requires':set(('kind', 'host',)),
                    'equal':{'host':'shaft', 'kind':'ass',},
                    'apply':(
                        {'property':'volume', 'value':u'epsilon',},
                        {'property':'profile', 'value':u'original',},
                    ),
                },
                {
                    'requires':set(('kind', 'host',)),
                    'equal':{'host':'shaft', 'kind':'dts',},
                    'apply':(
                        {'property':'volume', 'value':u'epsilon',},
                        {'property':'profile', 'value':u'original',},
                    ),
                },
            ],
        },
        'multivac':{
            'enable':False,
            'domain':u'galanti.no-ip.info',
            'mongodb':{
                'database':u'mp4pack',
                'username':u'mp4pack',
                'password':u'poohbear',
                'host':u'multivac',
            },
            'remote':{
                'download port':u'22040',
                'priority port':u'22010',
                'tunneled mongodb port':u'27018',
            },
            'volume':{
                'default':{
                    'index':True,
                    'scan':True,
                },
                'synonym':['path'],
                'element':{
                    u'alpha':{
                        'name':u'Alpha',
                        'path':u'/net/multivac/Volumes/alphaville/alpha',
                    },
                    u'beta':{
                        'name':u'Beta',
                        'path':u'/net/vito/media/nyc/beta',
                    },
                    u'gama':{
                        'name':u'Gama',
                        'path':u'/net/vito/media/cambridge/gama',
                    },
                    u'kappa':{
                        'name':u'Kappa',
                        'path':u'/net/vito/media/tokyo/kappa',
                    },
                    u'eta':{
                        'name':u'Eta',
                        'path':u'/net/multivac/Volumes/boston/eta',
                    },
                    u'epsilon':{
                        'name':u'Epsilon',
                        'path':u'/net/multivac/Volumes/nagasaki/epsilon',
                    },
                },
            },
            'mapping':[
                {
                    'path':u'/net/multivac/Volumes/alphaville',
                    'alternate':[
                        u'/Volumes/alphaville',
                    ],
                },
                {
                    'path':u'/net/vito/media/nyc',
                    'alternate':[
                        u'/Volumes/nyc',
                    ],
                },
                {
                    'path':u'/net/vito/media/cambridge',
                    'alternate':[
                        u'/Volumes/cambridge',
                    ],
                },
                {
                    'path':u'/net/vito/media/tokyo',
                    'alternate':[
                        u'/Volumes/tokyo',
                    ],
                },
                {
                    'path':u'/net/multivac/Volumes/boston',
                    'alternate':[
                        u'/Volumes/boston',
                    ],
                },
                {
                    'path':u'/net/multivac/Volumes/nagasaki',
                    'alternate':[
                        u'/Volumes/nagasaki',
                    ],
                },
            ],
            'routing':[
                {
                    'requires':set(('kind', 'host',)),
                    'equal':{'host':'multivac', 'kind':'srt',},
                    'apply':(
                        {'property':'volume', 'value':u'alpha',},
                        {'property':'profile', 'value':u'clean',},
                    ),
                },
                {
                    'requires':set(('kind', 'host',)),
                    'equal':{'host':'multivac', 'kind':'png',},
                    'apply':(
                        {'property':'volume', 'value':u'alpha',},
                        {'property':'profile', 'value':u'normal',},
                    ),
                },
                {
                    'requires':set(('kind', 'host',)),
                    'equal':{'host':'multivac', 'kind':'chpl',},
                    'apply':(
                        {'property':'volume', 'value':u'alpha',},
                        {'property':'profile', 'value':u'chapter',},
                    ),
                },
                {
                    'requires':set(('kind', 'host',)),
                    'equal':{'host':'multivac', 'kind':'m4v',},
                    'apply':(
                        {'property':'volume', 'value':u'epsilon',},
                        {'property':'profile', 'value':u'iA4',},
                    ),
                },
                {
                    'requires':set(('kind', 'host',)),
                    'equal':{'host':'multivac', 'kind':'m4a',},
                    'apply':(
                        {'property':'volume', 'value':u'alpha',},
                        {'property':'profile', 'value':u'lossless',},
                    ),
                },
                {
                    'requires':set(('kind', 'host',)),
                    'equal':{'host':'multivac', 'kind':'mkv',},
                    'apply':(
                        {'property':'volume', 'value':u'epsilon',},
                        {'property':'profile', 'value':u'720',},
                    ),
                },
                {
                    'requires':set(('kind', 'host',)),
                    'equal':{'host':'multivac', 'kind':'avi',},
                    'apply':(
                        {'property':'volume', 'value':u'epsilon',},
                        {'property':'profile', 'value':u'sd',},
                    ),
                },
                {
                    'requires':set(('kind', 'host',)),
                    'equal':{'host':'multivac', 'kind':'ac3',},
                    'apply':(
                        {'property':'volume', 'value':u'epsilon',},
                        {'property':'profile', 'value':u'normal',},
                    ),
                },
                {
                    'requires':set(('kind', 'host',)),
                    'equal':{'host':'multivac', 'kind':'ass',},
                    'apply':(
                        {'property':'volume', 'value':u'epsilon',},
                        {'property':'profile', 'value':u'original',},
                    ),
                },
                {
                    'requires':set(('kind', 'host',)),
                    'equal':{'host':'multivac', 'kind':'dts',},
                    'apply':(
                        {'property':'volume', 'value':u'epsilon',},
                        {'property':'profile', 'value':u'original',},
                    ),
                },
            ]
        },
    },
}