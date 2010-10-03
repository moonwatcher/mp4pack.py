#!/usr/bin/env python
# -*- coding: utf-8 -*-

tmdb_apikey = u'a8b9f96dde091408a03cb4c78477bd14'
tvdb_apikey = u'7B3B400B0146EA83'

repository_config = {
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
        'indent':25, 
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
    },
    'Volume':{
        'alpha':'/Users/lg/Downloads/pool/alpha',
        'beta':'/Users/lg/Downloads/pool/beta',
        'gama':'/Users/lg/Downloads/pool/gama',
        'delta':'/Users/lg/Downloads/pool/delta',
        'eta':'/Users/lg/Downloads/pool/eta',
        'epsilon':'/Users/lg/Downloads/pool/epsilon',
    },
    'Media Kind':{
        'tvshow':{'schema':'^(.+) (s([0-9]+)e([0-9]+))(?: (.*))?\.([^\.]+)$', 'name':'TV Show', 'stik':10},
        'movie':{'schema':'^IMDb(tt[0-9]+)(?: (.*))?\.([^\.]+)$', 'name':'Movie', 'stik':9},
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
                            {'kind':'ac3', 'profile':'dump'}
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
                                'to': {'height':0.1, 'Name':'Normal'},
                            },
                            {
                                'from': {'language':'eng', 'kind':'srt'},
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
                        'filter':('comment', 'typo'),
                    },
                    'update':{
                        'smart':{'language':'swe', 'Name':'Default', 'order':('heb', 'eng'), 'height':0.1},
                        'related':(
                            {
                                'from': {'language':'heb', 'kind':'srt'},
                                'to': {'height':0.1, 'Name':'Normal'},
                            },
                            {
                                'from': {'language':'eng', 'kind':'srt'},
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
    'comment':{
        'scope':'line',
        'action':'drop',
        'case':'insensitive',
        'expression':(
            ur'^[-\s]*$',
            ur'\bswsub\b',
            ur'\bresync\b',
            ur'cync\sby\slanmao',
            ur'www\.1000fr\.com',
            ur'www\.tvsubtitles\.net',
            ur'YTET-Vicky8800',
            ur'www\.ydy\.com/bbs',
            ur'sync:gagegao',
            ur'FRM-lanma',
            ur'nowa\swizja',
            ur'ssmink',
            ur'תורגם על ידי',
            ur':תרגום',
            ur'\bLiNX\b',
            ur'(T|t)orec',
            ur'\byanx26\b',
            ur'הודה בוז',
            ur'\bGreenScorpion\b',
            ur'\bNeoTrix\b',
            ur'\bQsubs\b',
            ur'סונכרן',
            ur'\bglfinish\b',
            ur'\bShloogy\b',
            ur'עמוס נמני',
            ur'\.co\.il',
            ur'\bY0NaTaN\b',
            ur'מוקדש לך',
            ur'אינדיאנית שלי',
            ur'יומולדת שמח',
            ur'\beLAD\b',
            ur'תורגם ע"י',
            ur'מונחים רפואיים - ג\'ון דו',
            ur'מפורום תפוז',
            ur'סנכרן לגרסה זו',
            ur'מוקדש לפולי שלי',
            ur'sratim',
            ur'Donkey Cr3w',
            ur'R-Subs',
            ur'\[D-S\]',
            ur'ponkoit',
            ur'תורגם משמיעה',
            ur'י ביצה קשה',
            ur'כתובית זו הובאה',
            ur'שופצה, נערכה וסונכרנה לגרסה זו',
            ur':כתוביות',
            ur'\bsubbie\b',
            ur'\bXsesA\b',
            ur'Napisy pobrane',
            ur'קריעה וסינכרון',
            ur'^ב$',
            ur'^בי$',
            ur'^ביצ$',
            ur'^ביצה$',
            ur'^ביצה ק$',
            ur'^ביצה קש$',
            ur'^ביצה קשה$',
            ur'\bphaelox\b',
            ur'divxstation',
            ur'\bPetaBit\b',
            ur'\bRONKEY\b',
            ur'^בלעדית עבור$',
            ur'כתוביות ע"י',
            ur'chococat3@walla',
            ur'מוקדש לכל אוהבי האוס אי שם',
            ur'\bDrSub\b',
            ur'\bEliavgold\b',
            ur'^Elvira$',
            ur'ברוכה הבאה אלוירה',
            ur'לצוות מתרגמי האוס',
            ur'אלוירה ברוכה הבאה',
            ur'\bLob93\b',
            ur'הורד מהאתר',
            ur'על ההגהה Workbook',
            ur'\bElvir\b',
            ur'\boofir\b',
            ur'תוקן על ידי',
            ur'תורגם על-ידי',
            ur'תורגם ע"י',
            ur'תוקן ע"י',
            ur'תוקן קלות ע"י',
            ur'\bKROK\b',
            ur'\bQsubd\b',
            ur'\bQSubs\b',
            ur'\bAriel046\b',
            ur'סונכרן לגירסא זו ע"י',
            ur'\bZIPC\b',
            ur'\bTecNodRom\b',
            ur'www\.(T|t)orec\.(N|n)et',
            ur'\bמצוות פושל\b',
            ur'Visiontext Subtitles',
            ur'ENGLISH SDH',
            ur'ערן טלמור',
            ur'תרגום: שמעון אברג\'יל',
            ur'Srulikg',
            ur'ליונהארט',
            ur'תרגום: רותם ושמעון',
            ur'תרגום: קובי אלמוזנינו',
            ur'LH Translators Team',
            ur'שיפוץ: השייח\' הסעודי',
            ur'שופץ ע"י השייח\' הסעודי',
            ur'תרגום: שמעון ורותם אברג\'יל',
            ur'^עריכה לשונית$',
            ur'-= Sub-Zero =-',
            ur'-= SUB-ZERO-=',
            ur'Lionetwork',
            ur'תרגום זה בוצע על ידי',
            ur'(D|d)(-|a)k(w|W)arez',
            ur'תרגום זה נעשה על ידי',
            ur'--תורגם עם הרבה זיעה על ידי--',
            ur'תורגם מספרדית ע"י אסף פארי',
            ur'^EriC$',
            ur'SubZ3ro',
            ur'TheTerminator נערך ותוקן בשיתוף עם',
            ur'התרגום נעשה על ידי המוריד',
            ur'^David-Z$',
            ur'(D|d)r(Z|z)iv@(Y|y)ahoo',
            ur'ELRAN_O',
            ur'MCsnagel',
            ur'הגהה וסנכרון ע"י',
            ur'ialfan-ו mb0:עברית',
            ur'תורגם וסונוכרן משמיעה ע"י',
            ur'\bOutwit\b',
            ur'^נקרע ותוקן$',
            ur'^תרגום: אבי דניאלי$',
            ur'^GimLY$',
            ur'^White Fang-תרגום: עמית יקיר ו$',
            ur'^.Shayx ע"י$',
            ur'\btinyurl\b',
            ur'\bצפייה מהנה\b',
            ur'\bצפיה מהנה\b',
            ur'\bFoxRiver\b',
            ur'^Extreme מקבוצת$',
            ur'\bextremesubs\b',
            ur'\bCiWaN\b',
            ur'\bNata4ever\b',
            ur'\bYosefff\b',
            ur'\bassem נקרע ע"י\b',
            ur'\bKawa: סנכרון\b',
            ur'\bHentaiman\b',
            ur'\bfoxi9\b',
            ur'\b-תודה מיוחדת ל\b',
            ur'\bGamby\b',
            ur'\bBrassica nigra\b',
            ur'\bqsubs\b',
            ur'\bעדי-בלי-בצל\b',
            ur'\bבקרו אותנו בפורום\b',
            ur'\bShareTW\b',
            ur'\bSeretHD\b',
            ur'\b[A-Za-z0-9\.]+@gmail.\s*com\b',
            ur'אוהבים את התרגומים שלנו',
            ur'נקלענו למאבק',
            ur'משפטי מתמשך',
            ur'לבילד המתקשה בהבנת קרדיטים',
            ur'אנא תרמו לנו כדי',
            ur'שנוכל להמשיך לתרגם',
            ur':לפרטים',
            ur'הגהה על-ידי',
            ur'HAZY7868',
            ur'^[-\s]*$'
        ),
    },
    'evil':{
        'scope':'block',
        'action':'drop',
        'case':'insensitive',
        'expression':(),
    },
    'typo':{
        'scope':'line',
        'action':'replace',
        'case':'insensitive',
        'expression':(
            (r'\b *(,|\.|\?|%|!|\$) *\b', r'\1 '),
            (r'\.\s*\.\s*\.\.?', r'...'),
            (r'</?[a-z]+/?>', r''),
            (r'\'{2}', r'"'),
            (r'\s+\)', r')'),
            (r'\(\s+', '('),
            (r'\s+\]', r']'),
            (r'\[\s+', '['),
            (r'\[[^\]]+\]\s*', r''),
            (r'^[^\]]+\]', r''),
            (r'\[[^\]]+\$', r''),
            (r'\([A-Z0-9l\s]+\)', r''),
            (r'\([A-Z0-9l\s]+$', r''),
            (r'^[A-Z0-9l\s]+\)', r''),
            (r'\b[-A-Z0-9\s]+:\s*', r''),
            (r'Theysaid', r'They said'),
            (r'\bIast\b', r'last'),
            (r'\bIook\b', r'look'),
            (r'\bIetting\b', r'letting'),
            (r'\bIet\b', r'let'),
            (r'\bshe\'II\b', r'she\'ll'),
            (r'\bIooking\b', r'looking'),
            (r'\bIife\b', r'life'),
            (r'\bIeft\b', r'left'),
            (r'\bIike\b', r'like'),
            (r'\bIittle\b', r'little'),
            (r'\b(P|p)Iease\b', r'\1lease'),
            (r'\bIadies\b', r'ladies'),
            (r'\bIearn\b', r'learn'),
            (r'\bIanded\b', r'landed'),
            (r'\bIocked\b', r'locked'),
            (r'\bIie\b', r'lie'),
            (r'\bCIaire\b', r'Claire'),
            (r'\bIong\b', r'long'),
            (r'\bIine\b', r'line'),
            (r'\byou\'II\b', r'you\'ll'),
            (r'\bIives\b', r'lives'),
            (r'\bIeave\b', r'leave'),
            (r'\bIawyer\b', r'lawyer'),
            (r'\bAIex\b', r'Alex'),
            (r'\bIogs\b', r'logs'),
            (r'\b(P|p)Ieasure\b', r'\1leasure'),
            (r'\bIack\b', r'lack'),
            (r'\bIove\b', r'love'),
            (r'\bAIexandra\b', r'Alexandra'),
            (r'\bIot\b', r'lot'),
            (r'\bIanding\b', r'landing'),
            (r'\bThey\'II\b', r'They\'ll'),
            (r'\bIet\'s\b', r'let\'s'),
            (r'\bIand\b', r'land'),
            (r'\bIying\b', r'lying'),
            (r'\bIist\b', r'list'),
            (r'\bAIIow\b', r'Allow'),
            (r'\bIoved\b', r'loved'),
            (r'\bIoss\b', r'loss'),
            (r'\bIied\b', r'lied'),
            (r'\bIaugh\b', r'laugh'),
            (r'\bpIace\b', r'place'),
            (r'\b(h|H)avert\b', r'\1aven\'t'),
            (r'\b(w|W)asrt\b', r'\1asn\'t'),
            (r'\b(d|D)oesrt\b', r'\1oesn\'t'),
            (r'\b(d|D)ort\b', r'\1on\'t'),
            (r'\b(d|D)idrt\b', r'\1idn\'t'),
            (r'\b(a|A)irt\b', r'\1in\'t'),
            (r'\b(i|I)srt\b', r'\1sn\'t'),
            (r'\b(w|W)ort\b', r'\1on\'t'),
            (r'\b(c|C|w|W|s|S)ouldrt\b', r'\1ouldn\'t'),
            (r'\barert\b', r'aren\'t'),
            (r'\bls\b', r'Is'),
            (r'\bLf\b', r'If'),
            (r'\blf\b', r'If'),
            (r'\blt\b', r'It'),
            (r'\blt\'s\b', r'It\'s'),
            (r'\bl\'m\b', r'I\'m'),
            (r'\bl\'ll\b', r'I\'ll'),
            (r'\bl\'ve\b', r'I\'ve'),
            (r'\bl\b', r'I'),
            (r'\bln\b', r'In'),
            (r'\blmpossible\b', r'Impossible'),
            (r'\bIight\b', r'light'),
            (r'\bIevitation\b', r'levitation'),
            (r'\bIeaving\b', r'leaving'),
            (r'\bIooked\b', r'looked'),
            (r'\bwe\'II\b', r'we\'ll'),
            (r'\bIucky\b', r'lucky'),
            (r'\bIuck\b', r'luck'),
            (r'\bIater\b', r'later'),
            (r'\bIift\b', r'lift'),
            (r'\bIip\b', r'lip'),
            (r'\bhe\'II\b', r'he\'ll'),
            (r'\b(A|a)Iso\b', r'\1lso'),
            (r'\bIooks\b', r'looks'),
            (r'\b(P|p)Iayed\b', r'\1layed'),
            (r'\bIaid\b', r'laid'),
            (r'\bIikely\b', r'likely'),
            (r'\bIow\b', r'low'),
            (r'\bIeast\b', r'least'),
            (r'\bIeader\b', r'leader'),
            (r'\bIocate\b', r'locate'),
            (r'\bIaw\b', r'law'),
            (r'\bIately\b', r'lately'),
            (r'\bFIying\b', r'Flying'),
            (r'\bIiar\b', r'liar'),
            (r'\b(s|S)chooI\b', r'\1chool'),
            (r'\b(s|S)eriousIy\b', r'\1eriously'),
            (r'\bIate\b', r'late'),
            (r'\b(S|s)urgicaI\b', r'\1urgical'),
            (r'\b(B|b)Iood\b', r'\1lood'),
            (r'\b(f|F)eeIs\b', r'\1eels'),
            (r'\b(S|s)Iept\b', r'\1lept'),
            (r'\b(b|B)Iew\b', r'\1lew'),
            (r'\b(T|t)aiI\b', r'\1ail'),
            (r'\b(N|n)earIy\b', r'\1early'),
            (r'\b(C|c)Iose\b', r'\1lose'),
            (r'\b(C|c)Ioser\b', r'\1loser'),
            (r'\b(E|e)viI\b', r'\1vil'),
            (r'\b(M|m)odeI\b', r'\1odel'),
            (r'\b(S|s)yphiIis\b', r'\1yphilis'),
            (r'\b(R|r)eIationship\b', r'\1elationship'),
            (r'\b(F|f)aIIing\b', r'\1alling'),
            (r'\b(P|p)eopIe\b', r'\1eople'),
            (r'\b(C|c|B|b)aII\b', r'\1all'),
            (r'\b(W|w)ouId\b', r'\1ould'),
            (r'\b(A|a)ppIe\b', r'\1pple'),
            (r'\b(F|f)amiIiar\b', r'\1amiliar'),
            (r'\b(R|r)eaIIy\b', r'\1eally'),
            (r'\b(W|w|H|h|Y|y)eII\b', r'\1ell'),
            (r'\b(P|p)robIem\b', r'\1roblem'),
            (r'\bIonger\b', r'longer'),
            (r'\b(G|g)irIfriend\b', r'\1irlfriend'),
            (r'\b(F|f)Iew\b', r'\1lew'),
            (r'\b(R|r)eaIize\b', r'\1ealize'),
            (r'\bIive\b', r'live'),
            (r'\b(S|s)tiII\b', r'\1till'),
            (r'\b(W|w)iII\b', r'\1ill'),
            (r'\bRusseII\b', r'Russell'),
            (r'\b(S|s)maII\b', r'\1mall'),
            (r'^[-\s]*$', r''),
        ),
    },
}

db_config = {
    'cache':u'/Users/lg/Downloads/pool/cache/',
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
        (79501, 'Heroes'),
        (75930, 'Alias'),
        (76290, '24'),
        (73800, 'Desperate Housewives'),
        (79349, 'Dexter'),
        (73871, 'Futurama'),
        (73255, 'House'),
        (73739, 'Lost'),
        (79169, 'Seinfeld'),
        (75299, 'The Sopranos'),
        (73762, 'Greys Anatomy'),
        (79126, 'The Wire'),
        (75164, 'Samurai Jack'),
        (74543, 'Entourage'),
        (85527, 'Yellowstone'),
        (79257, 'Planet Earth'),
        (74845, 'Weeds'),
        (75450, 'Six Feet Under'),
        (80252, 'Flight of the Conchords'),
        (82066, 'Fringe'),
        (80337, 'Mad Men'),
        (73508, 'Rome'),
        (77398, 'The X-Files'),
        (70682, 'Oz'),
        (77526, 'Star Trek'),
        (77231, 'Mission Impossible'),
        (83268, 'Star Wars - The Clone Wars'),
        (74805, 'The Prisoner'),
        (85242, 'The Prisoner 2009'),
        (83602, 'Lie To Me'),
        (80349, 'Californication'),
        (82109, 'Generation Kill'),
        (70533, 'Twin Peaks'),
        (72628, 'The Singing Detective'),
        (80593, 'Dirty Sexy Money'),
        (79177, 'Life on Mars'),
        (82289, 'Life on Mars US'),
        (118421, 'Life BBC'),
        (130421, 'Faces of Earth'),
        (147071, 'Wonders of the Solar System'),
        (108611, 'White Collar'),
        (85149, 'Berlin Alexanderplatz'),
        (94971, 'V 2009'),
        (82459, 'The Mentalist'),
        (82283, 'True Blood'),
    ),
}
