#!/usr/bin/env python
# -*- coding: utf-8 -*-

tmdb_apikey = u'a8b9f96dde091408a03cb4c78477bd14'
tvdb_apikey = u'7B3B400B0146EA83'
cache_path = u'/net/multivac/Volumes/alphaville/cache/'

repository_config = {
    'Volume':{
        'alpha':'/Volumes/alphaville/alpha',
        'beta':'/Volumes/nyc/beta',
        'gama':'/Volumes/cambridge/gama',
        'delta':'/net/vito/media/fairfield/delta',
        'eta':'/net/vito/media/tlv/eta',
        'epsilon':'/Volumes/alphaville/epsilon',
    },
    'Command':{
        'rsync':{
            'base':[u'rsync']
        },
        'mv':{
            'base':[u'mv']
        },
        'handbrake':{
            'base':[u'HandbrakeCLI']
        },
        'subler':{
            'base':[u'SublerCLI']
        },
        'mkvmerge':{
            'base':[u'mkvmerge']
        },
        'mkvinfo':{
            'base':[u'mkvinfo']
        },
        'mkvextract':{
            'base':[u'mkvextract']
        },
        'mp4info':{
            'base':[u'mp4info']
        },
        'mp4chaps':{
            'base':[u'mp4chaps']
        },
        'mp4file':{
            'base':[u'mp4file']
        },
        'mp4art':{
            'base':[u'mp4art']
        },
        'aften':{
            'base':[u'aften']
        },
        'dcadec':{
            'base':[u'dcadec']
        },
    },
    'Display':{
        'wrap':120, 
        'indent':30, 
        'margin':2,
    },
    'Action':{
        'pack': ('mkv',),
        'transcode':('m4v', 'mkv', 'srt', 'txt', 'jpg', 'ac3', 'tc'),
        'update':('srt','jpg', 'txt'),
    },
    'Codec':{
        'Audio':{
            'ac3':'ac-3|AC3',
            'aac':'AAC',
            'dts':'DTS',
            'mp3':'MPEG/L3',
        },
        'Subtitle':{
            'srt':'S_TEXT/UTF8',
            'ass':'S_TEXT/ASS',
        },
    },
    'Language':{
        'heb':'Hebrew', 
        'eng':'English',
        'swe':'Swedish',
        'fre':'French',
        'ita':'Italian',
        'jpa':'Japanese',
    },
    'Media Kind':{
        'tvshow':{'schema':ur'^(.+) (s([0-9]+)e([0-9]+))(?:\s*(.*))?\.([^\.]+)$', 'name':'TV Show', 'stik':10},
        'movie':{'schema':ur'^IMDb(tt[0-9]+)(?: (.*))?\.([^\.]+)$', 'name':'Movie', 'stik':9},
        #'music':{'schema':'^([0-9]+)(?:-([0-9]+))?(?: (.*))?\.([^\.]+)$', 'name':'Music', 'stik':1},
        #'audiobook':{'schema':'^([0-9]+)(?:-([0-9]+))?(?: (.*))?\.([^\.]+)$', 'name':'Audiobook', 'stik':2},
    },
    'Kind':{
        'm4v':{
            'container':'mp4',
            'default':{'volume':'epsilon'},
            'Profile':{
                'universal':{
                    'description':'an SD profile that decodes on every cabac capable apple device',
                    'default':{
                        'tvshow':{'volume':'beta'},
                        'movie':{'volume':'gama'},
                    },
                    'transcode':{
                        'options':{
                            '--quality':18,
                            '--encoder':'x264',
                            '--x264opts':'ref=2:me=umh:b-adapt=2:weightp=0:trellis=0:subme=9:cabac=1',
                            '--maxWidth':720,
                        },
                        'flags':('--large-file',),
                        'audio':(
                            (
                                {
                                    'from': {'kind':'ac3', 'type':'audio'},
                                    'to': {'--aencoder':'ac3', '--ab':'auto', '--mixdown':'auto'},
                                }, 
                                {
                                    'from': {'kind':'ac3', 'type':'audio'},
                                    'to': {'--aencoder':'ca_aac', '--ab':160, '--mixdown':'dpl2'},
                                },
                            ),
                            (
                                {
                                    'from': {'kind':'aac', 'type':'audio'},
                                    'to': {'--aencoder':'ca_aac', '--ab':128, '--mixdown':'stereo'},
                                },
                                {
                                    'from': {'kind':'mp3', 'type':'audio'},
                                    'to': {'--aencoder':'ca_aac', '--ab':128, '--mixdown':'stereo'},
                                },
                            ),
                        ),
                    },
                },
                'appletv':{
                    'description':'Intel based AppleTV profile',
                    'default':{
                        'tvshow':{'volume':'beta'},
                        'movie':{'volume':'eta'},
                    },
                    'transcode':{
                        'options':{
                            '--quality':22,
                            '--encoder':'x264',
                            '--x264opts':'ref=3:bframes=3:me=umh:b-adapt=2:weightp=0:weightb=0:trellis=0:subme=9:vbv-maxrate=9500:vbv-bufsize=9500:cabac=1',
                            '--maxWidth':1280,
                        },
                        'flags':('--large-file',),
                        'audio':(
                            (
                                {
                                    'from': {'kind':'ac3', 'type':'audio'},
                                    'to': {'--aencoder':'ac3', '--ab':'auto', '--mixdown':'auto'},
                                }, 
                                {
                                    'from': {'kind':'ac3', 'type':'audio'},
                                    'to': {'--aencoder':'ca_aac', '--ab':160, '--mixdown':'dpl2'},
                                },
                            ),
                            (
                                {
                                    'from': {'kind':'aac', 'type':'audio'},
                                    'to': {'--aencoder':'ca_aac', '--ab':128, '--mixdown':'stereo'},
                                },
                            ),
                            (
                                {
                                    'from': {'kind':'mp3', 'type':'audio'},
                                    'to': {'--aencoder':'ca_aac', '--ab':128, '--mixdown':'stereo'},
                                },
                            ),
                        ),
                    },
                },
                'ipod':{
                    'description':'All iPod touch models profile',
                    'default':{
                        'tvshow':{'volume':'epsilon'},
                        'movie':{'volume':'epsilon'},
                    },
                    'transcode':{
                        'options':{
                            '--quality':21,
                            '--encoder':'x264',
                            '--x264opts':'ref=2:me=umh:bframes=0:8x8dct=0:trellis=0:subme=6:weightp=0:cabac=0',
                            '--maxWidth':480,
                        },
                        'audio':(
                            (
                                {
                                    'from': {'kind':'ac3', 'type':'audio'},
                                    'to': {'--aencoder':'ca_aac', '--ab':128, '--mixdown':'stereo'},
                                },
                            ),
                            (
                                {
                                    'from': {'kind':'aac', 'type':'audio'},
                                    'to': {'--aencoder':'ca_aac', '--ab':128, '--mixdown':'stereo'},
                                },
                            ),
                            (
                                {
                                    'from': {'kind':'mp3', 'type':'audio'},
                                    'to': {'--aencoder':'ca_aac', '--ab':128, '--mixdown':'stereo'},
                                },
                            ),
                        ),
                    },
                },
                'high':{
                    'description':'High profile',
                    'default':{
                        'tvshow':{'volume':'beta'},
                        'movie':{'volume':'eta'},
                    },
                    'transcode':{
                        'options':{
                            '--quality':18,
                            '--encoder':'x264',
                            '--x264opts':'ref=3:bframes=3:me=umh:b-adapt=2:weightp=0:weightb=0:trellis=0:subme=9:vbv-maxrate=10000:vbv-bufsize=10000:cabac=1',
                            '--maxWidth':1280
                        },
                        'flags':('--large-file',),
                        'audio':(
                            (
                                {
                                    'from': {'kind':'ac3', 'type':'audio'},
                                    'to': {'--aencoder':'ac3', '--ab':'auto', '--mixdown':'auto'},
                                }, 
                                {
                                    'from': {'kind':'ac3', 'type':'audio'},
                                    'to': {'--aencoder':'ca_aac', '--ab':192, '--mixdown':'dpl2'},
                                },
                            ),
                            (
                                {
                                    'from': {'kind':'aac', 'type':'audio'},
                                    'to': {'--aencoder':'ca_aac', '--ab':128, '--mixdown':'stereo'},
                                },
                                {
                                    'from': {'kind':'mp3', 'type':'audio'},
                                    'to': {'--aencoder':'ca_aac', '--ab':128, '--mixdown':'stereo'},
                                },
                            ),
                        ),
                    },
                },
            },
        },
        'm4a':{
            'container':'mp4',
            'default':{'volume':'alpha'},
            'Profile':{
                'lossless':{},
                'portable':{},
            },
        },
        'mkv':{
            'container':'matroska',
            'default':{'volume':'epsilon'},
            'Profile':{
                'sd':{
                    'default':{
                        'tvshow':{'volume':'delta'},
                        'movie':{'volume':'delta'},
                    },
                    'pack':{
                        'related':(
                            {'kind':'srt', 'profile':'clean', 'language':'heb'},
                            {'kind':'srt', 'profile':'clean', 'language':'eng'},
                            {'kind':'txt', 'profile':'chapter'},
                            {'kind':'ac3', 'profile':'dump'},
                            {'kind':'tc', 'profile':'dump'},
                        ),
                        'tracks':(
                            {'type':'video'},
                            {'type':'audio', 'kind':'ac3'},
                            {'type':'audio', 'kind':'mp3'},
                            {'type':'audio', 'kind':'aac'},
                            {'type':'audio', 'kind':'dts'},
                        ),
                    },
                },
                '720':{
                    'default':{
                        'tvshow':{'volume':'delta'},
                        'movie':{'volume':'delta'},
                    },
                    'pack':{
                        'related':(
                            {'kind':'srt', 'profile':'clean', 'language':'heb'},
                            {'kind':'srt', 'profile':'clean', 'language':'eng'},
                            {'kind':'txt', 'profile':'chapter'},
                            {'kind':'ac3', 'profile':'dump'},
                            {'kind':'tc', 'profile':'dump'},
                        ),
                        'tracks':(
                            {'type':'video'},
                            {'type':'audio', 'kind':'ac3'},
                            {'type':'audio', 'kind':'mp3'},
                            {'type':'audio', 'kind':'aac'},
                            {'type':'audio', 'kind':'dts'},
                        ),
                    },
                },
                '1080':{
                    'default':{
                        'tvshow':{'volume':'delta'},
                        'movie':{'volume':'delta'},
                    },
                    'pack':{
                        'related':(
                            {'kind':'srt', 'profile':'clean', 'language':'heb'},
                            {'kind':'srt', 'profile':'clean', 'language':'eng'},
                            {'kind':'txt', 'profile':'chapter'},
                            {'kind':'ac3', 'profile':'dump'},
                            {'kind':'tc', 'profile':'dump'}
                        ),
                        'tracks':(
                            {'type':'video'},
                            {'type':'audio', 'kind':'ac3'},
                            {'type':'audio', 'kind':'mp3'},
                            {'type':'audio', 'kind':'aac'},
                            {'type':'audio', 'kind':'dts'},
                        ),
                    },
                },
            },
        },
        'srt':{
            'container':'subtitles',
            'default':{'profile':'original'},
            'Profile':{
                'dump':{
                    'description':'Special profile used by extract command',
                    'default':{
                        'tvshow':{'volume':'epsilon'},
                        'movie':{'volume':'epsilon'},
                    },
                    'extract':{
                        'tracks':(
                            {'type':'subtitles', 'language':'heb', 'kind':'srt'},
                            {'type':'subtitles', 'language':'eng', 'kind':'srt'},
                        ),
                    },
                },
                'original':{
                    'default':{
                        'tvshow':{'volume':'alpha'},
                        'movie':{'volume':'alpha'},
                    },
                    'update':{
                        'smart':{'language':'swe', 'Name':'Default', 'order':('heb', 'eng'), 'height':0.1},
                        'related':(
                            {
                                'from': {'language':'heb', 'kind':'srt'},
                                'to': {'height':0.1, 'Name':'Normal', 'profile':'original'},
                            },
                            {
                                'from': {'language':'eng', 'kind':'srt', 'profile':'original'},
                                'to': {'height':0.1, 'Name':'Normal'},
                            },
                        ),
                    },
                },
                'clean':{
                    'default':{
                        'tvshow':{'volume':'alpha'},
                        'movie':{'volume':'alpha'},
                    },
                    'transcode':{
                        'filter':('noise', 'typo', 'leftover'),
                    },
                    'update':{
                        'smart':{'language':'swe', 'Name':'Default', 'order':('heb', 'eng'), 'height':0.1},
                        'related':(
                            {
                                'from': {'language':'heb', 'kind':'srt', 'profile':'clean'},
                                'to': {'height':0.1, 'Name':'Normal'},
                            },
                            {
                                'from': {'language':'eng', 'kind':'srt', 'profile':'clean'},
                                'to': {'height':0.1, 'Name':'Normal'},
                            },
                        ),
                    },
                },
            },
        },
        'ass':{
            'container':'subtitles',
            'default':{'profile':'dump'},
            'Profile':{
                'dump':{
                    'description':'Special profile used by extract command',
                    'default':{
                        'tvshow':{'volume':'epsilon'},
                        'movie':{'volume':'epsilon'},
                    },
                    'extract':{
                        'tracks':(
                            {'type':'subtitles', 'language':'heb', 'kind':'ass'},
                            {'type':'subtitles', 'language':'eng', 'kind':'ass'},
                        ),
                    },
                },
            },
        },
        'sub':{
            'container':'subtitles',
            'default':{'profile':'original'},
            'Profile':{
                'original':{},
            },
        },
        'txt':{
            'container':'chapters',
            'default':{'profile':'chapter'},
            'Profile':{
                'chapter':{
                    'default':{
                        'tvshow':{'volume':'alpha'},
                        'movie':{'volume':'alpha'},
                    },
                },
            },
        },
        'jpg':{
            'container':'image',
            'default':{
                'profile':'normal',
                'volume':'alpha'
            },
            'Profile':{
                'download':{
                    'description':'Special profile for fetching artwork from the web',
                    'default':{
                        'tvshow':{'volume':'alpha'},
                        'movie':{'volume':'alpha'},
                    },
                },
                'normal':{
                    'default':{
                        'tvshow':{'volume':'alpha'},
                        'movie':{'volume':'alpha'},
                    },
                    'transcode':{
                        'aspect ratio':'preserve',
                        'size':1024,
                        'constraint':'max',
                    },
                },
                'criterion':{
                    'default':{
                        'tvshow':{'volume':'alpha'},
                        'movie':{'volume':'alpha'},
                    },
                    'transcode':{
                        'aspect ratio':'preserve',
                        'size':1024,
                        'constraint':'min'
                    },
                },
                'legacy':{
                    'default':{
                        'tvshow':{'volume':'alpha'},
                        'movie':{'volume':'alpha'},
                    },
                    'transcode':{
                        'aspect ratio':'preserve',
                        'size':1024,
                        'constraint':'min'
                    },
                },
            },
        },
        'png':{
            'container':'image',
            'default':{
                'profile':'normal',
                'volume':'alpha'
            },
            'Profile':{
                'download':{
                    'description':'Special profile for fetching original artwork from the web',
                    'default':{
                        'tvshow':{'volume':'alpha'},
                        'movie':{'volume':'alpha'},
                    },
                },
            },
        },
        'ac3':{
            'container':'raw audio',
            'default':{
                'profile':'dump',
                'volume':'epsilon',
            },
            'Profile':{
                'dump':{
                    'description':'Special profile for dts track exctracted from matroska',
                    'default':{
                        'tvshow':{'volume':'epsilon'},
                        'movie':{'volume':'epsilon'},
                    },
                    'transcode':{
                        'dcadec':{ '-o':'wavall', '-g':'32'},
                        'aften':{ '-b':'448' }
                    }
                },
            },
        },
        'dts':{
            'container':'raw audio',
            'default':{
                'profile':'dump',
                'volume':'epsilon',
            },
            'Profile':{
                'dump':{
                    'description':'Special profile for dts track exctracted from matroska',
                    'default':{
                        'tvshow':{'volume':'epsilon'},
                        'movie':{'volume':'epsilon'},
                    },
                    'extract':{
                        'tracks':(
                            {'type':'audio', 'kind':'dts'},
                        ),
                    },
                },
            },
        },
        'tc':{
            'container':'timecode',
            'default':{
                'profile':'dump',
                'volume':'epsilon',
            },
            'Profile':{
                'dump':{
                    'description':'Special profile for timecode track extracted from matroska',
                    'default':{
                        'tvshow':{'volume':'epsilon'},
                        'movie':{'volume':'epsilon'},
                    },
                },
            },
        },
    },
}

subtitle_config = {
    'leftover':{
        'scope':'line',
        'action':'drop',
        'case':'insensitive',
        'expression':(
            ur'^[-\s]*$',
            ur'^\([^\)]+\)$',
        ),
    },
    'noise':{
        'scope':'block',
        'action':'drop',
        'case':'insensitive',
        'expression':(
            ur'\bswsub\b',
            ur'\bresync\b',
            ur'\b[A-Za-z0-9\.]+@gmail.\s*com\b',
            ur'cync\sby\slanmao',
            ur'www\.1000fr\.com',
            ur'www\.tvsubtitles\.net',
            ur'YTET-Vicky8800',
            ur'www\.ydy\.com/bbs',
            ur'sync:gagegao',
            ur'FRM-lanma',
            ur'nowa\swizja',
            ur'ssmink',
            ur'\bLiNX\b',
            ur'(T|t)orec',
            ur'\byanx26\b',
            ur'\bGreenScorpion\b',
            ur'\bNeoTrix\b',
            ur'\bQsubs\b',
            ur'\bglfinish\b',
            ur'\bShloogy\b',
            ur'\.co\.il',
            ur'\bY0NaTaN\b',
            ur'\beLAD\b',
            ur'sratim',
            ur'Donkey Cr3w',
            ur'R-Subs',
            ur'\[D-S\]',
            ur'ponkoit',
            ur'\bsubbie\b',
            ur'\bXsesA\b',
            ur'Napisy pobrane',
            ur'\bphaelox\b',
            ur'divxstation',
            ur'\bPetaBit\b',
            ur'\bRONKEY\b',
            ur'chococat3@walla',
            ur'warez',
            ur'\bDrSub\b',
            ur'\bEliavgold\b',
            ur'^Elvira$',
            ur'\bLob93\b',
            ur'\bElvir\b',
            ur'\boofir\b',
            ur'\bKROK\b',
            ur'\bQsubd\b',
            ur'\bQSubs\b',
            ur'\bAriel046\b',
            ur'\bZIPC\b',
            ur'\bTecNodRom\b',
            ur'www\.(T|t)orec\.(N|n)et',
            ur'Visiontext Subtitles',
            ur'ENGLISH SDH',
            ur'Srulikg',
            ur'LH Translators Team',
            ur'[-=\s]+sub-zero[-=\s]+',
            ur'Lionetwork',
            ur'^EriC$',
            ur'SubZ3ro',
            ur'^David-Z$',
            ur'(D|d)r(Z|z)iv@(Y|y)ahoo',
            ur'ELRAN_O',
            ur'MCsnagel',
            ur'\bOutwit\b',
            ur'^GimLY$',
            ur'\btinyurl\b',
            ur'\bFoxRiver\b',
            ur'\bextremesubs\b',
            ur'MegaloMania Tree',
            ur'XmonWoW',
            ur'\bCiWaN\b',
            ur'\bNata4ever\b',
            ur'\bYosefff\b',
            ur'\bHentaiman\b',
            ur'\bfoxi9\b',
            ur'\bGamby\b',
            ur'\bBrassica nigra\b',
            ur'\bqsubs\b',
            ur'\bShareTW\b',
            ur'\bSeretHD\b',
            ur'HAZY7868',
            ur'\bTorec\b',
            ur'SubsCenter\.org'
            ur'\bLAKOTA\b',
            ur'\bnzigi\b'
            ur'\bqwer90\b',
            ur':סנכרון',
            ur':תרגום',
            ur':שיפוץ',
            ur':לפרטים',
            ur'סונכרן',
            ur'תורגם על ידי',
            ur'סנכרן לגרסה זו',
            ur'תורגם ע"י',
            ur'תורגם משמיעה',
            ur'קריעה וסינכרון',
            ur'תוקן על ידי',
            ur'תורגם על-ידי',
            ur'תורגם ע"י',
            ur'תוקן ע"י',
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
            ur'^.Shayx ע"י$',
            ur'PUSEL :סנכרון',
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
            ur'על ההגהה Workbook',
            ur'מוקדש לכל אוהבי האוס אי שם',
            ur'TheTerminator נערך ותוקן בשיתוף עם',
            ur'התרגום נעשה על ידי המוריד',
            ur'תורגם וסונוכרן משמיעה ע"י',
            ur'\bצפייה מהנה\b',
            ur'\bצפיה מהנה\b',
            ur'^נקרע ותוקן$',
            ur'^תרגום: אבי דניאלי$',
            ur'אוהבים את התרגומים שלנו',
            ur'נקלענו למאבק',
            ur'משפטי מתמשך',
            ur'לבילד המתקשה בהבנת קרדיטים',
            ur'אנא תרמו לנו כדי',
            ur'הגהה על-ידי',
            ur'^עריכה לשונית$',
            ur'^White Fang-תרגום: עמית יקיר ו$',
            ur'ערן טלמור',
            ur'\bעדי-בלי-בצל\b',
            ur'\bבקרו אותנו בפורום\b',
            ur'הודה בוז',
            ur'\b-תודה מיוחדת ל\b',
            ur'^Extreme מקבוצת$',
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
            ur'\bKawa: סנכרון\b',
            ur'אוהבת לנצח, שרון'
        ),
    },
    'typo':{
        'scope':'line',
        'action':'replace',
        'case':'sensitive',
        'expression':(
            (r'\b +(,|\.|\?|%|!)\b', '\\1 '),
            (r'\b(,|\.|\?|%|!) +\b', '\\1 '),
            (r'\.\s*\.\s*\.\.?', '...'),
            (r'</?[a-z]+/?>', ''),
            (r'\'{2}', '"'),
            (r'\s+\)', ')'),
            (r'\(\s+', '('),
            (r'\s+\]', ']'),
            (r'\[\s+', '['),
            (r'\[[^\]]+\]\s*', ''),
            (r'^[^\]]+\]', ''),
            (r'\[[^\]]+$', ''),
            (r'\([A-Z0-9l\s]+\)', ''),
            (r'\([A-Z0-9l\s]+$', ''),
            (r'^[A-Z0-9l\s]+\)', ''),
            (r'^[-\s]+', ''),
            (r'[-\s]+$', ''),
            (r'\b^[-A-Z\s]+[0-9]*:\s*', ''),
            (r'(?<=[a-zA-Z\'])I', 'l'),
            (r'Theysaid', 'They said'),
            (r'\bIast\b', 'last'),
            (r'\bIook\b', 'look'),
            (r'\bIetting\b', 'letting'),
            (r'\bIet\b', 'let'),
            (r'\bIooking\b', 'looking'),
            (r'\bIife\b', 'life'),
            (r'\bIeft\b', 'left'),
            (r'\bIike\b', 'like'),
            (r'\bIittle\b', 'little'),
            (r'\bIadies\b', 'ladies'),
            (r'\bIearn\b', 'learn'),
            (r'\bIanded\b', 'landed'),
            (r'\bIocked\b', 'locked'),
            (r'\bIie\b', 'lie'),
            (r'\bIong\b', 'long'),
            (r'\bIine\b', 'line'),
            (r'\bIives\b', 'lives'),
            (r'\bIeave\b', 'leave'),
            (r'\bIawyer\b', 'lawyer'),
            (r'\bIogs\b', 'logs'),
            (r'\bIack\b', 'lack'),
            (r'\bIove\b', 'love'),
            (r'\bIot\b', 'lot'),
            (r'\bIanding\b', 'landing'),
            (r'\bIet\'s\b', 'let\'s'),
            (r'\bIand\b', 'land'),
            (r'\bIying\b', 'lying'),
            (r'\bIist\b', 'list'),
            (r'\bIoved\b', 'loved'),
            (r'\bIoss\b', 'loss'),
            (r'\bIied\b', 'lied'),
            (r'\bIaugh\b', 'laugh'),
            (r'\b(h|H)avert\b', '\\1aven\'t'),
            (r'\b(w|W)asrt\b', '\\1asn\'t'),
            (r'\b(d|D)oesrt\b', '\\1oesn\'t'),
            (r'\b(d|D)ort\b', '\\1on\'t'),
            (r'\b(d|D)idrt\b', '\\1idn\'t'),
            (r'\b(a|A)irt\b', '\\1in\'t'),
            (r'\b(i|I)srt\b', '\\1sn\'t'),
            (r'\b(w|W)ort\b', '\\1on\'t'),
            (r'\b(c|C|w|W|s|S)ouldrt\b', '\\1ouldn\'t'),
            (r'\barert\b', 'aren\'t'),
            (r'\bls\b', 'Is'),
            (r'\b(L|l)f\b', 'If'),
            (r'\blt\b', 'It'),
            (r'\blt\'s\b', 'It\'s'),
            (r'\bl\'m\b', 'I\'m'),
            (r'\bl\'ll\b', 'I\'ll'),
            (r'\bl\'ve\b', 'I\'ve'),
            (r'\bl\b', 'I'),
            (r'\bln\b', 'In'),
            (r'\blmpossible\b', 'Impossible'),
            (r'\bIight\b', 'light'),
            (r'\bIevitation\b', 'levitation'),
            (r'\bIeaving\b', 'leaving'),
            (r'\bIooked\b', 'looked'),
            (r'\bIucky\b', 'lucky'),
            (r'\bIuck\b', 'luck'),
            (r'\bIater\b', 'later'),
            (r'\bIift\b', 'lift'),
            (r'\bIip\b', 'lip'),
            (r'\bIooks\b', 'looks'),
            (r'\bIaid\b', 'laid'),
            (r'\bIikely\b', 'likely'),
            (r'\bIow\b', 'low'),
            (r'\bIeast\b', 'least'),
            (r'\bIeader\b', 'leader'),
            (r'\bIocate\b', 'locate'),
            (r'\bIaw\b', 'law'),
            (r'\bIately\b', 'lately'),
            (r'\bIiar\b', 'liar'),
            (r'\bIate\b', 'late'),
            (r'\bIonger\b', 'longer'),
            (r'\bIive\b', 'live'),
            (r'^[-\s]*$', ''),
        ),
    },
}

db_config = {
    'cache':cache_path,
    'db':{
        'name':'mp4pack'
    },
    'tmdb':{
        'apikey':tmdb_apikey,
        'urls':{
            'Movie.getInfo':u'http://api.themoviedb.org/2.1/Movie.getInfo/en/json/{0}/{{0}}'.format(tmdb_apikey),
            'Movie.imdbLookup':u'http://api.themoviedb.org/2.1/Movie.imdbLookup/en/json/{0}/{{0}}'.format(tmdb_apikey),
            'Person.getInfo':u'http://api.themoviedb.org/2.1/Person.getInfo/en/json/{0}/{{0}}'.format(tmdb_apikey),
            'Person.search':u'http://api.themoviedb.org/2.1/Person.search/en/json/{0}/{{0}}'.format(tmdb_apikey),
        },
    },
    'tvdb':{
        'apikey':tvdb_apikey,
        'fuzzy':{
            'minimum_person_name_length':3,
        },
        'urls':{
            'Show.getInfo':u'http://www.thetvdb.com/api/{0}/series/{{0}}/all/en.xml'.format(tvdb_apikey),
            'Banner.getImage':u'http://www.thetvdb.com/banners/{0}'
        },
    },
    'tag':(
        # Tag name map
        # Schema: canonic name, subler name, mp4info name
        ('Track #', 'Track #', 'Track'),
        ('Disk #', 'Disk #', 'Disk'),
        ('Album', 'Album', 'Album'),
        ('Album Artist', 'Album Artist', 'Album Artist'),
        ('Artist', 'Artist', 'Artist'),
        ('ArtistID', None, 'Artist ID'),
        ('Tempo', 'Tempo', 'BPM'),
        ('Cast', 'Cast', None),
        ('Codirector', 'Codirector', None),
        ('Category', None, 'Category'),
        ('Comments', 'Comments', 'Comments'),
        ('Composer', 'Composer', 'Composer'),
        ('ComposerID', None, 'Composer ID'),
        ('contentID', 'contentID', 'Content ID'),
        ('Content Rating', 'Content Rating', 'Content Rating'),
        ('Copyright', 'Copyright', 'Copyright'),
        ('Artwork Pieces', None, 'Cover Art pieces'),
        ('Director', 'Director', None),
        ('Encoded By', 'Encoded By', 'Encoded by'),
        ('Encoding Tool', 'Encoding Tool', 'Encoded with'),
        ('Genre', 'Genre', 'Genre'),
        ('GenreID', None, 'Genre ID'),
        ('GenreType', None, 'GenreType'),
        ('Grouping', 'Grouping', 'Grouping'),
        ('HD Video', 'HD Video', 'HD Video'),
        ('Keywords', None, 'Keywords'),
        ('Long Description', 'Long Description', 'Long Description'),
        ('Lyrics', 'Lyrics', 'Lyrics'),
        ('Media Kind', 'Media Kind', 'Media Type'),
        ('Name', 'Name', 'Name'),
        ('Compilation', None, 'Part of Compilation'),
        ('Gapless', 'Gapless', 'Part of Gapless Album'),
        ('PlaylistID', None, 'Playlist ID'),
        ('Podcast', None, 'Podcast'),
        ('Producers', 'Producers', None),
        ('Purchase Date', 'Purchase Date', 'Purchase Date'),
        ('Rating', 'Rating', None),
        ('Rating Annotation', 'Rating Annotation', None),
        ('Release Date', 'Release Date', 'Release Date'),
        ('Screenwriters', 'Screenwriters', None),
        ('Description', 'Description', 'Short Description'),
        ('Sort Album', None, 'Sort Album'),
        ('Sort Album Artist', None, 'Sort Album Artist'),
        ('Sort Artist', None, 'Sort Artist'),
        ('Sort Composer', None, 'Sort Composer'),
        ('Sort Name', None, 'Sort Name'),
        ('Sort TV Show', None, 'Sort TV Show'),
        ('Studio', 'Studio', None),
        ('TV Episode #', 'TV Episode #', 'TV Episode'),
        ('TV Episode ID', 'TV Episode ID', 'TV Episode Number'),
        ('TV Network', 'TV Network', 'TV Network'),
        ('TV Season', 'TV Season', 'TV Season'),
        ('TV Show', 'TV Show', 'TV Show'),
        ('iTunes Account', 'iTunes Account', 'iTunes Account'),
        ('iTunes Account Type', None, 'iTunes Account Type'),
        ('iTunes Store Country', None, 'iTunes Store Country'),
        ('XID', 'XID', 'xid'),
    ),
}

genre_map = (
    # Genre map
    # allows mapping different names for genres to another
    ('science-fiction', 'sci-fi'),
)

base_config = {
    'genre':(
        # ITMF Genre
        # The standard itmf names and codes for genres
        {'_id':'blues', 'itmf':2, 'name':'Blues'},
        {'_id':'classic rock', 'itmf':3, 'name':'Classic Rock'},
        {'_id':'country', 'itmf':4, 'name':'Country'},
        {'_id':'dance', 'itmf':5, 'name':'Dance'},
        {'_id':'disco', 'itmf':6, 'name':'Disco'},
        {'_id':'funk', 'itmf':7, 'name':'Funk'},
        {'_id':'grunge', 'itmf':8, 'name':'Grunge'},
        {'_id':'hip hop', 'itmf':9, 'name':'Hip Hop'},
        {'_id':'jazz', 'itmf':10, 'name':'Jazz'},
        {'_id':'metal', 'itmf':11, 'name':'Metal'},
        {'_id':'new age', 'itmf':12, 'name':'New Age'},
        {'_id':'oldies', 'itmf':13, 'name':'Oldies'},
        {'_id':'other', 'itmf':14, 'name':'Other'},
        {'_id':'pop', 'itmf':15, 'name':'Pop'},
        {'_id':'r&b', 'itmf':16, 'name':'R&B'},
        {'_id':'rap', 'itmf':17, 'name':'Rap'},
        {'_id':'reggae', 'itmf':18, 'name':'Reggae'},
        {'_id':'rock', 'itmf':19, 'name':'Rock'},
        {'_id':'techno', 'itmf':20, 'name':'Techno'},
        {'_id':'industrial', 'itmf':21, 'name':'Industrial'},
        {'_id':'alternative', 'itmf':22, 'name':'Alternative'},
        {'_id':'ska', 'itmf':23, 'name':'Ska'},
        {'_id':'death metal', 'itmf':24, 'name':'Death Metal'},
        {'_id':'pranks', 'itmf':25, 'name':'Pranks'},
        {'_id':'soundtrack', 'itmf':26, 'name':'Soundtrack'},
        {'_id':'euro techno', 'itmf':27, 'name':'Euro Techno'},
        {'_id':'ambient', 'itmf':28, 'name':'Ambient'},
        {'_id':'trip hop', 'itmf':29, 'name':'Trip Hop'},
        {'_id':'vocal', 'itmf':30, 'name':'Vocal'},
        {'_id':'jazz funk', 'itmf':31, 'name':'Jazz Funk'},
        {'_id':'fusion', 'itmf':32, 'name':'Fusion'},
        {'_id':'trance', 'itmf':33, 'name':'Trance'},
        {'_id':'classical', 'itmf':34, 'name':'Classical'},
        {'_id':'instrumental', 'itmf':35, 'name':'Instrumental'},
        {'_id':'acid', 'itmf':36, 'name':'Acid'},
        {'_id':'house', 'itmf':37, 'name':'House'},
        {'_id':'game', 'itmf':38, 'name':'Game'},
        {'_id':'sound clip', 'itmf':39, 'name':'Sound Clip'},
        {'_id':'gospel', 'itmf':40, 'name':'Gospel'},
        {'_id':'noise', 'itmf':41, 'name':'Noise'},
        {'_id':'alternrock', 'itmf':42, 'name':'Alternrock'},
        {'_id':'bass', 'itmf':43, 'name':'Bass'},
        {'_id':'soul', 'itmf':44, 'name':'Soul'},
        {'_id':'punk', 'itmf':45, 'name':'Punk'},
        {'_id':'space', 'itmf':46, 'name':'Space'},
        {'_id':'meditative', 'itmf':47, 'name':'Meditative'},
        {'_id':'instrumental pop', 'itmf':48, 'name':'Instrumental Pop'},
        {'_id':'instrumental rock', 'itmf':49, 'name':'Instrumental Rock'},
        {'_id':'ethnic', 'itmf':50, 'name':'Ethnic'},
        {'_id':'gothic', 'itmf':51, 'name':'Gothic'},
        {'_id':'darkwave', 'itmf':52, 'name':'Darkwave'},
        {'_id':'techno industrial', 'itmf':53, 'name':'Techno Industrial'},
        {'_id':'electronic', 'itmf':54, 'name':'Electronic'},
        {'_id':'pop folk', 'itmf':55, 'name':'Pop Folk'},
        {'_id':'eurodance', 'itmf':56, 'name':'Eurodance'},
        {'_id':'dream', 'itmf':57, 'name':'Dream'},
        {'_id':'southern rock', 'itmf':58, 'name':'Southern Rock'},
        {'_id':'comedy', 'itmf':59, 'name':'Comedy'},
        {'_id':'cult', 'itmf':60, 'name':'Cult'},
        {'_id':'gangsta', 'itmf':61, 'name':'Gangsta'},
        {'_id':'top 40', 'itmf':62, 'name':'Top 40'},
        {'_id':'christian rap', 'itmf':63, 'name':'Christian Rap'},
        {'_id':'pop funk', 'itmf':64, 'name':'Pop Funk'},
        {'_id':'jungle', 'itmf':65, 'name':'Jungle'},
        {'_id':'native American', 'itmf':66, 'name':'Native American'},
        {'_id':'cabaret', 'itmf':67, 'name':'Cabaret'},
        {'_id':'new wave', 'itmf':68, 'name':'New Wave'},
        {'_id':'psychedelic', 'itmf':69, 'name':'Psychedelic'},
        {'_id':'rave', 'itmf':70, 'name':'Rave'},
        {'_id':'showtunes', 'itmf':71, 'name':'Showtunes'},
        {'_id':'trailer', 'itmf':72, 'name':'Trailer'},
        {'_id':'lo fi', 'itmf':73, 'name':'Lo Fi'},
        {'_id':'tribal', 'itmf':74, 'name':'Tribal'},
        {'_id':'acid punk', 'itmf':75, 'name':'Acid Punk'},
        {'_id':'acid jazz', 'itmf':76, 'name':'Acid Jazz'},
        {'_id':'polka', 'itmf':77, 'name':'Polka'},
        {'_id':'retro', 'itmf':78, 'name':'Retro'},
        {'_id':'musical', 'itmf':79, 'name':'Musical'},
        {'_id':'rock and roll', 'itmf':80, 'name':'Rock and Roll'},
    ),
    
    'tvshow':(
        # TV Show map
        # The initial TVDB TV Show id map
        (79501, u'heroes'),
        (75930, u'alias'),
        (76290, u'24'),
        (73800, u'desperate housewives'),
        (79349, u'dexter'),
        (73871, u'futurama'),
        (73255, u'house'),
        (73739, u'lost'),
        (79169, u'seinfeld'),
        (75299, u'the sopranos'),
        (73762, u'greys anatomy'),
        (79126, u'the wire'),
        (75164, u'samurai jack'),
        (74543, u'entourage'),
        (85527, u'yellowstone'),
        (79257, u'planet earth'),
        (74845, u'weeds'),
        (75450, u'six feet under'),
        (80252, u'flight of the conchords'),
        (82066, u'fringe'),
        (80337, u'mad men'),
        (73508, u'rome'),
        (77398, u'the x files'),
        (70682, u'oz'),
        (77526, u'star trek'),
        (77231, u'mission impossible'),
        (83268, u'star wars the clone wars'),
        (74805, u'the prisoner'),
        (85242, u'the prisoner 2009'),
        (83602, u'lie to me'),
        (80349, u'californication'),
        (82109, u'generation kill'),
        (70533, u'twin peaks'),
        (72628, u'the singing detective'),
        (80593, u'dirty sexy money'),
        (79177, u'life on mars uk'),
        (82289, u'life on mars us'),
        (118421, u'life bbc'),
        (130421, u'faces of earth'),
        (147071, u'wonders of the solar system'),
        (108611, u'white collar'),
        (85149, u'berlin alexanderplatz'),
        (94971, u'v 2009'),
        (82459, u'the mentalist'),
        (82283, u'true blood'),
        (79488, u'30 rock'),
        (74205, u'band of brothers'),
        (124561, u'world war 2 in high definition'),
        (81189, u'breaking bad'),
        (71663, u'the simpsons'),
        (85040, u'caprica'),
        
    ),
}
